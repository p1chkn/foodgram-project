from rest_framework import serializers

from recipes.models import Favorites, Follow, Ingredient, Purchases


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['title', 'dimension']
        model = Ingredient


class PurchasesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['recipe']
        model = Purchases


class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['recipe']
        model = Favorites


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['author']
        model = Follow
