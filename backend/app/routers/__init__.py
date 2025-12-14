# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2025/10/09 17:34:34
@Author  :   Alucard Zheng
@Version :   1.0
@Contact :   zheng.hanbin@sihanfu.cn
@Desc    :   None
"""

from pathlib import Path
import importlib


current_dir = Path(__file__).parent
# 初始化 __all__ 列表
__all__ = []

# 遍历文件夹中的所有 .py 文件
for file in current_dir.glob("*.py"):
    if file.name != "__init__.py":  # 跳过 __init__.py 文件
        module_name = file.stem  # 获取模块名（文件名去掉 .py）
        module = importlib.import_module(
            f".{module_name}", package=__name__
        )  # 动态导入模块

        # 假设每个模块都有一个名为 `router` 的对象
        if hasattr(module, "router"):
            router_name = f"{module_name}_router"
            globals()[router_name] = module.router  # 将 router 添加到全局变量
            __all__.append(router_name)  # 将 router 名称添加到 __all__
