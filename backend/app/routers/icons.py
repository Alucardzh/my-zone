'''
 # @ Author: Alucard
 # @ Create Time: 2025-10-09 15:22:40
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 16:19:23
 # @ Description:
 '''

from pathlib import Path
from email.utils import formatdate, parsedate_to_datetime
from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse
from app.config import system_settings


router = APIRouter(prefix="/icons", tags=["icons"])


@router.get("/{icons}")
async def show_icons(icons: str, request: Request) -> Response:
    """后台展示icon(开发用)"""
    icon_file = Path('icons') / icons
    stat = icon_file.stat()
    # 使用弱 ETag，避免跨平台精度问题
    etag = f'W/"{stat.st_mtime_ns}-{stat.st_size}"'
    last_modified = formatdate(stat.st_mtime, usegmt=True)

    # 条件请求 - If-None-Match 优先
    inm = request.headers.get("If-None-Match")
    if inm and inm == etag:
        return Response(status_code=304)

    # 条件请求 - If-Modified-Since 其次
    ims = request.headers.get("If-Modified-Since")
    if ims:
        try:
            ims_dt = parsedate_to_datetime(ims)
            # 文件未更新，返回 304
            if ims_dt.timestamp() >= stat.st_mtime:
                return Response(status_code=304)
        except Exception:
            pass

    headers = {
        "Cache-Control": system_settings.cache_header,
        "ETag": etag,
        "Last-Modified": last_modified,
    }
    return FileResponse(icon_file, headers=headers)
