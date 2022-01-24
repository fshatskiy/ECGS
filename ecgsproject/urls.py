from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LogoutView

admin.site.site_header = 'Portail EcoSoft'
# ajouter l'accueil

#app_name = "ecgsproject"

urlpatterns = [ 
    path('', views.accueil, name='accueil'),
    path('admin/', views.accueil, name='admin'),
    path('register/', views.signup, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('login/', views.loginPage, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("conditions d'utilisation/", views.conditions, name='conditions'),
    path("calcul/", views.calcul, name='calcul'),
    
    url(r'^', include('django.contrib.auth.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/token/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]