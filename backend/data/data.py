import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()


import sys

sys.path.append(r"D:\Dev\foodgram-project-react\backend\recipes")
import json
import pprint

from models import Ingredients

with open('D:/Dev/foodgram-project-react/data/ingredients0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
for ingredient in data:

    # Ingredients.object.create(name=ingredient['fields']['name'], measurement_unit=ingredient['fields']['measurement_unit'])
    print(ingredient['fields']['name'])
    print(ingredient['fields']['measurement_unit'])

