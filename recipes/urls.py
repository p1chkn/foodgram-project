from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new_recipe, name="new_recipe"),
    path('recipe/<int:recipe_id>/', views.recipe_view, name="recipe"),
    path('shoplist/', views.shoplist_view, name="shoplist"),
    path('favorites/', views.favorites_view, name="favorites"),
    path('editin/<int:recipe_id>/', views.recipe_edit, name="editing"),
    path('recipe/user/<int:user_id>/', views.user_view, name="user_recipe"),
    path('follows/', views.follow_view, name="follows"),
    path('recipe/delete/<int:recipe_id>/', views.remove_recipe,
         name="remove_recipe"),
]
