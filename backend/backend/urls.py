from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('recipes.urls')),
    path('api/', include('users.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),

    

    path('api/auth/token/login/', TokenCreateView.as_view()),
    path('api/auth/token/logout/', TokenDestroyView.as_view()),
    path('api/auth/', include('djoser.urls')),
    #path('api/auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

