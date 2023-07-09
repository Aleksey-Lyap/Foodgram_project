from recipes.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'recipes'

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = router.urls
