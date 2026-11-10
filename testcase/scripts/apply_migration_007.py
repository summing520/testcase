"""Apply migration 007: add interface_doc_path to testcase_tasks."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from backend.db.connection import get_connection  # noqa: E402


def main() -> int:
    conn = get_connection()
    try:
        row = conn.execute(
            "SHOW COLUMNS FROM testcase_tasks LIKE %s",
            ("interface_doc_path",),
        ).fetchone()
        if row:
            print("Column interface_doc_path already exists — nothing to do.")
            return 0
        conn.execute(
            """
            ALTER TABLE testcase_tasks
              ADD COLUMN interface_doc_path VARCHAR(512) NOT NULL DEFAULT ''
                COMMENT '生成用例时使用的接口文档路径'
                AFTER external_cooperation_url
            """
        )
        conn.commit()
        print("Migration 007 applied: interface_doc_path column added.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
