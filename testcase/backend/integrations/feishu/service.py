import os

from dotenv import load_dotenv

from backend.integrations.feishu.client import (
    get_docx_raw_content,
    get_drive_file_meta,
    get_file_content,
    get_tenant_access_token,
    get_wiki_node,
)
from backend.integrations.feishu.parser import extract_token_from_url, parse_content_to_markdown

load_dotenv()


class FeishuConfigError(RuntimeError):
    """Raised when Feishu credentials are missing."""


def _load_feishu_credentials() -> tuple[str, str]:
    app_id = (os.environ.get("FEISHU_APP_ID") or "").strip()
    app_secret = (os.environ.get("FEISHU_APP_SECRET") or "").strip()
    return app_id, app_secret


def feishu_resolve_url_preview(url: str) -> dict[str, str]:
    """
    Resolve Feishu wiki / doc URL to a display title without downloading full body.
    Used by step1 URL preview (lighter than feishu_url_to_markdown).
    """
    normalized_url = (url or "").strip()
    if not normalized_url:
        raise ValueError("飞书链接为空")

    app_id, app_secret = _load_feishu_credentials()
    if not app_id or not app_secret:
        raise FeishuConfigError(
            "未配置飞书凭证：请在项目根 `.env` 中设置 FEISHU_APP_ID、FEISHU_APP_SECRET，"
            "或导出同名环境变量后重试。"
        )

    file_token, doc_type = extract_token_from_url(normalized_url)
    if doc_type == "sheet":
        raise ValueError("当前不支持表格链接，请使用文档或知识库页面链接")

    access_token = get_tenant_access_token(app_id, app_secret)

    if doc_type == "wiki":
        node_resp = get_wiki_node(file_token, access_token)
        node = node_resp.get("data", {}).get("node") or {}
        title = (node.get("title") or "").strip() or "（无标题）"
    else:
        meta_resp = get_drive_file_meta(file_token, access_token)
        file_data = meta_resp.get("data") or {}
        name = file_data.get("name")
        if not name and isinstance(file_data.get("file"), dict):
            name = file_data["file"].get("name")
        title = (name or "").strip() or "（无标题）"

    return {"title": title, "url": normalized_url}


def feishu_url_to_markdown(url: str) -> str:
    """
    Pull content from Feishu doc/wiki URL and convert to Markdown.
    Sheets are intentionally unsupported.
    """
    normalized_url = (url or "").strip()
    if not normalized_url:
        raise ValueError("飞书链接为空")

    app_id, app_secret = _load_feishu_credentials()
    if not app_id or not app_secret:
        raise FeishuConfigError(
            "未配置飞书凭证：请在项目根 `.env` 中设置 FEISHU_APP_ID、FEISHU_APP_SECRET，"
            "或导出同名环境变量后重试。"
        )

    file_token, doc_type = extract_token_from_url(normalized_url)
    if doc_type == "sheet":
        raise RuntimeError("当前仅支持文档与知识库链接，不支持表格（/sheets/）。")

    access_token = get_tenant_access_token(app_id, app_secret)

    if doc_type == "wiki":
        node_resp = get_wiki_node(file_token, access_token)
        node = node_resp.get("data", {}).get("node") or {}
        obj_token = node.get("obj_token")
        obj_type = (node.get("obj_type") or "").lower()

        if not obj_token:
            raise RuntimeError("知识库节点未返回 obj_token，可能无权限或节点类型不支持")

        if obj_type == "docx":
            docx_resp = get_docx_raw_content(obj_token, access_token)
            content_text = docx_resp.get("data", {}).get("content", "")
            markdown = content_text.strip() if content_text else ""
        else:
            content = get_file_content(obj_token, access_token)
            markdown = parse_content_to_markdown(content)
    else:
        content = get_file_content(file_token, access_token)
        markdown = parse_content_to_markdown(content)

    header = "\n".join(
        [
            "# 飞书文档解析结果",
            "",
            f"> 来源：`{normalized_url}`",
            "",
            "---",
            "",
        ]
    )
    body = markdown.strip() if markdown else "（文档内容为空或暂无法解析为文本）"
    return header + body + "\n"
