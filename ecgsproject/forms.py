from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        #fields = ['Nom', 'Prenom', 'Adresse e-mail', 'Téléphone', 'Nom Entreprise', 'Votre fonction', 'password1', 'password2']
        fields = ['email', 'password1', 'password2']