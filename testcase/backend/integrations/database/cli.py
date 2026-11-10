"""
CLI: 列出表、查看表结构、预览表数据。

用法（在项目根目录）:
  python -m backend.integrations.database.cli tables
  python -m backend.integrations.database.cli describe my_table
  python -m backend.integrations.database.cli preview my_table --limit 20
  python -m backend.integrations.database.cli schema-doc
"""

from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

load_dotenv()

from backend.integrations.database.client import DatabaseConfigError  # noqa: E402
from backend.integrations.database.service import (  # noqa: E402
    describe_table,
    format_rows_as_json,
    format_table_description_as_text,
    list_tables,
    sample_table_rows,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="查询数据库表结构及采样数据（配置见 .env DB_QUERY_URL）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_tables = sub.add_parser("tables", help="列出所有表名")
    p_desc = sub.add_parser("describe", help="输出表结构（列、主键、外键）")
    p_desc.add_argument("table", help="表名")

    p_prev = sub.add_parser("preview", help="预览表数据（只读 SELECT）")
    p_prev.add_argument("table", help="表名")
    p_prev.add_argument("--limit", type=int, default=50, help="最多行数，默认 50，最大 500")
    p_prev.add_argument("--offset", type=int, default=0, help="偏移")

    p_schema = sub.add_parser(
        "schema-doc",
        help="根据 DB_QUERY_URL 重写 docs/knowledge/数据库表结构.md（忽略已存指纹，强制刷新）",
    )

    args = parser.parse_args()

    try:
        if args.cmd == "tables":
            names = list_tables()
            for n in names:
                print(n)
            return
        if args.cmd == "describe":
            info = describe_table(args.table)
            print(format_table_description_as_text(info))
            return
        if args.cmd == "preview":
            rows = sample_table_rows(args.table, limit=args.limit, offset=args.offset)
            print(format_rows_as_json(rows))
            return
        if args.cmd == "schema-doc":
            from backend.services.schema_knowledge import rebuild_schema_knowledge_document

            ok = rebuild_schema_knowledge_document()
            print("已刷新表结构知识文档。" if ok else "未写入（可能未配置 DB_QUERY_URL 或不支持的方言）。")
            return
    except DatabaseConfigError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
