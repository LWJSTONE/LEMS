package com.lab.common.feign;

import com.lab.common.result.R;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/**
 * 用户服务Feign客户端
 */
@FeignClient(name = "lab-user", path = "/api/v1/user", fallbackFactory = UserFeignClientFallbackFactory.class)
public interface UserFeignClient {

    @GetMapping("/inner/{id}")
    R<?> getUserById(@PathVariable("id") Long id);

    @GetMapping("/inner/{id}/phone")
    R<String> getUserPhone(@PathVariable("id") Long id);
}
