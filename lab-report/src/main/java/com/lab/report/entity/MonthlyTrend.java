package com.lab.report.entity;

import lombok.Data;

/**
 * 月度借用趋势
 */
@Data
public class MonthlyTrend {
    private String month;
    private Long borrowCount;
    private Long totalQuantity;
}
