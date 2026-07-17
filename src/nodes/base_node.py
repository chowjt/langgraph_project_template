"""
节点基类与工具函数
所有自定义节点应遵循此模式
"""

from abc import ABC, abstractmethod
from typing import Any, Callable

from langchain_core.language_models.chat_models import BaseChatModel

from src.models.llm import get_llm
from src.utils import logger


class BaseNode(ABC):
    """
    工作流节点基类

    子类需实现 __call__ 方法，接收 state 返回更新后的 state
    """

    def __init__(self, llm: BaseChatModel | None = None, name: str = ""):
        self.llm = llm or get_llm()
        self.name = name or self.__class__.__name__

    @abstractmethod
    def __call__(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        执行节点逻辑

        Args:
            state: 当前工作流状态

        Returns:
            状态更新字典（只返回需要修改的字段）
        """
        pass

    def log_step(self, message: str) -> None:
        """记录节点执行日志"""
        logger.info(f"[{self.name}] {message}")


def create_node(
    func: Callable[[dict[str, Any]], dict[str, Any]],
    name: str = "",
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    将普通函数包装为节点（用于简单场景）

    使用示例：
        def my_node(state):
            return {"result": "done"}

        workflow.add_node("my_node", create_node(my_node, "MyNode"))
    """
    node_name = name or func.__name__

    def wrapper(state: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"[{node_name}] 开始执行")
        try:
            result = func(state)
            logger.info(f"[{node_name}] 执行完成")
            return result
        except Exception as e:
            logger.error(f"[{node_name}] 执行失败: {e}")
            return {"error": str(e), "is_complete": True}

    wrapper.__name__ = node_name
    return wrapper
