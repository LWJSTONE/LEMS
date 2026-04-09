package com.lab.device.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 维修记录实体
 */
@Data
@TableName("device_maintenance")
public class DeviceMaintenance {
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;
    private Long deviceId;
    private Long reportUserId;
    private String faultDesc;
    private Integer status;
    private BigDecimal cost;
    private String repairCompany;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime finishTime;
    @TableLogic
    private Integer deleted;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;
    @TableField(exist = false)
    private String deviceName;
    @TableField(exist = false)
    private String reportUserName;
}
