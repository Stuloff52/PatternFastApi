"""
Pydantic схемы для аутентификации.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    """Схема токена."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Схема данных из токена."""

    user_id: str | None = None
    username: str | None = None


class LoginRequest(BaseModel):
    """Схема для входа."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=7, max_length=14)


class RegisterRequest(BaseModel):
    """Схема для регистрации."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=200)
    password: str = Field(..., min_length=7, max_length=14)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация пароля."""
        if len(v) < 7 or len(v) > 14:
            raise ValueError("Пароль должен быть от 7 до 14 символов")
        return v


class RefreshTokenRequest(BaseModel):
    """Схема для обновления токена."""

    refresh_token: str

