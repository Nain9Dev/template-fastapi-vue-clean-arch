import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_check_endpoint(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["database"] == "connected"


def test_create_and_list_item(client: TestClient):
    payload = {"title": "Test Production Item", "description": "High-assurance testing"}
    create_res = client.post("/api/v1/items", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["title"] == "Test Production Item"
    assert "id" in created

    list_res = client.get("/api/v1/items")
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(i["id"] == created["id"] for i in items)
