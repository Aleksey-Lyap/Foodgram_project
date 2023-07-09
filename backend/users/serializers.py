from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.serializers import RecipeSubFavorCartSerializer
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        print(obj)
        return obj.following.filter(user_id=self.context['request'].user.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['user'].check_password(value):
            raise serializers.ValidationError(
                'Cтарый пароль был введен неправильно')
        return value

    def validate_new_password(self, value):
        print(value)
        validate_password(value)
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'recipes_count', 'recipes')

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        return obj.following.filter(user=request_user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        limit = request.GET.get('recipes_limit')
        print('gdbnt', {limit})
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSubFavorCartSerializer(
            recipes, many=True, context={'request': request})
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
