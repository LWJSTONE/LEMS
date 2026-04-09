package com.lab.borrow;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * 借用预约服务启动类
 */
@SpringBootApplication(scanBasePackages = "com.lab")
@EnableDiscoveryClient
@EnableFeignClients(basePackages = "com.lab.common.feign")
@MapperScan("com.lab.borrow.mapper")
@EnableScheduling
public class BorrowApplication {
    public static void main(String[] args) {
        SpringApplication.run(BorrowApplication.class, args);
    }
}
