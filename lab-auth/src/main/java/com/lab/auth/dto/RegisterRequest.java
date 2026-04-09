package com.lab.auth.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * 注册请求DTO
 */
@Data
public class RegisterRequest {

    @NotBlank(message = "用户名不能为空")
    private String username;

    @NotBlank(message = "密码不能为空")
    private String password;

    @NotBlank(message = "姓名不能为空")
    private String realName;

    private String phone;
    private String email;
    private String roleType;
    private Long labId;
}
