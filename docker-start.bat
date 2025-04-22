@echo off
echo Запуск проекта FoodPlan в Docker...
echo.

echo Создание и запуск контейнеров...
docker-compose up -d

echo.
echo Проект запущен и доступен по адресу http://localhost:8000
echo Для завершения работы используйте команду: docker-compose down
echo.

pause 