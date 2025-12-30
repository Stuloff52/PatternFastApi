"""
Сервис аутентификации.
"""
from datetime import timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, AlreadyExistsError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.config import settings


class AuthService:
    """Сервис для работы с аутентификацией."""

    @staticmethod
    async def register(
        db: AsyncSession,
        user_data: RegisterRequest,
    ) -> User:
        """
        Регистрация нового пользователя.
        """
        # Проверка существования username
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise AlreadyExistsError("Пользователь с таким username уже существует")

        # Проверка существования email
        stmt = select(User).where(User.email == user_data.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise AlreadyExistsError("Пользователь с таким email уже существует")

        # Создание нового пользователя
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def authenticate(
        db: AsyncSession,
        login_data: LoginRequest,
    ) -> Optional[User]:
        """
        Аутентификация пользователя.
        """
        stmt = select(User).where(User.username == login_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        if not verify_password(login_data.password, user.hashed_password):
            return None

        if not user.is_active:
            raise AuthenticationError("Пользователь деактивирован")

        return user

    @staticmethod
    async def login(
        db: AsyncSession,
        login_data: LoginRequest,
    ) -> Token:
        """
        Вход пользователя и получение токенов.
        """
        user = await AuthService.authenticate(db, login_data)
        if not user:
            raise AuthenticationError("Неверный username или пароль")

        # Создание токенов
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "username": user.username}
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @staticmethod
    async def refresh_token(refresh_token: str) -> Token:
        """
        Обновление access токена через refresh токен.
        """
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Неверный refresh токен")

        user_id = payload.get("sub")
        username = payload.get("username")
        if not user_id or not username:
            raise AuthenticationError("Неверный формат токена")

        # Создание новых токенов
        access_token = create_access_token(
            data={"sub": user_id, "username": username}
        )
        new_refresh_token = create_refresh_token(
            data={"sub": user_id, "username": username}
        )

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

    @staticmethod
    async def get_current_user(
        db: AsyncSession,
        token: str,
    ) -> User:
        """
        Получение текущего пользователя по токену.
        """
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            raise AuthenticationError("Неверный токен")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Неверный формат токена")

        stmt = select(User).where(User.id == UUID(user_id))
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise AuthenticationError("Пользователь не найден")

        if not user.is_active:
            raise AuthenticationError("Пользователь деактивирован")

        return user

