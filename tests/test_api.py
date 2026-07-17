"""
API 端点测试
"""

import pytest
from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


class TestHealth:
    """健康检查测试"""

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestWorkflow:
    """工作流 API 测试"""

    def test_run_workflow(self):
        response = client.post(
            "/workflow/run",
            json={"query": "什么是Python？"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "thread_id" in data

    def test_run_workflow_with_thread_id(self):
        response = client.post(
            "/workflow/run",
            json={"query": "你好", "thread_id": "test-thread-123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["thread_id"] == "test-thread-123"

    def test_run_workflow_empty_query(self):
        response = client.post(
            "/workflow/run",
            json={"query": ""},
        )
        assert response.status_code == 422  # Pydantic 验证失败
