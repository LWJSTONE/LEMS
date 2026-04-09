package com.lab.device.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.device.entity.DeviceCategory;
import com.lab.device.entity.DeviceInfo;
import com.lab.device.entity.DeviceMaintenance;
import com.lab.device.mapper.DeviceCategoryMapper;
import com.lab.device.mapper.DeviceInfoMapper;
import com.lab.device.mapper.DeviceMaintenanceMapper;
import com.lab.device.service.DeviceService;
import com.lab.common.exception.BusinessException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.*;

/**
 * 设备管理服务实现
 * ★ 关键：库存扣减使用乐观锁控制（decreaseAvailableQuantity）
 */
@Slf4j
@Service
public class DeviceServiceImpl implements DeviceService {

    @Resource
    private DeviceInfoMapper deviceInfoMapper;

    @Resource
    private DeviceCategoryMapper deviceCategoryMapper;

    @Resource
    private DeviceMaintenanceMapper deviceMaintenanceMapper;

    // ==================== 设备分类 ====================

    @Override
    public List<DeviceCategory> getCategoryTree() {
        List<DeviceCategory> allCategories = deviceCategoryMapper.selectList(
                new LambdaQueryWrapper<DeviceCategory>().orderByAsc(DeviceCategory::getSortOrder)
        );
        return buildTree(allCategories, 0L);
    }

    private List<DeviceCategory> buildTree(List<DeviceCategory> all, Long parentId) {
        List<DeviceCategory> tree = new ArrayList<>();
        for (DeviceCategory cat : all) {
            if (parentId.equals(cat.getParentId())) {
                cat.setChildren(buildTree(all, cat.getId()));
                tree.add(cat);
            }
        }
        return tree;
    }

    @Override
    public void addCategory(DeviceCategory category) {
        category.setDeleted(0);
        deviceCategoryMapper.insert(category);
    }

    @Override
    public void updateCategory(DeviceCategory category) {
        deviceCategoryMapper.updateById(category);
    }

    @Override
    public void deleteCategory(Long id) {
        // 检查该分类下是否有关联设备
        Long deviceCount = deviceInfoMapper.selectCount(
                new LambdaQueryWrapper<DeviceInfo>().eq(DeviceInfo::getCategoryId, id)
        );
        if (deviceCount > 0) {
            throw new BusinessException("该分类下存在关联设备（共" + deviceCount + "台），无法删除");
        }
        // 检查是否有子分类
        Long childCount = deviceCategoryMapper.selectCount(
                new LambdaQueryWrapper<DeviceCategory>().eq(DeviceCategory::getParentId, id)
        );
        if (childCount > 0) {
            throw new BusinessException("该分类下存在子分类，请先删除子分类");
        }
        deviceCategoryMapper.deleteById(id);
    }

    // ==================== 设备台账 ====================

    @Override
    public void addDevice(DeviceInfo deviceInfo) {
        // 检查设备编号唯一性
        Long count = deviceInfoMapper.selectCount(
                new LambdaQueryWrapper<DeviceInfo>().eq(DeviceInfo::getCode, deviceInfo.getCode())
        );
        if (count > 0) {
            throw new BusinessException("设备编号已存在: " + deviceInfo.getCode());
        }
        deviceInfo.setDeleted(0);
        deviceInfo.setVersion(0);
        // 默认可用数量等于总数量
        if (deviceInfo.getAvailableQuantity() == null) {
            deviceInfo.setAvailableQuantity(deviceInfo.getTotalQuantity());
        }
        deviceInfoMapper.insert(deviceInfo);
        log.info("新增设备: code={}, name={}", deviceInfo.getCode(), deviceInfo.getName());
    }

    @Override
    public void updateDevice(DeviceInfo deviceInfo) {
        int rows = deviceInfoMapper.updateById(deviceInfo);
        if (rows == 0) {
            throw new BusinessException("设备信息已被其他用户修改，请刷新后重试");
        }
        log.info("修改设备: id={}", deviceInfo.getId());
    }

