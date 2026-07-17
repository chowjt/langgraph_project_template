"""
工作流状态定义 - 所有 Graph 共享的基础状态模型
使用 TypedDict 以获得 LangGraph 最佳兼容性
"""

from typing import Annotated, Any, Literal, Optional, TypedDict

from langgraph.graph.message import add_messages


# === 消息类型 ===
class MessageDict(TypedDict, total=False):
    """单条消息结构"""
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str]
    tool_calls: Optional[list[dict[str, Any]]]


# === 基础工作流状态 ===
class BaseWorkflowState(TypedDict, total=False):
    """
    基础工作流状态
    所有具体工作流状态应继承或包含此结构
    """
    # 消息历史（使用 LangGraph 内置的 add_messages reducer）
    messages: Annotated[list, add_messages]

    # 用户原始输入
    user_input: str

    # 当前步骤/节点名称
    current_step: str

    # 执行迭代计数
    iteration: int

    # 错误信息
    error: Optional[str]

    # 是否完成
    is_complete: bool

    # 元数据
    metadata: dict[str, Any]


# === 示例：RAG 工作流状态 ===
class RAGState(BaseWorkflowState, total=False):
    """RAG（检索增强生成）工作流专用状态"""
    # 检索到的文档
    retrieved_docs: list[dict[str, Any]]

    # 检索查询
    search_query: str

    # 生成的回答
    answer: str

    # 置信度
    confidence: Literal["high", "medium", "low"]

    # 是否需要人工审核
    needs_review: bool


# === 示例：多智能体协作状态 ===
class MultiAgentState(BaseWorkflowState, total=False):
    """多智能体协作工作流专用状态"""
    # 各智能体的输出
    agent_outputs: dict[str, str]

    # 协调结果
    coordinator_decision: str

    # 最终输出
    final_output: str

    # 任务分配
    task_assignments: dict[str, list[str]]
