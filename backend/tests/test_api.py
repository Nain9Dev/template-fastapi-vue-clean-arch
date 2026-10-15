import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.infrastructure.db import init_db


@pytest_asyncio.fixture(autouse=True)
async def setup_test_database():
    await init_db()


@pytest.mark.asyncio
async def test_health_check_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_create_and_list_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create item
        payload = {"title": "Test Production Item", "description": "High-assurance testing"}
        create_res = await client.post("/api/v1/items", json=payload)
        assert create_res.status_code == 201
        created = create_res.json()
        assert created["title"] == "Test Production Item"
        assert "id" in created

        # List items
        list_res = await client.get("/api/v1/items")
        assert list_res.status_code == 200
        items = list_res.json()
        assert len(items) >= 1
        assert any(i["id"] == created["id"] for i in items)
