"""
Модели базы данных.
"""
from app.models.base import BaseModel
from app.models.product import Product
from app.models.user import User, UserRole

__all__ = ["BaseModel", "User", "UserRole", "Product"]

