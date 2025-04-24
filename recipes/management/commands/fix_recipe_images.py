import os
from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Исправляет пути к изображениям рецептов'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        updated = 0
        
        for recipe in recipes:
            old_path = recipe.image.name
            if old_path.startswith('static/img/'):
                # Получаем только имя файла
                filename = os.path.basename(old_path)
                
                # Устанавливаем новый путь
                recipe.image = f'recipes/{filename}'
                recipe.save(update_fields=['image'])
                
                updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Обновлен путь к изображению для рецепта {recipe.title}: {old_path} -> {recipe.image.name}'
                ))
        
        self.stdout.write(self.style.SUCCESS(f'Обновлено {updated} рецептов')) 