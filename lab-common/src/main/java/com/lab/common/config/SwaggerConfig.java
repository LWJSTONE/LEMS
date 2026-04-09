package com.lab.common.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;

/**
 * Swagger2 接口文档配置
 * 各微服务引入 lab-common 后扫描自己的 controller 包即可
 */
@Configuration
@ConditionalOnClass(name = "springfox.documentation.spring.web.plugins.Docket")
public class SwaggerConfig {

    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.OAS_30)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.lab"))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("LEMS 实验设备管理系统 API 文档")
                .description("基于 Spring Cloud 微服务架构的高校实验室设备全生命周期管理平台")
                .version("V1.0")
                .contact(new Contact("LEMS", "", ""))
                .build();
    }
}
