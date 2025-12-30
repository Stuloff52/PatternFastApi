FROM python:3.13-slim

WORKDIR /app

# Установка uv
RUN pip install uv

# Копирование файлов зависимостей (включая README.md для сборки пакета)
COPY pyproject.toml uv.lock* README.md ./

# Установка зависимостей
RUN uv sync --frozen

# Копирование кода приложения
COPY . .

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Порт приложения
EXPOSE 8000

# Команда запуска (используем явный путь к Python из venv)
CMD [".venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

