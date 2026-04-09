package com.lab.user.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.user.entity.LabInfo;
import com.lab.user.entity.SysUser;

import java.util.List;

/**
 * 用户服务接口
 */
public interface UserService {

    /**
     * 根据ID获取用户信息
     */
    SysUser getUserById(Long id);

    /**
     * 获取用户手机号
     */
    String getUserPhone(Long id);

    /**
     * 获取当前用户个人信息
     */
    SysUser getProfile(Long userId);

    /**
     * 修改个人信息
     */
    void updateProfile(Long userId, SysUser user);

    /**
     * 分页查询用户列表（管理员）
     */
    Page<SysUser> getUserPage(int pageNum, int pageSize, String keyword, String roleType);

    /**
     * 更新用户状态
     */
    void updateUserStatus(Long userId, Integer status);

    /**
     * 获取实验室列表
     */
    List<LabInfo> getLabList();

    /**
     * 获取实验室成员列表
     */
    Page<SysUser> getLabMembers(Long labId, int pageNum, int pageSize);

    /**
     * 新增实验室
     */
    void addLab(LabInfo labInfo);

    /**
     * 修改实验室
     */
    void updateLab(LabInfo labInfo);

    /**
     * 修改密码
     */
    void changePassword(Long userId, String oldPassword, String newPassword);
}
