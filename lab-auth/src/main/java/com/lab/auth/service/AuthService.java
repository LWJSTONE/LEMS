package com.lab.auth.service;

import com.lab.auth.dto.LoginRequest;
import com.lab.auth.dto.LoginResponse;
import com.lab.auth.dto.RegisterRequest;

/**
 * 认证服务接口
 */
public interface AuthService {

    /**
     * 用户登录
     */
    LoginResponse login(LoginRequest request);

    /**
     * 用户注册
     */
    void register(RegisterRequest request);

    /**
     * 用户登出（将token加入黑名单）
     */
    void logout(String token);
}
