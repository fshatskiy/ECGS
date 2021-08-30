from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url
from . import views
from ecgsproject.views import CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

admin.site.site_header = 'Administration générale de EcoGreenSoft'
# ajouter l'accueil

#app_name = "ecgsproject"

urlpatterns = [ 
    path('', views.accueil, name='accueil'),
    
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    url(r'^', include('django.contrib.auth.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/token/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]