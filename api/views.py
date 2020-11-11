from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import re
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Ingredient, Purchases, Recipe
from .serializers import IngredientSerializer, PurchasesSerializer


@api_view(['GET'])
def ingredients(request):

    query = request.GET.get('query', '')
    data = Ingredient.objects.filter(title__contains=query).all()
    serializer = IngredientSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


def purchases(request):

    if request.method == 'GET':
        user = request.user
        data = Purchases.objects.filter(user=user).all()
        serializer = PurchasesSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        recipe_id = int(''.join(re.findall(r'\d+', body)))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        purches = Purchases.objects.filter(user=user, recipe=recipe).exists()
        if not purches:
            Purchases.objects.create(user=user, recipe=recipe)
        return JsonResponse(data={"success": True})
    return JsonResponse(data={"success": False})


@api_view(['DELETE'])
def remove_purchases(request, recipe_id):

    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    purches = get_object_or_404(Purchases, user=user, recipe=recipe)
    purches.delete()
    return JsonResponse(data={"success": True})
