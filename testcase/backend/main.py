import os
from pathlib import Path

from dotenv import load_dotenv
import json
import queue
import threading
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from langchain_openai import ChatOpenAI

from backend.agents.test_agent import TestGenerationAgent
from backend.db.connection import init_db
from backend.integrations.feishu.service import FeishuConfigError, feishu_resolve_url_preview
from backend.models.task import (
    AdoptTaskRequest,
    CheckItemResult,
    CheckItemsUpdateRequest,
    FeishuUrlPreviewResponse,
    GenerateTaskResponse,
    ParseTaskResponse,
    TaskCreateRequest,
    TaskDetailResponse,
    TaskMarkdownUpdateRequest,
    TaskSummary,
    TestCaseLibraryItem,
)
from backend.models.test_case import TestGenerationRequest, TestGenerationResponse
from backend.models.pipeline import PipelineConfig, PipelineConfigUpdateRequest
from backend.services.pipeline_config_service import (
    get_pipeline_config,
    reset_pipeline_config,
    update_pipeline_config,
)
from backend.services.task_service import (
    adopt_generated_test_case,
    create_task,
    delete_task,
    generate_test_cases,
    get_markdown_file_content,
    get_task,
    list_tasks,
    list_step1_doc_options,
    list_adopted_test_cases,
    parse_task_requirement,
    parse_task_requirement_with_reporter,
    generate_test_cases_with_reporter,
    clear_external_cooperation_doc,
    update_external_cooperation_doc,
    update_task_config,
    update_task_preview_markdown,
    update_check_items,
)

load_dotenv()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_FAVICON_PATH = _PROJECT_ROOT / "frontend" / "favicon.ico"

app = FastAPI(title="testcase", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_llm() -> ChatOpenAI:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, detail="Missing DEEPSEEK_API_KEY in environment variables."
        )

    # 旧版 deepseek-chat 默认最大输出约 4K tokens，长用例易截断；显式提高到 API 允许上限（当前文档为 8K）。
    raw = (os.getenv("DEEPSEEK_MAX_OUTPUT_TOKENS") or "8192").strip()
    try:
        max_out = int(raw)
    except ValueError:
        max_out = 8192
    max_out = max(1024, min(max_out, 8192))

    model_name = (os.getenv("DEEPSEEK_MODEL") or "deepseek-v4-flash").strip() or "deepseek-v4-flash"

    # DeepSeek OpenAI 兼容接口；模型名见官方文档，如 deepseek-v4-pro / deepseek-v4-flash。
    return ChatOpenAI(
        model=model_name,
        temperature=0.2,
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        max_tokens=max_out,
    )


def build_agent() -> TestGenerationAgent:
    return TestGenerationAgent(build_llm())


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    if not _FAVICON_PATH.is_file():
        raise HTTPException(status_code=404, detail="favicon not found")
    return FileResponse(_FAVICON_PATH, media_type="image/x-icon")


@app.post("/generate-tests", response_model=TestGenerationResponse)
def generate_tests(request: TestGenerationRequest) -> TestGenerationResponse:
    try:
        agent = build_agent()
        return agent.run(request)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc


@app.post("/tasks", response_model=TaskSummary)
def create_generation_task(request: TaskCreateRequest) -> TaskSummary:
    try:
        return create_task(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Create task failed: {exc}") from exc


@app.get("/tasks", response_model=list[TaskSummary])
def get_generation_tasks() -> list[TaskSummary]:
    try:
        return list_tasks()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"List tasks failed: {exc}") from exc


