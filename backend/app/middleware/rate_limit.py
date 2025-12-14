"""
API限流中间件
用于防止DDoS攻击和API滥用
"""

import time
import asyncio
from typing import Dict, Optional, Tuple
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.logging import setup_logging, INFO


logger = setup_logging(logger_name=__name__, level=INFO, backup_count=1)


class RateLimiter:
    """基于内存的限流器"""

    def __init__(self):
        # 存储每个IP的请求记录 {ip: [(timestamp, count), ...]}
        self.requests: Dict[str, deque] = defaultdict(deque)
        # 清理任务
        self.cleanup_task = None

    async def is_allowed(
        self,
        key: str,
        limit: int,
        window: int
    ) -> Tuple[bool, Optional[int]]:
        """
        检查是否允许请求

        Args:
            key: 限流键值（通常是IP地址）
            limit: 限制的请求数量
            window: 时间窗口（秒）

        Returns:
            (是否允许, 剩余重试时间)
        """
        current_time = time.time()
        cutoff_time = current_time - window

        # 获取该IP的请求记录
        request_times = self.requests[key]

        # 清理过期的请求记录
        while request_times and request_times[0] < cutoff_time:
            request_times.popleft()

        # 检查是否超过限制
        if len(request_times) >= limit:
            # 计算剩余重试时间
            oldest_request = request_times[0]
            retry_after = int(oldest_request + window - current_time) + 1
            return False, retry_after

        # 记录当前请求
        request_times.append(current_time)
        return True, None

    async def cleanup(self):
        """定期清理过期的记录"""
        while True:
            try:
                current_time = time.time()
                cutoff_time = current_time - 3600  # 清理1小时前的记录

                for key in list(self.requests.keys()):
                    request_times = self.requests[key]
                    while request_times and request_times[0] < cutoff_time:
                        request_times.popleft()

                    # 如果队列为空，删除该键
                    if not request_times:
                        del self.requests[key]

                await asyncio.sleep(300)  # 每5分钟清理一次

            except Exception as e:
                logger.error("Rate limiter cleanup error: %s", e)
                await asyncio.sleep(60)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """API限流中间件"""

    def __init__(
        self,
        app,
        # 默认配置：每分钟60次请求
        default_limit: int = 60,
        default_window: int = 60,
        # 特殊路径配置
        login_limit: int = 5,      # 登录接口：每分钟5次
        login_window: int = 60,    # 登录接口：1分钟窗口
        upload_limit: int = 10,    # 上传接口：每分钟10次
        upload_window: int = 60,   # 上传接口：1分钟窗口
        # 白名单IP（不限流）
        whitelist_ips: Optional[list] = None,
        # 启用清理任务
        enable_cleanup: bool = True
    ):
        super().__init__(app)
        self.rate_limiter = RateLimiter()
        self.default_limit = default_limit
        self.default_window = default_window
        self.login_limit = login_limit
        self.login_window = login_window
        self.upload_limit = upload_limit
        self.upload_window = upload_window
        self.whitelist_ips = set(whitelist_ips or [])

        # 启动清理任务
        if enable_cleanup:
            self.cleanup_task = asyncio.create_task(
                self.rate_limiter.cleanup())

        logger.info("Rate limit middleware initialized")

    async def dispatch(self, request: Request, call_next) -> Response:
        """处理请求"""
        # 获取客户端IP
        client_ip = self._get_client_ip(request)

        # 检查白名单
        if client_ip in self.whitelist_ips:
            return await call_next(request)

        # 获取路径
        path = request.url.path

        # 确定限流策略
        if self._is_login_path(path):
            limit, window = self.login_limit, self.login_window
            rate_limit_type = "login"
        else:
            limit, window = self.default_limit, self.default_window
            rate_limit_type = "default"

        # 检查限流
        allowed, retry_after = await self.rate_limiter.is_allowed(
            key=f"{client_ip}:{rate_limit_type}",
            limit=limit,
            window=window
        )

        if not allowed:
            logger.warning(
                "Rate limit exceeded for IP: %s, Path: %s, Type: %s, Retry after: %ds",
                client_ip, path, rate_limit_type, retry_after
            )

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "请求过于频繁，请稍后再试",
                    "retry_after": retry_after,
                    "limit": limit,
                    "window": window
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Window": str(window),
                    "X-RateLimit-Type": rate_limit_type
                }
            )

        # 添加响应头
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Window"] = str(window)
        response.headers["X-RateLimit-Type"] = rate_limit_type

        return response

    def _get_client_ip(self, request: Request) -> str:
        """获取客户端真实IP"""
        # 检查代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For: client, proxy1, proxy2
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()

        # 回退到客户端IP
        if hasattr(request, 'client') and request.client:
            return request.client.host

        return "unknown"

    def _is_login_path(self, path: str) -> bool:
        """判断是否为登录相关路径"""
        login_paths = [
            "/auth/login",
        ]
        return any(path.startswith(p) for p in login_paths)


class AdvancedRateLimiter:
    """高级限流器，支持多种限流策略"""

    def __init__(self):
        # 滑动窗口限流器
        self.sliding_windows: Dict[str, deque] = defaultdict(deque)
        # 令牌桶限流器
        self.token_buckets: Dict[str, dict] = {}
        # 固定窗口计数器
        self.fixed_counters: Dict[str, Tuple[int, float]] = {}

    async def sliding_window_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> Tuple[bool, Optional[int]]:
        """滑动窗口限流"""
        current_time = time.time()
        cutoff_time = current_time - window

        window_requests = self.sliding_windows[key]

        # 清理过期请求
        while window_requests and window_requests[0] < cutoff_time:
            window_requests.popleft()

        if len(window_requests) >= limit:
            oldest_request = window_requests[0]
            retry_after = int(oldest_request + window - current_time) + 1
            return False, retry_after

        window_requests.append(current_time)
        return True, None

    async def token_bucket_limit(
        self,
        key: str,
        capacity: int,
        refill_rate: float
    ) -> Tuple[bool, Optional[int]]:
        """令牌桶限流"""
        current_time = time.time()

        if key not in self.token_buckets:
            self.token_buckets[key] = {
                'tokens': capacity,
                'last_refill': current_time
            }

        bucket = self.token_buckets[key]

        # 补充令牌
        time_passed = current_time - bucket['last_refill']
        tokens_to_add = time_passed * refill_rate
        bucket['tokens'] = min(capacity, bucket['tokens'] + tokens_to_add)
        bucket['last_refill'] = current_time

        # 检查是否有足够令牌
        if bucket['tokens'] < 1:
            # 计算需要等待的时间
            wait_time = (1 - bucket['tokens']) / refill_rate
            return False, int(wait_time) + 1

        # 消费令牌
        bucket['tokens'] -= 1
        return True, None


# 全局限流器实例
global_rate_limiter = RateLimiter()
advanced_rate_limiter = AdvancedRateLimiter()
