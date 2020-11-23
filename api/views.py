import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Favorites, Follow, Ingredient, Purchases, Recipe
from users.models import User

from .serializers import IngredientSerializer, PurchasesSerializer, FavoritesSerializer
from .permissions import IsAuthenticated


@api_view(['GET'])
def ingredients(request):

    query = request.GET.get('query', '')
    data = Ingredient.objects.filter(title__contains=query).all()
    serializer = IngredientSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)


class PurchasesViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = PurchasesSerializer

    def get_queryset(self):
        queryset = Purchases.objects.filter(user=self.request.user).all()
        return queryset

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=request._data['id'])
        if request.user.is_authenticated:
            user = request.user
            Purchases.objects.get_or_create(user=user, recipe=recipe)
            return JsonResponse(data={"success": True})
        else:
            purchases = request.session.get('purchases', [])
            if recipe not in purchases:
                purchases.append(recipe.id)
                request.session['purchases'] = purchases
            return JsonResponse(data={"success": True})
        return Response(data={"success": True}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
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


class FavoritesViewSet(viewsets.ModelViewSet):

    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=request._data['id'])
        user = request.user
        Favorites.objects.get_or_create(user=user, recipe=recipe)
        return JsonResponse(data={"success": True})

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        favorites = get_object_or_404(
            Favorites, user=request.user, recipe=recipe)
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
