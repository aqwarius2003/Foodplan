import json
import os
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Recipe, RecipeIngredient
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Импортирует рецепты и ингредиенты из JSON-файла'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Путь к JSON-файлу')

    def handle(self, *args, **options):
        file_path = options['json_file']
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Импорт ингредиентов
        ingredient_mapping = {}
        for ingredient_data in data.get('ingredients', []):
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_data['name'],
                defaults={
                    'category': ingredient_data['category'],
                    'unit': ingredient_data['unit'],
                    'is_allergen': ingredient_data['is_allergen'],
                    'allergen_type': ingredient_data['allergen_type']
                }
            )
            ingredient_mapping[ingredient_data['name']] = ingredient
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан ингредиент: {ingredient.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Ингредиент уже существует: {ingredient.name}'))
        
        # Импорт рецептов
        for recipe_data in data.get('recipes', []):
            try:
                # Проверяем, существует ли файл изображения
                image_path = recipe_data['image']
                
                # Создаем или получаем рецепт
                recipe, created = Recipe.objects.get_or_create(
                    title=recipe_data['title'],
                    defaults={
                        'description': recipe_data['description'],
                        'cooking_time': recipe_data['cooking_time'],
                        'calories': recipe_data['calories'],
                        'category': recipe_data['category'],
                        'menu_type': recipe_data['menu_type'],
                        'instructions': recipe_data['instructions'],
                        'image': image_path
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан рецепт: {recipe.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Рецепт уже существует: {recipe.title}'))
                
                # Добавление ингредиентов
                for ingredient_item in recipe_data.get('ingredients', []):
                    ingredient_name = ingredient_item['ingredient_name']
                    
                    # Поиск ингредиента
                    if ingredient_name in ingredient_mapping:
                        ingredient = ingredient_mapping[ingredient_name]
                    else:
                        try:
                            ingredient = Ingredient.objects.get(name=ingredient_name)
                            ingredient_mapping[ingredient_name] = ingredient
                        except Ingredient.DoesNotExist:
                            # Если ингредиент не найден, создаем новый
                            ingredient = Ingredient.objects.create(
                                name=ingredient_name,
                                category='Прочее',
                                unit='г',
                                is_allergen=False
                            )
                            ingredient_mapping[ingredient_name] = ingredient
                            self.stdout.write(self.style.SUCCESS(f'Создан новый ингредиент: {ingredient.name}'))
                    
                    # Создаем связь ингредиента с рецептом
                    RecipeIngredient.objects.get_or_create(
                        recipe=recipe,
                        ingredient=ingredient,
                        defaults={'amount': ingredient_item['amount']}
                    )
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при импорте рецепта {recipe_data["title"]}: {str(e)}'))
                continue
                
        self.stdout.write(self.style.SUCCESS('Импорт завершен!')) 