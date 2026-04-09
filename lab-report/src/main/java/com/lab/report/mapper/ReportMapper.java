package com.lab.report.mapper;

import com.lab.report.entity.DeviceUsageStat;
import com.lab.report.entity.MonthlyTrend;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
 * 统计报表Mapper
 */
@Mapper
public interface ReportMapper {

    /**
     * 设备使用率Top10
     */
    @Select("SELECT d.id, d.name, d.code, d.total_quantity AS totalQuantity, " +
            "d.available_quantity AS availableQuantity, " +
            "COUNT(br.id) AS borrowCount, " +
            "SUM(br.borrow_quantity) AS totalBorrowQuantity, " +
            "ROUND(SUM(br.borrow_quantity) / d.total_quantity * 100, 2) AS usageRate " +
            "FROM device_info d " +
            "LEFT JOIN borrow_record br ON d.id = br.device_id AND br.status IN (1, 2, 3) " +
            "WHERE d.deleted = 0 " +
            "GROUP BY d.id, d.name, d.code, d.total_quantity, d.available_quantity " +
            "ORDER BY usageRate DESC " +
            "LIMIT 10")
    List<DeviceUsageStat> getDeviceUsageTop10();

    /**
     * 月度借用趋势图
     */
    @Select("SELECT DATE_FORMAT(br.create_time, '%Y-%m') AS month, " +
            "COUNT(br.id) AS borrowCount, " +
            "SUM(br.borrow_quantity) AS totalQuantity " +
            "FROM borrow_record br " +
            "WHERE br.create_time >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH) " +
            "GROUP BY DATE_FORMAT(br.create_time, '%Y-%m') " +
            "ORDER BY month ASC")
    List<MonthlyTrend> getMonthlyTrend();

    /**
     * 首页统计：总设备数、总借用数、待审批数、逾期数
     */
    @Select("SELECT " +
            "(SELECT COUNT(*) FROM device_info WHERE deleted = 0) AS totalDevices, " +
            "(SELECT COUNT(*) FROM borrow_record WHERE status IN (1, 3)) AS activeBorrows, " +
            "(SELECT COUNT(*) FROM borrow_record WHERE status = 0) AS pendingApprovals, " +
            "(SELECT COUNT(*) FROM borrow_record WHERE status = 3) AS overdueCount, " +
            "(SELECT COUNT(*) FROM sys_user WHERE deleted = 0) AS totalUsers")
    java.util.Map<String, Object> getDashboardStats();
}
