# Generated by Django 4.2.1 on 2023-07-13 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipe_create_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='amount',
            field=models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления'),
        ),
    ]
