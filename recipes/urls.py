from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new_recipe, name="new_recipe"),
    path('recipe/<int:recipe_id>/', views.recipe_view, name="recipe"),
    path('shoplist/', views.shoplist_view, name="shoplist"),
]
