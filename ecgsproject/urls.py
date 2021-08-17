from django.contrib import admin
from django.urls import path, include
from . import views
""" admin.site.site_header = 'Administration générale de EcoGreenSoft' """

""" from ecgsproject.admin import employeadmin, intadmin """
# ajouter l'accueil

urlpatterns = [
    path('', views.accueil)
]

""" path('employeadmin/', include('employeadmin.urls')), """