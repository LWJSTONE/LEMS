package com.lab.borrow.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.LambdaUpdateWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.borrow.entity.BorrowRecord;
import com.lab.borrow.mapper.BorrowRecordMapper;
import com.lab.borrow.service.BorrowService;
import com.lab.common.exception.BusinessException;
import com.lab.common.result.R;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.TimeUnit;

/**
 * 借用预约服务实现
 *
 * ★ 关键：库存并发控制
 * - 申请阶段(预占): 使用Redis分布式锁 + 乐观锁双保险
 * - 乐观锁: deviceInfoMapper.decreaseAvailableQuantity (UPDATE ... WHERE version = ? AND available_quantity >= ?)
 * - 若影响行数为0，抛出 BusinessException("库存不足或操作频繁")
 * - 归还/取消/驳回: 使用乐观锁回加库存
 */
@Slf4j
@Service
public class BorrowServiceImpl implements BorrowService {

    @Resource
    private BorrowRecordMapper borrowRecordMapper;

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    @Resource
    private com.lab.common.feign.DeviceFeignClient deviceFeignClient;

    @Resource
    private com.lab.common.feign.UserFeignClient userFeignClient;

    /**
     * ★ 提交借用申请（核心：库存预占，使用分布式锁 + 乐观锁）
     *
     * 流程：
     * 1. 获取Redis分布式锁(lock:device:${deviceId})，避免乐观锁重试风暴
     * 2. 通过Feign查询设备详情，获取当前availableQuantity和version
     * 3. 通过Feign调用设备服务乐观锁扣减库存
     *    deviceMapper.decreaseAvailableQuantity(id, quantity, version)
     *    SQL: UPDATE device_info SET available_quantity = available_quantity - #{quantity}, version = version + 1
     *         WHERE id = #{id} AND version = #{version} AND available_quantity >= #{quantity}
     * 4. 若更新影响行数为0 → 抛出 BusinessException("库存不足或操作频繁")，事务回滚
     * 5. 插入借用申请记录
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void apply(BorrowRecord record, Long userId) {
        Long deviceId = record.getDeviceId();
        Integer quantity = record.getBorrowQuantity();
        String lockKey = "lock:device:" + deviceId;

        // 获取Redis分布式锁（避免乐观锁重试风暴）
        String lockValue = UUID.randomUUID().toString();
        Boolean locked = stringRedisTemplate.opsForValue().setIfAbsent(lockKey, lockValue, 30, TimeUnit.SECONDS);
        if (Boolean.FALSE.equals(locked)) {
            throw new BusinessException("操作过于频繁，请稍后重试");
        }

        try {
            // 查询设备信息（含版本号）
            com.lab.common.result.R<?> deviceResult = deviceFeignClient.getDeviceInfo(deviceId);
            if (deviceResult.getCode() != 200 || deviceResult.getData() == null) {
                throw new BusinessException("设备不存在或服务不可用");
            }
            @SuppressWarnings("unchecked")
            Map<String, Object> deviceMap = (Map<String, Object>) deviceResult.getData();
            Integer availableQuantity = Integer.valueOf(deviceMap.get("availableQuantity").toString());
            Integer version = Integer.valueOf(deviceMap.get("version").toString());
            Integer status = Integer.valueOf(deviceMap.get("status").toString());

            if (status != 0) {
                throw new BusinessException("设备当前状态不可借用");
            }
            if (availableQuantity < quantity) {
                throw new BusinessException("库存不足，当前可用数量为 " + availableQuantity);
            }

            // ★ 乐观锁扣减库存
            Map<String, Object> params = new java.util.HashMap<>();
            params.put("deviceId", deviceId);
            params.put("quantity", quantity);
            params.put("operation", "DECREASE");
            params.put("version", version);

            com.lab.common.result.R<?> stockResult = deviceFeignClient.updateAvailableQuantity(params);
            if (stockResult.getCode() != 200) {
                throw new BusinessException("库存不足或操作频繁，请重试");
            }

            // 插入借用记录
            record.setUserId(userId);
            record.setStatus(0); // 待审批
            record.setVersion(0);
            try {
                borrowRecordMapper.insert(record);
            } catch (Exception e) {
                // 插入失败，补偿：回加已扣减的库存
                log.error("借用记录插入失败，尝试补偿回加库存: deviceId={}", deviceId, e);
                try {
                    // 重新查询最新版本号（扣减后version已+1）
                    com.lab.common.result.R<?> latestDeviceResult = deviceFeignClient.getDeviceInfo(deviceId);
                    if (latestDeviceResult.getCode() == 200 && latestDeviceResult.getData() != null) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> latestDeviceMap = (Map<String, Object>) latestDeviceResult.getData();
                        Integer latestVersion = Integer.valueOf(latestDeviceMap.get("version").toString());
                        Map<String, Object> compensateParams = new java.util.HashMap<>();
                        compensateParams.put("deviceId", deviceId);
                        compensateParams.put("quantity", quantity);
                        compensateParams.put("operation", "INCREASE");
                        compensateParams.put("version", latestVersion);
                        com.lab.common.result.R<?> compensateResult = deviceFeignClient.updateAvailableQuantity(compensateParams);
                        if (compensateResult.getCode() != 200) {
                            log.error("库存补偿回加失败（版本冲突）: deviceId={}, version={}", deviceId, latestVersion);
                        }
                    }
                } catch (Exception ex) {
                    log.error("库存补偿回加异常: deviceId={}", deviceId, ex);
                }
                throw new BusinessException("提交申请失败，请重试");
            }

            log.info("借用申请成功: borrowId={}, deviceId={}, quantity={}, userId={}", record.getId(), deviceId, quantity, userId);

        } finally {
            // 释放分布式锁（仅释放自己持有的锁）
            String currentValue = stringRedisTemplate.opsForValue().get(lockKey);
            if (lockValue.equals(currentValue)) {
                stringRedisTemplate.delete(lockKey);
            }
        }
    }

    @Override
    public Page<BorrowRecord> myList(Long userId, int pageNum, int pageSize, Integer status) {
        Page<BorrowRecord> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<BorrowRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(BorrowRecord::getUserId, userId);
        if (status != null) {
            wrapper.eq(BorrowRecord::getStatus, status);
        }
        wrapper.orderByDesc(BorrowRecord::getCreateTime);
        Page<BorrowRecord> result = borrowRecordMapper.selectPage(page, wrapper);
        // 填充虚拟字段 deviceName, deviceCode, userName, approverName
        fillBorrowRecordDisplayFields(result.getRecords());
        return result;
    }

    @Override
    public Page<BorrowRecord> pendingList(int pageNum, int pageSize) {
        Page<BorrowRecord> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<BorrowRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(BorrowRecord::getStatus, 0); // 待审批
        wrapper.orderByAsc(BorrowRecord::getCreateTime);
        Page<BorrowRecord> result = borrowRecordMapper.selectPage(page, wrapper);
        // 填充虚拟字段 deviceName, deviceCode, userName, approverName
        fillBorrowRecordDisplayFields(result.getRecords());
        return result;
    }

    /**
     * 审批通过
     * ★ 库存已预占（申请时已扣减），无需再次操作库存
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void approve(Long id, Long approverId) {
        BorrowRecord record = borrowRecordMapper.selectById(id);
        if (record == null) {
            throw new BusinessException("借用记录不存在");
        }
        if (record.getStatus() != 0) {
            throw new BusinessException("该申请已审批");
        }

        record.setStatus(1); // 已批准（借用中）
        record.setApproverId(approverId);
        record.setApproveTime(LocalDateTime.now());
        int rows = borrowRecordMapper.updateById(record);
        if (rows == 0) {
            throw new BusinessException("审批失败，该申请可能已被其他管理员处理");
        }

        log.info("审批通过: borrowId={}, approverId={}", id, approverId);
    }

    /**
     * 驳回申请
     * ★ 释放预占库存（乐观锁回加）
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void reject(Long id, Long approverId, String reason) {
        BorrowRecord record = borrowRecordMapper.selectById(id);
        if (record == null) {
            throw new BusinessException("借用记录不存在");
        }
        if (record.getStatus() != 0) {
            throw new BusinessException("该申请已审批");
        }

        // 更新借用记录状态
        record.setStatus(4); // 已驳回
        record.setApproverId(approverId);
        record.setApproveTime(LocalDateTime.now());
        record.setRejectReason(reason);
        int rows = borrowRecordMapper.updateById(record);
        if (rows == 0) {
            throw new BusinessException("驳回失败，该申请可能已被其他管理员处理");
        }

        // ★ 释放预占库存（乐观锁回加）
        releaseStock(record.getDeviceId(), record.getBorrowQuantity());

        log.info("驳回申请: borrowId={}, approverId={}, reason={}", id, approverId, reason);
    }

    /**
     * 取消申请
     * ★ 释放预占库存（乐观锁回加）
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void cancel(Long id, Long userId) {
        BorrowRecord record = borrowRecordMapper.selectById(id);
        if (record == null) {
            throw new BusinessException("借用记录不存在");
        }
        if (record.getStatus() != 0) {
            throw new BusinessException("仅待审批状态可取消");
        }
        if (!record.getUserId().equals(userId)) {
            throw new BusinessException("无权取消他人申请");
        }

        record.setStatus(5); // 已取消
        int rows = borrowRecordMapper.updateById(record);
        if (rows == 0) {
            throw new BusinessException("取消失败，该申请状态已变更");
        }

        // ★ 释放预占库存（乐观锁回加）
        releaseStock(record.getDeviceId(), record.getBorrowQuantity());

        log.info("取消申请: borrowId={}, userId={}", id, userId);
    }

    /**
     * 归还确认
     * ★ 库存回增（乐观锁），更新actual_return_time
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void returnDevice(Long id, Long userId, String remark) {
        BorrowRecord record = borrowRecordMapper.selectById(id);
        if (record == null) {
            throw new BusinessException("借用记录不存在");
        }
        if (record.getStatus() != 1 && record.getStatus() != 3) {
            throw new BusinessException("当前状态不允许归还");
        }

        record.setStatus(2); // 已归还
        record.setActualReturnTime(LocalDateTime.now());
        record.setReturnRemark(remark);
        int rows = borrowRecordMapper.updateById(record);
        if (rows == 0) {
            throw new BusinessException("归还失败，该申请状态已变更");
        }

        // ★ 库存回增（乐观锁回加）
        releaseStock(record.getDeviceId(), record.getBorrowQuantity());

        log.info("归还确认: borrowId={}, userId={}", id, userId);
    }

    @Override
    public Page<BorrowRecord> overdueList(int pageNum, int pageSize) {
        Page<BorrowRecord> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<BorrowRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(BorrowRecord::getStatus, 3); // 已逾期
        wrapper.orderByDesc(BorrowRecord::getEndTime);
        Page<BorrowRecord> result = borrowRecordMapper.selectPage(page, wrapper);
        // 填充虚拟字段 deviceName, deviceCode, userName, approverName
        fillBorrowRecordDisplayFields(result.getRecords());
        return result;
    }

    /**
     * 定时任务：每小时扫描并标记逾期借用记录
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void checkOverdueRecords() {
        LambdaUpdateWrapper<BorrowRecord> wrapper = new LambdaUpdateWrapper<>();
        wrapper.eq(BorrowRecord::getStatus, 1) // 已批准（借用中）
               .lt(BorrowRecord::getEndTime, LocalDateTime.now()) // end_time < 当前时间
               .set(BorrowRecord::getStatus, 3); // 标记为已逾期

        int count = borrowRecordMapper.update(null, wrapper);
        if (count > 0) {
            log.info("定时任务标记逾期记录: count={}", count);
        }
    }

    // ==================== 虚拟字段填充辅助方法 ====================

    /**
     * 批量填充借用记录的虚拟字段（deviceName, deviceCode, userName, approverName）
     * 使用缓存避免重复 Feign 调用
     */
    private void fillBorrowRecordDisplayFields(List<BorrowRecord> records) {
        if (records == null || records.isEmpty()) {
            return;
        }

        // 收集所有需要查询的唯一 ID
        Set<Long> deviceIds = new HashSet<>();
        Set<Long> userIds = new HashSet<>();
        Set<Long> approverIds = new HashSet<>();

        for (BorrowRecord record : records) {
            if (record.getDeviceId() != null) {
                deviceIds.add(record.getDeviceId());
            }
            if (record.getUserId() != null) {
                userIds.add(record.getUserId());
            }
            if (record.getApproverId() != null) {
                approverIds.add(record.getApproverId());
            }
        }

        // 合并所有需要查询的用户 ID（userId + approverId）
        Set<Long> allUserIds = new HashSet<>();
        allUserIds.addAll(userIds);
        allUserIds.addAll(approverIds);

        // 批量查询设备信息（deviceId -> {name, code}）
        Map<Long, Map<String, String>> deviceInfoMap = new HashMap<>();
        for (Long deviceId : deviceIds) {
            try {
                R<?> result = deviceFeignClient.getDeviceInfo(deviceId);
                if (result != null && result.getCode() == 200 && result.getData() != null) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> data = (Map<String, Object>) result.getData();
                    Map<String, String> info = new HashMap<>();
                    Object name = data.get("name");
                    Object code = data.get("code");
                    info.put("name", name != null ? name.toString() : null);
                    info.put("code", code != null ? code.toString() : null);
                    deviceInfoMap.put(deviceId, info);
                }
            } catch (Exception e) {
                log.warn("Feign查询设备信息失败: deviceId={}, error={}", deviceId, e.getMessage());
            }
        }

