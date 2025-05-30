# Generated by Django 3.2.20 on 2025-04-21 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Код')),
                ('discount_percent', models.PositiveSmallIntegerField(verbose_name='Процент скидки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('valid_from', models.DateTimeField(verbose_name='Действует с')),
                ('valid_to', models.DateTimeField(verbose_name='Действует до')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('pending', 'Ожидает оплаты'), ('paid', 'Оплачен'), ('canceled', 'Отменен'), ('refunded', 'Возврат средств')], default='pending', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ID платежа')),
                ('promo_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.promocode')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
