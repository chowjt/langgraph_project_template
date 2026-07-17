"""
LLM 模型初始化与管理
支持多模型切换、重试策略、Fallback
"""

from functools import lru_cache

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.config import settings
from src.utils import logger


@lru_cache()
def get_llm(
    model: str | None = None,
    temperature: float | None = None,
    streaming: bool = False,
) -> BaseChatModel:
    """
    获取 LLM 实例（带缓存）

    Args:
        model: 模型名称，默认从配置读取
        temperature: 温度参数
        streaming: 是否启用流式输出

    Returns:
        配置好的 ChatModel 实例
    """
    model_name = model or settings.openai_model
    temp = temperature if temperature is not None else settings.openai_temperature

    logger.info(f"初始化 LLM: model={model_name}, temperature={temp}, streaming={streaming}")

    llm = ChatOpenAI(
        model=model_name,
        temperature=temp,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        max_tokens=settings.openai_max_tokens,
        timeout=settings.openai_timeout,
        streaming=streaming,
        # 自动重试配置（由 tenacity 底层支持）
        max_retries=settings.retry_max_attempts,
    )

    return llm


def get_fast_llm() -> BaseChatModel:
    """获取快速/低成本模型（用于简单任务）"""
    return get_llm(model="gpt-4o-mini", temperature=0.3)


def get_creative_llm() -> BaseChatModel:
    """获取创意型模型（用于生成任务）"""
    return get_llm(model="gpt-4o", temperature=0.9)