    @Override
    public void deleteDevice(Long id) {
        DeviceInfo device = deviceInfoMapper.selectById(id);
        if (device == null) {
            throw new BusinessException("设备不存在");
        }
        if (device.getAvailableQuantity() < device.getTotalQuantity()) {
            throw new BusinessException("该设备存在未归还的借用记录（已借出" + (device.getTotalQuantity() - device.getAvailableQuantity()) + "台），无法删除");
        }
        // 检查是否有未完成的维修记录
        Long maintCount = deviceMaintenanceMapper.selectCount(
                new LambdaQueryWrapper<DeviceMaintenance>()
                        .eq(DeviceMaintenance::getDeviceId, id)
                        .in(DeviceMaintenance::getStatus, 0, 1)
        );
        if (maintCount > 0) {
            throw new BusinessException("该设备存在未完成的维修记录，无法删除");
        }
        deviceInfoMapper.deleteById(id);
        log.info("删除设备: id={}", id);
    }

    @Override
    public DeviceInfo getDeviceById(Long id) {
        DeviceInfo device = deviceInfoMapper.selectById(id);
        if (device == null) {
            throw new BusinessException("设备不存在");
        }
        // 填充虚拟字段 categoryName
        if (device.getCategoryId() != null) {
            DeviceCategory category = deviceCategoryMapper.selectById(device.getCategoryId());
            if (category != null) {
                device.setCategoryName(category.getName());
            }
        }
        return device;
    }

    @Override
    public Page<DeviceInfo> getDevicePage(int pageNum, int pageSize, String name, Long categoryId, Long labId, Integer status) {
        Page<DeviceInfo> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<DeviceInfo> wrapper = new LambdaQueryWrapper<>();
        if (StrUtil.isNotBlank(name)) {
            wrapper.like(DeviceInfo::getName, name);
        }
        if (categoryId != null) {
            wrapper.eq(DeviceInfo::getCategoryId, categoryId);
        }
        if (labId != null) {
            wrapper.eq(DeviceInfo::getLabId, labId);
        }
        if (status != null) {
            wrapper.eq(DeviceInfo::getStatus, status);
        }
        wrapper.orderByDesc(DeviceInfo::getCreateTime);
        Page<DeviceInfo> result = deviceInfoMapper.selectPage(page, wrapper);
        // 填充虚拟字段 categoryName
        fillCategoryName(result.getRecords());
        return result;
    }

    @Override
    public void updateDeviceStatus(Long id, Integer status) {
        DeviceInfo existing = deviceInfoMapper.selectById(id);
        if (existing == null) {
            throw new BusinessException("设备不存在");
        }
        existing.setStatus(status);
        int rows = deviceInfoMapper.updateById(existing);
        if (rows == 0) {
            throw new BusinessException("设备状态更新冲突，请刷新后重试");
        }
        log.info("更新设备状态: id={}, status={}", id, status);
    }

    // ==================== 库存操作（乐观锁核心实现） ====================

    /**
     * ★ 核心方法：乐观锁扣减可用库存
     *
     * 使用 deviceMapper.update(null, wrapper) 搭配乐观锁控制并发扣减：
     * UPDATE device_info SET available_quantity = available_quantity - #{quantity},
     * version = version + 1
     * WHERE id = #{id} AND version = #{version} AND available_quantity >= #{quantity}
     *
     * 若影响行数为0，表示库存不足或被并发修改，抛出 BusinessException
     *
     * @param deviceId 设备ID
     * @param quantity 扣减数量
     * @param version  乐观锁版本号
     * @return true=扣减成功, false=扣减失败
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean decreaseStock(Long deviceId, Integer quantity, Integer version) {
        int affectedRows = deviceInfoMapper.decreaseAvailableQuantity(deviceId, quantity, version);
        if (affectedRows == 0) {
            log.warn("库存扣减失败（库存不足或并发冲突）: deviceId={}, quantity={}, version={}", deviceId, quantity, version);
            return false;
        }
        log.info("库存扣减成功: deviceId={}, quantity={}", deviceId, quantity);
        return true;
    }

    /**
     * 乐观锁回加库存（归还/取消/驳回时调用）
     *
     * @param deviceId 设备ID
     * @param quantity 回加数量
     * @param version  乐观锁版本号
     * @return true=成功, false=失败
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public boolean increaseStock(Long deviceId, Integer quantity, Integer version) {
        int affectedRows = deviceInfoMapper.increaseAvailableQuantity(deviceId, quantity, version);
        if (affectedRows == 0) {
            log.warn("库存回加失败（并发冲突）: deviceId={}, quantity={}, version={}", deviceId, quantity, version);
            return false;
        }
        log.info("库存回加成功: deviceId={}, quantity={}", deviceId, quantity);
        return true;
    }

    /**
     * 获取设备信息（含版本号，供库存操作使用）
     */
    @Override
    public DeviceInfo getDeviceInfoWithVersion(Long deviceId) {
        DeviceInfo device = deviceInfoMapper.selectById(deviceId);
        if (device == null) {
            throw new BusinessException("设备不存在");
        }
        return device;
    }

