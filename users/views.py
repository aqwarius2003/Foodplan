from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    # Фильтрация активных подписок пользователя
    active_subscriptions = request.user.subscriptions.filter(
        is_active=True,
        end_date__gte=timezone.now().date()
    )

    context = {
        'form': form,
        'active_subscriptions': active_subscriptions,
    }
    return render(request, 'users/profile.html', context) 