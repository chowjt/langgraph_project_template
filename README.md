# 🤖 LangGraph 工作流项目模板

> **生产级 AI 工作流开发模板**
>
> 基于 **LangGraph 1.2.9** + **LangChain Core 1.4.9** + **Pydantic 2.13.4**
>
> 支持 **Windows 开发（PyCharm）** → **Linux 容器部署** 的完整工作流

---

## 📋 目录

- [项目概述](#-项目概述)
- [技术栈](#-技术栈)
- [项目结构](#-项目结构)
- [环境要求](#-环境要求)
- [快速开始](#-快速开始)
  - [Windows 开发环境搭建](#windows-开发环境搭建)
  - [Linux/Mac 开发环境搭建](#linuxmac-开发环境搭建)
  - [配置环境变量](#配置环境变量)
  - [运行 CLI 测试](#运行-cli-测试)
  - [启动 API 服务](#启动-api-服务)
- [核心模块详解](#-核心模块详解)
  - [配置管理（config）](#1-配置管理-config)
  - [状态模型（models/state）](#2-状态模型-modelsstate)
  - [LLM 初始化（models/llm）](#3-llm-初始化-modelsllm)
  - [节点基类（nodes）](#4-节点基类-nodes)
  - [提示词管理（prompts）](#5-提示词管理-prompts)
  - [工具封装（tools）](#6-工具封装-tools)
  - [工作流图（graphs）](#7-工作流图-graphs)
- [工作流示例：RAG](#-工作流示例-rag)
- [API 接口文档](#-api-接口文档)
- [Docker 部署指南](#-docker-部署指南)
  - [开发环境部署](#开发环境部署)
  - [生产环境部署](#生产环境部署)
  - [仅构建镜像](#仅构建镜像)
- [测试指南](#-测试指南)
- [扩展开发指南](#-扩展开发指南)
  - [添加新的工作流](#添加新的工作流)
  - [添加新的节点](#添加新的节点)
  - [添加新的工具](#添加新的工具)
  - [添加新的 API 端点](#添加新的-api-端点)
- [依赖版本说明](#-依赖版本说明)
- [常见问题](#-常见问题)
- [开发规范](#-开发规范)
- [生产环境检查清单](#-生产环境检查清单)
- [许可证](#-许可证)

---

## 🎯 项目概述

本项目是一个**生产级的 LangGraph 工作流开发模板**，旨在解决以下实际问题：

| 痛点 | 解决方案 |
|---|---|
| 开发环境与生产环境不一致 | Docker 统一环境，Windows 开发 → Linux 部署无缝衔接 |
| 配置分散、难以管理 | Pydantic Settings 集中管理，支持 `.env` 文件和环境变量覆盖 |
| 工作流状态类型不安全 | TypedDict + Annotated reducer，编译时类型检查 |
| 节点逻辑重复、难以复用 | 基类抽象 + 工厂函数，统一日志和错误处理 |
| 提示词散落在代码各处 | 模板化管理，支持变量验证和多语言 |
| LLM 实例频繁创建 | `@lru_cache` 单例模式，支持多模型策略 |
| 缺乏可观测性 | LangSmith 集成 + 结构化日志 |
| 状态无法持久化 | 内存（开发）→ PostgreSQL（生产）一键切换 |

### 适用场景

- 🤖 **智能客服系统** - 多轮对话 + 知识库检索
- 📄 **文档处理工作流** - 解析 → 提取 → 校验 → 生成
- 🔍 **RAG 问答系统** - 检索增强生成 + 置信度评估
- 🧠 **多智能体协作** - 任务分解 → 分配 → 执行 → 汇总
- ✅ **审批工作流** - 条件路由 + 人工审核节点
- 🔄 **自动化流水线** - 数据清洗 → 分析 → 报告生成

---

## 🛠️ 技术栈

### 核心框架

| 技术 | 版本 | 用途 |
|---|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | 1.2.9 | 工作流引擎，支持循环、条件路由、持久化 |
| [LangChain Core](https://python.langchain.com/docs/concepts/) | 1.4.9 | 核心抽象（Messages、ChatModel、Tools）|
| [LangChain OpenAI](https://python.langchain.com/docs/integrations/chat/openai/) | 1.3.5 | OpenAI 模型集成 |
| [Pydantic](https://docs.pydantic.dev/) | 2.13.4 | 数据校验、配置管理、API 请求/响应模型 |
| [Pydantic Core](https://github.com/pydantic/pydantic-core) | 2.46.4 | Pydantic 底层校验引擎 |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | 1.66.0 | OpenAI API 调用 |

### 基础设施

| 技术 | 版本 | 用途 |
|---|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | ≥0.110 | REST API 框架（需安装）|
| [Uvicorn](https://www.uvicorn.org/) | ≥0.29 | ASGI 服务器（需安装）|
| [python-dotenv](https://saurabh-kumar.com/python-dotenv/) | 1.2.2 | `.env` 文件加载 |
| [PyYAML](https://pyyaml.org/) | 6.0.3 | YAML 配置解析 |
| [Tenacity](https://github.com/jd/tenacity) | 9.1.4 | 重试策略 |
| [HTTPX](https://www.python-httpx.org/) | 0.28.1 | 异步 HTTP 客户端 |

### 部署与运维

| 技术 | 用途 |
|---|---|
| Docker + Docker Compose | 容器化部署 |
| PostgreSQL | 状态持久化（检查点）|
| Redis | 缓存、消息队列 |
| LangSmith | 可观测性、追踪、调试 |

### 开发工具

| 技术 | 用途 |
|---|---|
| Pytest | 单元测试、集成测试 |
| Black | 代码格式化 |
| Ruff | 代码检查（Lint）|
| MyPy | 静态类型检查 |

---

## 📁 项目结构

```
langgraph_project_template/
│
├── 📂 src/                          # 源代码主目录
│   │
│   ├── 📂 config/                   # 配置管理模块
│   │   ├── __init__.py              # 导出 Settings、get_settings
│   │   └── settings.py              # Pydantic Settings 全局配置
│   │
│   ├── 📂 models/                   # 数据模型模块
│   │   ├── __init__.py              # 导出状态模型
│   │   ├── state.py                 # TypedDict 工作流状态定义
│   │   └── llm.py                   # LLM 初始化与管理（单例缓存）
│   │
│   ├── 📂 nodes/                    # 工作流节点模块
│   │   ├── __init__.py              # 导出 BaseNode、create_node
│   │   └── base_node.py             # 节点基类 + 工厂函数
│   │
│   ├── 📂 tools/                    # 外部工具模块
│   │   ├── __init__.py              # 导出工具
│   │   └── web_search.py            # DuckDuckGo 搜索工具示例
│   │
│   ├── 📂 prompts/                  # 提示词模板模块
│   │   ├── __init__.py              # 导出提示词模板
│   │   └── system_prompts.py        # 提示词模板定义与管理
│   │
│   ├── 📂 graphs/                   # 工作流图定义模块
│   │   ├── __init__.py              # 导出工作流图
│   │   └── rag_graph.py             # RAG 工作流完整示例
│   │
│   ├── main.py                      # CLI 入口（命令行模式）
│   └── api.py                       # FastAPI 服务入口（API 模式）
│
├── 📂 docker/                       # Docker 配置文件
│   ├── Dockerfile                   # 生产环境 Dockerfile
│   └── Dockerfile.dev               # 开发环境 Dockerfile
│
├── 📂 scripts/                      # 便捷脚本
│   ├── run_cli.py                   # 快速运行 CLI 工作流
│   └── run_api.py                   # 快速启动 API 服务
│
├── 📂 tests/                        # 测试目录
│   ├── __init__.py
│   ├── test_graph.py                # 工作流 Graph 单元测试
│   └── test_api.py                  # API 端点测试
│
├── 📂 docs/                         # 文档目录（可扩展）
│
├── requirements.txt                 # 生产依赖（已锁定兼容版本）
├── pyproject.toml                   # 现代 Python 包配置 + 工具配置
├── docker-compose.yml               # 生产环境 Docker Compose 编排
├── docker-compose.dev.yml           # 开发环境 Docker Compose 编排
│
├── .env.example                     # 环境变量模板（复制为 .env 使用）
├── .gitignore                       # Git 忽略规则
├── .dockerignore                    # Docker 构建忽略规则
│
└── README.md                        # 本文件
```

---

## 🖥️ 环境要求

### 最低要求

- **Python**: 3.11 或更高版本（推荐 3.12）
- **操作系统**: Windows 10/11、macOS 12+、Linux（Ubuntu 20.04+）
- **内存**: 4GB RAM（开发）/ 8GB RAM（生产）
- **磁盘**: 2GB 可用空间

### 开发工具推荐

- **IDE**: PyCharm Professional / VS Code（安装 Python 插件）
- **容器**: Docker Desktop（Windows/Mac）或 Docker Engine（Linux）
- **API 测试**: Postman / curl / HTTPie
- **数据库客户端**: DBeaver / pgAdmin（PostgreSQL）

### 网络要求

- 能访问 OpenAI API（或配置代理 `OPENAI_BASE_URL`）
- 能访问 LangSmith（可选，用于可观测性）

---

## 🚀 快速开始

### Windows 开发环境搭建

#### 步骤 1：克隆/下载项目

```powershell
# 方式 1：Git 克隆
git clone <your-repo-url>
cd langgraph_project_template

# 方式 2：直接解压 zip 文件
cd langgraph_project_template
```

#### 步骤 2：创建虚拟环境（强烈推荐）

```powershell
# 使用 venv（Python 内置）
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 激活后，命令行提示符前会显示 (venv)
```

> 💡 **PyCharm 用户**：可以直接在 PyCharm 中创建虚拟环境：
> `File → Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter → Virtualenv Environment`

#### 步骤 3：安装依赖

```powershell
# 安装生产依赖
pip install -r requirements.txt

# 可选：安装开发依赖（测试、格式化、类型检查）
pip install pytest pytest-asyncio black ruff mypy uvicorn fastapi
```

#### 步骤 4：验证安装

```powershell
python -c "import langgraph, langchain_core, pydantic; print('✅ 依赖安装成功')"
```

---

### Linux/Mac 开发环境搭建

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 可选：开发依赖
pip install pytest pytest-asyncio black ruff mypy uvicorn fastapi
```

---

### 配置环境变量

项目使用 `.env` 文件管理配置，**切勿将 `.env` 提交到 Git！**

```bash
# 复制模板文件
cp .env.example .env

# Windows
copy .env.example .env
```

编辑 `.env` 文件，填入你的实际配置：

```ini
# ============================================
# 必填：OpenAI API 配置
# ============================================
OPENAI_API_KEY=sk-your-actual-api-key-here

# 可选：如果使用代理或第三方 API 平台
OPENAI_BASE_URL=https://api.openai.com/v1

# 可选：模型选择（默认 gpt-4o-mini）
OPENAI_MODEL=gpt-4o-mini

# ============================================
# 可选：LangSmith 可观测性
# ============================================
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=langgraph-workflow

# ============================================
# 应用配置
# ============================================
APP_ENV=development
APP_LOG_LEVEL=INFO
APP_DEBUG=true

# ============================================
# 持久化配置（开发用 memory，生产用 postgres）
# ============================================
CHECKPOINTER_TYPE=memory
```

> 🔐 **安全提示**：`.env` 文件已加入 `.gitignore`，不会意外提交。生产环境建议使用 Docker Secrets 或 Kubernetes ConfigMap/Secret。

---

### 运行 CLI 测试

CLI 模式适合快速测试工作流逻辑，无需启动 Web 服务。

```bash
# 默认查询（什么是 LangGraph？）
python -m src.main

# 自定义查询
python -m src.main "什么是机器学习？"

# 流式输出（实时显示生成内容）
python -m src.main "请详细解释深度学习" --stream

# 查看帮助
python -m src.main --help
```

**预期输出示例**：

```
2025-01-15 10:30:00 | INFO     | langgraph | 环境: development
2025-01-15 10:30:00 | INFO     | langgraph | 模型: gpt-4o-mini
2025-01-15 10:30:00 | INFO     | langgraph | 检查点: memory
2025-01-15 10:30:00 | INFO     | langgraph | [Retrieve] 查询: 什么是机器学习？
2025-01-15 10:30:02 | INFO     | langgraph | [Evaluate] 置信度: high

==================================================
📋 工作流执行结果
==================================================
📝 回答: 机器学习是人工智能的一个分支...
🎯 置信度: high
🔄 迭代次数: 1
📍 最终步骤: evaluate
==================================================
```

---

### 启动 API 服务

API 模式提供 REST 接口，供前端或其他服务调用。

```bash
# 方式 1：使用便捷脚本
python scripts/run_api.py

# 方式 2：直接使用 uvicorn（推荐）
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

# 方式 3：生产模式（多 worker）
uvicorn src.api:app --host 0.0.0.0 --port 8000 --workers 4
```

**访问服务**：

| 地址 | 说明 |
|---|---|
| `http://localhost:8000` | 服务根地址 |
| `http://localhost:8000/docs` | 自动生成的 Swagger UI 文档 |
| `http://localhost:8000/redoc` | ReDoc 文档（替代风格）|
| `http://localhost:8000/health` | 健康检查端点 |

**API 测试示例**：

```bash
# 健康检查
curl http://localhost:8000/health

# 运行工作流
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"query": "什么是LangGraph？"}'

# 带会话 ID 的工作流（状态隔离）
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"query": "继续刚才的话题", "thread_id": "user-123"}'
```

---

## 📚 核心模块详解

### 1. 配置管理（config）

**文件**: `src/config/settings.py`

使用 **Pydantic Settings** 实现类型安全的配置管理，支持：

- `.env` 文件自动加载
- 环境变量覆盖
- 字段验证（如 API Key 格式检查）
- 多环境切换（dev/staging/prod）

```python
from src.config import settings

# 读取配置
print(settings.openai_model)        # gpt-4o-mini
print(settings.is_production)       # False
print(settings.app_env)             # development

# 配置是单例的（@lru_cache），全局共享
from src.config import get_settings
s = get_settings()  # 返回缓存的实例
```

**自定义配置字段**：

```python
# 在 Settings 类中添加新字段
class Settings(BaseSettings):
    # ... 现有字段 ...

    # 新增：自定义超时
    custom_timeout: int = Field(default=30, alias="CUSTOM_TIMEOUT")

    # 新增：功能开关
    feature_x_enabled: bool = Field(default=False, alias="FEATURE_X_ENABLED")
```

---

### 2. 状态模型（models/state）

**文件**: `src/models/state.py`

使用 **TypedDict** 定义工作流状态，这是 LangGraph 推荐的方式：

```python
from typing import Annotated
from langgraph.graph.message import add_messages

class BaseWorkflowState(TypedDict, total=False):
    messages: Annotated[list, add_messages]  # 自动合并消息
    user_input: str
    current_step: str
    iteration: int
    error: Optional[str]
    is_complete: bool
```

**关键概念**：

- **`total=False`**: 所有字段可选，节点只返回需要修改的字段
- **`Annotated[..., add_messages]`**: 消息列表使用 reducer 自动追加而非覆盖
- **继承扩展**: 为特定工作流添加专用字段

```python
# 定义 RAG 专用状态
class RAGState(BaseWorkflowState, total=False):
    retrieved_docs: list[dict]   # 检索到的文档
    answer: str                   # 生成的回答
    confidence: Literal["high", "medium", "low"]
```

---

### 3. LLM 初始化（models/llm）

**文件**: `src/models/llm.py`

使用 `@lru_cache` 实现 LLM 实例的单例模式，避免重复创建：

```python
from src.models.llm import get_llm, get_fast_llm, get_creative_llm

# 默认模型（从配置读取）
llm = get_llm()

# 快速/低成本模型（简单任务）
fast_llm = get_fast_llm()

# 创意型模型（生成任务）
creative_llm = get_creative_llm()

# 自定义参数
llm = get_llm(model="gpt-4o", temperature=0.9, streaming=True)
```

**特性**：

- ✅ 自动重试（Tenacity 底层支持）
- ✅ 超时配置
- ✅ 流式输出支持
- ✅ 多模型策略

---

### 4. 节点基类（nodes）

**文件**: `src/nodes/base_node.py`

提供两种节点开发模式：

#### 模式 A：继承基类（复杂节点）

```python
from src.nodes import BaseNode

class MyCustomNode(BaseNode):
    def __call__(self, state):
        self.log_step("开始处理")
        # ... 业务逻辑 ...
        return {"result": "done", "current_step": "my_node"}

# 使用
workflow.add_node("my_node", MyCustomNode())
```

#### 模式 B：函数包装（简单节点）

```python
from src.nodes import create_node

def my_simple_node(state):
    return {"result": state["user_input"].upper()}

# 自动添加日志和错误处理
workflow.add_node("simple", create_node(my_simple_node, "SimpleNode"))
```

---

### 5. 提示词管理（prompts）

**文件**: `src/prompts/system_prompts.py`

集中管理所有提示词模板，支持变量替换和验证：

```python
from src.prompts import get_prompt, RAG_SYSTEM

# 方式 1：直接使用模板
prompt = RAG_SYSTEM.format(context="文档内容...")

# 方式 2：通过名称获取
template = get_prompt("rag")
prompt = template.format(context="文档内容...")

# 方式 3：在节点中使用
from langchain_core.messages import SystemMessage
system_msg = SystemMessage(content=RAG_SYSTEM.format(context=context))
```

**添加新模板**：

```python
# 在 system_prompts.py 中
MY_NEW_PROMPT = PromptTemplate(
    """你是一个{role}。请处理以下内容：
{content}

要求：{requirements}
"""
)

# 注册到 get_prompt()
def get_prompt(name: str) -> PromptTemplate:
    prompts = {
        # ... 现有模板 ...
        "my_new": MY_NEW_PROMPT,
    }
    # ...
```

---

### 6. 工具封装（tools）

**文件**: `src/tools/web_search.py`

工具是可被 LLM 调用的外部功能：

```python
from src.tools import web_search

# 直接调用
results = web_search("Python 最新版本")

# 绑定到 LLM（让 LLM 自主决定是否调用）
from src.models.llm import get_llm
llm = get_llm().bind_tools([web_search])
```

**添加新工具**：

```python
# 1. 在 tools/ 下创建新文件
# 2. 实现工具函数（需有 docstring，LLM 据此理解用途）
def calculate(expression: str) -> str:
    """计算数学表达式。输入如："1 + 2 * 3""""
    try:
        return str(eval(expression))
    except:
        return "计算错误"

# 3. 导出并在节点中绑定
```

---

### 7. 工作流图（graphs）

**文件**: `src/graphs/rag_graph.py`

这是项目的核心，定义了完整的工作流逻辑：

```python
from langgraph.graph import StateGraph, END

# 1. 定义状态
class MyState(TypedDict):
    user_input: str
    result: str

# 2. 定义节点
def node_a(state):
    return {"result": f"处理: {state['user_input']}"}

# 3. 构建图
workflow = StateGraph(MyState)
workflow.add_node("a", node_a)
workflow.set_entry_point("a")
workflow.add_edge("a", END)

# 4. 编译
app = workflow.compile()

# 5. 运行
result = app.invoke({"user_input": "你好"})
```

---

## 🔄 工作流示例：RAG

本项目包含一个完整的 **RAG（检索增强生成）工作流**，流程如下：

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   用户输入   │────▶│   retrieve  │────▶│   generate  │
│  user_input  │     │  网络搜索    │     │  生成回答    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │   evaluate  │
                                         │  评估质量    │
                                         └──────┬──────┘
                                                │
                                    ┌───────────┼───────────┐
                                    ▼           ▼           ▼
                               confidence   confidence    max_iter
                                  == high    == medium      reached
                                    │           │           │
                                    ▼           ▼           ▼
                                   END         END         END
                                    │
                                    │  confidence == low
                                    ▼
                              ┌─────────────┐
                              │    retry    │
                              │  优化查询    │
                              └──────┬──────┘
                                     │
                                     └─────────────────────┐
                                                            │
                                                            ▼
                                                     ┌─────────────┐
                                                     │   generate  │
                                                     │  重新生成    │
                                                     └─────────────┘
```

### 节点说明

| 节点 | 功能 | 输出字段 |
|---|---|---|
| `retrieve` | 执行网络搜索，获取相关文档 | `retrieved_docs`, `search_query` |
| `generate` | 基于检索结果调用 LLM 生成回答 | `answer`, `messages` |
| `evaluate` | 评估回答质量（长度、关键词启发式）| `confidence` |
| `retry` | 优化查询后重新检索 | `user_input`（优化后）|

### 条件路由

```python
def route_by_confidence(state):
    confidence = state.get("confidence", "low")
    iteration = state.get("iteration", 0)

    if confidence == "high":
        return END           # 质量高，直接结束
    elif iteration >= 10:    # 最大迭代次数
        return END
    elif confidence == "low":
        return "retry"       # 质量低，优化后重试
    else:
        return END
```

---

## 🌐 API 接口文档

启动 API 后访问 `http://localhost:8000/docs` 查看交互式文档。

### 端点列表

#### `GET /health` - 健康检查

**响应**：
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development",
  "model": "gpt-4o-mini"
}
```

#### `POST /workflow/run` - 运行工作流

**请求体**：
```json
{
  "query": "什么是LangGraph？",
  "thread_id": "user-123",
  "metadata": {"source": "web", "priority": "high"}
}
```

**响应**：
```json
{
  "thread_id": "user-123",
  "answer": "LangGraph 是一个用于构建...",
  "confidence": "high",
  "iteration": 1,
  "current_step": "evaluate",
  "metadata": {"source": "web", "priority": "high"}
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `query` | string | ✅ | 用户查询，1-4000 字符 |
| `thread_id` | string | ❌ | 会话 ID，为空则自动生成 UUID |
| `metadata` | object | ❌ | 附加元数据，会原样返回 |

#### `POST /workflow/stream` - 流式运行

**请求体**：同 `/workflow/run`

**响应**：SSE（Server-Sent Events）流

```
data: {"retrieve": {"retrieved_docs": [...]}}

data: {"generate": {"messages": [...]}}

data: {"evaluate": {"confidence": "high"}}

data: [DONE]
```

---

## 🐳 Docker 部署指南

### 前置要求

- [Docker](https://docs.docker.com/get-docker/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+
- Linux 服务器（Ubuntu 20.04+ / CentOS 8+）

### 开发环境部署

适合本地开发调试，支持代码热重载。

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up --build

# 后台运行
docker-compose -f docker-compose.dev.yml up -d --build

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f app

# 停止
docker-compose -f docker-compose.dev.yml down
```

**开发环境特性**：

- ✅ 代码热重载（修改宿主机代码自动同步到容器）
- ✅ 开发工具预装（pytest、black、ruff、mypy）
- ✅ 可选 PostgreSQL（用于测试持久化）
- ✅ 内存检查点（无需外部数据库）

### 生产环境部署

```bash
# 1. 上传项目到服务器
scp -r langgraph_project_template user@server:/opt/

# 2. 在服务器上进入项目目录
cd /opt/langgraph_project_template

# 3. 配置生产环境变量
cp .env.example .env
# 编辑 .env，设置 APP_ENV=production，配置数据库等

# 4. 构建并启动
docker-compose up -d --build

# 5. 查看状态
docker-compose ps
docker-compose logs -f app

# 6. 停止服务
docker-compose down

# 7. 完全清理（包括数据卷）
docker-compose down -v
```

**生产环境架构**：

```
┌─────────────────────────────────────────────────────┐
│                    Docker Network                    │
│              (langgraph-net / bridge)               │
│                                                      │
│  ┌──────────────┐      ┌──────────────┐            │
│  │   langgraph  │      │   postgres   │            │
│  │     app      │◄────►│   (PG 16)    │            │
│  │   :8000      │      │   :5432      │            │
│  └──────────────┘      └──────────────┘            │
│         ▲                                            │
│         │                                            │
│  ┌──────┴──────┐                                    │
│  │    redis    │                                    │
│  │   :6379     │                                    │
│  └─────────────┘                                    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**生产环境特性**：

- ✅ 非 root 用户运行（安全）
- ✅ 健康检查（自动重启故障容器）
- ✅ PostgreSQL 状态持久化
- ✅ Redis 缓存
- ✅ 日志文件持久化
- ✅ 自动重启策略

### 仅构建镜像

```bash
# 构建生产镜像
docker build -f docker/Dockerfile -t langgraph-app:latest .

# 运行容器
docker run -d \
  --name langgraph-app \
  -p 8000:8000 \
  --env-file .env \
  langgraph-app:latest

# 查看日志
docker logs -f langgraph-app
```

---

## 🧪 测试指南

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_graph.py -v

# 运行特定测试类
pytest tests/test_api.py::TestHealth -v

# 带覆盖率报告
pytest tests/ --cov=src --cov-report=html --cov-report=term

# 覆盖率报告会在 htmlcov/ 目录生成 HTML 版本
# 用浏览器打开 htmlcov/index.html 查看
```

### 测试结构

```python
# tests/test_graph.py
class TestRAGGraph:
    @pytest.fixture
    def graph(self):
        return build_rag_graph()

    def test_graph_compiles(self, graph):
        """Graph 能正确编译"""
        assert graph is not None

    def test_simple_query(self, graph):
        """简单查询能完成执行"""
        result = graph.invoke({"user_input": "测试", "iteration": 0})
        assert "answer" in result
```

### 添加新测试

```bash
# 1. 在 tests/ 下创建新文件
# 2. 使用 pytest 编写测试
# 3. 运行验证
pytest tests/test_your_feature.py -v
```

---

## 🔧 扩展开发指南

### 添加新的工作流

以创建一个 **代码审查工作流** 为例：

#### 步骤 1：定义状态

```python
# src/models/state.py
class CodeReviewState(BaseWorkflowState, total=False):
    code: str
    language: str
    review_result: dict
    score: int
```

#### 步骤 2：创建 Graph 文件

```python
# src/graphs/code_review_graph.py
from langgraph.graph import StateGraph, END
from src.models import CodeReviewState

def parse_code_node(state: CodeReviewState):
    return {"current_step": "parse"}

def review_node(state: CodeReviewState):
    # 调用 LLM 审查代码
    return {"review_result": {...}, "current_step": "review"}

def build_code_review_graph():
    workflow = StateGraph(CodeReviewState)
    workflow.add_node("parse", parse_code_node)
    workflow.add_node("review", review_node)
    workflow.set_entry_point("parse")
    workflow.add_edge("parse", "review")
    workflow.add_edge("review", END)
    return workflow.compile()
```

#### 步骤 3：导出

```python
# src/graphs/__init__.py
from .code_review_graph import build_code_review_graph
```

#### 步骤 4：添加 API 端点

```python
# src/api.py
from src.graphs import build_code_review_graph

code_review_app = build_code_review_graph()

@app.post("/workflow/code-review")
async def run_code_review(request: CodeReviewRequest):
    result = code_review_app.invoke({"code": request.code, ...})
    return result
```

### 添加新的节点

```python
# 方式 1：继承基类（推荐复杂节点）
from src.nodes import BaseNode

class DataValidationNode(BaseNode):
    def __call__(self, state):
        self.log_step("验证数据中...")
        # 验证逻辑
        if not state.get("user_input"):
            return {"error": "输入为空", "is_complete": True}
        return {"current_step": "validation"}

# 方式 2：函数包装（简单节点）
from src.nodes import create_node

def simple_transform(state):
    return {"processed": state["user_input"].strip()}

transform_node = create_node(simple_transform, "TransformNode")
```

### 添加新的工具

```python
# src/tools/calculator.py

def calculator(expression: str) -> str:
    """
    计算数学表达式。

    Args:
        expression: 数学表达式，如 "1 + 2 * 3"

    Returns:
        计算结果
    """
    try:
        # 安全计算（实际项目中使用 asteval 等安全库）
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

# 在节点中绑定到 LLM
llm = get_llm().bind_tools([calculator])
```

### 添加新的 API 端点

```python
# src/api.py
from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "en"

class TranslateResponse(BaseModel):
    original: str
    translated: str
    target_language: str

@app.post("/workflow/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """翻译工作流"""
    # 调用工作流
    result = translate_app.invoke({"text": request.text, ...})
    return TranslateResponse(
        original=request.text,
        translated=result["translated"],
        target_language=request.target_language,
    )
```

---

## 📦 依赖版本说明

| 包 | 版本 | 用途 | 兼容性 |
|---|---|---|---|
| `langgraph` | 1.2.9 | 工作流引擎 | ✅ 最新稳定版 |
| `langchain-core` | 1.4.9 | 核心框架 | ✅ 兼容 langgraph 1.2.9 |
| `langchain-openai` | 1.3.5 | OpenAI 集成 | ✅ 兼容 openai 1.x |
| `pydantic` | 2.13.4 | 数据校验 | ✅ 最新稳定版 |
| `pydantic-core` | 2.46.4 | 校验引擎 | ✅ 必须与 pydantic 2.13.4 匹配 |
| `openai` | 1.66.0 | OpenAI SDK | ✅ 1.x 稳定版 |
| `httpx` | 0.28.1 | HTTP 客户端 | ✅ 兼容 |
| `tiktoken` | 0.13.0 | Token 计算 | ✅ 兼容 |
| `tenacity` | 9.1.4 | 重试策略 | ✅ 兼容 |
| `PyYAML` | 6.0.3 | YAML 解析 | ✅ 兼容 |
| `requests` | 2.34.2 | HTTP 请求 | ✅ 兼容 |
| `urllib3` | 2.7.0 | HTTP 客户端 | ✅ 兼容 |
| `xxhash` | 3.8.1 | 哈希算法 | ✅ 兼容 |
| `langgraph-sdk` | 0.2.37 | LangGraph SDK | ✅ 兼容 |

> ⚠️ **重要**：`pydantic-core` 版本必须与 `pydantic` 严格匹配。`pydantic 2.13.4` 要求 `pydantic-core 2.46.4`，不可使用 2.47.0。

---

## ❓ 常见问题

### Q1: Windows 上激活虚拟环境失败？

```powershell
# 如果执行 venv\Scripts\activate 报错，尝试：
venv\Scripts\Activate.ps1

# 如果 PowerShell 执行策略限制，先运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q2: `ModuleNotFoundError: No module named 'src'`？

```bash
# 确保在项目根目录运行
# 错误：cd src && python main.py
# 正确：python -m src.main

# 或在 PyCharm 中设置工作目录为项目根目录
# Run → Edit Configurations → Working directory: <项目根目录>
```

### Q3: OpenAI API 连接超时？

```ini
# .env 中增加超时配置
OPENAI_TIMEOUT=120

# 或使用代理
OPENAI_BASE_URL=https://your-proxy.com/v1
```

### Q4: Docker 构建失败？

```bash
# 清理缓存后重试
docker-compose down -v
docker system prune -f
docker-compose up -d --build --no-cache
```

### Q5: 如何切换检查点到 PostgreSQL？

```ini
# .env
CHECKPOINTER_TYPE=postgres
DATABASE_URI=postgresql://user:pass@localhost:5432/langgraph
```

```python
# src/graphs/rag_graph.py
from langgraph.checkpoint.postgres import PostgresSaver

# 替换 MemorySaver
# checkpointer = MemorySaver()
checkpointer = PostgresSaver.from_conn_string(settings.database_uri)
```

### Q6: 如何查看 LangGraph 工作流图？

```python
# 在代码中导出 Mermaid 图
from src.graphs import rag_app

# 获取 Mermaid 语法
print(rag_app.get_graph().draw_mermaid())

# 或保存为 PNG（需要安装 graphviz）
rag_app.get_graph().draw_png("workflow.png")
```

---

## 📝 开发规范

### 代码风格

- 使用 **Black** 格式化（行宽 100）
- 使用 **Ruff** 检查代码
- 使用 **MyPy** 进行类型检查

```bash
# 格式化代码
black src/ tests/

# 检查代码
ruff check src/ tests/

# 类型检查
mypy src/
```

### 提交规范

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
style: 代码格式调整
refactor: 重构代码
test: 添加测试
chore: 构建/工具变更
```

### 文档规范

- 所有模块、类、函数必须有 docstring
- 复杂逻辑添加行内注释
- API 变更同步更新 README

---

## ✅ 生产环境检查清单

部署到生产环境前，请确认以下事项：

- [ ] `.env` 中 `APP_ENV=production`
- [ ] `.env` 中 `APP_DEBUG=false`
- [ ] `OPENAI_API_KEY` 使用生产环境密钥
- [ ] `CHECKPOINTER_TYPE` 设置为 `postgres`
- [ ] `DATABASE_URI` 指向生产数据库
- [ ] 配置了 LangSmith 追踪（可选但推荐）
- [ ] Docker 镜像使用非 root 用户运行
- [ ] 配置了健康检查
- [ ] 日志持久化到卷或外部系统
- [ ] 配置了监控告警
- [ ] 进行了压力测试
- [ ] 备份策略已制定

---

## 📄 许可证

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
