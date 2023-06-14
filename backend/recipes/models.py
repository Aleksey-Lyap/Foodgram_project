from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Ingredients(models.Model):

    name = models.CharField(
        unique = True,
        max_length=200,
        verbose_name='Название')
    quantity = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Количество')
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True)
    color = ColorField(
        verbose_name='Цвет',
        unique=True)
    slug = models.SlugField(
        unique=True,
        verbose_name='Текстовый идентификатор тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/image/')
    text = models.TextField(
        verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='Продукты в рецепте')
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тег рецепта')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления')
    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')

    class Meta:
        ordering = ('-create_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):

    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredients_recipes',
        verbose_name='Ингридиенты')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_ingredients',
        verbose_name='Рецепт')

    def __str__(self):
        return f'{self.ingredients} {self.recipe}'


class TagRecipe(models.Model):

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipes',
        verbose_name='Тег')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_tag',
        verbose_name='Рецепт')
    
    def __str__(self):
        return f'{self.tag} {self.recipe}' 


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_favorite')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):

        return f'{self.recipe} {self.user}'


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='purchases')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'