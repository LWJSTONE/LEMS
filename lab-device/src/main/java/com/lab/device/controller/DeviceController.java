package com.lab.device.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.common.result.R;
import com.lab.device.entity.DeviceCategory;
import com.lab.device.entity.DeviceInfo;
import com.lab.device.entity.DeviceMaintenance;
import com.lab.device.service.DeviceService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

/**
 * 设备管理控制器
 */
@RestController
@RequestMapping("/api/v1/device")
public class DeviceController {

    @Resource
    private DeviceService deviceService;

    // ==================== 设备分类 ====================

    @GetMapping("/categories/tree")
    public R<List<DeviceCategory>> getCategoryTree() {
        return R.ok(deviceService.getCategoryTree());
    }

    @PostMapping("/categories")
    public R<Void> addCategory(@RequestBody DeviceCategory category) {
        deviceService.addCategory(category);
        return R.ok();
    }

    @PutMapping("/categories")
    public R<Void> updateCategory(@RequestBody DeviceCategory category) {
        deviceService.updateCategory(category);
        return R.ok();
    }

    @DeleteMapping("/categories/{id}")
    public R<Void> deleteCategory(@PathVariable Long id) {
        deviceService.deleteCategory(id);
        return R.ok();
    }

    // ==================== 设备台账 ====================

    @PostMapping("/info")
    public R<Void> addDevice(@RequestBody DeviceInfo deviceInfo) {
        deviceService.addDevice(deviceInfo);
        return R.ok();
    }

    @PutMapping("/info")
    public R<Void> updateDevice(@RequestBody DeviceInfo deviceInfo) {
        deviceService.updateDevice(deviceInfo);
        return R.ok();
    }

    @DeleteMapping("/info/{id}")
    public R<Void> deleteDevice(@PathVariable Long id) {
        deviceService.deleteDevice(id);
        return R.ok();
    }

    @GetMapping("/info/{id}")
    public R<DeviceInfo> getDeviceById(@PathVariable Long id) {
        return R.ok(deviceService.getDeviceById(id));
    }

    @GetMapping("/info/page")
    public R<Page<DeviceInfo>> getDevicePage(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) Long labId,
            @RequestParam(required = false) Integer status) {
        return R.ok(deviceService.getDevicePage(current, size, name, categoryId, labId, status));
    }

    @PutMapping("/info/{id}/status")
    public R<Void> updateDeviceStatus(@PathVariable Long id, @RequestParam Integer status) {
        deviceService.updateDeviceStatus(id, status);
        return R.ok();
    }

    // ==================== 维修记录 ====================

    @PostMapping("/maintenance")
    public R<Void> addMaintenance(@RequestBody DeviceMaintenance maintenance) {
        deviceService.addMaintenance(maintenance);
        return R.ok();
    }

    @PutMapping("/maintenance/{id}/status")
    public R<Void> updateMaintenanceStatus(@PathVariable Long id, @RequestParam Integer status) {
        deviceService.updateMaintenanceStatus(id, status);
        return R.ok();
    }

    @GetMapping("/maintenance/page")
    public R<Page<DeviceMaintenance>> getMaintenancePage(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Long deviceId,
            @RequestParam(required = false) Integer status) {
        return R.ok(deviceService.getMaintenancePage(current, size, deviceId, status));
    }

    // ==================== 内部Feign调用接口 ====================

    /**
     * 内部接口：根据ID获取设备信息（含版本号）
     */
    @GetMapping("/inner/{id}")
    public R<DeviceInfo> getDeviceInfoInner(@PathVariable Long id) {
        return R.ok(deviceService.getDeviceInfoWithVersion(id));
    }

    /**
     * 内部接口：更新可用库存（乐观锁）
     * params: deviceId, quantity, operation(DECREASE/INCREASE), version
     */
    @PutMapping("/inner/quantity")
    public R<Void> updateAvailableQuantity(@RequestBody Map<String, Object> params) {
        Long deviceId = Long.valueOf(params.get("deviceId").toString());
        Integer quantity = Integer.valueOf(params.get("quantity").toString());
        String operation = params.get("operation").toString();
        Integer version = Integer.valueOf(params.get("version").toString());

        boolean success;
        if ("DECREASE".equals(operation)) {
            success = deviceService.decreaseStock(deviceId, quantity, version);
        } else {
            success = deviceService.increaseStock(deviceId, quantity, version);
        }

        if (!success) {
            return R.fail("库存不足或操作频繁，请重试");
        }
        return R.ok();
    }
}
