FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Используем entrypoint для запуска сервера
CMD ["./entrypoint.sh"] 