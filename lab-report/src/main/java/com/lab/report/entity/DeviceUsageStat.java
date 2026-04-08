package com.lab.report.entity;

import lombok.Data;

/**
 * 设备使用率统计
 */
@Data
public class DeviceUsageStat {
    private Long id;
    private String name;
    private String code;
    private Integer totalQuantity;
    private Integer availableQuantity;
    private Long borrowCount;
    private Long totalBorrowQuantity;
    private Double usageRate;
}
