"""
# @ Author: Alucard
# @ Create Time: 2025-11-16 10:00:54
# @ Modified by: Alucard
# @ Modified time: 2025-11-16 10:00:54
# @ Description: 日志记录器
"""

__all__ = [
    "setup_logging",
    "logger",
    "LOG_DIR",
]

from pathlib import Path
from logging import getLogger, Formatter, Logger
from logging.handlers import RotatingFileHandler
from typing import Optional

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 配置日志logger_level
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def setup_logging(
    logger_name: Optional[str] = None,
    backup_count: int = 10,    # 保留 10 个备份文件
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB 备份大小
    level: int = DEBUG,
) -> Logger:
    """设置日志记录器

    Args:
        logger_name: 日志记录器名称
        backup_count: 备份文件数量
        max_bytes: 备份文件大小
        level: 日志级别

    Returns:
        logger: 日志记录器
    """
    log_file = LOG_DIR / f"{logger_name if logger_name else __name__}.log"
    tmp_logger = getLogger(logger_name)
    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    formatter = Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    tmp_logger.addHandler(handler)
    tmp_logger.setLevel(level)
    return tmp_logger


# 创建全局日志记录器实例
logger = setup_logging()
