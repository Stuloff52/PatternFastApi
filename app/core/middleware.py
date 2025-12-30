"""
Middleware для приложения: CORS, логирование, метрики.
"""
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.core.monitoring import (
    http_requests_total,
    http_request_duration_seconds,
)
from app.logging_config import get_logger

logger = get_logger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware для сбора метрик Prometheus."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Обработка запроса с сбором метрик."""
        start_time = time.time()
        method = request.method
        endpoint = request.url.path

        response = await call_next(request)

        # Сбор метрик
        duration = time.time() - start_time
        status_code = response.status_code

        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status_code,
        ).inc()

        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint,
        ).observe(duration)

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования запросов."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Обработка запроса с логированием."""
        start_time = time.time()
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "Request started",
            method=method,
            path=path,
            client_ip=client_ip,
        )

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            logger.info(
                "Request completed",
                method=method,
                path=path,
                status_code=response.status_code,
                duration=f"{duration:.3f}s",
            )
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "Request failed",
                method=method,
                path=path,
                error=str(e),
                duration=f"{duration:.3f}s",
                exc_info=True,
            )
            raise



