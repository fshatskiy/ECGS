from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
#from django.contrib.auth.models import User
from .models import CustomUser
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query_utils import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm

UserModel = get_user_model()
# Create your views here.

def accueil(request):
    return render(request, 'index.html')


""" class CustomLoginView(LoginView):
    #form_class = LoginForm
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    #def user_is_active(self, user):
    if user.is_active:
            messages.success('Votre compte a bien été activé.')
        else:
            messages.warning('Votre compte n\'a pas encore été approuvé par l\'administrateur du site.')
        return reverse_lazy('accueil')
        
    def get_success_url(self):
        return reverse_lazy('admin') """


#mettre en place les if : sécurité
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]# We check if the data is correct
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)# we connect the user
            return redirect('admin')
        else:  # otherwise an error will be displayed
                messages.error(request, 'Adresse email ou mot de passe sont invalides')
    else:
        form=LoginForm()
    return render(request, 'login.html', {'form': form})

# ajouter les check necessaires : if not empty, doesn't exist...
def signup(request):
    print("enter signup")
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']#check if the email address already exists
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                messages.error(request, 'Cette adresse email a déjà été utilisée.')
                return redirect('register')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation de votre compte.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            #check
            messages.success(request, 'Veuillez confirmer votre adresse email afin de terminer l\'inscription')
            return redirect('accueil')
        messages.error(request, "Les informations sont invalides")
        return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


#activation du nouveau compte via le lien de vérification
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmed=True
        user.save()
        messages.success(request, 'Votre compte a bien été vérifié. Veuillez maintenant vérifier si l\'administrateur a activé votre compte en vous connectant sur le portail http://127.0.0.1:8000/admin .')
        return redirect('accueil')
    else:
        messages.error(request, 'Le lien d\'activation n\'est plus valide ! Veuillez vous réinscrire')
        return redirect('accueil')
            


    