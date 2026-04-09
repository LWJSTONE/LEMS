package com.lab.common.annotation;

import java.lang.annotation.*;

/**
 * 角色权限注解
 * 标注在Controller方法上，限制只有指定角色的用户才能访问
 */
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface RequireRole {
    String[] value();
}