@app.get("/tasks/{task_id}", response_model=TaskDetailResponse)
def get_generation_task(task_id: str) -> TaskDetailResponse:
    data = get_task(task_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskDetailResponse(**data)


@app.delete("/tasks/{task_id}")
def delete_generation_task(task_id: str) -> dict:
    try:
        ok = delete_task(task_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"ok": True, "id": task_id}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Delete task failed: {exc}") from exc


@app.post("/tasks/{task_id}/parse", response_model=ParseTaskResponse)
def parse_requirement(task_id: str) -> ParseTaskResponse:
    try:
        parsed = parse_task_requirement(task_id, build_llm())
        if parsed is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return ParseTaskResponse(**parsed)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Parse failed: {exc}") from exc


@app.get("/tasks/{task_id}/parse-stream")
def parse_requirement_stream(task_id: str, requirement_title: str | None = None):
    """
    SSE: 流式推送步骤1解析进度（飞书解析/模型/保存等）。
    客户端 EventSource 连接后会触发一次解析，并持续收到 data 事件（JSON）。
    """

    q: "queue.Queue[dict | None]" = queue.Queue()

    def reporter(evt: dict) -> None:
        q.put(evt)

    def worker() -> None:
        try:
            reporter({"stage": "start", "message": "开始解析飞书需求"})
            llm = build_llm()
            reporter(
                {
                    "stage": "model",
                    "message": f"模型：{getattr(llm, 'model_name', None) or getattr(llm, 'model', None) or 'unknown'}",
                }
            )
            result = parse_task_requirement_with_reporter(
                task_id,
                llm=llm,
                reporter=reporter,
                requirement_title=requirement_title,
            )
            if result is None:
                reporter({"stage": "error", "message": "Task not found"})
            else:
                reporter({"stage": "done", "message": "解析完成"})
        except Exception as exc:  # noqa: BLE001
            reporter({"stage": "error", "message": f"{exc}"})
        finally:
            q.put(None)

    threading.Thread(target=worker, daemon=True).start()

    def event_gen():
        while True:
            item = q.get()
            if item is None:
                yield "event: end\ndata: {}\n\n"
                break
            data = json.dumps(item, ensure_ascii=False)
            yield f"data: {data}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@app.get("/tasks/{task_id}/check-items", response_model=list[CheckItemResult])
def get_task_check_items(task_id: str) -> list[CheckItemResult]:
    data = get_task(task_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return data["check_items"]


@app.put("/tasks/{task_id}/check-items", response_model=list[CheckItemResult])
def update_task_check_items(
    task_id: str, request: CheckItemsUpdateRequest
) -> list[CheckItemResult]:
    try:
        updated = update_check_items(task_id, request.items)
        if updated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated["check_items"]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Update check items failed: {exc}") from exc


@app.post("/tasks/{task_id}/generate", response_model=GenerateTaskResponse)
def generate_task_test_cases(task_id: str) -> GenerateTaskResponse:
    try:
        generated = generate_test_cases(task_id, build_llm())
        if generated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return GenerateTaskResponse(
            task=generated["task"],
            generated_testcase_markdown=generated["generated_testcase_markdown"] or "",
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Generate failed: {exc}") from exc


@app.put("/tasks/{task_id}/preview-markdown", response_model=TaskDetailResponse)
def save_task_preview_markdown(
    task_id: str, request: TaskMarkdownUpdateRequest
) -> TaskDetailResponse:
    """保存 Markdown 预览/编辑页中的需求或测试用例正文。"""
    try:
        markdown = request.markdown if request.markdown is not None else ""
        if not markdown.strip():
            raise HTTPException(status_code=400, detail="markdown is required")
        updated = update_task_preview_markdown(task_id, request.kind, markdown)
        if updated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskDetailResponse(**updated)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Save preview markdown failed: {exc}"
        ) from exc


@app.put("/tasks/{task_id}/external-doc", response_model=TaskDetailResponse)
def save_external_doc(task_id: str, payload: dict) -> TaskDetailResponse:
    """
    步骤2：保存用户上传/粘贴的对接接口文档 Markdown（作为知识注入）。
    payload:
      - markdown: str (required unless clear=true)
      - url: str (optional)
      - source_path: str (optional) — 接口文档路径或「用户上传/文件名」
      - clear: bool (optional) — 为 true 时清除已保存的对接文档
    """
    try:
        if payload.get("clear"):
            updated = clear_external_cooperation_doc(task_id)
            if updated is None:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskDetailResponse(**updated)
        markdown = (payload.get("markdown") or "").strip()
        if not markdown:
            raise HTTPException(status_code=400, detail="markdown is required")
        url = (payload.get("url") or "").strip() or None
        source_path = (payload.get("source_path") or "").strip() or None
        updated = update_external_cooperation_doc(
            task_id, markdown, url=url, source_path=source_path
        )
        if updated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskDetailResponse(**updated)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Save external doc failed: {exc}") from exc


@app.put("/tasks/{task_id}/config", response_model=TaskDetailResponse)
def update_task_configuration(task_id: str, payload: dict) -> TaskDetailResponse:
    """
    更新任务选择项（知识文档/规则/生成选项）。
    payload:
      - selected_knowledge_docs: list[str] (optional)
      - selected_rule_docs: list[str] (optional)
      - generation_options: dict (optional)
    """
    try:
        selected_knowledge_docs = payload.get("selected_knowledge_docs")
        selected_rule_docs = payload.get("selected_rule_docs")
        generation_options = payload.get("generation_options")
        updated = update_task_config(
            task_id,
            selected_knowledge_docs=selected_knowledge_docs,
            selected_rule_docs=selected_rule_docs,
            generation_options=generation_options,
        )
        if updated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskDetailResponse(**updated)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Update config failed: {exc}") from exc


@app.get("/tasks/{task_id}/generate-stream")
def generate_task_stream(task_id: str):
    """
    SSE: 流式推送生成进度。
    客户端 EventSource 连接后会触发一次生成，并持续收到 data 事件（JSON）。
    """

    q: "queue.Queue[dict | None]" = queue.Queue()

    def reporter(evt: dict) -> None:
        q.put(evt)

    def worker() -> None:
        try:
            reporter({"stage": "start", "message": "开始生成任务"})
            llm = build_llm()
            reporter(
                {
                    "stage": "model",
                    "message": f"模型：{getattr(llm, 'model_name', None) or getattr(llm, 'model', None) or 'unknown'}",
                }
            )
            result = generate_test_cases_with_reporter(task_id, llm, reporter=reporter)
            if result is None:
                reporter({"stage": "error", "message": "Task not found"})
            else:
                reporter({"stage": "done", "message": "生成完成"})
        except Exception as exc:  # noqa: BLE001
            reporter({"stage": "error", "message": f"{exc}"})
        finally:
            q.put(None)

    threading.Thread(target=worker, daemon=True).start()

    def event_gen():
        while True:
            item = q.get()
            if item is None:
                yield "event: end\ndata: {}\n\n"
                break
            data = json.dumps(item, ensure_ascii=False)
            yield f"data: {data}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@app.post("/tasks/{task_id}/adopt", response_model=TaskDetailResponse)
def adopt_task_result(task_id: str, request: AdoptTaskRequest) -> TaskDetailResponse:
    try:
        adopted = adopt_generated_test_case(task_id, request.title)
        if adopted is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskDetailResponse(**adopted)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Adopt failed: {exc}") from exc


@app.get("/test-case-library", response_model=list[TestCaseLibraryItem])
def get_test_case_library() -> list[TestCaseLibraryItem]:
    try:
        return list_adopted_test_cases()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query library failed: {exc}") from exc


@app.get("/doc-options")
def get_doc_options() -> dict[str, list[str]]:
    try:
        return list_step1_doc_options()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query doc options failed: {exc}") from exc


@app.get("/feishu/url-preview", response_model=FeishuUrlPreviewResponse)
def feishu_url_preview(url: str = Query(..., description="飞书文档或知识库页面 URL")) -> FeishuUrlPreviewResponse:
    """步骤1：根据链接拉取文档标题（不下载正文），用于前端展示。"""
    try:
        meta = feishu_resolve_url_preview(url)
        return FeishuUrlPreviewResponse(**meta)
    except FeishuConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"解析飞书链接失败：{exc}") from exc


@app.get("/markdown-file-content")
def markdown_file_content(path: str = Query(..., description="Relative markdown path")) -> dict:
    try:
        content = get_markdown_file_content(path)
        return {"path": path, "content": content}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Read markdown failed: {exc}") from exc


@app.get("/pipeline-config", response_model=PipelineConfig)
def get_testcase_pipeline_config() -> PipelineConfig:
    try:
        return get_pipeline_config()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Get pipeline config failed: {exc}") from exc


@app.put("/pipeline-config", response_model=PipelineConfig)
def put_testcase_pipeline_config(request: PipelineConfigUpdateRequest) -> PipelineConfig:
    try:
        return update_pipeline_config(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Update pipeline config failed: {exc}") from exc


@app.post("/pipeline-config/reset", response_model=PipelineConfig)
def post_pipeline_config_reset() -> PipelineConfig:
    try:
        return reset_pipeline_config()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Reset pipeline config failed: {exc}") from exc
