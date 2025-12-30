"""
Модуль для мониторинга и метрик Prometheus.
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.requests import Request
from starlette.responses import Response

# Метрики для HTTP запросов
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

# Метрики для базы данных
db_queries_total = Counter(
    "db_queries_total",
    "Total database queries",
    ["operation"],
)

db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds",
    ["operation"],
)

# Метрики для Redis
redis_operations_total = Counter(
    "redis_operations_total",
    "Total Redis operations",
    ["operation"],
)

# Общие метрики приложения
active_connections = Gauge(
    "active_connections",
    "Number of active connections",
)

app_uptime_seconds = Gauge(
    "app_uptime_seconds",
    "Application uptime in seconds",
)


def get_metrics() -> Response:
    """
    Endpoint для получения метрик Prometheus.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

