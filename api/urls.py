from django.urls import path
from . import views


urlpatterns = [
    path('v1/ingredients/', views.ingredients),
    path('v1/purchases/', views.add_purchases),
]
