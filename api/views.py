import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from recipes.models import Favorites, Follow, Ingredient, Purchases, Recipe
from users.models import User

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
        if request.user.is_authenticated:
            user = request.user
            purches = Purchases.objects.filter(
                user=user, recipe=recipe).exists()
            if not purches:
                Purchases.objects.create(user=user, recipe=recipe)
            return JsonResponse(data={"success": True})
        else:
            purchases = request.session.get('purchases', [])
            if recipe not in purchases:
                purchases.append(recipe.id)
                request.session['purchases'] = purchases
            return JsonResponse(data={"success": True})
    return JsonResponse(data={"success": False})


@api_view(['DELETE'])
def remove_purchases(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_authenticated:
        user = request.user
        purches = get_object_or_404(Purchases, user=user, recipe=recipe)
        purches.delete()
        return JsonResponse(data={"success": True})
    else:
        purchases = request.session.get('purchases', [])
        purchases.remove(recipe.id)
        request.session['purchases'] = purchases
        return JsonResponse(data={"success": True})


def add_favorites(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        recipe_id = int(''.join(re.findall(r'\d+', body)))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        favorites = Favorites.objects.filter(user=user, recipe=recipe).exists()
        if not favorites:
            Favorites.objects.create(user=user, recipe=recipe)
        return JsonResponse(data={"success": True})
    return JsonResponse(data={"success": False})


def remove_favorites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorites = get_object_or_404(Favorites, user=user, recipe=recipe)
    favorites.delete()
    return JsonResponse(data={"success": True})


def add_sbscriptions(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        author_id = int(''.join(re.findall(r'\d+', body)))
        author = get_object_or_404(User, id=author_id)
        user = request.user
        follow = Follow.objects.filter(user=user, author=author).exists()
        if not follow:
            Follow.objects.create(user=user, author=author)
        return JsonResponse(data={"success": True})
    return JsonResponse(data={"success": False})


def remove_subscriptions(request, user_id):
    user = request.user
    auhtor = get_object_or_404(User, id=user_id)
    follow = get_object_or_404(Follow, user=user, author=auhtor)
    follow.delete()
    return JsonResponse(data={"success": True})
