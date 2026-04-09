package com.lab.user.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * 密码修改请求 DTO
 */
@Data
public class PasswordChangeRequest {

    @NotBlank(message = "旧密码不能为空")
    private String oldPassword;

    @NotBlank(message = "新密码不能为空")
    private String newPassword;
}
