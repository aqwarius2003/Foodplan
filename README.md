# FoodPlan - Сервис планирования питания

FoodPlan - это веб-сервис, помогающий пользователям планировать питание на неделю. Система предлагает готовые меню с рецептами и автоматически формирует список покупок.

## Функциональные возможности

- Регистрация и авторизация пользователей
- Выбор плана питания из 4 типов меню (Классическое, Низкоуглеводное, Вегетарианское, Кето)
- Подписка на сервис с выбором параметров (срок, приемы пищи, количество персон, аллергены)
- Оплата через ЮКасса (с демо-режимом для разработки)
- Личный кабинет с просмотром активной подписки и меню
- Использование промокодов для получения скидки

## Технологический стек

- Python 3.8+ (проверено на Python 3.11)
- Django 3.2+
- SQLite (для разработки)
- PostgreSQL (опционально, для продакшена)
- Bootstrap 5
- ЮКасса API (в демо-режиме)

## Быстрый запуск проекта

### Windows

1. Запустите `start.bat` для локальной разработки

### Linux/MacOS

1. Запустите `bash start.sh` для локальной разработки

## Ручной запуск проекта для локальной разработки

1. Клонировать репозиторий:
```
git clone <ссылка на репозиторий>
cd Foodplan
```

2. Создать и активировать виртуальное окружение:
```
python -m venv venv
venv\Scripts\activate  # Для Windows
source venv/bin/activate  # Для Linux/Mac
```

3. Установить зависимости:
```
pip install -r requirements.txt
```

4. Применить миграции и запустить сервер:
```
python manage.py migrate
python manage.py createsuperuser  # создание админ-пользователя
python manage.py runserver
```

5. Открыть в браузере: http://127.0.0.1:8000

## Структура проекта

```
foodplan/
├── config/                  # Настройки проекта
├── users/                   # Приложение пользователей
├── subscriptions/           # Приложение подписок
├── recipes/                 # Приложение рецептов
├── orders/                  # Приложение заказов и оплаты
├── templates/               # HTML шаблоны
├── static/                  # CSS, JS, изображения
├── media/                   # Загружаемые файлы
└── manage.py
```

## Тестирование оплаты

Для тестирования используется демо-режим без подключения к ЮКасса API. 
В демо-режиме вы можете использовать кнопки "Оплатить (успешно)" и "Отменить платеж" для симуляции различных сценариев оплаты.

Если вы настроите ключи ЮКасса в `.env` файле, то можете использовать тестовые карты:
- Успешная оплата: `1111 1111 1111 1026`, дата: `12/24`, CVC: `000`
- Неуспешная оплата: `5555 5555 5555 4444`, дата: `12/24`, CVC: `000`

## Лицензия

MIT 

## Подготовка к продакшену

### 1. Экспорт данных из базы данных

#### Экспорт данных

```bash
# Создание JSON-дампа всех данных
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > foodplan_data.json

# Экспорт только рецептов и ингредиентов
python manage.py dumpdata recipes > recipes_data.json
```

#### Экспорт медиафайлов

Скопируйте директории `media` и `static` для переноса изображений:

```bash
# Создание архива с медиафайлами
tar -czf foodplan_media.tar.gz media
```

### 2. Настройка GitHub и Docker

1. Создайте репозиторий на GitHub
2. Добавьте файлы проекта в репозиторий:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

3. Убедитесь, что в репозитории есть все необходимые файлы:
   - `Dockerfile`
   - `docker-compose.yml`
   - `entrypoint.sh`
   - `requirements.txt`
   - `nginx/nginx.conf`
   - `.env.example`

### 3. Деплой на сервер

1. Клонируйте репозиторий на сервер:

```bash
git clone YOUR_GITHUB_REPO_URL
cd foodplan
```

2. Создайте `.env` файл на основе `.env.example`:

```bash
cp .env.example .env
nano .env  # Отредактируйте файл с реальными значениями
```

3. Создайте директорию для Nginx:

```bash
mkdir -p nginx
```

4. Запустите Docker Compose:

```bash
docker-compose up -d
```

### 4. Восстановление данных

1. Загрузите архив с данными на сервер:

```bash
scp foodplan_data.json user@your_server:/path/to/foodplan/
scp foodplan_media.tar.gz user@your_server:/path/to/foodplan/
```

2. Распакуйте медиафайлы:

```bash
tar -xzf foodplan_media.tar.gz
```

3. Загрузите данные в базу:

```bash
docker-compose exec web python manage.py loaddata foodplan_data.json
```

### 5. Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

## Обновление сайта

Для обновления сайта после внесения изменений:

```bash
git pull
docker-compose down
docker-compose up -d --build
```

## Мониторинг и обслуживание

### Просмотр логов

```bash
docker-compose logs -f web
```

### Резервное копирование

Регулярно создавайте резервные копии данных:

```bash
# Резервное копирование базы
docker-compose exec db pg_dump -U postgres foodplan > backup_$(date +%Y%m%d).sql

# Резервное копирование медиафайлов
tar -czf media_backup_$(date +%Y%m%d).tar.gz media
``` 