from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Ingredient
from django.http import JsonResponse
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
