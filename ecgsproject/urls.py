from django.contrib import admin
from django.urls import path, include
from . import views
from ecgsproject.views import CustomLoginView

admin.site.site_header = 'Administration générale de EcoGreenSoft'
# ajouter l'accueil

#app_name = "ecgsproject"

urlpatterns = [ 
    path('', views.accueil, name='accueil'),
    path('register/', views.register_page, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    #path('logout/', views.CustomLogoutForm, name='logout'),
]