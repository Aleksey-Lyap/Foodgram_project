from djoser.views import UserViewSet
from users.serializers import CustomUserSerializer
from users.models import Follow, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
