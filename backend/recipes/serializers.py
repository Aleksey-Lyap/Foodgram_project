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

class TagRecipeSerializer(serializers.PrimaryKeyRelatedField,serializers.ModelSerializer):
    class Meta:
        model = TagRecipe
        fields = ('tag', 'recipe')


class IngredientsRecipeSerializer(serializers.PrimaryKeyRelatedField,serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all(), write_only=True )
    quantity =  serializers.IntegerField()
    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'quantity')



class DetailRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields =('id', 'tags', 'author', 'ingredients',
                 'name', 'image', 'text', 'is_favorited',
                 'is_in_shopping_cart', 'cooking_time')
        
    def get_author(self, obj):
        if obj.author is not None:
            return { "email": obj.author.email,
                     "id": obj.author.id,
                     "username": obj.author.username,
                     "first_name": obj.author.first_name,
                     "last_name": obj.author.last_name,
                     "is_subscribed":Follow.objects.filter(user_id = self.context['request'].user.id, author_id = obj.author.id).exists()
            }
        return None

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


class ListRecipeSerializer(DetailRecipeSerializer):
    
    class Meta:
        model = Recipe
        fields =('id', 'tags', 'author', 'ingredients',
                 'name', 'image', 'text', 'is_favorited',
                 'is_in_shopping_cart', 'cooking_time')
       

class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
   # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    ingredients = IngredientsRecipeSerializer(many = True)
    tags = TagRecipeSerializer(queryset = TagRecipe.objects.all(), many = True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'quantity', 'tags', 'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags_data:
            TagRecipe.objects.create(recipe=recipe, tag=tag)
        self.create_ingredients(
            ingredients_data=ingredients_data, recipe=recipe)
        return recipe
    
    def update(self, instance, validated_data):
        instance.ingredients = validated_data.get("ingredients", instance.ingredients)
        instance.tags = validated_data.get("tags", instance.tags)
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get("cooking_time", instance.cooking_time)
        instance.save()
        return instance
