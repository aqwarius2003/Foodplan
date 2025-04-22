#!/bin/bash

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate

# Собираем статику
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запускаем сервер
echo "Starting server..."
if [ "$DEBUG" = "True" ]; then
    echo "Running in debug mode..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Running in production mode..."
    gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi 