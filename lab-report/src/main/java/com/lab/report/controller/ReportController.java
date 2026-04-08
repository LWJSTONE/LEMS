package com.lab.report.controller;

import com.lab.common.result.R;
import com.lab.report.entity.DeviceUsageStat;
import com.lab.report.entity.MonthlyTrend;
import com.lab.report.mapper.ReportMapper;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

/**
 * 统计报表控制器
 */
@RestController
@RequestMapping("/api/v1/report")
public class ReportController {

    @Resource
    private ReportMapper reportMapper;

    /**
     * 首页仪表盘统计数据
     */
    @GetMapping("/dashboard")
    public R<Map<String, Object>> getDashboardStats() {
        return R.ok(reportMapper.getDashboardStats());
    }

    /**
     * 设备使用率Top10（Echarts数据）
     */
    @GetMapping("/device/usage/top")
    public R<List<DeviceUsageStat>> getDeviceUsageTop() {
        return R.ok(reportMapper.getDeviceUsageTop10());
    }

    /**
     * 月度借用趋势图（Echarts数据）
     */
    @GetMapping("/borrow/trend")
    public R<List<MonthlyTrend>> getMonthlyTrend() {
        return R.ok(reportMapper.getMonthlyTrend());
    }
}
