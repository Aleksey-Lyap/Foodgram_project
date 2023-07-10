from django.shortcuts import get_object_or_404
from recipes.mixins import GetSerializerClassMixin
from recipes.pagination import RecipesAPIListPagination
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User
from users.serializers import (CustomUserCreateSerializer,
                               CustomUserSerializer, PasswordSerializer,
                               SubscriptionSerializer)


class CustomUserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    serializer_class_by_action = {
        'create': CustomUserCreateSerializer,
        'partial': CustomUserCreateSerializer,
    }
    permission_classes = (AllowAny,)
    pagination_class = RecipesAPIListPagination

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, *args, **kwargs):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, *args, **kwargs):
        user = self.request.user
        context = {'user': user}
        serializer = PasswordSerializer(
            data=self.request.data,
            context=context
        )
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        author = get_object_or_404(User, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            Follow.objects.create(user=user, author=author)
            serializer = CustomUserSerializer(author, context=context)
            return Response(serializer.data, status.HTTP_201_CREATED)

        get_object_or_404(Follow, author=author, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, context=context, many=True)
        return self.get_paginated_response(serializer.data)
