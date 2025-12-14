'''
 # @ Author: Alucard
 # @ Create Time: 2025-09-30 14:49:51
 # @ Modified by: Alucard
 # @ Modified time: 2025-10-10 17:04:50
 # @ Description:
 '''

__all__ = ["system_settings", "db_settings",
           "admin_config", "jwt_config", "rate_limit_config"]

from typing import Optional, List, Dict
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import SecretStr

ENV_FILE = "/root/.env"


class SystemConfig(BaseSettings):
    """应用配置类"""
    # 时区配置
    timezone: str = "Asia/Shanghai"

    # Fastapi基础设置
    refresh_interval: int = 30
    debug: bool = False
    base_url: Optional[str] = None
    allowed_hosts: List[str] = []
    provide: bool = False
    # 设置缓存控制的响应头，这里设置最大缓存时间为1小时（3600秒）
    cache_header: str = "public, max-age=3600"
    js_cache_header: str = "public, max-age=600"
    css_cache_header: str = "public, max-age=86400"

    class Config:
        """系统配置类"""
        env_file = ENV_FILE  # 表示从环境变量中获取
        env_file_encoding = "utf-8"
        case_sensitive = False
        # 环境变量前缀（可选）
        env_prefix = ""
        # 允许额外字段
        extra = "ignore"  # 或者使用 "ignore"


class JwtConfig(BaseSettings):
    """应用配置类"""
    # 应用配置
    algorithm: str = "HS256"
    access_token_expire_seconds: int = 60 * 60 * 24  # 一天的秒数
    secret_key: SecretStr = SecretStr("")

    @property
    def secret_key_value(self) -> str:
        """获取密钥"""
        return self.secret_key.get_secret_value()

    class Config:
        """系统配置类"""
        env_file = ENV_FILE  # 表示从环境变量中获取
        env_file_encoding = "utf-8"
        case_sensitive = False
        # 环境变量前缀（可选）
        env_prefix = "JWT_"
        # 允许额外字段
        extra = "ignore"  # 或者使用 "ignore"


class DatabaseSettings(BaseSettings):
    """应用配置类"""
    # 数据库类型选择: "postgres" 或 "sqlite"
    db_type: str = "postgres"
    external: bool = False
    # PostgreSQL 数据库配置
    host: str = "db"
    port: int = 5432
    user: str = "its_me"
    password: SecretStr = SecretStr("itsmynavidb")
    database: str = "my_navi"

    # SQLite 数据库配置
    sqlite_db_path: str = "./db_data/my_navi.sqlite3"

    @property
    def config(self) -> Dict:
        """获取 PostgreSQL 配置"""
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": self.host,
                        "port": self.port,
                        "user": self.user,
                        "password": str(self.password.get_secret_value()),
                        "database": self.database},
                }
            },
            "apps": {
                "models": {
                    "models": ["app.db.models", "aerich.models"],
                    "default_connection": "default",
                }
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }

    @property
    def sqlite_config(self) -> Dict:
        """获取 SQLite 配置"""
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {
                        "file_path": self.sqlite_db_path
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["app.db.models", "aerich.models"],
                    "default_connection": "default",
                }
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }

    @property
    def db_config(self) -> Dict:
        """获取数据库配置"""
        if self.db_type.lower() == "sqlite":
            return self.sqlite_config
        else:
            return self.config

    class Config:
        """数据库配置类"""
        env_file = ENV_FILE  # 表示从环境变量中获取
        case_sensitive = False
        # 环境变量前缀（可选）
        env_prefix = "postgres_"
        # 允许额外字段
        extra = "ignore"  # 或者使用 "ignore"


class AdminConfig(BaseSettings):
    """应用配置类"""
    name: str = ""
    password: SecretStr = SecretStr("")

    @property
    def password_value(self) -> str:
        """获取密码"""
        return self.password.get_secret_value()

    class Config:
        """管理员配置类"""
        env_file = ENV_FILE  # 表示从环境变量中获取
        case_sensitive = False
        # 环境变量前缀（可选）
        env_prefix = "superadmin_"  # 不使用前缀
        # 允许额外字段
        extra = "ignore"  # 或者使用 "ignore"


class RateLimitConfig(BaseSettings):
    """限流配置"""
    # 是否启用限流
    enabled: bool = True
    # 默认限流：每分钟60次请求
    default_limit: int = 60
    default_window: int = 60
    # 登录接口限流：每分钟5次请求
    login_limit: int = 5
    login_window: int = 60
    # 上传接口限流：每分钟10次请求
    upload_limit: int = 10
    upload_window: int = 60
    # 白名单IP（多个IP用逗号分隔）
    whitelist_ips: str = ""
    # 是否启用自动清理
    enable_cleanup: bool = True

    def get_whitelist_ips(self) -> list:
        """获取白名单IP列表"""
        if not self.whitelist_ips.strip():
            return []
        return [ip.strip() for ip in self.whitelist_ips.split(",") if ip.strip()]

    class Config:
        """配置类"""
        env_file = ENV_FILE
        env_prefix = "RATE_LIMIT_"  # 使用 RATE_LIMIT_ 前缀
        case_sensitive = False
        extra = 'ignore'


@lru_cache()
def get_settings() -> SystemConfig:
    """获取配置实例（单例模式）"""
    config = SystemConfig()
    return config


system_settings = get_settings()
db_settings = DatabaseSettings()
admin_config = AdminConfig()
jwt_config = JwtConfig()
rate_limit_config = RateLimitConfig()
