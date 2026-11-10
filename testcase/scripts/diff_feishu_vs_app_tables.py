# -*- coding: utf-8 -*-
"""Feishu parsed wiki vs APP用户流程涉及表.md — tables in Feishu not listed in APP doc."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "docs" / "knowledge" / "APP用户流程涉及表.md"
FEI_DEFAULT = ROOT / "docs" / "knowledge" / "_feishu_app_flow_parsed.md"

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


def app_pairs(text: str) -> set[tuple[str, str]]:
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
    # 避免默认 Unicode \\b 把中文等视作“单词字符”，导致 record表 无法结束匹配
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
    app = APP_PATH.read_text(encoding="utf-8")
    fei = fei_path.read_text(encoding="utf-8")
    a = app_pairs(app)
    f = feishu_pairs(fei)
    diff = sorted(f - a, key=lambda x: (x[0], x[1]))
    print(f"APP 清单 `库.表` 数: {len(a)}")
    print(f"飞书解析稿识别 `库.表` 数: {len(f)}")
    print(f"飞书有、APP 清单无: {len(diff)}")
    for s, t in diff:
        print(f"  {s}.{t}")


if __name__ == "__main__":
    main()
