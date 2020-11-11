from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import re
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Ingredient, Purchases, Recipe
from .serializers import IngredientSerializer


@api_view(['GET'])
def ingredients(request):
    try:
        query = request.GET['query']
    except Exception:
        query = ''
    data = Ingredient.objects.filter(title__contains=query).all()
    serializer = IngredientSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def add_purchases(request):
    body = request.body.decode('utf-8')
    recipe_id = int(''.join(re.findall(r'\d+', body)))
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    Purchases.objects.create(user=user, recipe=recipe)
    return JsonResponse(data={"success": True})


@api_view(['DELETE'])
def remove_purchases(request):
    pass
