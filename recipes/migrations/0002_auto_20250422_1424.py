# Generated by Django 3.2.20 on 2025-04-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_type',
            field=models.CharField(choices=[('classic', 'Классическое'), ('low_carb', 'Низкоуглеводное'), ('vegetarian', 'Вегетарианское'), ('keto', 'Кето'), ('vegan', 'Веганское')], max_length=50, verbose_name='Тип меню'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='menu_type',
            field=models.CharField(choices=[('classic', 'Классическое'), ('low_carb', 'Низкоуглеводное'), ('vegetarian', 'Вегетарианское'), ('keto', 'Кето'), ('vegan', 'Веганское')], max_length=50, verbose_name='Тип меню'),
        ),
    ]
