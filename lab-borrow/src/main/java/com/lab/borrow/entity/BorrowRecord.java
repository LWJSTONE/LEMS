package com.lab.borrow.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 借用预约记录实体
 */
@Data
@TableName("borrow_record")
public class BorrowRecord {
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;
    private Long deviceId;
    private Long userId;
    private String purpose;
    private Integer borrowQuantity;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime startTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime endTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime actualReturnTime;
    private Integer status;
    private Long approverId;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime approveTime;
    private String rejectReason;
    private String returnRemark;
    @Version
    private Integer version;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
    @TableField(exist = false)
    private String deviceName;
    @TableField(exist = false)
    private String deviceCode;
    @TableField(exist = false)
    private String userName;
    @TableField(exist = false)
    private String approverName;
}
