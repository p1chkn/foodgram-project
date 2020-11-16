from django.urls import path
from . import views


urlpatterns = [
    path('v1/ingredients/', views.ingredients),
    path('v1/purchases/', views.purchases),
    path('v1/purchases/<int:recipe_id>/', views.remove_purchases),
    path('v1/favorites/', views.add_favorites),
    path('v1/favorites/<int:recipe_id>/', views.remove_favorites),
    path('v1/subscriptions/', views.add_sbscriptions),
    path('v1/subscriptions/<int:user_id>/', views.remove_subscriptions),
]
