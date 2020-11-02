from django.contrib import admin
from .models import Ingredient, Recipe, Ingredients_in_recipe


class IngredientAdmin(admin.ModelAdmin):

    list_display = ('title', 'dimension')


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('title', 'author')
    list_filter = ('title', 'author', 'tag')


class Ingredients_in_recipeAdmin(admin.ModelAdmin):

    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients_in_recipe, Ingredients_in_recipeAdmin)
