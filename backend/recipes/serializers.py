from rest_framework import serializers
from recipes.models import Ingredients, Tag, Recipe
from django.contrib.auth import get_user_model


User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('name', 'quantity', 'measurement_units')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)
    tags = TagSerializer(many=True)
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'image', 'text',
            'ingredients', 'tags', 'cooking_time') 
