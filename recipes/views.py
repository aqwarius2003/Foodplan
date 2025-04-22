from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Menu


def home(request):
    """Домашняя страница."""
    menu_types = {
        'classic': 'Классическое',
        'low_carb': 'Низкоуглеводное',
        'vegetarian': 'Вегетарианское',
        'keto': 'Кето',
    }
    
    context = {
        'menu_types': menu_types
    }
    return render(request, 'recipes/home.html', context)


def recipe_list(request):
    """Список всех рецептов с возможностью фильтрации."""
    recipes = Recipe.objects.all()
    
    # Фильтрация по типу меню
    menu_type = request.GET.get('menu_type')
    if menu_type:
        recipes = recipes.filter(menu_type=menu_type)
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        recipes = recipes.filter(category=category)
    
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, recipe_id):
    """Детальная информация о рецепте."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    context = {
        'recipe': recipe,
    }
    return render(request, 'recipes/recipe_detail.html', context)


def menu_by_type(request, menu_type):
    """Меню определенного типа."""
    # Проверяем доступ пользователя к данному типу меню
    has_access = False
    subscription_info = None
    
    if request.user.is_authenticated:
        # Проверяем, есть ли у пользователя активная подписка на данный тип меню
        user_subscriptions = request.user.subscriptions.filter(
            is_active=True, 
            menu_type=menu_type
        )
        
        if user_subscriptions.exists():
            has_access = True
            subscription_info = user_subscriptions.first()
    
    # Получаем меню указанного типа
    menu = Menu.objects.filter(menu_type=menu_type).order_by('-week_number').first()
    
    if not menu:
        # Если меню не найдено, покажем все рецепты данного типа
        recipes = Recipe.objects.filter(menu_type=menu_type)
    else:
        recipes = menu.recipes.all()
    
    # Если у пользователя нет доступа, показываем ограниченное количество рецептов
    if not has_access and not request.user.is_staff:
        recipes = recipes[:3]  # Показываем только 3 рецепта как демо
    
    context = {
        'menu': menu,
        'recipes': recipes,
        'menu_type': menu_type,
        'menu_type_display': dict(Recipe.MENU_TYPE_CHOICES)[menu_type],
        'has_access': has_access,
        'subscription_info': subscription_info,
        'is_demo': not has_access and not request.user.is_staff,
    }
    
    return render(request, 'recipes/menu_by_type.html', context)


def privacy_policy(request):
    """Страница политики конфиденциальности."""
    return render(request, 'recipes/privacy_policy.html')


def terms_of_use(request):
    """Страница пользовательского соглашения."""
    return render(request, 'recipes/terms_of_use.html') 