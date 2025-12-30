"""
Главный файл приложения FastAPI.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import settings
from app.core.exceptions import AppException
from app.core.middleware import MetricsMiddleware, LoggingMiddleware
from app.core.monitoring import get_metrics
from app.database import close_db, init_db
from app.cache import close_redis, init_redis
from app.logging_config import setup_logging, get_logger

# Настройка логирования
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.
    """
    # Startup
    logger.info("Starting application", version=settings.APP_VERSION)
    await init_db()
    await init_redis()
    logger.info("Application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down application")
    await close_db()
    await close_redis()
    logger.info("Application shut down")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Универсальный шаблон FastAPI приложения для интернет-магазина",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(MetricsMiddleware)
app.add_middleware(LoggingMiddleware)
# CORS должен быть первым middleware
from starlette.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Обработка исключений
@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    """Обработчик кастомных исключений."""
    logger.error(
        "Application exception",
        status_code=exc.status_code,
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Обработчик общих исключений."""
    logger.error("Unhandled exception", error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": {"message": str(exc)} if settings.DEBUG else {},
        },
    )


# Подключение роутеров
app.include_router(api_router, prefix="/api/v1")

# Health check и метрики
@app.get("/health")
async def health_check():
    """Проверка здоровья приложения."""
    return {"status": "ok", "version": settings.APP_VERSION}


@app.get("/metrics")
async def metrics():
    """Endpoint для метрик Prometheus."""
    return get_metrics()


@app.get("/")
async def root():
    """Корневой endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }

