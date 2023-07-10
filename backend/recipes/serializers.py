import base64

from django.core.files.base import ContentFile
from recipes.models import (Cart, Favorite, Ingredients, IngredientsRecipe,
                            Recipe, Tag, TagRecipe)
from rest_framework import serializers
from users.models import Follow


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientsRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        source='ingredients',
        write_only=True
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'is_favorited',
                  'is_in_shopping_cart', 'cooking_time')

    def get_author(self, obj):
        if obj.author is not None:
            return {"email": obj.author.email,
                    "id": obj.author.id,
                    "username": obj.author.username,
                    "first_name": obj.author.first_name,
                    "last_name": obj.author.last_name,
                    "is_subscribed": Follow.objects.filter(
                        user_id=self.context['request'].user.id,
                        author_id=obj.author.id
                    ).exists()}
        return None

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(recipe_id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(recipe_id=obj.id).exists()

    def get_ingredients(self, obj):
        ingredients_recipe = IngredientsRecipe.objects.filter(recipe_id=obj.id)
        return [
            {"id": ingredient_recipe.ingredients.id,
             "name": ingredient_recipe.ingredients.name,
             "amount": ingredient_recipe.amount,
             "measurement_unit":
             ingredient_recipe.ingredients.measurement_unit}
            for ingredient_recipe in ingredients_recipe
        ]

    def get_tags(self, obj):
        tags_recipe = TagRecipe.objects.filter(recipe_id=obj.id)
        return [
            {"id": tag_recipe.tag.id,
             "name": tag_recipe.tag.name,
             "color": tag_recipe.tag.color}
            for tag_recipe in tags_recipe
        ]


class CreateUpdateRecipeSerializer(RecipeSerializer):
    ingredients = IngredientsRecipeCreateSerializer(many=True, write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags_data:
            TagRecipe.objects.create(recipe_id=recipe.id, tag=tag)
        for ingredient in ingredients_data:
            IngredientsRecipe.objects.create(
                recipe_id=recipe.id,
                amount=ingredient['amount'],
                ingredients=ingredient['ingredients']
            )
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        super().update(recipe, validated_data)

        if tags_data:
            recipe.tags.set(tags_data)

        if ingredients_data:
            IngredientsRecipe.objects.filter(recipe=recipe).delete()
            for ingredient in ingredients_data:
                IngredientsRecipe.objects.create(
                    recipe=recipe,
                    ingredients=ingredient['ingredients'],
                    amount=ingredient['amount'])
        return recipe


class RecipeSubFavorCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
