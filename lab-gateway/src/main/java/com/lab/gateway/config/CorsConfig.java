package com.lab.gateway.config;

import org.springframework.context.annotation.Configuration;

/**
 * 跨域配置
 * CORS 已在 application.yml 中通过 spring.cloud.gateway.globalcors 配置
 * 此类保留用于后续扩展其他网关配置
 */
@Configuration
public class CorsConfig {
    // CORS 由 YAML 配置统一管理，无需额外的 CorsWebFilter Bean
}
