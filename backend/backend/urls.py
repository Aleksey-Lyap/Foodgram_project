from django.contrib import admin
from django.urls import path, include
from recipes.views import RecipeViewSet

urlpatterns = [
    path('admin/', admin.site.urls),

   # path('api/recipes/', RecipeViewSet.as_view({'get': 'list'})),
    path('api/', include('recipes.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),


]
