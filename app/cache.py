"""
Настройка Redis для кеширования.
"""
from typing import Any, Optional

import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.config import settings

# Глобальный Redis клиент
redis_client: Optional[Redis] = None


async def init_redis() -> Redis:
    """
    Инициализация Redis клиента.
    """
    global redis_client
    redis_client = await aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=50,
    )
    return redis_client


async def get_redis() -> Redis:
    """
    Получение Redis клиента.
    Dependency для FastAPI.
    """
    if redis_client is None:
        await init_redis()
    return redis_client


async def close_redis() -> None:
    """
    Закрытие соединения с Redis.
    """
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


class CacheService:
    """Сервис для работы с кешем."""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Optional[str]:
        """Получить значение из кеша."""
        return await self.redis.get(key)

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600,
    ) -> bool:
        """Установить значение в кеш."""
        if isinstance(value, (dict, list)):
            import json

            value = json.dumps(value)
        return await self.redis.setex(key, expire, value)

    async def delete(self, key: str) -> int:
        """Удалить ключ из кеша."""
        return await self.redis.delete(key)

    async def delete_pattern(self, pattern: str) -> int:
        """Удалить все ключи по паттерну."""
        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0

    async def exists(self, key: str) -> bool:
        """Проверить существование ключа."""
        return await self.redis.exists(key) > 0


async def get_cache_service() -> CacheService:
    """
    Dependency для получения сервиса кеширования.
    """
    redis = await get_redis()
    return CacheService(redis)

