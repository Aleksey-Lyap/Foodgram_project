# Generated by Django 4.2.1 on 2023-06-26 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_ingredients_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания'),
        ),
    ]
