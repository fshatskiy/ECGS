from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
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

""" class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['email', 'password']
        
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'})
        } """
    
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class Calcul_accueilForm(forms.Form):
    nom = forms.CharField()
    prenom = forms.CharField()
    email = forms.EmailField()
    tel = forms.IntegerField()
    entreprise = forms.CharField()
    
class CalculForm(forms.Form):
    pass
    
    
    
class RegisterForm(UserCreationForm):
    class Meta:  
        model = CustomUser  
        fields = ('email', 'password1', 'password2', 'nom', 'prenom', 'tel', 'entreprise', 'fonction')# fields = ['Nom', 'Prenom', 'Adresse e-mail', 'Téléphone', 'Nom Entreprise', 'Votre fonction', 'password1', 'password2']
            
        """ nom = forms.CharField()
        prenom = forms.CharField()
        email = forms.EmailField()
        tel = forms.IntegerField()
        entreprise = forms.CharField()    """ 
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)