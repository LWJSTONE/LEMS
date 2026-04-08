package com.lab.auth.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

/**
 * 系统用户实体（认证服务专用）
 */
@Data
@TableName("sys_user")
public class SysUser {
    private Long id;
    private String username;
    private String passwordHash;
    private String realName;
    private String phone;
    private String email;
    private String roleType;
    private Long labId;
    private Integer status;
    private Integer deleted;
    @TableField(exist = false)
    private String token;
}
