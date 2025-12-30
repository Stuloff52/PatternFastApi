"""
API endpoints для работы с пользователями.
"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user, get_current_superuser
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Annotated[AsyncSession, Depends(get_db)] = None,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
) -> list[UserResponse]:
    """
    Получить список пользователей (требует аутентификации).
    """
    users, total = await UserService.get_users(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Получить информацию о текущем пользователе.
    """
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Получить пользователя по ID.
    """
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserResponse.model_validate(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_superuser)],
) -> UserResponse:
    """
    Создать нового пользователя (только для админов).
    """
    user = await UserService.create_user(db, user_data)
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Обновить пользователя.
    """
    user = await UserService.update_user(db, user_id, user_data, current_user)
    return UserResponse.model_validate(user)


@router.patch("/{user_id}/password", response_model=UserResponse)
async def update_user_password(
    user_id: UUID,
    password_data: UserPasswordUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    """
    Обновить пароль пользователя.
    """
    user = await UserService.update_user_password(db, user_id, password_data, current_user)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_superuser)],
) -> None:
    """
    Удалить пользователя (только для админов).
    """
    await UserService.delete_user(db, user_id, current_user)

