"""提示词模块."""

from .system_prompts import CODE_REVIEW, COORDINATOR_SYSTEM, GENERAL_ASSISTANT, RAG_SYSTEM, PromptTemplate, get_prompt

__all__ = [
    "PromptTemplate",
    "GENERAL_ASSISTANT",
    "RAG_SYSTEM",
    "CODE_REVIEW",
    "COORDINATOR_SYSTEM",
    "get_prompt",
]
