from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import PurchasesViewSet, FavoritesViewSet

purchases_router = DefaultRouter()
purchases_router.register('v1/purchases', PurchasesViewSet)
favorites_router = DefaultRouter()
favorites_router.register('v1/favorites', FavoritesViewSet)

urlpatterns = [
    path('', include(purchases_router.urls)),
    path('', include(favorites_router.urls)),
    path('v1/ingredients/', views.ingredients),
    path('v1/subscriptions/', views.add_sbscriptions),
    path('v1/subscriptions/<int:user_id>/', views.remove_subscriptions),
]
