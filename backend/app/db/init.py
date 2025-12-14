'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 14:49:55
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 15:36:03
 # @ Description:
 '''

__all__ = ['init_db', 'close_db']

from typing import Dict
from tortoise import Tortoise
from tortoise.transactions import in_transaction
from tortoise.exceptions import IntegrityError
from app.config import admin_config as admin
from app.security import get_password_hash
from .models import User


async def init_db(config: Dict) -> None:
    """初始化数据库"""
    await Tortoise.init(config=config)
    # 不生成模式，避免约束冲突
    try:
        await Tortoise.generate_schemas(safe=True)
        superadmin = await User.get_or_none(
            username=admin.name)
        if not superadmin:
            try:
                async with in_transaction():
                    hashed_password = get_password_hash(
                        f"{admin.password_value}")
                    await User.create(
                        username=admin.name,
                        password_hash=hashed_password
                    )
                    print("Superadmin account created.")
                    print(f'Superadmin: {admin.name}')
                    print("Superadmin Password: ", admin.password_value)
            except IntegrityError:
                pass
    except IntegrityError:
        pass


async def close_db() -> None:
    """关闭数据库连接"""
    await Tortoise.close_connections()
