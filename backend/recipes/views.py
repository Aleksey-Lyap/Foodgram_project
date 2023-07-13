from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.filter import RecipeFilter
from recipes.mixins import GetSerializerClassMixin
from recipes.models import (Cart, Favorite, Ingredient, IngredientsRecipe,
                            Recipe, Tag)
from recipes.pagination import RecipesAPIListPagination
from recipes.serializers import (CreateUpdateRecipeSerializer,
                                 IngredientsSerializer, RecipeSerializer,
                                 RecipeSubFavorCartSerializer, TagSerializer)

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

    def get_filter(self, model, request, context={}, *args, **kwargs):
        context['request'] = self.request
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeSubFavorCartSerializer(recipe, context=context)
            return Response(serializer.data, status.HTTP_201_CREATED)

        get_object_or_404(model, user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, context={}, *args, **kwargs):
        return self.get_filter(Favorite, request, context, **kwargs)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, context={}, *args, **kwargs):
        return self.get_filter(Cart, request, context, **kwargs)

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
            shop_list += f'{ingredient["ingredients__name"]}\
                           {ingredient["sum_amount"]}\
                           {ingredient["ingredients__measurement_unit"]}\n'

        response = HttpResponse(content=shop_list,
                                content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')

        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            return self.queryset.filter(name__icontains=name)
        return super().get_queryset()
