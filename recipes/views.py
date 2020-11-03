from django.shortcuts import render
from .models import Ingredient
import json


def index(request):
    """
    with open('ingredients.json', 'r') as ingredients:
        ingredients_json = json.load(ingredients)
        for ingredient in ingredients_json:
            Ingredient.objects.create(title=ingredient['title'], dimension=ingredient['dimension'])
    """
    return render(request, 'indexNotAuth.html')
