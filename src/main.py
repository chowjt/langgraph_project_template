"""
项目入口 - 支持 CLI 和 API 两种运行模式
"""

import argparse
import asyncio
import sys
from typing import Any

from src.config import settings
from src.graphs import rag_app
from src.utils import logger


def run_cli(query: str) -> dict[str, Any]:
    """命令行模式运行工作流"""
    logger.info(f"CLI 模式 | 输入: {query}")

    # 配置（thread_id 用于状态持久化）
    config = {"configurable": {"thread_id": "cli-session-001"}}

    # 运行工作流
    result = rag_app.invoke(
        {"user_input": query, "iteration": 0, "is_complete": False},
        config=config,
    )

    # 输出结果
    print("\n" + "=" * 50)
    print("📋 工作流执行结果")
    print("=" * 50)
    print(f"📝 回答: {result.get('answer', 'N/A')}")
    print(f"🎯 置信度: {result.get('confidence', 'N/A')}")
    print(f"🔄 迭代次数: {result.get('iteration', 0)}")
    print(f"📍 最终步骤: {result.get('current_step', 'N/A')}")

    if result.get("error"):
        print(f"❌ 错误: {result['error']}")

    print("=" * 50)

    return result


async def run_stream(query: str) -> None:
    """流式输出模式"""
    logger.info(f"流式模式 | 输入: {query}")

    config = {"configurable": {"thread_id": "stream-session-001"}}

    print("\n🤖 ", end="", flush=True)
    async for chunk in rag_app.astream(
        {"user_input": query, "iteration": 0, "is_complete": False},
        config=config,
    ):
        if "generate" in chunk:
            msg = chunk["generate"].get("messages", [])
            if msg:
                print(msg[-1].content, end="", flush=True)
    print("\n")


def main() -> int:
    """主入口"""
    parser = argparse.ArgumentParser(description="LangGraph 工作流 CLI")
    parser.add_argument(
        "query",
        nargs="?",
        default="什么是LangGraph？",
        help="用户查询（默认: 什么是LangGraph？）",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="启用流式输出",
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="环境变量文件路径（默认: .env）",
    )

    args = parser.parse_args()

    # 打印环境信息
    logger.info(f"环境: {settings.app_env}")
    logger.info(f"模型: {settings.openai_model}")
    logger.info(f"检查点: {settings.checkpointer_type}")

    try:
        if args.stream:
            asyncio.run(run_stream(args.query))
        else:
            run_cli(args.query)
        return 0
    except KeyboardInterrupt:
        logger.info("用户中断")
        return 130
    except Exception as e:
        logger.error(f"执行失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
