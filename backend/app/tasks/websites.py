'''
 # @ Author: Alucard
 # @ Create Time: 2025-10-09 12:24:02
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 16:52:59
 # @ Description:
 '''

__all__ = ["download_favicon", "restore_data"]

from os import chmod
from pathlib import Path
from typing import Dict
from uuid import uuid4
from urllib.parse import urljoin
import aiofiles
from fastapi import HTTPException
import httpx
from app.db.models import Website, Category, User
from app.logging import setup_logging, INFO

logger = setup_logging(logger_name=__name__, level=INFO, backup_count=1)


async def get_favicon(
    favicon_url: str,
    filename: str,
    file_path: str,
    website: Website
) -> None:
    """下载图标"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(favicon_url)
            if response.status_code == 200:
                # 保存文件
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(response.content)

                # 设置文件权限为777
                try:
                    chmod(file_path, 0o777)
                except OSError as e:
                    logger.error("设置文件权限失败 %s: %s", file_path, e)

                # 更新数据库中的icon字段
                website.icon = filename
                await website.save()
                logger.info("网站 %s 的图标已保存: %s", website.id, website.icon)
            else:
                raise HTTPException(status_code=response.status_code, detail="下载网站图标失败")
        except HTTPException as e:
            logger.error("下载网站 %s 的图标时出错: %s", website.id, e)


async def download_favicon(website_id: int):
    """
    后台任务：下载网站的favicon并保存到本地
    """
    try:
        # 获取网站信息
        w = await Website.get_or_none(id=website_id)
        if not w:
            logger.error("未找到网站 %s", website_id)
            return

        # 确保icons文件夹存在
        icons_dir = Path("icons")
        icons_dir.mkdir(parents=True, exist_ok=True)

        # 生成唯一的文件名
        filename = f"{uuid4().hex}.ico"
        file_path = icons_dir / filename

        # 尝试获取favicon，先尝试主URL，如果失败则尝试back_url
        favicon_url = await get_favicon_url(str(w.url))

        # 如果主URL获取favicon失败，且存在back_url，则尝试back_url
        if not favicon_url and w.back_url:
            logger.info(
                "尝试使用备用链接获取网站 %s 的图标: %s", website_id, w.back_url)
            favicon_url = await get_favicon_url(str(w.back_url))
        if favicon_url:
            # 下载favicon
            await get_favicon(
                favicon_url=favicon_url, filename=filename,
                file_path=file_path, website=w)
        else:
            w.icon = "default.webp"
            await w.save()
            logger.info("未找到网站 %s 的图标", website_id)

    except HTTPException as e:
        logger.error("下载网站 %s 图标任务出错: %s", website_id, e)


async def get_favicon_url(base_url: str) -> str | None:
    """
    获取网站的favicon URL
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 首先尝试常见的favicon路径
        common_paths = [
            '/favicon.ico',
            '/favicon.png',
            '/apple-touch-icon.png',
            '/apple-touch-icon-precomposed.png'
        ]

        for path in common_paths:
            favicon_url = urljoin(base_url, path)
            try:
                response = await client.head(favicon_url)
                if response.status_code == 200:
                    return favicon_url
            except HTTPException as e:
                logger.error("获取网站 %s 的图标URL时出错: %s", base_url, e)
                continue

    return None


async def restore_data(data: Dict, user: User) -> None:
    """恢复数据的后台任务"""
    imported_categories = 0
    # 导入分类数据
    cid_mapping = {}  # 用于映射旧ID到新ID
    for cat_data in data.get("categories", []):
        # 检查是否已存在同名分类
        existing_category = await Category.filter(
            name=cat_data["name"],
            websites__owner_id=user.id
        ).first()

        if not existing_category:
            new_category = await Category.create(
                name=cat_data["name"],
                description=cat_data.get("description"),
                icon=cat_data.get("icon", "bookmark"),
                sort_order=cat_data.get("sort_order", 0),
                created_user=user
            )
            cid_mapping[cat_data["id"]] = new_category.id
            imported_categories += 1
        else:
            cid_mapping[cat_data["id"]] = existing_category.id

        # 导入网站数据
    imported_website_ids = []  # 记录导入的网站ID，用于后台下载图标
    for w in data.get("websites", []):
        # 检查是否已存在同名网站
        existing_website = await Website.filter(
            name=w["name"],
            owner_id=user.id
        ).first()

        if not existing_website:
            # 映射分类ID
            category_id = None
            if w.get("category_id") and w["category_id"] in cid_mapping:
                category_id = cid_mapping[w["category_id"]]

            new_website = await Website.create(
                name=w["name"],
                url=w["url"],
                back_url=w.get("back_url"),
                description=w.get("description"),
                sort_order=w.get("sort_order", 0),
                is_public=w.get("is_public", True),
                icon=w.get("icon"),
                category_id=category_id,
                owner=user
            )
            imported_website_ids.append(new_website.id)

        # 为导入的网站添加后台任务下载图标
    for website_id in imported_website_ids:
        await download_favicon(website_id=website_id)
