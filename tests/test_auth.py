"""
Тесты для аутентификации.
"""
import pytest
from httpx import AsyncClient

from app.schemas.auth import RegisterRequest


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """Тест регистрации пользователя."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "newpass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, test_user):
    """Тест регистрации с существующим username."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "different@example.com",
            "full_name": "Different User",
            "password": "newpass123",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    """Тест входа пользователя."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user):
    """Тест входа с неверными данными."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, test_user):
    """Тест обновления токена."""
    # Сначала логинимся
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123",
        },
    )
    refresh_token = login_response.json()["refresh_token"]

    # Обновляем токен
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

