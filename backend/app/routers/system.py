'''
 # @ Author: Alucard
 # @ Create Time: 2025-10-10 14:34:04
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 16:20:10
 # @ Description:系统相关的 API 路由
 '''
from os import getenv
import httpx
from fastapi import APIRouter


router = APIRouter(prefix="/system", tags=["system"])


@router.get("/searxng/health")
async def check_searxng_health():
    """检查 SearXNG 服务健康状态"""
    try:
        # 从环境变量获取 SearXNG 地址
        searxng_host = getenv("SEARXNG_HOST", "searxng")
        searxng_port = getenv("SEARXNG_PORT", "8080")
        searxng_url = f"http://{searxng_host}:{searxng_port}"

        # 尝试访问 SearXNG 健康检查端点
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{searxng_url}/healthz")

            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "available": True,
                    "url": searxng_url
                }
            else:
                return {
                    "status": "unhealthy",
                    "available": False,
                    "error": f"Status code: {response.status_code}"
                }
    except httpx.ConnectTimeout:
        return {
            "status": "timeout",
            "available": False,
            "error": "Connection timeout"
        }
    except httpx.ConnectError:
        return {
            "status": "unavailable",
            "available": False,
            "error": "Connection refused - service may not be running"
        }
    except Exception as e:
        return {
            "status": "error",
            "available": False,
            "error": str(e)
        }


@router.get("/searxng/config")
async def get_searxng_config():
    """获取 SearXNG 配置信息"""
    searxng_host = getenv("SEARXNG_HOST", "searxng")
    searxng_port = getenv("SEARXNG_PORT", "8080")
    searxng_bind_host = getenv("SEARXNG_BIND_HOST", "localhost")
    searxng_bind_port = getenv("SEARXNG_BIND_PORT", "8080")

    return {
        "internal_url": f"http://{searxng_host}:{searxng_port}",
        "external_url": f"http://{searxng_bind_host}:{searxng_bind_port}",
        "search_path": "/search"
    }
