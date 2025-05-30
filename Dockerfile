# Dockerfile для Django
FROM python:3.12

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
