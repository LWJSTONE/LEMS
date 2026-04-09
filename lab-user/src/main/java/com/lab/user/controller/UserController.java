package com.lab.user.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.common.annotation.RequireRole;
import com.lab.common.result.R;
import com.lab.user.dto.PasswordChangeRequest;
import com.lab.user.entity.LabInfo;
import com.lab.user.entity.SysUser;
import com.lab.user.service.UserService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;

/**
 * 用户管理控制器
 */
@RestController
@RequestMapping("/api/v1/user")
public class UserController {

    @Resource
    private UserService userService;

    /**
     * 获取当前用户个人信息
     */
    @GetMapping("/profile")
    public R<SysUser> getProfile(@RequestHeader("X-User-Id") Long userId) {
        return R.ok(userService.getProfile(userId));
    }

    /**
     * 修改个人信息
     */
    @PutMapping("/profile")
    public R<Void> updateProfile(@RequestHeader("X-User-Id") Long userId,
                                  @RequestBody SysUser user) {
        userService.updateProfile(userId, user);
        return R.ok();
    }

    /**
     * 修改密码
     */
    @PutMapping("/password")
    public R<Void> changePassword(@RequestHeader("X-User-Id") Long userId,
                                   @RequestBody PasswordChangeRequest request) {
        userService.changePassword(userId, request.getOldPassword(), request.getNewPassword());
        return R.ok();
    }

    /**
     * 分页查询用户列表（管理员）
     */
    @RequireRole("ADMIN")
    @GetMapping("/page")
    public R<Page<SysUser>> getUserPage(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) String roleType) {
        return R.ok(userService.getUserPage(current, size, keyword, roleType));
    }

    /**
     * 更新用户状态（管理员）
     */
    @RequireRole("ADMIN")
    @PutMapping("/{id}/status")
    public R<Void> updateUserStatus(@PathVariable Long id, @RequestParam Integer status) {
        userService.updateUserStatus(id, status);
        return R.ok();
    }

    /**
     * 获取实验室列表
     */
    @GetMapping("/lab/list")
    public R<List<LabInfo>> getLabList() {
        return R.ok(userService.getLabList());
    }

    /**
     * 获取实验室成员列表
     */
    @GetMapping("/lab/members")
    public R<Page<SysUser>> getLabMembers(
            @RequestParam Long labId,
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size) {
        return R.ok(userService.getLabMembers(labId, current, size));
    }

    /**
     * 新增实验室（管理员）
     */
    @RequireRole("ADMIN")
    @PostMapping("/lab")
    public R<Void> addLab(@RequestBody LabInfo labInfo) {
        userService.addLab(labInfo);
        return R.ok();
    }

    /**
     * 修改实验室（管理员）
     */
    @RequireRole("ADMIN")
    @PutMapping("/lab")
    public R<Void> updateLab(@RequestBody LabInfo labInfo) {
        userService.updateLab(labInfo);
        return R.ok();
    }

    // ========== 内部Feign调用接口 ==========

    /**
     * 内部接口：根据ID获取用户信息
     */
    @GetMapping("/inner/{id}")
    public R<?> getUserById(@PathVariable Long id) {
        return R.ok(userService.getUserById(id));
    }

    /**
     * 内部接口：获取用户手机号
     */
    @GetMapping("/inner/{id}/phone")
    public R<String> getUserPhone(@PathVariable Long id) {
        return R.ok(userService.getUserPhone(id));
    }
}
