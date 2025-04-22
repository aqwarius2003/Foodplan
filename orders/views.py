import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone

import yookassa
from yookassa import Configuration, Payment

from .models import Order, PromoCode
from subscriptions.models import Subscription


# Инициализация API ЮКасса
if settings.YOOKASSA_SHOP_ID and settings.YOOKASSA_SECRET_KEY:
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


@login_required
def create_order(request, subscription_id):
    """Создание заказа для подписки."""
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    
    # Проверяем, есть ли уже заказ для этой подписки
    existing_order = Order.objects.filter(
        subscription=subscription,
        status='pending'
    ).first()
    
    if existing_order:
        order = existing_order
    else:
        order = Order(
            user=request.user,
            subscription=subscription
        )
        order.save()
    
    context = {
        'order': order,
    }
    return render(request, 'orders/create.html', context)


@login_required
@require_POST
def apply_promo_code(request):
    """Применение промокода к заказу."""
    code = request.POST.get('code')
    order_id = request.POST.get('order_id')
    
    if not code or not order_id:
        return JsonResponse({'success': False, 'error': 'Не указан промокод или ID заказа'})
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Заказ не найден'})
    
    try:
        promo_code = PromoCode.objects.get(
            code=code,
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        )
    except PromoCode.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Промокод недействителен'})
    
    # Применяем промокод к заказу
    order.promo_code = promo_code
    # Пересчитываем сумму заказа
    order.amount = order.calculate_amount()
    order.save()
    
    return JsonResponse({
        'success': True,
        'discount': promo_code.discount_percent,
        'new_amount': order.amount
    })


@login_required
def payment(request, order_id):
    """Инициализация платежа через ЮКасса."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        return redirect('users:profile')
    
    if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
        # Для разработки, когда ЮКасса не настроена
        return render(request, 'orders/payment_demo.html', {'order': order})
    
    # Создание платежа в ЮКасса
    payment_data = {
        'amount': {
            'value': str(order.amount),
            'currency': 'RUB'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': request.build_absolute_uri(f'/orders/payment-success/{order.id}/')
        },
        'capture': True,
        'description': f'Оплата подписки FoodPlan #{order.id}',
        'metadata': {
            'order_id': order.id
        }
    }
    
    try:
        payment = Payment.create(payment_data)
        
        # Сохраняем ID платежа
        order.payment_id = payment.id
        order.save()
        
        # Редирект на страницу оплаты
        return redirect(payment.confirmation.confirmation_url)
    except Exception as e:
        print(f"Ошибка создания платежа: {e}")
        return render(request, 'orders/payment_error.html', {'error': str(e)})


@login_required
def payment_success(request, order_id):
    """Обработка успешной оплаты."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending' and order.payment_id:
        # Проверка статуса платежа в ЮКасса
        try:
            if settings.YOOKASSA_SHOP_ID and settings.YOOKASSA_SECRET_KEY:
                payment = Payment.find_one(order.payment_id)
                if payment.status == 'succeeded':
                    order.status = 'paid'
                    order.save()
                    
                    # Активируем подписку
                    subscription = order.subscription
                    subscription.is_active = True
                    subscription.save()
        except Exception as e:
            print(f"Ошибка при проверке платежа: {e}")
    
    context = {
        'order': order,
    }
    return render(request, 'orders/payment_success.html', context)


@login_required
def payment_cancel(request, order_id):
    """Обработка отмены платежа."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/payment_cancel.html', context)


@csrf_exempt
@require_POST
def yookassa_webhook(request):
    """Обработка вебхуков от ЮКасса."""
    if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
        return HttpResponse(status=200)
    
    try:
        event_json = yookassa.Webhook.get_event(request.body)
        
        if event_json['event'] == 'payment.succeeded':
            # Платеж успешно совершен
            payment_id = event_json['object']['id']
            
            try:
                order = Order.objects.get(payment_id=payment_id)
                order.status = 'paid'
                order.save()
                
                # Активируем подписку
                subscription = order.subscription
                subscription.is_active = True
                subscription.save()
            except Order.DoesNotExist:
                print(f"Заказ для платежа {payment_id} не найден")
        
        elif event_json['event'] == 'payment.canceled':
            # Платеж отменен
            payment_id = event_json['object']['id']
            
            try:
                order = Order.objects.get(payment_id=payment_id)
                order.status = 'canceled'
                order.save()
            except Order.DoesNotExist:
                print(f"Заказ для платежа {payment_id} не найден")
    
    except Exception as e:
        print(f"Ошибка обработки вебхука: {e}")
    
    return HttpResponse(status=200) 