        // 批量查询用户信息（userId -> realName）
        Map<Long, String> userNameMap = new HashMap<>();
        for (Long userId : allUserIds) {
            try {
                R<?> result = userFeignClient.getUserById(userId);
                if (result != null && result.getCode() == 200 && result.getData() != null) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> data = (Map<String, Object>) result.getData();
                    Object realName = data.get("realName");
                    userNameMap.put(userId, realName != null ? realName.toString() : null);
                }
            } catch (Exception e) {
                log.warn("Feign查询用户信息失败: userId={}, error={}", userId, e.getMessage());
            }
        }

        // 填充记录
        for (BorrowRecord record : records) {
            // 填充设备信息
            if (record.getDeviceId() != null) {
                Map<String, String> deviceInfo = deviceInfoMap.get(record.getDeviceId());
                if (deviceInfo != null) {
                    record.setDeviceName(deviceInfo.get("name"));
                    record.setDeviceCode(deviceInfo.get("code"));
                }
            }
            // 填充申请人名称
            if (record.getUserId() != null) {
                record.setUserName(userNameMap.get(record.getUserId()));
            }
            // 填充审批人名称
            if (record.getApproverId() != null) {
                record.setApproverName(userNameMap.get(record.getApproverId()));
            }
        }
    }

    /**
     * 内部方法：释放库存（乐观锁回加）
     */
    private void releaseStock(Long deviceId, Integer quantity) {
        // 查询设备最新版本号
        com.lab.common.result.R<?> deviceResult = deviceFeignClient.getDeviceInfo(deviceId);
        if (deviceResult.getCode() != 200 || deviceResult.getData() == null) {
            log.error("释放库存失败：设备服务不可用, deviceId={}", deviceId);
            throw new BusinessException("设备服务不可用，请联系管理员");
        }
        @SuppressWarnings("unchecked")
        Map<String, Object> deviceMap = (Map<String, Object>) deviceResult.getData();
        Integer version = Integer.valueOf(deviceMap.get("version").toString());

        Map<String, Object> params = new java.util.HashMap<>();
        params.put("deviceId", deviceId);
        params.put("quantity", quantity);
        params.put("operation", "INCREASE");
        params.put("version", version);

        com.lab.common.result.R<?> stockResult = deviceFeignClient.updateAvailableQuantity(params);
        if (stockResult.getCode() != 200) {
            log.error("释放库存失败（版本冲突）: deviceId={}, version={}", deviceId, version);
            throw new BusinessException("库存操作失败，请联系管理员");
        }
    }
}
