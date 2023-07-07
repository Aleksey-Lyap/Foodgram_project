from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from recipes.models import Recipe, Tag, Ingredients, Favorite, Cart, IngredientsRecipe
from recipes.serializers import RecipeSerializer, CreateUpdateRecipeSerializer, TagSerializer, IngredientsSerializer, RecipeSubFavorCartSerializer

from recipes.mixins import GetSerializerClassMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import Sum

from recipes.pagination import RecipesAPIListPagination

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from recipes.filter import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend
from fpdf import FPDF

from django.http import HttpResponse
User = get_user_model()

class RecipeViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
    }
    serializer_class = CreateUpdateRecipeSerializer
    serializer_class_by_action = {
         'list': RecipeSerializer,
         'retrieve': RecipeSerializer
     }

    pagination_class = RecipesAPIListPagination
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubFavorCartSerializer(recipe, context=context)
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        get_object_or_404(Favorite, user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            Cart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubFavorCartSerializer(recipe, context=context)
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        get_object_or_404(Favorite, user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        user = request.user
        ingredients = IngredientsRecipe.objects.filter(
            recipe__carts__user=user).values(
            'ingredients__name', 'ingredients__measurement_unit').annotate(
            sum_amount=Sum('amount')
        ).order_by()

        shop_list = 'Список покупок\n\n'
        for ingredient in ingredients:
            shop_list += f'{ingredient["ingredients__name"]} {ingredient["ingredients__measurement_unit"]} {ingredient["sum_amount"]}\n'

        response = HttpResponse(content=shop_list,
                                content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')

        return response
    
    
class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            return self.queryset.filter(name__icontains=name)
        return super().get_queryset()
