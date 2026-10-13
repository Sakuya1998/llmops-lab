"""模型登记 API 的接口契约测试。"""

from fastapi.testclient import TestClient

from model_ops_api.main import app, _models

client = TestClient(app)


def setup_function() -> None:
    """每个测试执行前清空内存数据，避免测试之间相互影响。"""
    _models.clear()


def test_health_returns_ok() -> None:
    """健康检查接口应返回正常状态。"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_model() -> None:
    """登记模型后，应能在列表接口中查询到。"""
    payload = {
        "name": "demo-model",
        "provider": "vllm",
        "endpoint": "http://localhost:8001",
        "description": "本地学习模型",
    }

    created = client.post("/api/v1/models", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == payload["name"]
    assert body["provider"] == payload["provider"]
    assert "id" in body
    assert "created_at" in body

    listed = client.get("/api/v1/models")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["id"] == body["id"]


def test_get_missing_model_returns_404() -> None:
    """查询不存在的模型时应返回 404。"""
    response = client.get("/api/v1/models/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 404
    assert response.json()["detail"] == "未找到该模型"


def test_invalid_provider_is_rejected() -> None:
    """provider 不在允许范围内时应返回 422。"""
    response = client.post(
        "/api/v1/models",
        json={"name": "demo", "provider": "unknown-provider"},
    )
    assert response.status_code == 422


def test_blank_name_is_rejected() -> None:
    """模型名称为空时应返回 422。"""
    response = client.post("/api/v1/models", json={"name": ""})
    assert response.status_code == 422
