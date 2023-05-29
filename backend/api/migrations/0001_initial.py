# Generated by Django 2.2.19 on 2023-05-27 13:31

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный',
                'verbose_name_plural': 'Избранные',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название продукта', max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(help_text='Введите единицы измерения', max_length=50, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, help_text='Введите количество продукта', validators=[django.core.validators.MinValueValidator(1, message='Минимальное время приготовления 1 минута')], verbose_name='Количество продукта')),
            ],
            options={
                'verbose_name': 'Продукты в рецепте',
                'verbose_name_plural': 'Продукты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Выберите изображение рецепта', upload_to='recipes/image/', verbose_name='Изображение')),
                ('text', models.TextField(help_text='Введите описания рецепта', verbose_name='Описание рецепта')),
                ('cooking_time', models.IntegerField(help_text='Введите время приготовления', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Добавить дату создания', verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название тега', max_length=200, unique=True, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', help_text='Введите цвет тега', image_field=None, max_length=18, samples=None, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Введите текстовый идентификатор тега', unique=True, verbose_name='Текстовый идентификатор тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, to='api.Recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(help_text='Выберите теги рецепта', on_delete=django.db.models.deletion.CASCADE, to='api.Tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Теги рецепта',
                'verbose_name_plural': 'Теги рецепта',
            },
        ),
    ]
