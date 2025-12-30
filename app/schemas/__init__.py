"""
Pydantic схемы.
"""
from app.schemas.auth import LoginRequest, RegisterRequest, RefreshTokenRequest, Token, TokenData
from app.schemas.product import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate
from app.schemas.user import UserCreate, UserPasswordUpdate, UserResponse, UserUpdate

__all__ = [
    # Auth
    "Token",
    "TokenData",
    "LoginRequest",
    "RegisterRequest",
    "RefreshTokenRequest",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserPasswordUpdate",
    # Product
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductListResponse",
]

