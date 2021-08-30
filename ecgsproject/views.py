from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

""" def login_page(request):
    if request.method == "POST":
            # your sign in logic goes here
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('accueil')
            else:
                messages.info(request, 'Adresse email ou mot de passe incorrect')

    context = {}
    return render(request, 'login.html', context) """
    

def accueil(request):
    return render(request, 'accueil.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accueil')

class RegisterPage(FormView):
    template_name = 'register.html'
    #plus tard mettre CustomUserForm
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('accueil')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
            

""" def register_page(request):
    if request.method != 'POST':
        form = CustomUserForm()#render empty form
    else:
        form = CustomUserForm(request.POST)#hold the data being submitted by the user
        if form.is_valid():
            form.save()
            return redirect('accueil')#renvoie la personne vers la page accueil après l'enregistrement

    context = {'form': form}

    return render(request, 'register.html', context) """
    