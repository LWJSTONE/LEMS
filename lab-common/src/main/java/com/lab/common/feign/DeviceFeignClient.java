package com.lab.common.feign;

import com.lab.common.result.R;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 设备服务Feign客户端
 */
@FeignClient(name = "lab-device", path = "/api/v1/device", fallbackFactory = DeviceFeignClientFallbackFactory.class)
public interface DeviceFeignClient {

    @GetMapping("/inner/{id}")
    R<?> getDeviceInfo(@PathVariable("id") Long id);

    @PutMapping("/inner/quantity")
    R<?> updateAvailableQuantity(@RequestBody Map<String, Object> params);
}
