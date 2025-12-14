'''
 # @ Author: Alucard
 # @ Create Time: 2025-10-13 12:58:56
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-16 13:26:27
 # @ Description: 认证中间件
 '''


from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.security import decode_token


class AuthMiddleware(BaseHTTPMiddleware):
    """认证中间件"""

    # 不需要认证的路径
    WHITELIST_PATHS = [
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/auth",
        "/static",
        "/media",
    ]

    async def dispatch(self, request: Request, call_next):
        # 检查路径是否在白名单中
        if any(request.url.path.startswith(path) for path in self.WHITELIST_PATHS):
            return await call_next(request)

        # 获取 Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)

        # 提取 token
        token = auth_header.split(" ")[1]

        # 验证 token
        payload = decode_token(token)
        if payload:
            # 将用户信息添加到 request state
            request.state.user_id = payload.get("user_id")
            request.state.username = payload.get("username")

        return await call_next(request)
