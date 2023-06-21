

from rest_framework.routers import  DefaultRouter
from recipes.views import RecipeViewSet
from users.views import CustomUserViewSet

router =  DefaultRouter() 

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = router.urls 
