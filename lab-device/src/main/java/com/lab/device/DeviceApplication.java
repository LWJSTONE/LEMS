package com.lab.device;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 * 设备管理服务启动类
 */
@SpringBootApplication(scanBasePackages = "com.lab")
@EnableDiscoveryClient
@MapperScan("com.lab.device.mapper")
public class DeviceApplication {
    public static void main(String[] args) {
        SpringApplication.run(DeviceApplication.class, args);
    }
}
