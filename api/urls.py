from django.urls import path
from .views import ingredients


urlpatterns = [
    path('v1/ingredients/', ingredients)
]