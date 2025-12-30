"""
Настройка логирования через structlog.
"""
import logging
import sys

import structlog
from structlog.types import Processor

from app.config import settings


def setup_logging() -> None:
    """
    Настройка структурированного логирования.
    """
    # Процессоры для structlog
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Формат вывода: JSON для продакшена, консоль для разработки
    if settings.LOG_FORMAT == "json" or settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(
            structlog.dev.ConsoleRenderer(colors=True)
        )

    # Конфигурация structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Настройка стандартного логирования
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )

    # Уменьшение уровня логирования для некоторых библиотек
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str = None):
    """
    Получить настроенный логгер.
    """
    return structlog.get_logger(name)

