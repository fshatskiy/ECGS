from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import CustomUser
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ResultatAccueilForm, ContactForm, CalculForm
from django.http import HttpResponse
from django.utils.translation import ugettext as _


UserModel = get_user_model()
# Create your views here.

def forms_accueil(request):
    print("forms_accueil")
    if request.method == 'POST' and "submitResult" in request.POST:
        print("resultat form")
        formAccueil = ResultatAccueilForm(request.POST)
        if formAccueil.is_valid():
            data = formAccueil.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                messages.error(request, _('Cette adresse email a déjà été utilisée.'))
                return redirect('accueil') #METTRE '#cta'
            user = formAccueil.save(commit=False)
            user.is_active = False
            user.a_contacter=True
            user.save()
            print("user enregistré")
            return redirect('calcul')
        else:
            messages.error(request, _("Les informations rentrées sont invalides"))
    elif request.method == 'POST' and "submitContact" in request.POST:
        print("contact form")
        formContact = ContactForm(request.POST)
        if formContact.is_valid():
            #envoi du mail
           
            mail_subject = "Website Info Contact"
            body = {
            'nom': formContact.cleaned_data['nom'],
            'prenom': formContact.cleaned_data['prenom'],
            'adr_email': formContact.cleaned_data['adr_email'],
            'message': formContact.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            
            email = EmailMessage(
                mail_subject, message, to=["ecgstest@gmail.com"]
            )
            

            try:
                #send_mail(mail_subject, message, 'admin@example.com', ['admin@example.com'])
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, _('Votre message a bien été envoyé. Un de nos collaborateurs vous contactera sous-peu. '))
            return redirect ("accueil")
        messages.error(request, _("Les informations rentrées sont invalides"))
            
    formAccueil = ResultatAccueilForm()
    formContact = ContactForm()
    print("return fin")
    return render(request, 'index.html', {'formAccueil': formAccueil, 'formContact': formContact,})


#mettre en place les if : sécurité
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print("form =")
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]# We check if the data is correct
            associated_users = CustomUser.objects.filter(Q(email=email))
            if not associated_users.exists():
                print("enter ass users exists : error")
                messages.error(request, _("L'utilisateur avec cette adresse email n'existe pas."))
                return redirect('login')
            if email and password :
                user = authenticate(request, email=email, password=password)
            if user is not None and user.is_staff:
                login(request, user)# we connect the user
                """ if user.last_login == user.date_joined: 
                    return redirect('reset_password') """
                return redirect('admin')
            messages.error(request, _("Les informations sont invalides ou votre compte n'a pas encore été activé par l'administrateur"))
        else:  # otherwise an error will be displayed
            messages.error(request, _("Les informations sont invalides ou votre compte n'a pas encore été activé par l'administrateur"))
            return redirect('login')
    else:
        form=LoginForm()
    return render(request, 'login.html', {'form': form})

# ajouter les check necessaires : if not empty, doesn't exist...
def signup(request):
    print("enter signup")
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        print("enter post")
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("enter is valid")
            data = form.cleaned_data['email']#check if the email address already exists
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                print("enter ass users exists : error")
                messages.error(request, _("Cette adresse email a déjà été utilisée."))
                return redirect('register')
            user = form.save(commit=False)            
            #user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            print("user save")
            user.save()
            current_site = get_current_site(request)
            mail_subject = _('Activation de votre compte.')
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
            print("enter email sent")
            email.send()
            #check
            messages.success(request, _("Veuillez confirmer votre adresse email afin de terminer l'inscription"))
            return redirect('accueil')
        #messages.error(request, "Les informations rentrées sont invalides")
        """ return redirect('register') """
    else:
        print("invalid")
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
        messages.success(request, _("Votre compte a bien été vérifié. Veuillez maintenant vérifier si l'administrateur a activé votre compte en vous connectant."))
        return redirect('accueil')
    else:
        messages.error(request, _("Le lien d'activation n'est plus valide ! Veuillez vous réinscrire"))
        return redirect('accueil')
            

def conditions(request):
    return render(request, 'politiques.html')


def calcul(request):
    print("forms_accueil")
    submitbutton= request.POST.get("submit")
    nb_appareils=""
    nb_switchs=""
    pourcent=""
    wh_inut=""
    wh_ut_tot=""
    kwh=""
    euro=""
    #argent_perdu=""
    form = CalculForm(request.POST or None)
    if form.is_valid():
        nb_appareils = form.cleaned_data.get('nb_appareils')
        nb_switchs = form.cleaned_data.get('nb_switchs')
        
        
            
            
        wh_inut = nb_appareils*5.79+50*nb_switchs #wh utilisés par rapport au nb d'appareils et nb de switchs
        wh_ut_tot = wh_inut*8760 #pour totue l'année : 100%
        wh_inut=wh_inut*7182
        kwh = wh_inut/1000
        
        
        pourcent = wh_ut_tot/100
        pourcent = wh_inut/pourcent
        pourcent = round(pourcent, 2)
        
        
                
        print("wh_inut, kwh, wh_ut_tot, pourcent", wh_inut, kwh, wh_ut_tot, pourcent)
        
        
        euro = 0.33*kwh
        euro = round(euro, 2)
            
        
        
        
        
        
        #form = CalculForm(request.POST)
    context= {'form': form, 'nb_appareils': nb_appareils, 'nb_switchs': nb_switchs, 'wh_inut': wh_inut, 'pourcent': pourcent, 'kwh': kwh,'euro': euro, 'submitbutton': submitbutton}
    
    form = CalculForm()
    return render(request, 'calcul.html', context)
