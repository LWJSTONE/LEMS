package com.lab.device.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 设备台账实体
 */
@Data
@TableName("device_info")
public class DeviceInfo {
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;
    private String code;
    private String name;
    private String model;
    private Long categoryId;
    private Long labId;
    private Integer totalQuantity;
    private Integer availableQuantity;
    private String unit;
    private BigDecimal price;
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate purchaseDate;
    private Integer status;
    private String locationDetail;
    private String description;
    @Version
    private Integer version;
    @TableLogic
    private Integer deleted;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;
    @TableField(exist = false)
    private String categoryName;
    @TableField(exist = false)
    private String labName;
}
