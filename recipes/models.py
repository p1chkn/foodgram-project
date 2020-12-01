from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from users.models import User


class Ingredient(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    dimension = models.CharField(max_length=20,
                                 verbose_name='Единица измерения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ингредиенты"


class Recipe(models.Model):
    class TagChoices(models.IntegerChoices):
        BREAKFAST = 1, _('завтрак')
        LUNCH = 2, _('обед')
        DINNER = 3, _('ужин')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='recipe_image/',
                              verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    tag = MultiSelectField(choices=TagChoices.choices, null=True,
                           verbose_name='Тэг')
    done_time = models.IntegerField(verbose_name='Время приготовления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепты"


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                   related_name='ingredients_in_recipe',
                                   verbose_name='Ингредиент')
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return self.ingredient.title

    class Meta:
        verbose_name = "Ингредиенты в рецептах"


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Покупки"


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранное"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='following')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='follower')

    class Meta:
        verbose_name = "Подписки"
