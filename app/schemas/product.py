"""
Pydantic схемы для модели Product.
"""
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Базовая схема товара."""

    name: str = Field(..., min_length=1, max_length=500, description="Название товара")
    description: str | None = Field(None, description="Описание товара")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Цена товара")
    stock: int = Field(default=0, ge=0, description="Количество на складе")
    is_active: bool = Field(default=True, description="Активен ли товар")


class ProductCreate(ProductBase):
    """Схема для создания товара."""

    pass


class ProductUpdate(BaseModel):
    """Схема для обновления товара."""

    name: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    stock: int | None = Field(None, ge=0)
    is_active: bool | None = None


class ProductResponse(ProductBase):
    """Схема ответа с данными товара."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Схема для списка товаров с пагинацией."""

    items: list[ProductResponse]
    total: int
    page: int
    size: int
    pages: int

