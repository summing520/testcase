from __future__ import annotations

import json
import re
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.engine import CursorResult, Engine

from backend.integrations.database.client import DatabaseConfigError, get_engine
from backend.integrations.database.config import get_database_query_schema


_TABLE_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")


def _validate_table_identifier(name: str) -> str:
    n = (name or "").strip()
    if not n or not _TABLE_NAME_PATTERN.fullmatch(n):
        raise ValueError(f"非法表名: {name!r}（仅允许字母、数字、下划线）")
    return n


def _quote_table(engine: Engine, table: str) -> str:
    return engine.dialect.identifier_preparer.quote(table)


def _inspector_schema() -> str | None:
    return get_database_query_schema()


def list_tables() -> list[str]:
    """Return user-visible table names (current schema / database)."""
    engine = get_engine()
    insp = inspect(engine)
    schema = _inspector_schema()
    dialect = engine.dialect.name
    if schema and dialect not in ("postgresql", "mssql"):
        schema = None
    try:
        if schema:
            return list(insp.get_table_names(schema=schema))
        return list(insp.get_table_names())
    except TypeError:
        return list(insp.get_table_names())


def _ensure_table_exists(engine: Engine, table: str) -> None:
    safe = _validate_table_identifier(table)
    names = set(list_tables())
    if safe not in names:
        raise ValueError(f"表不存在或无权访问: {safe}")


def describe_table(table: str) -> dict[str, Any]:
    """
    Table structure: columns (name, type, nullable, default, autoincrement),
    primary key, foreign keys (simplified).
    """
    engine = get_engine()
    _ensure_table_exists(engine, table)
    safe = _validate_table_identifier(table)
    insp = inspect(engine)
    schema = _inspector_schema()
    dialect = engine.dialect.name
    if schema and dialect not in ("postgresql", "mssql"):
        schema = None

    kwargs: dict[str, Any] = {}
    if schema:
        kwargs["schema"] = schema

    cols = insp.get_columns(safe, **kwargs)
    column_rows: list[dict[str, Any]] = []
    for c in cols:
        col_type = c.get("type")
        column_rows.append(
            {
                "name": c.get("name"),
                "type": str(col_type) if col_type is not None else None,
                "nullable": c.get("nullable"),
                "default": c.get("default"),
                "autoincrement": c.get("autoincrement"),
                "comment": c.get("comment"),
            }
        )

    pk = insp.get_pk_constraint(safe, **kwargs)
    fks = insp.get_foreign_keys(safe, **kwargs)

    return {
        "table": safe,
        "columns": column_rows,
        "primary_key": pk.get("constrained_columns") or [],
        "foreign_keys": [
            {
                "name": fk.get("name"),
                "constrained_columns": fk.get("constrained_columns"),
                "referred_schema": fk.get("referred_schema"),
                "referred_table": fk.get("referred_table"),
                "referred_columns": fk.get("referred_columns"),
            }
            for fk in fks
        ],
    }


def sample_table_rows(table: str, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    """Read-only: SELECT * with LIMIT/OFFSET (identifier validated)."""
    engine = get_engine()
    _ensure_table_exists(engine, table)
    safe = _validate_table_identifier(table)
    qtable = _quote_table(engine, safe)
    lim = max(1, min(int(limit), 500))
    off = max(0, int(offset))

    stmt = text(f"SELECT * FROM {qtable} LIMIT :lim OFFSET :off")

    with engine.connect() as conn:
        result: CursorResult[Any] = conn.execute(stmt, {"lim": lim, "off": off})
        rows = result.mappings().all()

    out: list[dict[str, Any]] = []
    for row in rows:
        d = dict(row)
        out.append({k: _json_safe(v) for k, v in d.items()})
    return out


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def format_table_description_as_text(info: dict[str, Any]) -> str:
    lines = [f"表: {info.get('table')}", f"主键: {info.get('primary_key')}", "", "列:"]
    for c in info.get("columns") or []:
        lines.append(
            f"  - {c.get('name')}: {c.get('type')} nullable={c.get('nullable')} "
            f"default={c.get('default')!r}"
        )
    fks = info.get("foreign_keys") or []
    if fks:
        lines.append("", "外键:")
        for fk in fks:
            lines.append(f"  - {fk}")
    return "\n".join(lines)


def format_rows_as_json(rows: list[dict[str, Any]]) -> str:
    return json.dumps(rows, ensure_ascii=False, indent=2, default=str)
