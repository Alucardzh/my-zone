'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 15:08:38
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 16:21:36
 # @ Description:
 '''

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from app.db.models import Website, Category, User
from app.schemas import WebsiteCreate, WebsiteUpdate, WebsiteOut
from app.security import get_current_user
from app.tasks.websites import download_favicon


router = APIRouter(prefix="/websites", tags=["websites"])


@router.get("/", response_model=List[WebsiteOut])
async def list_websites(
    q: Optional[str] = Query(default=None, description="按名称搜索"),
    category_id: Optional[int] = Query(default=None, description="按分类筛选"),
):
    """查询webiste列表"""
    records = await Website.list_websites(q=q, cid=category_id)
    return [WebsiteOut.model_validate(r) for r in records]


@router.post("/", response_model=WebsiteOut)
async def create_website(
    payload: WebsiteCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
) -> WebsiteOut:
    """新建website"""
    record = await Website.new_data(payload=payload, user=user)
    if record is False:
        raise HTTPException(status_code=404, detail="未发现分类")
    # 添加后台任务下载favicon
    background_tasks.add_task(download_favicon, record.id)

    return WebsiteOut.model_validate(record)


@router.get("/{website_id}", response_model=WebsiteOut)
async def get_website(website_id: int) -> WebsiteOut:
    """查询website"""
    record = await Website.get_or_none(id=website_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return WebsiteOut.model_validate(record)


@router.put("/{website_id}", response_model=WebsiteOut)
async def update_website(
    website_id: int, payload: WebsiteUpdate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
) -> WebsiteOut:
    """更新网址"""
    record = await Website.get_or_none(id=website_id, owner_id=user.id)
    if record is None:
        raise HTTPException(status_code=404, detail="Website not found")

    new_data = payload.model_dump(exclude_unset=True)
    if "url" in new_data and new_data["url"] is not None:
        new_data["url"] = str(new_data["url"])  # AnyUrl -> str
    if "back_url" in new_data and new_data["back_url"] is not None:
        new_data["back_url"] = str(new_data["back_url"])  # AnyUrl -> str

    if "category_id" in new_data:
        category = None
        if new_data["category_id"] is not None:
            category = await Category.get_or_none(id=new_data["category_id"])
            if category is None:
                raise HTTPException(status_code=404, detail="未发现分类")
        new_data.pop("category_id")
        record.category = category

    for k, v in new_data.items():
        setattr(record, k, v)
    await record.save()
    # 添加后台任务下载favicon
    background_tasks.add_task(download_favicon, record.id)
    return WebsiteOut.model_validate(record)


@router.delete("/{website_id}")
async def delete_website(
    website_id: int,
    user: User = Depends(get_current_user)
) -> JSONResponse:
    """删除website"""
    record = await Website.get_or_none(id=website_id, owner_id=user.id)
    if record is None:
        raise HTTPException(status_code=404, detail="Website not found")
    await record.delete()
    return JSONResponse(content={"status": "deleted"}, status_code=200)
