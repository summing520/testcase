# -*- coding: utf-8 -*-
"""Compare DB schema.table refs in parsed Feishu wiki vs HUB用户流程涉及表.md.

用法::

  python scripts/diff_feishu_tables_vs_hub.py [飞书解析md路径]

默认读取 ``docs/knowledge/_feishu_wiki_parsed.md``（需先用 feishu CLI 生成）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB_PATH = ROOT / "docs" / "knowledge" / "HUB用户流程涉及表.md"
FEI_DEFAULT = ROOT / "docs" / "knowledge" / "_feishu_wiki_parsed.md"

# Schemas we treat as "database tables" (exclude com.*, java packages, etc.)
SCHEMAS = {
    "ams",
    "apv",
    "bcs",
    "brg",
    "cis",
    "cns",
    "cos",
    "crs",
    "css",
    "des",
    "dps",
    "dwd",
    "dws_analyze",
    "evt",
    "fas",
    "fms",
    "gos",
    "hover",
    "hub",
    "lcs",
    "lps",
    "lw_hub",
    "mail",
    "mds",
    "mes",
    "micros_fileservice",
    "micros_gatewayadmin",
    "micros_users",
    "pas",
    "rds",
    "rps",
    "tds",
    "trs",
    "web_tools",
    "widek",
    "xxljob",
    "zlist",
}


def hub_pairs(text: str) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for m in re.finditer(r"`([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)`", text):
        out.add((m.group(1).lower(), m.group(2).lower()))
    return out


def feishu_pairs(text: str) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    pat_bt = re.compile(r"`([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)`")
    pat_sql = re.compile(
        r"(?:\bFROM\b|\bJOIN\b|\bINTO\b|\bUPDATE\b|\bTABLE\b)\s+"
        r"([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)",
        re.I,
    )
    pat_ins = re.compile(r"\bINSERT\s+INTO\s+([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\b", re.I)
    pat_plain = re.compile(
        r"(?<![a-zA-Z0-9_])([a-z][a-z0-9_]{1,19})\.([a-z][a-z0-9_]*)(?![a-zA-Z0-9_])"
    )

    def add(s: str, t: str) -> None:
        s, t = s.lower(), t.lower()
        if s in SCHEMAS:
            out.add((s, t))

    for m in pat_bt.finditer(text):
        add(m.group(1), m.group(2))
    for m in pat_sql.finditer(text):
        add(m.group(1), m.group(2))
    for m in pat_ins.finditer(text):
        add(m.group(1), m.group(2))
    for m in pat_plain.finditer(text):
        add(m.group(1), m.group(2))
    return out


def main() -> None:
    fei_path = Path(sys.argv[1]) if len(sys.argv) > 1 else FEI_DEFAULT
    if not fei_path.is_absolute():
        fei_path = ROOT / fei_path
    hub = HUB_PATH.read_text(encoding="utf-8")
    fei = fei_path.read_text(encoding="utf-8")
    hs = hub_pairs(hub)
    fs = feishu_pairs(fei)
    diff = sorted(fs - hs, key=lambda x: (x[0], x[1]))
    print(f"HUB 清单（反引号 `库.表`）: {len(hs)}")
    print(f"飞书解析文本中识别到的库.表: {len(fs)}")
    print(f"飞书有、HUB 清单无: {len(diff)}")
    for s, t in diff:
        print(f"  {s}.{t}")


if __name__ == "__main__":
    main()
