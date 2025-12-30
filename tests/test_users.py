"""
Тесты для работы с пользователями.
"""
import pytest
from httpx import AsyncClient

from app.core.security import create_access_token
from app.models.user import User


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user):
    """Тест получения информации о текущем пользователе."""
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, test_user):
    """Тест получения списка пользователей."""
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    response = await client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, test_user):
    """Тест получения пользователя по ID."""
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    response = await client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_user.id)


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, test_user):
    """Тест обновления пользователя."""
    token = create_access_token(data={"sub": str(test_user.id), "username": test_user.username})
    response = await client.patch(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_create_user_as_admin(client: AsyncClient, test_admin_user):
    """Тест создания пользователя админом."""
    token = create_access_token(
        data={"sub": str(test_admin_user.id), "username": test_admin_user.username}
    )
    response = await client.post(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "newadminuser",
            "email": "newadmin@example.com",
            "full_name": "New Admin User",
            "password": "newpass123",
        },
    )
    assert response.status_code == 201

