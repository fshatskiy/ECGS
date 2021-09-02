#from django.contrib.auth.models import User
from django.db import models
import uuid
#from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import AbstractUser, BaseUserManager
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


class CustomUser(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    createur = models.ForeignKey('self', max_length=200, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()




#intégrer Personne avec utilisateurs directs afin qu'ils soient de la même instance que les personnes créées sur le site admin
class Personne(models.Model):
    id_personne = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False)
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.EmailField(max_length=200, unique=True)
    tel = models.CharField(max_length=20)
    entreprise = models.CharField(max_length=200)
    fonction = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    createur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# for request.user
    
    def __str__(self):
        return str(self.nom)

    
class Integrateur(models.Model):
    id_integrateur = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False)
    id_personne = models.OneToOneField(Personne, 
                                    on_delete=models.CASCADE,
                                    unique=True)
    adr_entreprise = models.CharField(max_length=250)
    tva = models.CharField(max_length=14, unique=True)#international, unique
    lieu_fonction = models.CharField(max_length=250)
    
    def __str__(self):
        return str(self.id_personne)
    
class Employe(models.Model):
    id_employe = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_personne = models.OneToOneField(Personne, 
                                on_delete=models.CASCADE,
                                unique=True)
    id_integrateur = models.ForeignKey(Integrateur, null=True, blank=True,
                                on_delete=models.CASCADE)
    lieu_fonction = models.CharField(max_length=250)
    createur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# for request.user
        
    def __str__(self):
        return str(self.id_personne)
        
class Resultat(models.Model):
    id_resultat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False
                                )
    nb_h_tot_prest_ann = models.PositiveIntegerField(null=True, blank=True)#test
    utilisation_inutile = models.PositiveIntegerField(null=True, blank=True)#test
    date = models.DateTimeField(auto_now_add=True)#test
    
    def __str__(self):
        return self.title
    
class Client(models.Model):
    INTERET = (
        ('Interessé', 'Interessé'),
        ('Abonné', 'Abonné'),
    )
    id_client = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_personne = models.OneToOneField(Personne, 
                                on_delete=models.CASCADE,
                                unique=True)
    id_employe = models.ForeignKey(Employe, 
                                null=True,   
                                blank=True,
                                on_delete=models.CASCADE)
    id_resultat = models.ForeignKey(Resultat,
                                    null=True,
                                    blank=True,
                                on_delete=models.CASCADE)
    adr_entreprise = models.CharField(max_length=250)
    num_contrat = models.PositiveIntegerField(null=True, blank=True, unique=True)#unique
    num_licence = models.PositiveIntegerField(null=True, blank=True, unique=True)#unique
    statut = models.CharField(max_length=200, choices=INTERET)#------------------------------------------- A MAJ
    createur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)# for request.user
    
    def __str__(self):
        return str(self.id_personne)
        
""" class Ticket(models.Model):
    STATUT = (
        ('Ouvert', 'Ouvert'),
        ('En attente', 'En attente'),
        ('Résolu', 'Résolu'),
        ('Fermé', 'Fermé')
    )
    id_ticket = models.UUIDField(default=uuid.uuid4, 
                                unique=True,
                                primary_key=True, 
                                editable=False)
    titre = models.CharField(max_length=200)
    num_licence = models.PositiveIntegerField()
    commentaire = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=200, choices=STATUT)

    def __str__(self):
        return str(self.titre)
        
        
class Detail_Ticket(models.Model):
    id_ticket = models.ForeignKey(Ticket,
                                null=True,
                                on_delete=models.SET_NULL)
    id_client = models.ForeignKey(Client, 
                                null=True,
                                on_delete=models.SET_NULL)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id_ticket)
        
class Rep_Ticket(models.Model):
    id_rep_ticket = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_ticket = models.ForeignKey(Ticket,
                                  null=True,
                                on_delete=models.SET_NULL)
    reponse = models.TextField(null=True)
    date = models.DateField(auto_now_add=True)
    resolu_par = models.CharField(max_length=200)#reprendre les noms depuis la bd ?
    
    def __str__(self):
        return str(self.id_ticket)

class Contrat(models.Model):
    id_contrat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_client = models.OneToOneField(Client, 
                                    on_delete=models.CASCADE,
                                    unique=True)#pls contrats possibles par client ?
    date_ctr = models.DateField()
        
    def __str__(self):
        return str(self.id_client) 
    
class Licence(models.Model):
    id_licence = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_contrat = models.ForeignKey(Contrat,
                                on_delete=models.CASCADE)
    date_lic = models.DateField()
    
    def __str__(self):
        return str(self.id_contrat) """