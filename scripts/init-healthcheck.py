from django.core.management.base import BaseCommand
from django.urls import path
from django.http import JsonResponse
from django.utils import timezone
import os

def health_check(request):
    """
    Простой эндпоинт для проверки работоспособности приложения.
    Возвращает 200 OK, если приложение работает нормально.
    """
    status = {
        "status": "ok",
        "timestamp": timezone.now().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "production"),
    }
    return JsonResponse(status)

class Command(BaseCommand):
    help = 'Создание эндпоинта для проверки здоровья приложения'

    def handle(self, *args, **options):
        from django.conf import settings
        from django.urls import include, path

        # Добавление URL-шаблона для проверки здоровья в urlpatterns
        # Примечание: Это изменение выполняется динамически при запуске
        # и не изменяет исходный файл urls.py
        
        if not any('/health/' in pattern.pattern.regex.pattern for pattern in settings.ROOT_URLCONF.urlpatterns):
            self.stdout.write('Добавление эндпоинта /health/ для проверки работоспособности...')
            settings.ROOT_URLCONF.urlpatterns += [
                path('health/', health_check, name='health_check'),
            ]
            self.stdout.write(self.style.SUCCESS('Эндпоинт /health/ успешно добавлен!'))
        else:
            self.stdout.write('Эндпоинт /health/ уже существует.') 