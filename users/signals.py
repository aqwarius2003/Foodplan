from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания профиля при создании пользователя
    """
    # В будущем здесь может быть дополнительная логика
    pass 