package com.lab.auth.controller;

import com.lab.auth.dto.LoginRequest;
import com.lab.auth.dto.LoginResponse;
import com.lab.auth.dto.RegisterRequest;
import com.lab.auth.service.AuthService;
import com.lab.common.result.R;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;

/**
 * 认证控制器
 */
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    @Resource
    private AuthService authService;

    /**
     * 用户登录
     */
    @PostMapping("/login")
    public R<LoginResponse> login(@Validated @RequestBody LoginRequest request) {
        LoginResponse response = authService.login(request);
        return R.ok(response);
    }

    /**
     * 用户注册
     */
    @PostMapping("/register")
    public R<Void> register(@Validated @RequestBody RegisterRequest request) {
        authService.register(request);
        return R.ok();
    }

    /**
     * 用户登出
     */
    @PostMapping("/logout")
    public R<Void> logout(HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        authService.logout(authHeader);
        return R.ok();
    }
}
