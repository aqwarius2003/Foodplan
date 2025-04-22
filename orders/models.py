from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from subscriptions.models import Subscription


class PromoCode(models.Model):
    """Модель промокода."""
    code = models.CharField(_('Код'), max_length=20, unique=True)
    discount_percent = models.PositiveSmallIntegerField(_('Процент скидки'))
    is_active = models.BooleanField(_('Активен'), default=True)
    valid_from = models.DateTimeField(_('Действует с'))
    valid_to = models.DateTimeField(_('Действует до'))
    
    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"
    
    class Meta:
        verbose_name = _('Промокод')
        verbose_name_plural = _('Промокоды')


class Order(models.Model):
    """Модель заказа."""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('canceled', 'Отменен'),
        ('refunded', 'Возврат средств'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    amount = models.DecimalField(_('Сумма'), max_digits=10, decimal_places=2)
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    payment_id = models.CharField(_('ID платежа'), max_length=255, blank=True, null=True)
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True,
        null=True
    )
    
    def calculate_amount(self):
        """Расчет стоимости заказа."""
        # Базовая цена за тип подписки и продолжительность
        base_prices = {
            1: 1000,  # 1 месяц
            3: 2700,  # 3 месяца (скидка 10%)
            6: 5100,  # 6 месяцев (скидка 15%)
            12: 9600,  # 12 месяцев (скидка 20%)
        }
        
        base_price = base_prices[self.subscription.duration]
        
        # Количество приемов пищи
        meals_count = sum([
            self.subscription.include_breakfast,
            self.subscription.include_lunch,
            self.subscription.include_dinner,
            self.subscription.include_dessert
        ])
        
        # Корректировка цены в зависимости от количества приемов пищи
        if meals_count < 4:
            base_price = base_price * (0.7 + 0.1 * meals_count)
        
        # Корректировка цены в зависимости от количества персон
        person_factor = 1 + (self.subscription.persons_count - 1) * 0.7
        
        amount = base_price * person_factor
        
        # Применение промокода, если есть
        if self.promo_code and self.promo_code.is_active:
            discount = amount * (self.promo_code.discount_percent / 100)
            amount -= discount
        
        return round(amount, 2)
    
    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.calculate_amount()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы') 