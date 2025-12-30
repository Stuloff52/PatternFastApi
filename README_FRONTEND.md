# 🚀 Быстрый старт - Запуск всего одной командой

## Автоматический запуск всех сервисов

```bash
docker-compose up -d --build
```

Эта команда запустит:
- ✅ PostgreSQL (порт 5432)
- ✅ Redis (порт 6379)
- ✅ FastAPI Backend (порт 8000)
- ✅ React Frontend (порт 3000)
- ✅ Prometheus (порт 9090)
- ✅ Grafana (порт 3001)
- ✅ Loki (порт 3100)

## 📍 Доступные URL после запуска:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🔧 Управление:

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Пересборка и запуск
docker-compose up -d --build

# Остановка с удалением volumes
docker-compose down -v
```

## ⚠️ Первый запуск:

При первом запуске нужно применить миграции:

```bash
docker-compose exec app .venv/bin/python -m alembic upgrade head
```

Или если запускаете локально:
```bash
uv run alembic upgrade head
```