    // ==================== 维修记录 ====================

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void addMaintenance(DeviceMaintenance maintenance) {
        maintenance.setDeleted(0);
        maintenance.setStatus(0);
        deviceMaintenanceMapper.insert(maintenance);
        // 同步更新设备状态为维修中（带乐观锁检查）
        DeviceInfo existing = deviceInfoMapper.selectById(maintenance.getDeviceId());
        if (existing != null) {
            existing.setStatus(1);
            deviceInfoMapper.updateById(existing);
        }
        log.info("新增维修记录: deviceId={}", maintenance.getDeviceId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateMaintenanceStatus(Long id, Integer status) {
        DeviceMaintenance existing = deviceMaintenanceMapper.selectById(id);
        if (existing == null) {
            throw new BusinessException("维修记录不存在");
        }
        existing.setStatus(status);
        deviceMaintenanceMapper.updateById(existing);
        // 如果修复完成，更新设备状态为正常
        if (status == 2 && existing.getDeviceId() != null) {
            DeviceInfo device = deviceInfoMapper.selectById(existing.getDeviceId());
            if (device != null) {
                device.setStatus(0);
                deviceInfoMapper.updateById(device);
            }
        }
        // 如果无法修复，更新设备状态为已报废
        if (status == 3 && existing.getDeviceId() != null) {
            DeviceInfo device = deviceInfoMapper.selectById(existing.getDeviceId());
            if (device != null) {
                device.setStatus(2);
                deviceInfoMapper.updateById(device);
            }
        }
    }

    @Override
    public Page<DeviceMaintenance> getMaintenancePage(int pageNum, int pageSize, Long deviceId, Integer status) {
        Page<DeviceMaintenance> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<DeviceMaintenance> wrapper = new LambdaQueryWrapper<>();
        if (deviceId != null) {
            wrapper.eq(DeviceMaintenance::getDeviceId, deviceId);
        }
        if (status != null) {
            wrapper.eq(DeviceMaintenance::getStatus, status);
        }
        wrapper.orderByDesc(DeviceMaintenance::getCreateTime);
        Page<DeviceMaintenance> result = deviceMaintenanceMapper.selectPage(page, wrapper);
        // 填充虚拟字段 deviceName（reportUserName 需要跨服务调用，暂不填充）
        fillDeviceNameForMaintenance(result.getRecords());
        return result;
    }

    // ==================== 虚拟字段填充辅助方法 ====================

    private void fillCategoryName(List<DeviceInfo> devices) {
        if (devices == null || devices.isEmpty()) {
            return;
        }
        // 批量收集 categoryId 并缓存查询结果
        Map<Long, String> categoryNameMap = new HashMap<>();
        for (DeviceInfo device : devices) {
            if (device.getCategoryId() != null && !categoryNameMap.containsKey(device.getCategoryId())) {
                DeviceCategory category = deviceCategoryMapper.selectById(device.getCategoryId());
                if (category != null) {
                    categoryNameMap.put(device.getCategoryId(), category.getName());
                }
            }
        }
        for (DeviceInfo device : devices) {
            if (device.getCategoryId() != null) {
                device.setCategoryName(categoryNameMap.get(device.getCategoryId()));
            }
        }
    }

    private void fillDeviceNameForMaintenance(List<DeviceMaintenance> records) {
        if (records == null || records.isEmpty()) {
            return;
        }
        // 批量收集 deviceId 并缓存查询结果
        Map<Long, String> deviceNameMap = new HashMap<>();
        for (DeviceMaintenance record : records) {
            if (record.getDeviceId() != null && !deviceNameMap.containsKey(record.getDeviceId())) {
                DeviceInfo device = deviceInfoMapper.selectById(record.getDeviceId());
                if (device != null) {
                    deviceNameMap.put(record.getDeviceId(), device.getName());
                }
            }
        }
        for (DeviceMaintenance record : records) {
            if (record.getDeviceId() != null) {
                record.setDeviceName(deviceNameMap.get(record.getDeviceId()));
            }
        }
    }
}
