from django.contrib.auth import get_user_model

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
