from django import forms

from .models import Ingredient, Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'done_time']
