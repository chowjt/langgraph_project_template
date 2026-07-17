"""
网络搜索工具
可替换为 DuckDuckGo、SerpAPI、Tavily 等
"""

from typing import Any

from langchain_community.tools import DuckDuckGoSearchRun

from src.utils import logger


class WebSearchTool:
    """网页搜索工具封装"""

    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    def search(self, query: str, max_results: int = 5) -> list[dict[str, Any]]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        logger.info(f"[WebSearch] 搜索: {query}")
        try:
            result = self.search.run(query)
            # DuckDuckGo 返回字符串，需要解析
            return [{"content": result, "source": "duckduckgo"}]
        except Exception as e:
            logger.error(f"[WebSearch] 搜索失败: {e}")
            return []


def web_search(query: str) -> str:
    """简单的搜索函数（用于 ToolNode）"""
    tool = WebSearchTool()
    results = tool.search(query)
    return "\n".join([r["content"] for r in results])
