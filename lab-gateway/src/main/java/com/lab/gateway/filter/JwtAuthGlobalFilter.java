package com.lab.gateway.filter;

import com.alibaba.fastjson2.JSON;
import com.lab.common.constant.CommonConstant;
import com.lab.common.result.R;
import com.lab.common.util.JwtUtil;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.data.redis.core.ReactiveStringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.util.AntPathMatcher;
import org.springframework.util.StringUtils;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import javax.annotation.Resource;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;

/**
 * JWT鉴权全局过滤器
 * 解析JWT并将userId/role放入Header传递给下游微服务
 * 使用 ReactiveStringRedisTemplate 避免阻塞 Netty 事件循环
 */
@Component
public class JwtAuthGlobalFilter implements GlobalFilter, Ordered {

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Resource
    private ReactiveStringRedisTemplate reactiveStringRedisTemplate;

    private static final AntPathMatcher PATH_MATCHER = new AntPathMatcher();

    /** 白名单路径（不需要鉴权） */
    private static final List<String> WHITE_LIST = Arrays.asList(
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/swagger-ui.html",
            "/swagger-ui/**",
            "/v3/api-docs/**",
            "/webjars/**",
            "/favicon.ico",
            "/actuator/**"
    );

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getURI().getPath();

        // 白名单路径放行
        for (String pattern : WHITE_LIST) {
            if (PATH_MATCHER.match(pattern, path)) {
                return chain.filter(exchange);
            }
        }

        // 获取Authorization头
        String authHeader = request.getHeaders().getFirst(CommonConstant.JWT_HEADER);

        if (!StringUtils.hasText(authHeader) || !authHeader.startsWith(CommonConstant.JWT_PREFIX)) {
            return unauthorizedResponse(exchange, "未登录或token已过期");
        }

        // 去掉Bearer前缀
        String token = authHeader.substring(CommonConstant.JWT_PREFIX.length());

        // 使用响应式Redis检查黑名单
        String blacklistKey = CommonConstant.JWT_BLACKLIST_PREFIX + token;

        return reactiveStringRedisTemplate.hasKey(blacklistKey)
                .flatMap(isBlacklisted -> {
                    if (Boolean.TRUE.equals(isBlacklisted)) {
                        return unauthorizedResponse(exchange, "token已失效，请重新登录");
                    }

                    try {
                        // 解析Token
                        Long userId = JwtUtil.getUserIdFromToken(token, jwtSecret);
                        String username = JwtUtil.getUsernameFromToken(token, jwtSecret);
                        String role = JwtUtil.getRoleFromToken(token, jwtSecret);

                        // 检查Token是否过期
                        if (JwtUtil.isTokenExpired(token, jwtSecret)) {
                            return unauthorizedResponse(exchange, "token已过期，请重新登录");
                        }

                        // 将用户信息放入请求头传递给下游微服务
                        ServerHttpRequest.Builder requestBuilder = request.mutate();
                        requestBuilder.header(CommonConstant.USER_ID_HEADER, String.valueOf(userId));
                        requestBuilder.header(CommonConstant.USERNAME_HEADER, username);
                        requestBuilder.header(CommonConstant.USER_ROLE_HEADER, role);

                        return chain.filter(exchange.mutate().request(requestBuilder.build()).build());

                    } catch (Exception e) {
                        return unauthorizedResponse(exchange, "token解析失败: " + e.getMessage());
                    }
                })
                .onErrorResume(e -> unauthorizedResponse(exchange, "认证服务异常，请稍后重试"));
    }

    private Mono<Void> unauthorizedResponse(ServerWebExchange exchange, String message) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.UNAUTHORIZED);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        R<?> result = R.unauthorized(message);
        String body = JSON.toJSONString(result);
        DataBuffer buffer = response.bufferFactory().wrap(body.getBytes(StandardCharsets.UTF_8));
        return response.writeWith(Mono.just(buffer));
    }

    @Override
    public int getOrder() {
        return -100;
    }
}
