from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Favorites, Follow, Ingredient, Purchases, Recipe
from users.models import User

from .permissions import IsAuthenticated
from .serializers import (FavoritesSerializer, FollowSerializer,
                          IngredientSerializer, PurchasesSerializer)


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


class SubscriptionViewSet(viewsets.ModelViewSet):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=request._data['id'])
        user = request.user
        Follow.objects.get_or_create(user=user, author=author)
        return JsonResponse(data={"success": True})

    def destroy(self, request, *args, **kwargs):
        auhtor = get_object_or_404(User, id=self.kwargs['pk'])
        follow = get_object_or_404(
            Follow, user=request.user, author=auhtor)
        follow.delete()
        return JsonResponse(data={"success": True})
