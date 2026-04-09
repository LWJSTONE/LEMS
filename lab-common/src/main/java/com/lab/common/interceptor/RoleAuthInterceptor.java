package com.lab.common.interceptor;

import com.lab.common.annotation.RequireRole;
import com.lab.common.constant.CommonConstant;
import com.lab.common.exception.BusinessException;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Arrays;

/**
 * 角色权限拦截器
 * 检查当前请求用户的角色是否满足 @RequireRole 注解的要求
 */
public class RoleAuthInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        if (!(handler instanceof HandlerMethod)) {
            return true;
        }
        HandlerMethod handlerMethod = (HandlerMethod) handler;

        // 检查方法上的注解
        RequireRole methodAnnotation = handlerMethod.getMethodAnnotation(RequireRole.class);
        // 检查类上的注解
        RequireRole classAnnotation = handlerMethod.getBeanType().getAnnotation(RequireRole.class);

        RequireRole requireRole = methodAnnotation != null ? methodAnnotation : classAnnotation;
        if (requireRole == null) {
            return true;
        }

        String userRole = request.getHeader(CommonConstant.USER_ROLE_HEADER);
        if (userRole == null || userRole.isEmpty()) {
            throw new BusinessException("未获取到用户角色信息，请重新登录");
        }

        String[] requiredRoles = requireRole.value();
        if (!Arrays.asList(requiredRoles).contains(userRole)) {
            throw new BusinessException("权限不足，无法执行此操作");
        }

        return true;
    }
}
