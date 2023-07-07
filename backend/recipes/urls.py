from rest_framework.routers import  DefaultRouter
from recipes.views import RecipeViewSet, TagsViewSet, IngredientsViewSet

router =  DefaultRouter()

app_name = 'recipes'

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = router.urls 
