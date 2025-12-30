"""
Сервис для работы с товарами.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Сервис для работы с товарами."""

    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_id: UUID) -> Optional[Product]:
        """Получить товар по ID."""
        stmt = select(Product).where(Product.id == product_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_products(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
    ) -> tuple[list[Product], int]:
        """Получить список товаров с пагинацией."""
        # Базовый запрос
        base_query = select(Product)

        # Фильтр по активности
        if is_active is not None:
            base_query = base_query.where(Product.is_active == is_active)

        # Подсчет общего количества
        count_stmt = select(func.count()).select_from(base_query.subquery())
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # Получение списка
        stmt = (
            base_query
            .offset(skip)
            .limit(limit)
            .order_by(Product.created_at.desc())
        )
        result = await db.execute(stmt)
        products = result.scalars().all()
        return list(products), total

    @staticmethod
    async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
        """Создать новый товар."""
        new_product = Product(**product_data.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    @staticmethod
    async def update_product(
        db: AsyncSession,
        product_id: UUID,
        product_data: ProductUpdate,
    ) -> Product:
        """Обновить товар."""
        product = await ProductService.get_product_by_id(db, product_id)
        if not product:
            raise NotFoundError("Товар не найден")

        # Обновление полей
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete_product(db: AsyncSession, product_id: UUID) -> None:
        """Удалить товар."""
        product = await ProductService.get_product_by_id(db, product_id)
        if not product:
            raise NotFoundError("Товар не найден")

        await db.delete(product)
        await db.commit()

