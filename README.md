# PatternFastAPI

Универсальный шаблон FastAPI приложения для интернет-магазина с полной инфраструктурой для продакшена.

## 🚀 Особенности

- **FastAPI** - современный, быстрый веб-фреймворк для Python
- **SQLAlchemy 2.0** - async ORM для работы с базой данных
- **PostgreSQL** - надежная реляционная база данных
- **Redis** - кеширование и сессии
- **JWT аутентификация** - безопасная аутентификация с access/refresh токенами
- **Alembic** - миграции базы данных
- **Pydantic** - валидация данных
- **Prometheus + Grafana** - мониторинг и метрики
- **Loki** - сбор и анализ логов
- **Pytest** - тестирование
- **Docker** - контейнеризация
- **GitHub Actions** - CI/CD pipeline
- **uv** - современный пакетный менеджер Python

## 📋 Требования

- Python 3.13+
- uv (пакетный менеджер)
- Docker и Docker Compose
- PostgreSQL 16+ (через Docker)
- Redis 7+ (через Docker)

## 🛠️ Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd PatternFastApi
```

### 2. Установка uv

```bash
# Windows (PowerShell)
pip install uv

# или через официальный инсталлятор
irm https://astral.sh/uv/install.ps1 | iex
```

### 3. Создание файла .env

Скопируйте `.env.example` в `.env` и настройте переменные окружения:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл, особенно `SECRET_KEY` для продакшена.

### 4. Установка зависимостей

```bash
uv sync
```

### 5. Запуск Docker контейнеров

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (порт 5432)
- Redis (порт 6379)
- Prometheus (порт 9090)
- Grafana (порт 3000)
- Loki (порт 3100)

### 6. Применение миграций

```bash
uv run alembic upgrade head
```

### 7. Запуск приложения

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу: http://localhost:8000

## 📚 API Документация

После запуска приложения доступна интерактивная документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Тестирование

```bash
# Запуск всех тестов
uv run pytest

# Запуск с покрытием кода
uv run pytest --cov=app --cov-report=html

# Запуск конкретного теста
uv run pytest tests/test_auth.py
```

## 🗄️ Миграции базы данных

```bash
# Создание новой миграции
uv run alembic revision --autogenerate -m "Описание миграции"

# Применение миграций
uv run alembic upgrade head

# Откат последней миграции
uv run alembic downgrade -1
```

## 🐳 Docker

### Запуск через Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f app

# Остановка всех сервисов
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

### Сборка Docker образа

```bash
docker build -t ecommerce-api:latest .
```

## 📊 Мониторинг

### Prometheus

- URL: http://localhost:9090
- Метрики приложения: http://localhost:8000/metrics

### Grafana

- URL: http://localhost:3000
- Логин: `admin`
- Пароль: `admin`

Grafana автоматически настроена с:
- Prometheus datasource
- Loki datasource

## 🏗️ Структура проекта

```
PatternFastApi/
├── app/                    # Основное приложение
│   ├── api/               # API роуты
│   ├── core/              # Ядро (безопасность, middleware, monitoring)
│   ├── models/            # SQLAlchemy модели
│   ├── schemas/           # Pydantic схемы
│   ├── services/          # Бизнес-логика
│   ├── config.py          # Конфигурация
│   ├── database.py        # Настройка БД
│   ├── cache.py           # Настройка Redis
│   └── main.py            # Точка входа
├── tests/                 # Тесты
├── migrations/            # Alembic миграции
├── docker/                # Docker конфигурации
├── .github/               # GitHub Actions workflows
├── pyproject.toml         # Зависимости проекта
└── docker-compose.yml     # Docker Compose конфигурация
```

## 🔐 Модели данных

### User (Пользователь)

- `id` - UUID
- `username` - уникальное имя пользователя
- `email` - уникальный email
- `full_name` - полное имя
- `hashed_password` - хешированный пароль
- `role` - роль (user, manager, admin)
- `is_active` - активен ли пользователь
- `is_superuser` - суперпользователь
- `created_at`, `updated_at` - временные метки

### Product (Товар)

- `id` - UUID
- `name` - название товара
- `description` - описание
- `price` - цена (Decimal)
- `stock` - количество на складе
- `is_active` - активен ли товар
- `created_at`, `updated_at` - временные метки

## 🔑 Аутентификация

API использует JWT токены для аутентификации:

1. **Регистрация**: `POST /api/v1/auth/register`
2. **Вход**: `POST /api/v1/auth/login`
3. **Обновление токена**: `POST /api/v1/auth/refresh`
4. **Выход**: `POST /api/v1/auth/logout`

После получения токена, используйте его в заголовке:

```
Authorization: Bearer <access_token>
```

## 🚦 Примеры использования API

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123"
  }'
```

### Вход

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Создание товара

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "name": "Test Product",
    "description": "Test Description",
    "price": "99.99",
    "stock": 10
  }'
```

## 🔧 Разработка

### Линтинг

```bash
uv run ruff check .
uv run ruff format .
```

### Типы

```bash
uv run mypy app
```

## 📝 Лицензия

MIT

## 🤝 Вклад

Pull requests приветствуются! Для больших изменений сначала откройте issue для обсуждения.

## 📧 Контакты

Для вопросов и предложений создавайте issue в репозитории.

