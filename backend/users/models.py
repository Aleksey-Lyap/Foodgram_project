from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Уникальное имя")
    email = models.EmailField(
        max_length=254,
        unique = True,
        verbose_name='Электронная почта')
    first_name = models.CharField(
        max_length=150,
        unique = True,
        verbose_name="Имя")
    last_name = models.CharField(
        max_length=150,
        unique = True,
        verbose_name="Фамилия")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Follow(models.Model): 

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follower') 
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following') 

    class Meta: 
        verbose_name = 'Подписка на автора' 
        verbose_name_plural = 'Подписки на авторов' 
        constraints = [ 
            models.UniqueConstraint(
                fields=['user', 'author'], name='user_author'
            ),
        ]
