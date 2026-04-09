package com.lab.common.feign;

import com.lab.common.result.R;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cloud.openfeign.FallbackFactory;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * 设备服务Feign降级工厂
 */
@Slf4j
@Component
public class DeviceFeignClientFallbackFactory implements FallbackFactory<DeviceFeignClient> {

    @Override
    public DeviceFeignClient create(Throwable cause) {
        log.error("设备服务Feign调用失败: {}", cause.getMessage());
        return new DeviceFeignClient() {
            @Override
            public R<?> getDeviceInfo(Long id) {
                return R.fail("设备服务不可用");
            }

            @Override
            public R<?> updateAvailableQuantity(Map<String, Object> params) {
                return R.fail("设备服务不可用");
            }
        };
    }
}
