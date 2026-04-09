package com.lab.user.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.user.entity.LabInfo;
import com.lab.user.entity.SysUser;
import com.lab.user.mapper.LabInfoMapper;
import com.lab.user.mapper.SysUserMapper;
import com.lab.user.service.UserService;
import com.lab.common.exception.BusinessException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.*;

/**
 * 用户服务实现
 */
@Slf4j
@Service
public class UserServiceImpl implements UserService {

    @Resource
    private SysUserMapper sysUserMapper;

    @Resource
    private LabInfoMapper labInfoMapper;

    @Override
    public SysUser getUserById(Long id) {
        SysUser user = sysUserMapper.selectById(id);
        if (user != null) {
            user.setPasswordHash(null);
        }
        return user;
    }

    @Override
    public String getUserPhone(Long id) {
        SysUser user = sysUserMapper.selectById(id);
        return user != null ? user.getPhone() : null;
    }

    @Override
    public SysUser getProfile(Long userId) {
        SysUser user = sysUserMapper.selectById(userId);
        if (user == null) {
            throw new BusinessException("用户不存在");
        }
        user.setPasswordHash(null);
        // 查询实验室名称
        if (user.getLabId() != null) {
            LabInfo lab = labInfoMapper.selectById(user.getLabId());
            if (lab != null) {
                user.setLabName(lab.getName());
            }
        }
        return user;
    }

    @Override
    public void updateProfile(Long userId, SysUser user) {
        SysUser existing = sysUserMapper.selectById(userId);
        if (existing == null) {
            throw new BusinessException("用户不存在");
        }
        existing.setRealName(user.getRealName());
        existing.setPhone(user.getPhone());
        existing.setEmail(user.getEmail());
        sysUserMapper.updateById(existing);
    }

    @Override
    public Page<SysUser> getUserPage(int pageNum, int pageSize, String keyword, String roleType) {
        Page<SysUser> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<SysUser> wrapper = new LambdaQueryWrapper<>();
        if (StrUtil.isNotBlank(keyword)) {
            wrapper.and(w -> w.like(SysUser::getUsername, keyword)
                    .or().like(SysUser::getRealName, keyword));
        }
        if (StrUtil.isNotBlank(roleType)) {
            wrapper.eq(SysUser::getRoleType, roleType);
        }
        wrapper.orderByDesc(SysUser::getCreateTime);
        Page<SysUser> result = sysUserMapper.selectPage(page, wrapper);
        // 清除密码字段
        result.getRecords().forEach(u -> u.setPasswordHash(null));
        // 填充虚拟字段 labName
        fillLabName(result.getRecords());
        return result;
    }

    @Override
    public void updateUserStatus(Long userId, Integer status) {
        SysUser existing = sysUserMapper.selectById(userId);
        if (existing == null) {
            throw new BusinessException("用户不存在");
        }
        existing.setStatus(status);
        sysUserMapper.updateById(existing);
    }

    @Override
    public List<LabInfo> getLabList() {
        List<LabInfo> labs = labInfoMapper.selectList(
                new LambdaQueryWrapper<LabInfo>().eq(LabInfo::getStatus, 1).orderByAsc(LabInfo::getId)
        );
        // 填充虚拟字段 managerName
        fillManagerName(labs);
        return labs;
    }

    @Override
    public Page<SysUser> getLabMembers(Long labId, int pageNum, int pageSize) {
        Page<SysUser> page = new Page<>(pageNum, pageSize);
        LambdaQueryWrapper<SysUser> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(SysUser::getLabId, labId);
        wrapper.orderByAsc(SysUser::getRoleType).orderByDesc(SysUser::getCreateTime);
        Page<SysUser> result = sysUserMapper.selectPage(page, wrapper);
        result.getRecords().forEach(u -> u.setPasswordHash(null));
        return result;
    }

    @Override
    public void addLab(LabInfo labInfo) {
        labInfo.setStatus(1);
        labInfo.setDeleted(0);
        labInfoMapper.insert(labInfo);
    }

    @Override
    public void updateLab(LabInfo labInfo) {
        LabInfo existing = labInfoMapper.selectById(labInfo.getId());
        if (existing == null) {
            throw new BusinessException("实验室不存在");
        }
        labInfoMapper.updateById(labInfo);
    }

    @Override
    public void changePassword(Long userId, String oldPassword, String newPassword) {
        SysUser user = sysUserMapper.selectById(userId);
        if (user == null) {
            throw new BusinessException("用户不存在");
        }
        BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        if (!passwordEncoder.matches(oldPassword, user.getPasswordHash())) {
            throw new BusinessException("旧密码不正确");
        }
        if (oldPassword.equals(newPassword)) {
            throw new BusinessException("新密码不能与旧密码相同");
        }
        user.setPasswordHash(passwordEncoder.encode(newPassword));
        sysUserMapper.updateById(user);
        log.info("用户 {} 修改密码成功", userId);
    }

    // ==================== 虚拟字段填充辅助方法 ====================

    /**
     * 批量填充用户的 labName 虚拟字段
     */
    private void fillLabName(List<SysUser> users) {
        if (users == null || users.isEmpty()) {
            return;
        }
        Map<Long, String> labNameMap = new HashMap<>();
        for (SysUser user : users) {
            if (user.getLabId() != null && !labNameMap.containsKey(user.getLabId())) {
                LabInfo lab = labInfoMapper.selectById(user.getLabId());
                if (lab != null) {
                    labNameMap.put(user.getLabId(), lab.getName());
                }
            }
        }
        for (SysUser user : users) {
            if (user.getLabId() != null) {
                user.setLabName(labNameMap.get(user.getLabId()));
            }
        }
    }

    /**
     * 批量填充实验室的 managerName 虚拟字段
     */
    private void fillManagerName(List<LabInfo> labs) {
        if (labs == null || labs.isEmpty()) {
            return;
        }
        Map<Long, String> managerNameMap = new HashMap<>();
        for (LabInfo lab : labs) {
            if (lab.getManagerId() != null && !managerNameMap.containsKey(lab.getManagerId())) {
                SysUser manager = sysUserMapper.selectById(lab.getManagerId());
                if (manager != null) {
                    managerNameMap.put(lab.getManagerId(), manager.getRealName());
                }
            }
        }
        for (LabInfo lab : labs) {
            if (lab.getManagerId() != null) {
                lab.setManagerName(managerNameMap.get(lab.getManagerId()));
            }
        }
    }
}
