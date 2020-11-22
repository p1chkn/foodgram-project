from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    class TagChoices(models.IntegerChoices):
        BREAKFAST = 1, _('breakfast')
        LUNCH = 2, _('lunch')
        DINNER = 3, _('dinner')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipe_image/')
    description = models.TextField()
    tag = MultiSelectField(choices=TagChoices.choices, null=True)
    done_time = models.IntegerField()

    def __str__(self):
        return self.title


class Ingredients_in_recipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                   related_name='ingredients_in_recipe')
    amount = models.IntegerField()

    def __str__(self):
        return self.ingredient.title


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='following')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='follower')
