from __future__ import annotations

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from backend.integrations.database.config import get_database_query_url


class DatabaseConfigError(RuntimeError):
    """Missing DB_QUERY_URL or engine cannot be created."""


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    url = get_database_query_url()
    if not url:
        raise DatabaseConfigError(
            "未配置数据库连接：请在项目根 `.env` 中设置 DB_QUERY_URL（示例见 `.env.example`）。"
        )
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
    )


def clear_engine_cache() -> None:
    get_engine.cache_clear()
