"""
全局配置管理 - 基于 Pydantic Settings
支持 .env 文件加载，环境变量覆盖
"""

import os
from functools import lru_cache
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用全局配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # === 应用基础配置 ===
    app_env: Literal["development", "staging", "production"] = Field(
        default="development", alias="APP_ENV"
    )
    app_debug: bool = Field(default=False, alias="APP_DEBUG")
    app_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", alias="APP_LOG_LEVEL"
    )

    # === OpenAI 配置 ===
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    openai_base_url: str = Field(
        default="https://api.openai.com/v1", alias="OPENAI_BASE_URL"
    )
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.7, alias="OPENAI_TEMPERATURE")
    openai_max_tokens: Optional[int] = Field(default=None, alias="OPENAI_MAX_TOKENS")
    openai_timeout: int = Field(default=60, alias="OPENAI_TIMEOUT")

    # === LangSmith 可观测性 ===
    langchain_tracing_v2: bool = Field(default=False, alias="LANGCHAIN_TRACING_V2")
    langchain_api_key: Optional[str] = Field(default=None, alias="LANGCHAIN_API_KEY")
    langchain_project: str = Field(default="langgraph-workflow", alias="LANGCHAIN_PROJECT")

    # === 检查点/持久化配置 ===
    checkpointer_type: Literal["memory", "postgres", "sqlite"] = Field(
        default="memory", alias="CHECKPOINTER_TYPE"
    )
    database_uri: Optional[str] = Field(default=None, alias="DATABASE_URI")

    # === 工作流配置 ===
    max_iterations: int = Field(default=10, alias="MAX_ITERATIONS")
    retry_max_attempts: int = Field(default=3, alias="RETRY_MAX_ATTEMPTS")

    @field_validator("openai_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or v.startswith("sk-your"):
            raise ValueError("OPENAI_API_KEY 未设置或使用了占位符值")
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache()
def get_settings() -> Settings:
    """获取全局配置单例（缓存）"""
    return Settings()


# 便捷导出
settings = get_settings()
