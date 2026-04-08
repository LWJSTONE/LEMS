package com.lab.user.entity;

import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 实验室实体
 */
@Data
@TableName("lab_info")
public class LabInfo {
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;
    private String name;
    private String location;
    private Long managerId;
    private String contactPhone;
    private Integer status;
    @TableLogic
    private Integer deleted;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createTime;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updateTime;
    @TableField(exist = false)
    private String managerName;
}
