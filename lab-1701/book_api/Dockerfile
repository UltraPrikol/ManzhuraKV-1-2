FROM python:3.11-slim as builder

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копирование зависимостей из builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Копирование исходного кода
COPY . .

# Обновление PATH для пользовательских установок
ENV PATH=/root/.local/bin:$PATH

# Настройка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Открытие порта
EXPOSE 8080

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]