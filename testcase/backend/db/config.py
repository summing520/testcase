from __future__ import annotations

import os


class AppDatabaseConfigError(RuntimeError):
    """Missing APP_DB_URL or invalid configuration."""


def get_app_db_url() -> str:
    url = (os.getenv("APP_DB_URL") or "").strip()
    if not url:
        raise AppDatabaseConfigError(
            "未配置应用数据库：请在项目根 `.env` 中设置 APP_DB_URL（示例见 `.env.example`）。"
        )
    return url
