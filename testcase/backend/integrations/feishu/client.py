import requests


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=10,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取 token 失败: {data.get('msg')}")
    return data["tenant_access_token"]


def get_file_content(file_token: str, access_token: str) -> dict:
    resp = requests.get(
        f"https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/content",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    try:
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"文档接口返回非 JSON，status={resp.status_code}，body 前 200 字: {resp.text[:200]}"
        ) from exc

    if data.get("code") != 0:
        raise RuntimeError(f"获取文档内容失败: {data.get('msg')}")
    return data


def get_wiki_node(wiki_token: str, access_token: str) -> dict:
    resp = requests.get(
        "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node",
        params={"token": wiki_token},
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    try:
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"知识库节点接口返回非 JSON，status={resp.status_code}，body: {resp.text[:200]}"
        ) from exc

    if data.get("code") != 0:
        raise RuntimeError(f"获取知识库节点失败: {data.get('msg')}")
    return data


def get_drive_file_meta(file_token: str, access_token: str) -> dict:
    """GET /drive/v1/files/:file_token — returns file name and metadata."""
    resp = requests.get(
        f"https://open.feishu.cn/open-apis/drive/v1/files/{file_token}",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    try:
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"文件元数据接口返回非 JSON，status={resp.status_code}，body: {resp.text[:200]}"
        ) from exc

    if data.get("code") != 0:
        raise RuntimeError(f"获取文件信息失败: {data.get('msg')}")
    return data


def get_docx_raw_content(document_id: str, access_token: str) -> dict:
    resp = requests.get(
        f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/raw_content",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    try:
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"docx 接口返回非 JSON，status={resp.status_code}，body: {resp.text[:200]}"
        ) from exc

    if data.get("code") != 0:
        raise RuntimeError(f"获取 docx 内容失败: {data.get('msg')}")
    return data
