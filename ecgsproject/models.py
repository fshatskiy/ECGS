from django.db import models
import uuid

# Create your models here.


class Personne(models.Model):
    id_personne = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False)
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    mail = models.EmailField(max_length=200)
    tel = models.CharField(max_length=20)
    entreprise = models.CharField(max_length=200)
    fonction = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    """ def __str__(self):
        return self.title """
    
class Integrateur(models.Model):
    id_integrateur = models.UUIDField(default=uuid.uuid4, 
                                   unique=True, 
                                   primary_key=True, 
                                   editable=False)
    id_personne = models.OneToOneField(Personne, 
                                    on_delete=models.CASCADE,
                                    unique=True)
    adr_entreprise = models.CharField(max_length=250)
    tva = models.CharField(max_length=14)#international
    lieu_fonction = models.CharField(max_length=250)
    
    """ def __str__(self):
        return self.title """
    
class Employe(models.Model):
    id_employe = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_personne = models.OneToOneField(Personne, 
                                on_delete=models.CASCADE,
                                unique=True)
    id_integrateur = models.ForeignKey(Integrateur, 
                                on_delete=models.CASCADE)
    lieu_fonction = models.CharField(max_length=250)
        
    """ def __str__(self):
        return self.title """
        
class Resultat(models.Model):
    id_resultat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    nb_h_tot_prest_ann = models.PositiveIntegerField(null=True, blank=True)#test
    utilisation_inutile = models.PositiveIntegerField(null=True, blank=True)#test
    date = models.DateTimeField(auto_now_add=True)#test
    
    """ def __str__(self):
        return self.title """
    
class Client(models.Model):
    id_client = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_personne = models.OneToOneField(Personne, 
                                on_delete=models.CASCADE,
                                unique=True)
    id_employe = models.ForeignKey(Employe, 
                                on_delete=models.CASCADE)
    id_resultat = models.ForeignKey(Resultat,
                                on_delete=models.CASCADE)
    adr_entreprise = models.CharField(max_length=250)
    num_contrat = models.PositiveIntegerField(null=True, blank=True)
    num_licence = models.PositiveIntegerField(null=True, blank=True)
    
    """ def __str__(self):
        return self.title """
        
class Ticket(models.Model):
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

    """ def __str__(self):
        return self.title """
        
        
class Detail_Ticket(models.Model):
    id_ticket = models.ForeignKey(Ticket,
                                null=True,
                                on_delete=models.SET_NULL)
    id_client = models.ForeignKey(Client, 
                                null=True,
                                on_delete=models.SET_NULL)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    """ def __str__(self):
        return self.title """
        
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
    
    """ def __str__(self):
        return self.title """

class Contrat(models.Model):
    id_contrat = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_client = models.OneToOneField(Client, 
                                    on_delete=models.CASCADE,
                                    unique=True)#pls contrats possibles par client ?
    date_ctr = models.DateField()
        
    """ def __str__(self):
        return self.title """
        
class Licence(models.Model):
    id_licence = models.UUIDField(default=uuid.uuid4, 
                                unique=True, 
                                primary_key=True, 
                                editable=False)
    id_contrat = models.ForeignKey(Contrat,
                                on_delete=models.CASCADE)
    date_lic = models.DateField()