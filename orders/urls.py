from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<int:subscription_id>/', views.create_order, name='create'),
    path('apply-promo-code/', views.apply_promo_code, name='apply_promo_code'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),
    path('webhook/', views.yookassa_webhook, name='webhook'),
] 