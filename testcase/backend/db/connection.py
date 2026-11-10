from __future__ import annotations

import json
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any

import pymysql
from pymysql.cursors import DictCursor
from sqlalchemy.engine import make_url

from backend.db.config import get_app_db_url
from backend.db import tables


class AppDatabaseError(RuntimeError):
    """Application database connection or schema error."""


class _CursorWrapper:
    def __init__(self, cursor: pymysql.cursors.Cursor) -> None:
        self._cursor = cursor

    def fetchone(self) -> dict[str, Any] | None:
        return self._cursor.fetchone()

    def fetchall(self) -> list[dict[str, Any]]:
        return self._cursor.fetchall()


class MySQLConnection:
    def __init__(self, conn: pymysql.connections.Connection) -> None:
        self._conn = conn

    def execute(self, sql: str, params: tuple | list | None = None) -> _CursorWrapper:
        if "?" in sql:
            sql = sql.replace("?", "%s")
        cursor = self._conn.cursor()
        cursor.execute(sql, params or ())
        return _CursorWrapper(cursor)

    def commit(self) -> None:
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


@lru_cache(maxsize=1)
def _connect_kwargs() -> dict[str, Any]:
    url = make_url(get_app_db_url())
    query = dict(url.query)
    charset = query.get("charset", "utf8mb4")
    return {
        "host": url.host or "127.0.0.1",
        "port": url.port or 3306,
        "user": url.username,
        "password": url.password or "",
        "database": url.database,
        "charset": charset,
        "cursorclass": DictCursor,
        "autocommit": False,
    }


def get_connection() -> MySQLConnection:
    try:
        raw = pymysql.connect(**_connect_kwargs())
    except pymysql.MySQLError as exc:
        raise AppDatabaseError(f"无法连接应用数据库: {exc}") from exc
    return MySQLConnection(raw)


def now_utc() -> datetime:
    """Naive UTC datetime for MySQL DATETIME(3) columns."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if value is None:
        raise ValueError("datetime value is required")
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def json_load(value: Any, default: Any | None = None) -> Any:
    if value is None:
        return default
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, (bytes, bytearray)):
        value = value.decode()
    return json.loads(value)


def init_db() -> None:
    """Verify MySQL schema exists (tables created via migrations/001_init_mysql8.sql)."""
    conn = get_connection()
    try:
        missing: list[str] = []
        for table in tables.ALL:
            row = conn.execute(
                """
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = DATABASE() AND table_name = %s
                LIMIT 1
                """,
                (table,),
            ).fetchone()
            if row is None:
                missing.append(table)
        if missing:
            names = ", ".join(missing)
            raise AppDatabaseError(
                f"应用数据库缺少表: {names}。请先执行 backend/db/migrations/001_init_mysql8.sql。"
            )
    finally:
        conn.close()
