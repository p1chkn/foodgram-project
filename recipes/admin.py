from django.contrib import admin

from .models import Ingredient, IngredientsInRecipe, Recipe


class IngredientAdmin(admin.ModelAdmin):

    list_display = ('title', 'dimension')


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('title', 'author')
    list_filter = ('title', 'author', 'tag')


class IngredientsInRecipeAdmin(admin.ModelAdmin):

    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsInRecipe, IngredientsInRecipeAdmin)
