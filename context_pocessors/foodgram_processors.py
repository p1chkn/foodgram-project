from recipes.models import Purchases


def counter(request):
    if request.user.is_authenticated:
        counter = Purchases.objects.filter(user=request.user).count()
    else:
        purchases = request.session.get('purchases', [])
        counter = len(purchases)
    return {
        'counter': counter
    }
