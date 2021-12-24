from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    
"""
    Personne
"""    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id_utilisateur = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False)
    email = models.EmailField(max_length=254, unique=True)
    nom = models.CharField(max_length=254, null=True, blank=True)
    prenom = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    tel = models.CharField(max_length=20)
    entreprise = models.CharField(max_length=200)
    fonction = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'tel', 'entreprise', 'fonction']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email
    def only_int(tel):
        if tel.isdigit()==False:
            raise ValidationError('Le numéro de téléphone contient des caractères')
    class Meta:
        db_table = 'ecgsproject_customuser'
        # Add verbose name
        verbose_name_plural = 'Utilisateurs'


class Integrateur(CustomUser):
    tva_integrateur = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False,
                                   max_length = 14)
    #id_utilisateur = models.OneToOneField(CustomUser, #onetoonefield
    #                                on_delete=models.CASCADE,
    #                                unique=True)
    adr_entreprise = models.CharField(max_length=254)
    #tva = models.CharField(max_length=14, unique=True)#international, unique
    lieu_fonction = models.CharField(max_length=254)
    tel_contact = models.CharField(max_length=20)
    
    """ def __str__(self):
        return str(self.id_utilisateur) """
    def __str__(self):
        return "%s %s" % (self.nom, self.prenom)
    def only_int(tel_contact):
        if tel_contact.isdigit()==False:
            raise ValidationError('Le numéro de téléphone contient des caractères')
    
class Employe(CustomUser):
    id_employe = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    #id_utilisateur = models.OneToOneField(CustomUser,
    #                                      unique=True,
    #                            on_delete=models.CASCADE)
    id_integrateur = models.ForeignKey(Integrateur,
                                on_delete=models.CASCADE)
    lieu_fonction = models.CharField(max_length=254)
    #id_utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# CHANGER DE NOM
        
    def __str__(self):
        return "%s %s" % (self.nom, self.prenom)
        

    
class Client(CustomUser):
    tva_cli = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False,
                                max_length = 14)
    id_employe = models.ForeignKey(Employe,
                                on_delete=models.CASCADE)
    adr_entreprise = models.CharField(max_length=254)
    
    #id_utilisateur = models.ForeignKey(CustomUser, 
    #                            on_delete=models.CASCADE)
    #num_contrat = models.PositiveIntegerField(null=True, blank=True, unique=True)#unique
    #num_licence = models.PositiveIntegerField(null=True, blank=True, unique=True)#unique
    #id_utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)#CHANGER DE NOM
    
    def __str__(self):
        return "%s %s" % (self.nom, self.prenom)
        

class Contrat(Client):
    num_contrat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    #id_client = models.OneToOneField(Client, 
    #                                on_delete=models.CASCADE,
    #                                unique=True)
    date_creation = models.DateField(null=False, blank=False)
    date_signature = models.DateField(null=True, blank=True)
    commentaires_contrat = models.CharField(max_length=250, null=True, blank=True)
        
    def __str__(self):
        return "%s %s %s" % (self.num_contrat, self.nom, self.prenom)


class Contrat_detail(Contrat):
    STATUT = (
        ('Signé', 'Signé'),
        ('En Attente', 'En Attente'),
    )
    statut = models.CharField(max_length=200, choices=STATUT)
    
        
    """ def __str__(self):
        return str(self.id_contrat) # ok ? """


class Licence(Contrat):
    num_licence = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    date_achat = models.DateField()
    nombre = models.PositiveIntegerField()
    type = models.CharField(max_length=250)
    commentaires_lic = models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return "%s %s %s" % (self.num_licence, self.num_contrat)
    
class Resultat(models.Model):
    id_resultat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False
                                )
    utilisateur = models.ForeignKey(CustomUser,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    nb_h_tot_prest_ann = models.PositiveIntegerField(null=True, blank=True)#test
    utilisation_inutile = models.PositiveIntegerField(null=True, blank=True)#test
    date = models.DateTimeField(auto_now_add=True)#test
    
    def __str__(self):
        return "%s %s %s" % (self.utilisateur.nom, self.utilisateur.prenom, self.id_resultat)