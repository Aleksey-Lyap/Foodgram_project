from rest_framework import serializers
from recipes.models import Ingredients, Tag, Recipe, IngredientsRecipe, TagRecipe, Favorite, Cart
from users.models import User, Follow


class IngredientsSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('name', 'measurement_unit')

class TagSerializer(serializers.PrimaryKeyRelatedField,serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color')



class DetailRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    

    class Meta:
        model = Recipe
        fields =('id', 'tags', 'author', 'ingredients',
            
                 'name', 'image', 'text', 'is_favorited', 'is_in_shopping_cart', 'cooking_time')
        
    def get_author(self, obj):
        return { "email": obj.author.email,
                 "id": obj.author.id,
                 "username": obj.author.username,
                 "first_name": obj.author.first_name,
                 "last_name": obj.author.last_name,
                 "is_subscribed": Follow.objects.filter(user_id = self.context['request'].user.id, author_id = obj.author.id).exists()
        }

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(recipe_id=obj.id).exists()
    
    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(recipe_id=obj.id).exists()

        
    def get_ingredients(self, obj):
        ingredients_recipe = IngredientsRecipe.objects.filter(recipe_id=obj.id)
        
        return [
           {    "id": ingredient_recipe.ingredients.id,
                "name": ingredient_recipe.ingredients.name,
                "amount": ingredient_recipe.quantity,
                "measurement_unit": ingredient_recipe.ingredients.measurement_unit,
            }
            for ingredient_recipe in ingredients_recipe
        ]

    def get_tags(self, obj):
        tags_recipe = TagRecipe.objects.filter(recipe_id=obj.id)
        return [
           {"id": tag_recipe.tag.id, "name": tag_recipe.tag.name, "color": tag_recipe.tag.color} for tag_recipe in tags_recipe
        ]


class ListRecipeSerializer(serializers.ModelSerializer):
    results = DetailRecipeSerializer(many=True )
    class Meta:
        model = Recipe
        fields = ('results',)
