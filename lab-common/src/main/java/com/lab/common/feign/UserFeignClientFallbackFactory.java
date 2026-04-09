package com.lab.common.feign;

import com.lab.common.result.R;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cloud.openfeign.FallbackFactory;
import org.springframework.stereotype.Component;

/**
 * 用户服务Feign降级工厂
 */
@Slf4j
@Component
public class UserFeignClientFallbackFactory implements FallbackFactory<UserFeignClient> {

    @Override
    public UserFeignClient create(Throwable cause) {
        log.error("用户服务Feign调用失败: {}", cause.getMessage());
        return new UserFeignClient() {
            @Override
            public R<?> getUserById(Long id) {
                return R.fail("用户服务不可用");
            }

            @Override
            public R<String> getUserPhone(Long id) {
                return R.fail("用户服务不可用");
            }
        };
    }
}
