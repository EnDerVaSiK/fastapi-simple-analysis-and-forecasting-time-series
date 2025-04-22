# Бэкенд
FROM python:3.9-slim as backend

# Установка системных зависимостей для Prophet
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY ./backend ./backend
COPY main.py .

# Создание папки для загрузок
RUN mkdir -p /app/uploads

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Фронтенд
FROM node:18-alpine as frontend

WORKDIR /app

# Установка зависимостей Node.js
COPY frontend/package.json frontend/package-lock.json* ./

RUN npm install --silent

# Копирование исходного кода фронтенда
COPY frontend/ ./

# Сборка проекта
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
