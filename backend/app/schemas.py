'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 15:08:22
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 17:06:46
 # @ Description:
 '''
__all__ = [
    "Token",
    "UserLogin",
    "UserCreate",
    "CategoryOut",
    "CategoryCreate",
    "CategoryUpdate",
    "WebsiteCreate",
    "WebsiteUpdate",
    "WebsiteOut"
]

from typing import Optional
from pydantic import BaseModel, AnyUrl, Field, field_validator


class Token(BaseModel):
    """Token 模型"""
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class UserCreate(BaseModel):
    """用户创建模型"""
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class CategoryOut(BaseModel):
    """分类输出模型"""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = "bookmark"
    sort_order: int

    class Config:
        """CategoryOut 配置"""
        from_attributes = True


class CategoryCreate(BaseModel):
    """分类创建模型"""
    name: str = Field(min_length=1, max_length=64)
    description: Optional[str] = None
    icon: Optional[str] = Field("bookmark", max_length=128)
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    """分类更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    description: Optional[str] = None
    icon: Optional[str] = Field("bookmark", max_length=128)
    sort_order: Optional[int] = None


class WebsiteCreate(BaseModel):
    """网站创建模型"""
    name: str
    url: AnyUrl
    back_url: Optional[AnyUrl] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: int = 0
    icon: Optional[str] = Field(None, max_length=255)

    @field_validator('back_url', mode='before')
    @classmethod
    def validate_back_url(cls, v):
        """将空字符串转换为 None"""
        if v == '' or v is None:
            return None
        return v


class WebsiteUpdate(BaseModel):
    """网站更新模型"""
    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    back_url: Optional[AnyUrl] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: Optional[int] = None
    icon: Optional[str] = Field(None, max_length=255)

    @field_validator('back_url', mode='before')
    @classmethod
    def validate_back_url(cls, v):
        """将空字符串转换为 None"""
        if v == '' or v is None:
            return None
        return v


class WebsiteOut(BaseModel):
    """网站输出模型"""
    id: int
    name: str
    url: AnyUrl
    back_url: Optional[AnyUrl] = None
    description: Optional[str] = None
    sort_order: int
    category_id: Optional[int] = None
    icon: Optional[str] = None

    @field_validator('back_url', mode='before')
    @classmethod
    def validate_back_url(cls, v):
        """将空字符串转换为 None"""
        if v == '' or v is None:
            return None
        return v

    class Config:
        """WebsiteOut 配置"""
        from_attributes = True
