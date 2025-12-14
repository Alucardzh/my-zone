'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 14:43:45
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 17:05:32
 # @ Description:
 '''

from typing import AsyncGenerator, Dict
from contextlib import asynccontextmanager
import importlib
from concurrent.futures import ThreadPoolExecutor
import asyncio
from fastapi import FastAPI, APIRouter
from app.middleware import AuthMiddleware, RateLimitMiddleware
from app.config import db_settings, rate_limit_config
from app.db.init import close_db, init_db
from app.tasks.db_backup import safe_backup

endpoints_module = importlib.import_module("app.routers")
executor = ThreadPoolExecutor(max_workers=2)


# 定义 lifespan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """生命周期"""
    # 初始化数据库连接（根据配置自动选择 PostgreSQL 或 SQLite）
    if db_settings.db_type == "sqlite":
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, safe_backup)
    await init_db(config=db_settings.db_config)
    yield
    # 关闭数据库连接
    await close_db()
    # 清理资源

app = FastAPI(lifespan=lifespan, title="MyNavi API", version="0.1.0")

# 添加限流中间件（如果启用）
if rate_limit_config.enabled:
    app.add_middleware(
        RateLimitMiddleware,
        default_limit=rate_limit_config.default_limit,
        default_window=rate_limit_config.default_window,
        login_limit=rate_limit_config.login_limit,
        login_window=rate_limit_config.login_window,
        upload_limit=rate_limit_config.upload_limit,
        upload_window=rate_limit_config.upload_window,
        whitelist_ips=rate_limit_config.get_whitelist_ips(),
        enable_cleanup=rate_limit_config.enable_cleanup
    )

app.add_middleware(AuthMiddleware)
# 获取 __all__ 列表中的所有路由实例
for router_name in endpoints_module.__all__:
    try:
        # 从 endpoints 模块中获取路由实例
        router = getattr(endpoints_module, router_name)
        # 检查是否是 APIRouter 实例
        if isinstance(router, APIRouter):
            # 注册路由
            app.include_router(router, prefix="/api")
        else:
            print(f"Skipped non-router object: {router_name}")
    except AttributeError as e:
        print(f"Error loading router {router_name}: {e}")


@app.get("/health")
async def health_check() -> Dict:
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
