from recipes.models import Purchases, Favorites, Follow


def counter(request):
    if request.user.is_authenticated:
        counter = Purchases.objects.filter(user=request.user).count()
    else:
        purchases = request.session.get('purchases', [])
        counter = len(purchases)
    return {
        'counter': counter
    }


def purchases_id(request):
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(
            user=request.user).select_related('recipe').all()
        purchases_id = [i.recipe.id for i in purchases]
    else:
        purchases_id = request.session.get('purchases', [])
    return {
        'purchases_id': purchases_id
    }


def favorites_id(request):
    if request.user.is_authenticated:
        favorites = Favorites.objects.filter(
            user=request.user).select_related('recipe').all()
        favorites_id = [i.recipe.id for i in favorites]
    else:
        favorites_id = []
    return {
        'favorites_id': favorites_id
    }


def subscriptions_id(request):
    if request.user.is_authenticated:
        follow = Follow.objects.filter(
            user=request.user).select_related('author').all()
        subscriptions_id = [i.author.id for i in follow]
    else:
        subscriptions_id = []
    return {
        'subscriptions_id': subscriptions_id
    }
