'''
 # @ Author: Alucard
 # @ Create Time: 2025-10-10 11:41:24
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 16:10:08
 # @ Description:
 '''

import json
from datetime import datetime
from fastapi import (APIRouter, Depends, HTTPException,
                     BackgroundTasks, UploadFile, File)
from fastapi.responses import JSONResponse
from app.db.models import Website, Category, User
from app.security import get_current_user
from app.tasks.websites import restore_data


router = APIRouter(prefix="/data", tags=["data"])


@router.post("/dump")
async def dump_user_data(
    user: User = Depends(get_current_user)
) -> JSONResponse:
    """导出当前用户的所有网站和分类数据"""
    # 获取用户的所有分类
    categories_data = await Category.dumpdata(user=user)
    # 获取用户的所有网站
    websites_data = await Website.dumpdata(user=user)

    # 构建导出数据
    export_info = {
        "user_id": user.id,
        "username": user.username,
        "export_time": datetime.now().isoformat(),
        "version": "1.0"
    }
    export_data = {
        "export_info": export_info,
        "categories": categories_data,
        "websites": websites_data
    }
    filename = "mynavi_backup_{user.username}_{export_info.export_time}.json"
    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/load")
async def load_user_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user)
) -> dict:
    """导入用户数据"""
    try:
        # 读取上传的JSON文件
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        # 验证数据格式
        if "categories" not in data and "websites" not in data:
            raise HTTPException(
                status_code=400, detail="Invalid backup file format")
        background_tasks.add_task(restore_data, data, user)
        return {
            "status": "success",
            "message": "请稍后刷新页面查看"
        }

    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid JSON file") from exc
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Import failed: {str(e)}") from e
