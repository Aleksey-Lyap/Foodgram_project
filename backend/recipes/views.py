from django.contrib.auth import get_user_model

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import DetailRecipeSerializer, ListRecipeSerializer, CreateUpdateRecipeSerializer
from recipes.mixins import GetSerializerClassMixin

from recipes.pagination import RecipesAPIListPagination

User = get_user_model()


class RecipeViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):

   queryset = Recipe.objects.all()
   serializer_class = ListRecipeSerializer
    #permission_classes_by_action = {
       #'list': [permissions.AllowAny],
       #'retrieve': [permissions.AllowAny],
       #'create': [permissions.IsAuthenticated],
    #}


   serializer_class_by_action = {
        'list': ListRecipeSerializer,
        'retrieve': DetailRecipeSerializer,
        'create': CreateUpdateRecipeSerializer,
        'update': CreateUpdateRecipeSerializer
    }

  # def get_serializer(self, *args, **kwargs):
    #  if self.action == 'list':
    #     return ListRecipeSerializer()
    #  return super().get_serializer(*args, **kwargs)

   pagination_class = RecipesAPIListPagination
   