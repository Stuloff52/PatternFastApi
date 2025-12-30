"""
Сервис для работы с пользователями.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, AlreadyExistsError, AuthorizationError
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate


class UserService:
    """Сервис для работы с пользователями."""

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Получить пользователя по ID."""
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Получить пользователя по username."""
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Получить пользователя по email."""
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[User], int]:
        """Получить список пользователей с пагинацией."""
        # Подсчет общего количества
        count_stmt = select(func.count()).select_from(User)
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # Получение списка
        stmt = select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await db.execute(stmt)
        users = result.scalars().all()
        return list(users), total

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Создать нового пользователя."""
        # Проверка существования username
        existing = await UserService.get_user_by_username(db, user_data.username)
        if existing:
            raise AlreadyExistsError("Пользователь с таким username уже существует")

        # Проверка существования email
        existing = await UserService.get_user_by_email(db, user_data.email)
        if existing:
            raise AlreadyExistsError("Пользователь с таким email уже существует")

        # Создание пользователя
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role=user_data.role,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: UUID,
        user_data: UserUpdate,
        current_user: User,
    ) -> User:
        """Обновить пользователя."""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")

        # Проверка прав: можно обновлять только себя, кроме админов
        if user.id != current_user.id and not current_user.is_superuser:
            raise AuthorizationError("Недостаточно прав для обновления этого пользователя")

        # Проверка уникальности username
        if user_data.username and user_data.username != user.username:
            existing = await UserService.get_user_by_username(db, user_data.username)
            if existing:
                raise AlreadyExistsError("Пользователь с таким username уже существует")

        # Проверка уникальности email
        if user_data.email and user_data.email != user.email:
            existing = await UserService.get_user_by_email(db, user_data.email)
            if existing:
                raise AlreadyExistsError("Пользователь с таким email уже существует")

        # Обновление полей
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user_password(
        db: AsyncSession,
        user_id: UUID,
        password_data: UserPasswordUpdate,
        current_user: User,
    ) -> User:
        """Обновить пароль пользователя."""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")

        # Проверка прав: можно обновлять только свой пароль
        if user.id != current_user.id:
            raise AuthorizationError("Недостаточно прав для обновления пароля")

        # Проверка старого пароля
        if not verify_password(password_data.old_password, user.hashed_password):
            raise AuthorizationError("Неверный старый пароль")

        # Установка нового пароля
        user.hashed_password = get_password_hash(password_data.new_password)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: UUID,
        current_user: User,
    ) -> None:
        """Удалить пользователя."""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")

        # Проверка прав: только админы могут удалять пользователей
        if not current_user.is_superuser:
            raise AuthorizationError("Недостаточно прав для удаления пользователя")

        # Нельзя удалить самого себя
        if user.id == current_user.id:
            raise AuthorizationError("Нельзя удалить самого себя")

        await db.delete(user)
        await db.commit()

