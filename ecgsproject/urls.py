from django.urls import path
from . import views

# ajouter l'accueil

urlpatterns = [
    path('', views.accueil),
]