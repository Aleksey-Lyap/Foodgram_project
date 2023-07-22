from django.contrib import admin
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('api/', include('users.urls')),
    path('api/auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('api/auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('api/auth/', include('djoser.urls')),
]
