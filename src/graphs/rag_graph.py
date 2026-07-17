"""
RAG（检索增强生成）工作流示例
包含：检索 -> 生成 -> 评估 -> 条件路由
"""

from typing import Any, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from src.config import settings
from src.models import RAGState
from src.models.llm import get_llm
from src.prompts import RAG_SYSTEM
from src.tools import web_search
from src.utils import logger


# === 节点函数 ===

def retrieve_node(state: RAGState) -> dict[str, Any]:
    """检索节点：执行网络搜索获取相关文档"""
    query = state.get("user_input", "")
    logger.info(f"[Retrieve] 查询: {query}")

    results = web_search(query)

    return {
        "retrieved_docs": [{"content": results, "source": "web"}],
        "search_query": query,
        "current_step": "retrieve",
        "iteration": state.get("iteration", 0) + 1,
    }


def generate_node(state: RAGState) -> dict[str, Any]:
    """生成节点：基于检索结果生成回答"""
    docs = state.get("retrieved_docs", [])
    query = state.get("user_input", "")

    # 构建上下文
    context = "\n\n".join([
        f"[来源: {doc.get('source', 'unknown')}]\n{doc.get('content', '')}"
        for doc in docs
    ])

    # 构建消息
    system_msg = SystemMessage(content=RAG_SYSTEM.format(context=context))
    human_msg = HumanMessage(content=query)

    llm = get_llm()
    response = llm.invoke([system_msg, human_msg])

    return {
        "answer": response.content,
        "current_step": "generate",
        "messages": [human_msg, response],
    }


def evaluate_node(state: RAGState) -> dict[str, Any]:
    """评估节点：评估回答质量"""
    answer = state.get("answer", "")

    # 简单启发式评估（实际项目中可用LLM评估）
    if len(answer) < 50:
        confidence = "low"
    elif "不确定" in answer or "不知道" in answer:
        confidence = "low"
    elif len(answer) > 200:
        confidence = "high"
    else:
        confidence = "medium"

    logger.info(f"[Evaluate] 置信度: {confidence}")

    return {
        "confidence": confidence,
        "current_step": "evaluate",
    }


# === 条件路由函数 ===

def route_by_confidence(state: RAGState) -> Literal["generate", "retry", END]:
    """根据置信度决定下一步"""
    confidence = state.get("confidence", "low")
    iteration = state.get("iteration", 0)

    if confidence == "high":
        return END
    elif iteration >= settings.max_iterations:
        logger.warning("达到最大迭代次数，强制结束")
        return END
    elif confidence == "low":
        return "retry"
    else:
        return END


def retry_node(state: RAGState) -> dict[str, Any]:
    """重试节点：优化查询后重新检索"""
    original_query = state.get("user_input", "")
    iteration = state.get("iteration", 0)

    # 使用 LLM 优化查询
    llm = get_llm()
    refine_prompt = f"""原查询: {original_query}
这是第 {iteration} 次尝试。请生成一个更精确的搜索查询，以获得更好的结果。
只输出优化后的查询，不要其他内容。"""

    response = llm.invoke(refine_prompt)
    refined_query = response.content.strip()

    logger.info(f"[Retry] 优化查询: {refined_query}")

    # 重新搜索
    results = web_search(refined_query)

    return {
        "user_input": refined_query,
        "retrieved_docs": [{"content": results, "source": "web"}],
        "current_step": "retry",
    }


# === 构建 Graph ===

def build_rag_graph():
    """构建并返回 RAG 工作流 Graph"""
    workflow = StateGraph(RAGState)

    # 添加节点
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("evaluate", evaluate_node)
    workflow.add_node("retry", retry_node)

    # 设置入口
    workflow.set_entry_point("retrieve")

    # 添加边
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "evaluate")

    # 条件边：根据评估结果路由
    workflow.add_conditional_edges(
        "evaluate",
        route_by_confidence,
        {
            "generate": "generate",
            "retry": "retry",
            END: END,
        }
    )

    workflow.add_edge("retry", "generate")

    # 编译（内存检查点，开发用）
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)

    return app


# 全局实例
rag_app = build_rag_graph()
