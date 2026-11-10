# testcase

testcase（本项目）基于 LangChain + FastAPI，默认使用 **DeepSeek V4 Flash（`deepseek-v4-flash`）**；可通过环境变量 `DEEPSEEK_MODEL` 切换为 `deepseek-v4-pro` 等。

## 功能概览

- 三阶段生成流程：代码分析 -> 测试设计 -> 测试代码生成
- 后端 API：`/generate-tests`
- 前端单页工具：`frontend/test_case_generator.html`
- DeepSeek：默认 `deepseek-v4-flash`，由 `DEEPSEEK_MODEL` 配置
- 支持本地开发与 Docker 部署

## 目录结构（摘要）

```text
testcase/
├── backend/
│   ├── main.py                 # FastAPI 入口
│   ├── agents/                 # test_agent（/generate-tests）、testcase_agent（任务流水线）
│   ├── chains/                 # 代码分析 / 测试设计 / 代码生成链（旧版 API）
│   ├── db/sqlite.py
│   ├── integrations/feishu/  # 飞书文档解析
│   ├── integrations/database/# MySQL 等只读查询 CLI
│   ├── models/
│   ├── prompts/
│   ├── services/               # task_service、schema_knowledge、channel_knowledge 等
│   ├── tools/task_tools.py     # 任务 bundle、用例生成上下文
│   └── utils/
├── frontend/
│   ├── test_case_generator.html
│   └── …
├── docs/
│   ├── checklist/              # 例：渠道需求检查项.md、机构需求检查项.md（步骤1 由 /doc-options 扫描）
│   ├── knowledge/              # biz/ 业务；interface/ 外部合作；db/ 数据库表与流程涉及表
│   └── rules/                  # 例：Demo-标准渠道-全流程API对接-测试用例.md
├── .env.example
├── requirements.txt
└── README.md
```

说明：步骤1 知识文档由 **`GET /doc-options`** 分别列出 `docs/knowledge/biz/`、`docs/knowledge/interface/`、`docs/knowledge/db/` 下的 Markdown；检查项与规则仍扫描 `docs/checklist/`、`docs/rules/`。**不存在的文件不会出现在步骤1**；知识、检查项、规则均需手动勾选。

## 技术栈

- Python 3.10+
- FastAPI + Uvicorn
- LangChain
- DeepSeek API（OpenAI 兼容接口）

## 一键启动（推荐）

### 1) 初始化环境变量

复制模板并填入你的真实 key：

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

编辑 `.env`：

```env
DEEPSEEK_API_KEY=your_real_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret
SQLITE_DB_PATH=data/test_case_generation.db
```

说明：
- `DEEPSEEK_API_KEY`：必填
- `DEEPSEEK_BASE_URL`：可选，默认 `https://api.deepseek.com`
- `DEEPSEEK_MODEL`：可选，默认 `deepseek-v4-flash`（例如可改为 `deepseek-v4-pro`）
- `FEISHU_APP_ID` / `FEISHU_APP_SECRET`：仅当使用飞书解析功能时必填
- `SQLITE_DB_PATH`：可选，默认 `data/test_case_generation.db`

### 2) 本地开发启动

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

局域网访问时，前端（如 `http://172.31.x.x:5500/frontend/test_case_generator.html`）会自动将 API 指向 `http://<当前主机>:8000`，无需再写死 `127.0.0.1`。

### 3) Docker 启动

```bash
docker compose up --build
```

## 访问地址

- Swagger: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/health`
- 前端页面：直接打开 `frontend/test_case_generator.html`

## 快速体验（推荐）

`docs/checklist/`、`docs/knowledge/{biz,interface,db}/`、`docs/rules/` 下可放入与对接相关的示例 Markdown。`docs/rules/` 含 Demo 用例骨架及《机构/渠道业务规则》；生成时按对接类型自动注入对应业务规则。**四步流程**见 [`docs/测试用例生成流程.md`](docs/测试用例生成流程.md)。打开 `frontend/test_case_generator.html` 后，步骤1 由 **`/doc-options`** 动态列出上述目录中的文件。

填写飞书需求链接并勾选所需文档后即可跑完整三步流程。若某路径已从磁盘删除，将不再出现在列表中。

## API 说明

### POST `/generate-tests`

请求体：

```json
{
  "source_code": "def add(a, b):\n    return a + b",
  "language": "python",
  "framework": "pytest",
  "extra_requirements": "优先覆盖边界条件和异常场景"
}
```

字段：
- `source_code`：待测源代码（必填）
- `language`：代码语言（默认 `python`）
- `framework`：测试框架（默认 `pytest`）
- `extra_requirements`：额外要求（可选）

响应体：

```json
{
  "analysis": "...",
  "test_design": "...",
  "generated_tests": "..."
}
```

### 任务流接口（SQLite 持久化）

- `POST /tasks`：创建任务（步骤1）
- `POST /tasks/{task_id}/parse`：解析飞书需求 + 匹配检查项（步骤2）
- `GET /tasks/{task_id}/check-items`：获取检查项匹配结果
- `PUT /tasks/{task_id}/check-items`：保存用户编辑后的检查项内容
- `POST /tasks/{task_id}/generate`：生成测试用例（步骤2 -> 步骤3）
- `GET /tasks/{task_id}`：获取任务完整详情
- `POST /tasks/{task_id}/adopt`：采纳测试用例入库
- `GET /test-case-library`：查看已采纳测试用例库
- `GET /doc-options`：查询步骤1可选文档（返回 `knowledge_biz_docs`、`knowledge_interface_docs`、`knowledge_db_docs`、`checklist_docs`、`rule_docs`、`demo_docs` 路径列表）

## 开发规范建议

- 不要提交真实 `.env`，只提交 `.env.example`
- 所有变更先通过 `/health` 与 `/docs` 自检
- 生成链路逻辑优先放在 `backend/chains/`，编排放在 `backend/agents/`
- 提示词只在 `backend/prompts/` 管理，避免分散

## 常见问题

- **`Missing DEEPSEEK_API_KEY in environment variables.`**
  - 检查 `.env` 是否在项目根目录
  - 检查变量名是否为 `DEEPSEEK_API_KEY`
  - 检查启动命令是否在项目根目录执行

- **前端请求失败 / `无法连接后端 http://127.0.0.1:8000`**
  - 本机访问：确认后端 `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
  - 通过 IP 访问静态页（如 `:5500`）时，页面会自动请求 `http://<该IP>:8000`；若仍失败，检查防火墙是否放行 8000 端口
  - 手动指定 API：`localStorage.setItem("testCaseApiBase","http://172.31.255.139:8000")` 后刷新
  - 浏览器控制台查看请求报错详情

- **Docker 启动后无法访问**
  - 检查 `docker compose ps` 是否显示 `api` 运行中
  - 查看日志：`docker compose logs -f api`

## 后续工程化增强（可选）

- 增加 `pre-commit`（格式化 + lint + 基础检查）
- 增加 `pytest` 与 API 集成测试
- 增加 CI（GitHub Actions）自动构建和健康检查
- 增加结构化日志与请求追踪

## 飞书文档解析（可选）

如果你需要把飞书文档/知识库内容转为 Markdown，可使用：

```bash
python -m backend.integrations.feishu.cli "https://xxx.feishu.cn/wiki/xxxxx" -o output.md
```
