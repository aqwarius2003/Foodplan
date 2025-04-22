#!/bin/bash

echo "Запуск проекта FoodPlan..."
echo

if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Применение миграций..."
python manage.py migrate

echo "Запуск сервера..."
python manage.py runserver 