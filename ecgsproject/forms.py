from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


""" class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        #fields = ['Nom', 'Prenom', 'Adresse e-mail', 'Téléphone', 'Nom Entreprise', 'Votre fonction', 'password1', 'password2']
        fields = ['email', 'password1', 'password2'] """

    
    
        
class RegisterForm(UserCreationForm):
    class Meta:  
        model = CustomUser  
        fields = ('email', 'password1', 'password2',)# fields = ['Nom', 'Prenom', 'Adresse e-mail', 'Téléphone', 'Nom Entreprise', 'Votre fonction', 'password1', 'password2']
            
        
        """ def clean(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                    raise ValidationError("Cette adresse email existe déjà")
            return self.cleaned_data """