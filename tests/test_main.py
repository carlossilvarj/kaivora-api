import pytest
from httpx import AsyncClient
from fastapi import status
from main import app  # ou o caminho correto pro seu FastAPI app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        item_data = {"name": "Teste", "description": "Item de teste"}
        response = await ac.post("/api/v1/items", json=item_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Teste"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
