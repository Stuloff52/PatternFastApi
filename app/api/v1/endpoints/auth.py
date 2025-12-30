"""
API endpoints для аутентификации.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, RegisterRequest, RefreshTokenRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """
    Регистрация нового пользователя.
    """
    user = await AuthService.register(db, user_data)
    # После регистрации создаем токены
    from app.core.security import create_access_token, create_refresh_token
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "username": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """
    Вход пользователя и получение JWT токенов.
    """
    return await AuthService.login(db, login_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: RefreshTokenRequest,
) -> Token:
    """
    Обновление access токена через refresh токен.
    """
    return await AuthService.refresh_token(token_data.refresh_token)


@router.post("/logout")
async def logout():
    """
    Выход пользователя (в будущем можно добавить blacklist токенов).
    """
    return {"message": "Успешный выход"}

