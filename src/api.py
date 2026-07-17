"""
FastAPI 服务入口
提供 REST API 供外部调用工作流
"""

import uuid
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import settings
from src.graphs import rag_app
from src.utils import logger


# === Pydantic 请求/响应模型 ===

class WorkflowRequest(BaseModel):
    """工作流请求"""
    query: str = Field(..., min_length=1, max_length=4000, description="用户查询")
    thread_id: str | None = Field(default=None, description="会话ID（为空则自动生成）")
    metadata: dict[str, Any] = Field(default_factory=dict, description="附加元数据")


class WorkflowResponse(BaseModel):
    """工作流响应"""
    thread_id: str
    answer: str
    confidence: str
    iteration: int
    current_step: str
    metadata: dict[str, Any]


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str = "0.1.0"
    environment: str
    model: str


# === FastAPI 应用 ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("🚀 API 服务启动")
    logger.info(f"环境: {settings.app_env}, 模型: {settings.openai_model}")
    yield
    logger.info("🛑 API 服务关闭")


app = FastAPI(
    title="LangGraph 工作流 API",
    description="基于 LangGraph 的 AI 工作流服务",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """健康检查端点"""
    return HealthResponse(
        status="healthy",
        environment=settings.app_env,
        model=settings.openai_model,
    )


@app.post("/workflow/run", response_model=WorkflowResponse)
async def run_workflow(request: WorkflowRequest) -> WorkflowResponse:
    """
    运行工作流

    - 同步执行，等待完整结果
    - 使用 thread_id 维持会话状态
    """
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    logger.info(f"[API] 工作流请求 | thread={thread_id}, query={request.query[:50]}...")

    try:
        result = rag_app.invoke(
            {
                "user_input": request.query,
                "iteration": 0,
                "is_complete": False,
                "metadata": request.metadata,
            },
            config=config,
        )

        return WorkflowResponse(
            thread_id=thread_id,
            answer=result.get("answer", ""),
            confidence=result.get("confidence", "unknown"),
            iteration=result.get("iteration", 0),
            current_step=result.get("current_step", ""),
            metadata=result.get("metadata", {}),
        )
    except Exception as e:
        logger.error(f"[API] 工作流执行失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow/stream")
async def stream_workflow(request: WorkflowRequest):
    """
    流式运行工作流（SSE）

    实时返回每个节点的执行结果
    """
    from fastapi.responses import StreamingResponse

    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        async for chunk in rag_app.astream(
            {
                "user_input": request.query,
                "iteration": 0,
                "is_complete": False,
            },
            config=config,
        ):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
