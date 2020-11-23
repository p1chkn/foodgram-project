from rest_framework import serializers

from recipes.models import Ingredient, Purchases, Favorites


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
