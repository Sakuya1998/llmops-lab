"""API contract tests for the starter model registry."""

from fastapi.testclient import TestClient

from model_ops_api.main import app, _models

client = TestClient(app)


def setup_function() -> None:
    _models.clear()


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_model() -> None:
    payload = {
        "name": "demo-model",
        "provider": "vllm",
        "endpoint": "http://localhost:8001",
        "description": "Local learning model",
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
    response = client.get("/api/v1/models/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found"


def test_invalid_provider_is_rejected() -> None:
    response = client.post(
        "/api/v1/models",
        json={"name": "demo", "provider": "unknown-provider"},
    )
    assert response.status_code == 422


def test_blank_name_is_rejected() -> None:
    response = client.post("/api/v1/models", json={"name": ""})
    assert response.status_code == 422
