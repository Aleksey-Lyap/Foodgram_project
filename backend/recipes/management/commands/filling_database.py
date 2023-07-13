import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options) -> str:
        with open(
            'D:/Dev/foodgram-project-react/backend/data/ingredients0.json',
            'r', encoding='utf-8'
        ) as f:
            data = json.load(f)
            for ingredient in data:
                Ingredient.objects.create(
                    name=ingredient['fields']['name'],
                    measurement_unit=ingredient['fields']['measurement_unit']
                )
        print('Finished')
