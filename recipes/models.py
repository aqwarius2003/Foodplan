from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(_('Название'), max_length=255)
    category = models.CharField(_('Категория'), max_length=100)
    unit = models.CharField(_('Единица измерения'), max_length=50)
    is_allergen = models.BooleanField(_('Аллерген'), default=False)
    
    ALLERGEN_CHOICES = [
        ('fish', 'Рыба и морепродукты'),
        ('meat', 'Мясо'),
        ('grains', 'Зерновые'),
        ('honey', 'Продукты пчеловодства'),
        ('nuts', 'Орехи и бобовые'),
        ('dairy', 'Молочные продукты'),
    ]
    
    allergen_type = models.CharField(
        _('Тип аллергена'),
        max_length=50,
        choices=ALLERGEN_CHOICES,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')


class Recipe(models.Model):
    """Модель рецепта."""
    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'))
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(_('Время приготовления (мин)'))
    calories = models.PositiveIntegerField(_('Калорийность'))
    
    CATEGORY_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('dessert', 'Десерт'),
    ]
    
    category = models.CharField(
        _('Категория'),
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    
    MENU_TYPE_CHOICES = [
        ('classic', 'Классическое'),
        ('low_carb', 'Низкоуглеводное'),
        ('vegetarian', 'Вегетарианское'),
        ('keto', 'Кето'),
        ('vegan', 'Веганское'),
    ]
    
    menu_type = models.CharField(
        _('Тип меню'),
        max_length=50,
        choices=MENU_TYPE_CHOICES
    )
    
    image = models.ImageField(_('Изображение'), upload_to='recipes/')
    instructions = models.TextField(_('Инструкции по приготовлению'))
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')


class RecipeIngredient(models.Model):
    """Связь между рецептом и ингредиентом с указанием количества."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(_('Количество'), max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.ingredient.name} для {self.recipe.title}"
    
    class Meta:
        verbose_name = _('Ингредиент рецепта')
        verbose_name_plural = _('Ингредиенты рецепта')


class Menu(models.Model):
    """Модель меню на неделю."""
    menu_type = models.CharField(
        _('Тип меню'),
        max_length=50,
        choices=Recipe.MENU_TYPE_CHOICES
    )
    week_number = models.PositiveIntegerField(_('Номер недели'))
    recipes = models.ManyToManyField(Recipe, related_name='menus')
    
    def __str__(self):
        return f"{self.get_menu_type_display()} меню на неделю {self.week_number}"
    
    class Meta:
        verbose_name = _('Меню')
        verbose_name_plural = _('Меню') 