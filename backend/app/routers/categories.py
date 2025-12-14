'''
 # @ Author: Alucard
 # @ Create Time: 2025-10-09 12:17:07
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 15:42:42
 # @ Description:
 '''

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.models import Category, User
from app.schemas import CategoryCreate, CategoryUpdate, CategoryOut
from app.security import get_current_user


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryOut])
async def list_categories(
    q: Optional[str] = Query(default=None, description="按名称搜索"),
) -> List[CategoryOut]:
    """按名称搜索分类"""
    records = await Category.get_list_categories(q=q)
    return [CategoryOut.model_validate(r) for r in records]


@router.post("/", response_model=CategoryOut)
async def create_category(
    payload: CategoryCreate,
    user: User = Depends(get_current_user)
) -> CategoryOut:
    """创建分类"""
    record = await Category.new_data(payload=payload, user=user)
    if record is False:
        raise HTTPException(
            status_code=400, detail="Category name already exists")
    return CategoryOut.model_validate(record)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int) -> CategoryOut:
    """检查分类名称是否已存在"""
    record = await Category.get_or_none(id=category_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryOut.model_validate(record)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    user: User = Depends(get_current_user)
) -> CategoryOut:
    """更新分类接口

    Args:
        category_id (int): _description_
        payload (CategoryUpdate): _description_
        user (User, optional): Defaults to Depends(get_current_user).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        CategoryOut: _description_
    """
    record = await Category.get_or_none(id=category_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # 如果更新名称，检查新名称是否已存在
    if payload.name and payload.name != record.name:
        existing_category = await Category.get_or_none(name=payload.name)
        if existing_category:
            raise HTTPException(
                status_code=400, detail="Category name already exists")

    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(record, k, v)
    await record.save()

    return CategoryOut.model_validate(record)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    user: User = Depends(get_current_user)
) -> dict:
    """删除分类"""
    res = await Category.clean(category_id=category_id)
    if res is False:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"status": "deleted"}
