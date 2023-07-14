from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.fields import Base64ImageField
from recipes.models import (Cart, Favorite, Ingredient, IngredientsRecipe,
                            Recipe, Tag, TagRecipe)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return obj.following.filter(
            user_id=self.context['request'].user.id
        ).exists()


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
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
        queryset=Ingredient.objects.all(),
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


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsRecipeSerializer(
        many=True,
        source='recipes_ingredients'
    )
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'is_favorited',
                  'is_in_shopping_cart', 'cooking_time')

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            recipe_id=obj.id,
            user=self.context['request'].user).exists()

    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(
            recipe_id=obj.id,
            user=self.context['request'].user).exists()


class CreateUpdateRecipeSerializer(RecipeSerializer):
    ingredients = IngredientsRecipeCreateSerializer(many=True, write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time')

    def validate(self, obj):
        inrgedients_list = [
            item['ingredients'] for item in obj.get('ingredients')
        ]
        unique_ingredients_list = set(inrgedients_list)
        if len(inrgedients_list) != len(unique_ingredients_list):
            raise serializers.ValidationError(
                'Ингредиенты повторяются'
            )
        return obj

    def enumeration(self, recipe, ingredients_data):
        bulk_list = []
        for ingredient in ingredients_data:
            bulk_list.append(
                IngredientsRecipe(
                    recipe=recipe,
                    ingredients=ingredient['ingredients'],
                    amount=ingredient['amount']
                )
            )
        IngredientsRecipe.objects.bulk_create(bulk_list)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        bulk_list = []
        for tag in tags_data:
            bulk_list.append(
                TagRecipe(recipe_id=recipe.id, tag=tag)
            )
        TagRecipe.objects.bulk_create(bulk_list)

        self.enumeration(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        super().update(recipe, validated_data)

        if tags_data:
            recipe.tags.set(tags_data)

        if ingredients_data:
            IngredientsRecipe.objects.filter(recipe=recipe).delete()
            self.enumeration(recipe, ingredients_data)
        return recipe


class RecipeSubFavorCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
