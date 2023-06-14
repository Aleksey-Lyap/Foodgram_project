
from django.urls import path, include

from rest_framework.routers import  DefaultRouter
from recipes.views import RecipeViewSet

router =  DefaultRouter() 




router.register('', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
