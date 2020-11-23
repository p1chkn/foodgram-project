from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import PurchasesViewSet

purchases_router = DefaultRouter()
purchases_router.register('v1/purchases', PurchasesViewSet)

urlpatterns = [
    path('', include(purchases_router.urls)),
    path('v1/ingredients/', views.ingredients),
    path('v1/favorites/', views.add_favorites),
    path('v1/favorites/<int:recipe_id>/', views.remove_favorites),
    path('v1/subscriptions/', views.add_sbscriptions),
    path('v1/subscriptions/<int:user_id>/', views.remove_subscriptions),
]
