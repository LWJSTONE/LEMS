package com.lab.auth.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.lab.auth.dto.LoginRequest;
import com.lab.auth.dto.LoginResponse;
import com.lab.auth.dto.RegisterRequest;
import com.lab.auth.entity.SysUser;
import com.lab.auth.mapper.SysUserMapper;
import com.lab.auth.service.AuthService;
import com.lab.common.constant.CommonConstant;
import com.lab.common.exception.BusinessException;
import com.lab.common.util.JwtUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.concurrent.TimeUnit;

/**
 * 认证服务实现
 */
@Slf4j
@Service
public class AuthServiceImpl implements AuthService {

    @Resource
    private SysUserMapper sysUserMapper;

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Value("${jwt.expiration}")
    private long jwtExpiration;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public LoginResponse login(LoginRequest request) {
        // 查询用户
        // @TableLogic 会自动追加 deleted=0 条件，无需手动添加
        SysUser user = sysUserMapper.selectOne(
                new LambdaQueryWrapper<SysUser>()
                        .eq(SysUser::getUsername, request.getUsername())
        );

        if (user == null) {
            throw new BusinessException("用户名或密码错误");
        }

        // 校验密码
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new BusinessException("用户名或密码错误");
        }

        // 校验状态
        if (user.getStatus() != 1) {
            throw new BusinessException("账号已被禁用，请联系管理员");
        }

        // 生成JWT Token
        String token = JwtUtil.generateToken(
                user.getId(),
                user.getUsername(),
                user.getRoleType(),
                jwtSecret,
                jwtExpiration
        );

        log.info("用户登录成功: userId={}, username={}, role={}", user.getId(), user.getUsername(), user.getRoleType());

        // LoginResponse字段: token, id, username, realName, roleType, labId
        // id 与 SysUser.id 一致，前端统一使用 userStore.userInfo.id
        return new LoginResponse(
                CommonConstant.JWT_PREFIX + token,
                user.getId(),
                user.getUsername(),
                user.getRealName(),
                user.getRoleType(),
                user.getLabId()
        );
    }

    @Override
    public void register(RegisterRequest request) {
        // 检查用户名是否已存在
        // @TableLogic 会自动追加 deleted=0 条件，无需手动添加
        Long count = sysUserMapper.selectCount(
                new LambdaQueryWrapper<SysUser>()
                        .eq(SysUser::getUsername, request.getUsername())
        );
        if (count > 0) {
            throw new BusinessException("用户名已存在");
        }

        // 构建用户实体
        SysUser user = new SysUser();
        user.setUsername(request.getUsername());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setRealName(request.getRealName());
        user.setPhone(request.getPhone());
        user.setEmail(request.getEmail());

        // 设置角色，仅允许学生或教师自注册（防止角色越权）
        String role = request.getRoleType();
        if (StrUtil.isBlank(role)) {
            user.setRoleType(CommonConstant.ROLE_STUDENT);
        } else if (CommonConstant.ROLE_STUDENT.equals(role) || CommonConstant.ROLE_TEACHER.equals(role)) {
            user.setRoleType(role);
        } else {
            throw new BusinessException("非法的角色类型，仅允许注册为学生或教师");
        }
        user.setLabId(request.getLabId());
        user.setStatus(1);
        user.setDeleted(0);

        sysUserMapper.insert(user);
        log.info("用户注册成功: username={}, role={}", user.getUsername(), user.getRoleType());
    }

    @Override
    public void logout(String token) {
        if (StrUtil.isBlank(token)) {
            return;
        }
        // 去掉Bearer前缀
        if (token.startsWith(CommonConstant.JWT_PREFIX)) {
            token = token.substring(CommonConstant.JWT_PREFIX.length());
        }

        // 将token加入Redis黑名单，设置过期时间与JWT过期时间一致
        String blacklistKey = CommonConstant.JWT_BLACKLIST_PREFIX + token;
        stringRedisTemplate.opsForValue().set(blacklistKey, "1", jwtExpiration, TimeUnit.MILLISECONDS);
        log.info("用户登出成功");
    }
}
