"""
Тесты для работы с товарами.
"""
import pytest
from httpx import AsyncClient
from decimal import Decimal

from app.core.security import create_access_token
from app.models.user import User


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient):
    """Тест получения списка товаров (публичный endpoint)."""
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, test_user):
    """Тест создания товара."""
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    response = await client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": "99.99",
            "stock": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == "99.99"


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient, test_user):
    """Тест получения товара по ID."""
    # Сначала создаем товар
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    create_response = await client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Product",
            "price": "50.00",
            "stock": 5,
        },
    )
    product_id = create_response.json()["id"]

    # Получаем товар
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, test_user):
    """Тест обновления товара."""
    # Сначала создаем товар
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    create_response = await client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Product",
            "price": "50.00",
            "stock": 5,
        },
    )
    product_id = create_response.json()["id"]

    # Обновляем товар
    response = await client.patch(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"price": "75.00", "stock": 15},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == "75.00"
    assert data["stock"] == 15


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, test_user):
    """Тест удаления товара."""
    # Сначала создаем товар
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    create_response = await client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Product",
            "price": "50.00",
            "stock": 5,
        },
    )
    product_id = create_response.json()["id"]

    # Удаляем товар
    response = await client.delete(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    # Проверяем, что товар удален
    get_response = await client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 404

