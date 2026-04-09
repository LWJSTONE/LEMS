package com.lab.device.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lab.device.entity.DeviceCategory;
import com.lab.device.entity.DeviceInfo;
import com.lab.device.entity.DeviceMaintenance;

import java.util.List;
import java.util.Map;

/**
 * 设备管理服务接口
 */
public interface DeviceService {

    // === 设备分类 ===
    List<DeviceCategory> getCategoryTree();
    void addCategory(DeviceCategory category);
    void updateCategory(DeviceCategory category);
    void deleteCategory(Long id);

    // === 设备台账 ===
    void addDevice(DeviceInfo deviceInfo);
    void updateDevice(DeviceInfo deviceInfo);
    void deleteDevice(Long id);
    DeviceInfo getDeviceById(Long id);
    Page<DeviceInfo> getDevicePage(int pageNum, int pageSize, String name, Long categoryId, Long labId, Integer status);
    void updateDeviceStatus(Long id, Integer status);

    // === 库存操作（供Feign内部调用，乐观锁控制）===
    boolean decreaseStock(Long deviceId, Integer quantity, Integer version);
    boolean increaseStock(Long deviceId, Integer quantity, Integer version);
    DeviceInfo getDeviceInfoWithVersion(Long deviceId);

    // === 维修记录 ===
    void addMaintenance(DeviceMaintenance maintenance);
    void updateMaintenanceStatus(Long id, Integer status);
    Page<DeviceMaintenance> getMaintenancePage(int pageNum, int pageSize, Long deviceId, Integer status);
}
