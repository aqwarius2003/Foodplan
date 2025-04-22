@echo off
echo Запуск проекта FoodPlan...
echo.

if not exist venv (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate

echo Установка зависимостей...
pip install -r requirements.txt

echo Применение миграций...
python manage.py migrate

echo Запуск сервера...
python manage.py runserver

pause 