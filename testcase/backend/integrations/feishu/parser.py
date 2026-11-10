import re


def extract_token_from_url(url: str) -> tuple[str, str]:
    """Return (token, doc_type), doc_type in: doc | sheet | wiki."""
    match = re.search(r"/docs/([^/?]+)", url)
    if match:
        return match.group(1), "doc"
    match = re.search(r"/sheets/([^/?]+)", url)
    if match:
        return match.group(1), "sheet"
    match = re.search(r"/wiki/([^/?]+)", url)
    if match:
        return match.group(1), "wiki"
    raise ValueError(f"无法识别的飞书 URL: {url}")


def extract_text_from_elements(elements: list[dict]) -> str:
    out = []
    for element in elements or []:
        if "textRun" in element:
            out.append(element["textRun"].get("content", ""))
        elif "link" in element:
            out.append(extract_text_from_elements(element["link"].get("elements", [])))
    return "".join(out)


def parse_block_to_markdown(block: dict) -> str:
    block_type = block.get("block_type")

    if block_type == "heading":
        heading = block.get("heading", {})
        level = heading.get("level", 1)
        text = extract_text_from_elements(heading.get("elements", []))
        return "#" * level + " " + text.strip()

    if block_type == "paragraph":
        paragraph = block.get("paragraph", {})
        text = extract_text_from_elements(paragraph.get("elements", []))
        return text.strip()

    if block_type == "table":
        rows = block.get("table", {}).get("rows", [])
        lines = []
        for row in rows:
            cells = []
            for cell in row.get("cells", []):
                cell_text = extract_text_from_elements(cell.get("elements", []))
                cells.append(cell_text.strip().replace("|", "\\|"))
            lines.append("| " + " | ".join(cells) + " |")
        if lines:
            n_cols = len(lines[0].split("|")[1:-1])
            lines.insert(1, "| " + " | ".join(["---"] * n_cols) + " |")
        return "\n".join(lines)

    if block_type == "list":
        items = []
        for element in block.get("list", {}).get("elements", []) or []:
            if "textRun" in element:
                items.append("- " + element["textRun"].get("content", ""))
        return "\n".join(items)

    return ""


def parse_content_to_markdown(content_response: dict) -> str:
    content = content_response.get("data", {}).get("content") or {}
    blocks = content.get("blocks") or []
    parts = []
    for block in blocks:
        text = parse_block_to_markdown(block)
        if text:
            parts.append(text)
    return "\n\n".join(parts)
