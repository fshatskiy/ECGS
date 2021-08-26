from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm
from django.contrib.auth.views import LoginView, LogoutView
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


#ajouter fonction du mail
def register_page(request):
    if request.method != 'POST':
        form = CustomUserForm()#render empty form
    else:
        form = CustomUserForm(request.POST)#hold the data being submitted by the user
        if form.is_valid():
            form.save()
            return redirect('accueil')#renvoie la personne vers la page accueil après l'enregistrement

    context = {'form': form}

    return render(request, 'register.html', context)