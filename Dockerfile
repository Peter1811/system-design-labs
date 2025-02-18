# Используем официальный образ FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение внутрь контейнера
COPY ./app /app