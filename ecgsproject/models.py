from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


# Create your models here.

#new custom user
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    
class DateCrDateMod(models.Model):
    created_date = models.DateTimeField(_("créé le"), auto_now=True)
    modified_date = models.DateTimeField(_("modifié le"), editable=False, null=True, blank=True)
    created_by = models.CharField(_("créé par"), max_length=254, editable=False)
    modified_by = models.CharField(_("modifié par"), max_length=254, editable=False, null=True, blank=True)

    class Meta:
        abstract = True

    
"""
    Personne
"""    
class CustomUser(AbstractBaseUser, PermissionsMixin, DateCrDateMod):
    id_utilisateur = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False)
    email = models.EmailField(max_length=254, unique=True)
    nom = models.CharField(max_length=254)#changer lorsque register.html sera complet
    prenom = models.CharField(max_length=254)#changer lorsque register.html sera complet
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    tel = models.CharField(_("téléphone"),max_length=20, validators=[RegexValidator()])#changer lorsque register.html sera complet
    entreprise = models.CharField(max_length=200)#changer lorsque register.html sera complet
    fonction = models.CharField(max_length=200)#changer lorsque register.html sera complet

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'tel', 'entreprise', 'fonction']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

    class Meta:
        db_table = 'ecgsproject_customuser'
        # Add verbose name
        verbose_name_plural = _('Utilisateurs')

class Resultat(models.Model):
    id_resultat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False
                                )
    utilisateur = models.OneToOneField(CustomUser, #onetoonefield
                                    on_delete=models.CASCADE,
                                    unique=True)
    nb_h_tot_prest_ann = models.PositiveIntegerField(null=True, blank=True)#test
    utilisation_inutile = models.PositiveIntegerField(null=True, blank=True)#test
    date = models.DateTimeField(auto_now=True)#test
    
    def __str__(self):
        return "%s" % (self.id_resultat)

class Integrateur(DateCrDateMod):
    id_integrateur = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False,
                                   max_length = 14)
    tva_integrateur = models.CharField(_("tva"),max_length = 14)
    utilisateur = models.OneToOneField(CustomUser, #onetoonefield
                                    on_delete=models.CASCADE,
                                    unique=True)
    adr_entreprise = models.CharField(_("adresse de l'entreprise"),max_length=254)
    #tva = models.CharField(max_length=14, unique=True)#international, unique
    lieu_fonction = models.CharField(_("lieu de sa fonction"),max_length=254)
    tel_contact = models.CharField(_("téléphone de contact"),max_length=20)
    
    def __str__(self):
        return "%s %s" % (self.utilisateur.nom, self.utilisateur.prenom)
    
class Employe(DateCrDateMod):
    id_employe = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    utilisateur = models.OneToOneField(CustomUser,
                                          unique=True,
                                on_delete=models.CASCADE)
    integrateur = models.ForeignKey(Integrateur,
                                on_delete=models.CASCADE)
    lieu_fonction = models.CharField(_("lieu de sa fonction"), max_length=254)
        
    def __str__(self):
        return "%s %s" % (self.utilisateur.nom, self.utilisateur.prenom)
        

    
class Client(DateCrDateMod):
    id_client = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    tva_cli = models.CharField(_("tva"), max_length = 14)
    employe = models.ForeignKey(Employe,
                                on_delete=models.CASCADE)
    utilisateur = models.OneToOneField(CustomUser,
                                          unique=True,
                                on_delete=models.CASCADE)
    adr_entreprise = models.CharField(_("adresse de l'entreprise"), max_length=254)
    
    def __str__(self):
        return "%s %s" % (self.utilisateur.nom, self.utilisateur.prenom)
    


class Contrat(DateCrDateMod):
    id_contrat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    num_contrat = models.CharField(_("numéro du contrat"), max_length=254, null=False, blank=False, unique=True)
    client = models.ForeignKey(Client, 
                               on_delete=models.CASCADE)
    #date_creation = models.DateField(null=False, blank=False, auto_now=True)
    commentaires_contrat = models.CharField(_("commentaires"), max_length=250, null=True, blank=True)
    
    
class Contrat_detail(models.Model):
    STATUT = (
        (_('Proposition'), _('Proposition')),
        (_('En négociation'), _('En négociation')),
        (_('Signé'), _('Signé')),
        (_('Arrêté'), _('Arrêté')),
    )
    id_contrat_detail = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    contrat = models.OneToOneField(Contrat, 
                               on_delete=models.CASCADE)
    statut = models.CharField(max_length=200, choices=STATUT)
    date_signature = models.DateField("date", null=True, blank=True)


class Licence(models.Model):
    id_licence = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    num_licence = models.CharField(_("numéro licence"), max_length=254, null=False, blank=False, unique=True)
    contrat = models.ForeignKey(Contrat, 
                               on_delete=models.CASCADE)
    date_achat = models.DateField(_("date d'achat de licence"))
    nombre = models.PositiveIntegerField(_("nombre de licences"))
    type = models.CharField(max_length=250)
    commentaires_lic = models.CharField(_("commentaires"), max_length=250, null=True, blank=True)
    
