from recipes.models import Purchases, Favorites


def counter(request):
    counter = Purchases.objects.filter(user=request.user).count()
    return {
        'counter': counter
    }


def purchases_id(request):
    purchases = Purchases.objects.filter(
        user=request.user).select_related('recipe').all()
    purchases_id = [i.recipe.id for i in purchases]
    return {
        'purchases_id': purchases_id
    }


def favorites_id(request):
    favorites = Favorites.objects.filter(
        user=request.user).select_related('recipe').all()
    favorites_id = [i.recipe.id for i in favorites]
    return {
        'favorites_id': favorites_id
    }
