# -*- coding: utf-8 -*-
"""One-off / reusable: trim 数据库表结构.md to selected schemas only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

KEEP_ORDER = ["ams", "cis", "hub", "lcs", "lps", "mds", "tds"]
KEEP = frozenset(KEEP_ORDER)


def _idx_startswith(lines: list[str], prefix: str) -> int:
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            return i
    raise SystemExit(f"missing section: {prefix!r}")


def _parse_summary_name(line: str) -> str | None:
    m = re.match(r"^### 库 `([^`]+)` 摘要\s*$", line)
    return m.group(1) if m else None


def _parse_detail_lib_name(line: str) -> str | None:
    m = re.match(r"^## 库 `([^`]+)`\s*$", line)
    return m.group(1) if m else None


def _parse_mermaid_lib_name(line: str) -> str | None:
    m = re.match(r"^#### 库 `([^`]+)`\s*$", line)
    return m.group(1) if m else None


def parse_summary_blocks(lines: list[str], start: int, end: int) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {}
    j = start
    while j < end:
        name = _parse_summary_name(lines[j])
        if name is None:
            j += 1
            continue
        block_start = j
        j += 1
        while j < end and _parse_summary_name(lines[j]) is None and not lines[j].startswith(
            "## "
        ):
            j += 1
        blocks[name] = lines[block_start:j]
    return blocks


def parse_detail_blocks(lines: list[str], start: int) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {}
    k = start
    n = len(lines)
    while k < n:
        name = _parse_detail_lib_name(lines[k])
        if name is None:
            k += 1
            continue
        block_start = k
        k += 1
        while k < n and _parse_detail_lib_name(lines[k]) is None:
            k += 1
        blocks[name] = lines[block_start:k]
    return blocks


def filter_fk_section(fk_lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    n = len(fk_lines)
    while i < n:
        line = fk_lines[i]
        mname = _parse_mermaid_lib_name(line)
        if mname is not None:
            start = i
            i += 1
            while i < n and _parse_mermaid_lib_name(fk_lines[i]) is None and not fk_lines[
                i
            ].startswith("### 外键约束明细"):
                i += 1
            if mname in KEEP:
                out.extend(fk_lines[start:i])
            continue
        if line.startswith("### 外键约束明细"):
            out.append(line)
            i += 1
            while i < n and fk_lines[i].strip() == "":
                out.append(fk_lines[i])
                i += 1
            while i < n and fk_lines[i].startswith("|"):
                row = fk_lines[i]
                if "---" in row:
                    out.append(row)
                    i += 1
                    continue
                schemas = re.findall(r"`([a-zA-Z0-9_]+)\.", row)
                if len(schemas) >= 2 and schemas[0] in KEEP and schemas[1] in KEEP:
                    out.append(row)
                i += 1
            continue
        out.append(line)
        i += 1
    return out


def build_trimmed(lines: list[str]) -> list[str]:
    i_summary = _idx_startswith(lines, "## 各库摘要")
    i_kg_db = _idx_startswith(lines, "## 知识图谱：库与库关联")
    i_kg_fk = _idx_startswith(lines, "## 知识图谱：表与表外键")
    i_detail = _idx_startswith(lines, "## 详细表结构")

    summary_blocks = parse_summary_blocks(lines, i_summary + 1, i_kg_db)
    for name in KEEP_ORDER:
        if name not in summary_blocks:
            raise SystemExit(f"missing summary block for {name!r}")

    first_detail_lib = None
    for k in range(i_detail, len(lines)):
        if _parse_detail_lib_name(lines[k]) is not None:
            first_detail_lib = k
            break
    if first_detail_lib is None:
        raise SystemExit("no ## 库 detail sections found")

    detail_blocks = parse_detail_blocks(lines, first_detail_lib)
    for name in KEEP_ORDER:
        if name not in detail_blocks:
            raise SystemExit(f"missing detail block for {name!r}")

    out: list[str] = []
    for h in range(0, i_summary):
        line = lines[h]
        if line.startswith("> **结构指纹**"):
            out.append(
                "> **结构指纹**：（文档已人工裁剪，仅保留指定库；原全库指纹不再适用）\n"
            )
            continue
        if line.startswith("> **生成时间**"):
            out.append(line)
            libs = "、".join(f"`{x}`" for x in KEEP_ORDER)
            out.append(f"> **保留库**：{libs}（其余库表信息已移除）。\n")
            continue
        out.append(line)
    out.append(lines[i_summary])
    out.append("\n")

    for name in KEEP_ORDER:
        out.extend(summary_blocks[name])

    out.append("\n")
    out.extend(lines[i_kg_db:i_kg_fk])
    out.extend(filter_fk_section(lines[i_kg_fk:i_detail]))

    out.append(lines[i_detail])
    if not lines[i_detail].endswith("\n"):
        out[-1] += "\n"
    out.append("\n")

    for name in KEEP_ORDER:
        out.extend(detail_blocks[name])

    return out


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "docs" / "knowledge" / "数据库表结构.md"
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    trimmed = build_trimmed(lines)
    path.write_text("".join(trimmed), encoding="utf-8")
    print(f"Wrote {path} ({len(trimmed)} lines)")


if __name__ == "__main__":
    main()
