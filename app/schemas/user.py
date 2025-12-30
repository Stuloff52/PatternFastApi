"""
Pydantic схемы для модели User.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес")
    full_name: str = Field(..., min_length=1, max_length=200, description="Полное имя")
    role: UserRole = Field(default=UserRole.USER, description="Роль пользователя")


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    password: str = Field(..., min_length=7, max_length=14, description="Пароль")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация пароля (длина от 7 до 14 символов)."""
        if len(v) < 7 or len(v) > 14:
            raise ValueError("Пароль должен быть от 7 до 14 символов")
        return v


class UserUpdate(BaseModel):
    """Схема для обновления пользователя."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=1, max_length=200)
    role: UserRole | None = None
    is_active: bool | None = None


class UserPasswordUpdate(BaseModel):
    """Схема для обновления пароля."""

    old_password: str = Field(..., min_length=7, max_length=14)
    new_password: str = Field(..., min_length=7, max_length=14)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация нового пароля."""
        if len(v) < 7 or len(v) > 14:
            raise ValueError("Пароль должен быть от 7 до 14 символов")
        return v


class UserResponse(UserBase):
    """Схема ответа с данными пользователя."""

    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """Схема пользователя в БД (с хешированным паролем)."""

    hashed_password: str

