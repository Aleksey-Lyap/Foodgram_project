from rest_framework.routers import  DefaultRouter

from users.views import CustomUserViewSet

router =  DefaultRouter() 
app_name = 'users'


router.register('users', CustomUserViewSet, basename='users')

urlpatterns = router.urls 
