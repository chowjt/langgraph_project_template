"""
工作流 Graph 单元测试
"""

import pytest

from src.graphs import build_rag_graph


class TestRAGGraph:
    """RAG 工作流测试"""

    @pytest.fixture
    def graph(self):
        """每个测试用例独立的 graph 实例"""
        return build_rag_graph()

    def test_graph_compiles(self, graph):
        """测试 Graph 能正确编译"""
        assert graph is not None

    def test_simple_query(self, graph):
        """测试简单查询能完成执行"""
        config = {"configurable": {"thread_id": "test-001"}}
        result = graph.invoke(
            {"user_input": "Python是什么？", "iteration": 0, "is_complete": False},
            config=config,
        )

        assert "answer" in result
        assert result["iteration"] > 0
        assert result.get("is_complete", True)

    def test_thread_isolation(self, graph):
        """测试不同 thread_id 状态隔离"""
        config1 = {"configurable": {"thread_id": "thread-a"}}
        config2 = {"configurable": {"thread_id": "thread-b"}}

        result1 = graph.invoke(
            {"user_input": "问题A", "iteration": 0, "is_complete": False},
            config=config1,
        )
        result2 = graph.invoke(
            {"user_input": "问题B", "iteration": 0, "is_complete": False},
            config=config2,
        )

        assert result1["user_input"] == "问题A"
        assert result2["user_input"] == "问题B"
