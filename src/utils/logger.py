"""
统一日志配置
支持结构化日志、文件轮转、不同环境级别
"""

import logging
import sys
from pathlib import Path

from src.config import settings


def setup_logger(
    name: str = "langgraph",
    level: str | None = None,
    log_file: str | None = None,
) -> logging.Logger:
    """
    配置并返回一个结构化日志记录器

    Args:
        name: 日志器名称
        level: 日志级别，默认从配置读取
        log_file: 日志文件路径，None 则只输出到控制台

    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    log_level = level or settings.app_log_level
    logger.setLevel(getattr(logging, log_level.upper()))

    # 格式化器
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出（生产环境推荐）
    if log_file or settings.is_production:
        file_path = log_file or "logs/app.log"
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# 全局日志器
logger = setup_logger()
