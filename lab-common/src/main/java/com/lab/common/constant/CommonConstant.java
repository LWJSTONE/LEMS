package com.lab.common.constant;

/**
 * 公共常量
 */
public class CommonConstant {

    /** JWT请求头 */
    public static final String JWT_HEADER = "Authorization";

    /** 用户ID请求头（网关传递） */
    public static final String USER_ID_HEADER = "X-User-Id";

    /** 用户角色请求头（网关传递） */
    public static final String USER_ROLE_HEADER = "X-User-Role";

    /** 用户名请求头（网关传递） */
    public static final String USERNAME_HEADER = "X-Username";

    /** JWT前缀 */
    public static final String JWT_PREFIX = "Bearer ";

    /** Redis JWT黑名单前缀 */
    public static final String JWT_BLACKLIST_PREFIX = "jwt:blacklist:";

    /** Redis分布式锁前缀 */
    public static final String LOCK_DEVICE_PREFIX = "lock:device:";

    /** 角色常量 */
    public static final String ROLE_ADMIN = "ADMIN";
    public static final String ROLE_TEACHER = "TEACHER";
    public static final String ROLE_STUDENT = "STUDENT";

    /** 默认分页大小 */
    public static final int DEFAULT_PAGE_SIZE = 10;

    /** 默认分页页码 */
    public static final int DEFAULT_PAGE_NUM = 1;
}
