'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 14:49:53
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 15:35:27
 # @ Description:
 '''


__all__ = [
    "User",
    "Category",
    "Website",
]
from typing import List, Dict, Union
from tortoise import fields
from tortoise.models import Model
from tortoise.expressions import Q
from app.schemas import CategoryCreate, WebsiteCreate


SORT_RULE = ["-sort_order", "created_at"]


class User(Model):
    """用户模型"""
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True, index=True)
    password_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        """用户模型元数据"""
        table = "users"


class Category(Model):
    """分类模型"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64, unique=True, index=True)
    description = fields.TextField(null=True)
    icon = fields.CharField(max_length=128, default="bookmark")
    sort_order = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_user = fields.ForeignKeyRelation(
        "models.User", related_name="categories", on_delete=fields.CASCADE
    )

    class Meta:
        """分类模型元数据"""
        table = "categories"

    @classmethod
    async def get_list_categories(cls, q: str) -> List["Category"]:
        """通过 name 过滤类别"""
        f = Q(name__icontains=q) if q else Q()
        return await cls.filter(f).order_by(*SORT_RULE)

    @classmethod
    async def clean(cls, category_id: int):
        """清理当前分类内容"""
        record = await cls.get_or_none(id=category_id)
        if record is None:
            return False
        websites = await Website.filter(category_id=category_id)
        if websites:
            for website in websites:
                await website.delete()
        await record.delete()
        return True

    @classmethod
    async def dumpdata(cls, user: User) -> List[Dict]:
        """导出分类数据"""
        data = await cls.filter(created_user=user).distinct().all()
        return [{
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "icon": c.icon,
            "sort_order": c.sort_order,
            "created_at": c.created_at.isoformat() if c.created_at else None
        } for c in data]

    @classmethod
    async def new_data(
        cls, payload: CategoryCreate, user: User
    ) -> Union[bool, "Category"]:
        """创建新的分类"""
        if await cls.get_or_none(name=payload.name):
            return False
        return await cls.create(
            name=payload.name,
            description=payload.description,
            icon=payload.icon,
            sort_order=payload.sort_order,
            created_user=user
        )


class Website(Model):
    """网站模型"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, index=True)
    url = fields.CharField(max_length=255)
    back_url = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    sort_order = fields.IntField(default=0)
    icon = fields.CharField(max_length=255, default="default.webp")
    category = fields.ForeignKeyField(
        "models.Category", related_name="websites",
        on_delete=fields.RESTRICT, null=True
    )
    owner: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="websites", on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        """网站模型元数据"""
        table = "websites"

    @classmethod
    async def dumpdata(cls, user: User) -> List[Dict]:
        """导出网址数据"""
        data = await cls.filter(owner_id=user.id).all()
        return [{
            "id": w.id,
            "name": w.name,
            "url": str(w.url),
            "back_url": str(w.back_url) if w.back_url else None,
            "description": w.description,
            "sort_order": w.sort_order,
            "icon": w.icon,
            "category_id": w.category_id,
            "created_at": w.created_at.isoformat() if w.created_at else None
        } for w in data]

    @classmethod
    async def new_data(
        cls, payload: WebsiteCreate, user: User
    ) -> Union[bool, "Website"]:
        """创建website"""
        category = None
        if payload.category_id:
            category = await Category.get_or_none(id=payload.category_id)
            if category is None:
                return False
        return await Website.create(
            name=payload.name,
            url=str(payload.url),
            back_url=str(payload.back_url) if payload.back_url else None,
            description=payload.description,
            sort_order=payload.sort_order,
            icon=payload.icon if payload.icon else "default.webp",
            category=category,
            owner=user,
        )

    @classmethod
    async def list_websites(cls, q: str = "", cid: int = 0) -> List['Website']:
        """查询网址列表"""
        f = Q()
        if q:
            f &= Q(name__icontains=q)
        if cid:
            f &= Q(category_id=cid)
        return await cls.filter(f).order_by(*SORT_RULE)
