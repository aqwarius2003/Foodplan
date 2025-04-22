from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Menu


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu_type', 'category', 'cooking_time', 'calories')
    list_filter = ('menu_type', 'category')
    search_fields = ('title', 'description')
    inlines = [RecipeIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'is_allergen', 'allergen_type')
    list_filter = ('category', 'is_allergen', 'allergen_type')
    search_fields = ('name',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_type', 'week_number')
    list_filter = ('menu_type',)
    filter_horizontal = ('recipes',) 