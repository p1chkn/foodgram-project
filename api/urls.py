from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import FavoritesViewSet, PurchasesViewSet, SubscriptionViewSet

purchases_router = DefaultRouter()
purchases_router.register('v1/purchases', PurchasesViewSet)
favorites_router = DefaultRouter()
favorites_router.register('v1/favorites', FavoritesViewSet)
subscription_router = DefaultRouter()
subscription_router.register('v1/subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(purchases_router.urls)),
    path('', include(favorites_router.urls)),
    path('', include(subscription_router.urls)),
    path('v1/ingredients/', views.ingredients),
]
