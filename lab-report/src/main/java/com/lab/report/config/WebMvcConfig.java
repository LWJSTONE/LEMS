package com.lab.report.config;

import com.lab.common.interceptor.RoleAuthInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new RoleAuthInterceptor())
                .addPathPatterns("/api/v1/**")
                .excludePathPatterns("/api/v1/auth/**");
    }
}
