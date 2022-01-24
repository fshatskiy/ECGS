from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import CustomUser
from django import forms
from .models import Resultat, CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

    
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class AccueilForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ("nom", "prenom", "email", "tel", "entreprise",)
    
    
""" class ResultatForm(forms.ModelForm):
    
    
    pass
    class Meta:
        model = Resultat
        fields = (,) """
    
    
    
class RegisterForm(UserCreationForm):
    class Meta:  
        model = CustomUser  
        fields = ('email', 'password1', 'password2', 'nom', 'prenom', 'tel', 'entreprise', 'fonction')# fields = ['Nom', 'Prenom', 'Adresse e-mail', 'Téléphone', 'Nom Entreprise', 'Votre fonction', 'password1', 'password2']
             
        
        #fonctionne ?
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)
                

class ContactForm(forms.Form):
    nom = forms.CharField(max_length = 50)
    prenom = forms.CharField(max_length = 50)
    adr_email = forms.EmailField(max_length = 150)
    mail_subject = forms.CharField(max_length = 50)
    message = forms.CharField(max_length = 2000)#a form field that accepts paragraph styled text.
    
    class Meta: 
        widgets = {
            'nom' : forms.TextInput(attrs={'class': 'form-control'}),
            'prenom' : forms.TextInput(attrs={'class': 'form-control'}),
            'adr_email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'mail_subject' : forms.TextInput(attrs={'class': 'form-control'}),
            'message' : forms.Textarea(attrs={'class': 'form-control'}),
        }