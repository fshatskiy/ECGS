from django.contrib import admin
from .models import Personne, Integrateur, Employe, Client
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.


#je crois que je devrais ajouter des autorisations pour cette page car je ne peux rien y voir, sauf lorsque
#je vais encore sur /admin/


#custom colonnes
@admin.display(description='Nom intégrateur')
def nom_int(obj):
    return "%s %s"%(obj.id_personne.nom, obj.id_personne.prenom)

@admin.display(description='Entreprise')
def int_entr(obj):
    return obj.id_personne.entreprise

@admin.display(description='Nom employé')
def nom_empl(obj):
    return "%s %s"%(obj.id_personne.nom, obj.id_personne.prenom)

@admin.display(description='Entreprise')
def empl_entr(obj):
    return obj.id_personne.entreprise

@admin.display(description='Nom client')
def nom_client(obj):
    return "%s %s"%(obj.id_personne.nom, obj.id_personne.prenom)




class IntegrateurAdmin(admin.ModelAdmin):    
    list_display = (nom_int, int_entr, 'adr_entreprise', 'tva', 'lieu_fonction')     

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    exclude = ('createur',)#to not be able to change it manually
    list_display = ('nom', 'prenom', 'mail', 'tel', 'entreprise', 'fonction', 'date_creation', 'createur')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.createur = request.user
        obj.save()
        
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Personne.objects.all()
        print(Personne.objects.filter(createur=request.user))
        return Personne.objects.filter(createur=request.user)
    

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    exclude = ('createur',)#to not be able to change it manually
    list_display = (nom_empl, 'id_integrateur', empl_entr, 'lieu_fonction', 'createur')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.createur = request.user
        obj.save()
        
    def get_queryset(self, request):
        queryset = super(EmployeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        """ if request.user.is_superuser:
            return Employe.objects.all() """
        print(Employe.objects.filter(createur=request.user))
        return Employe.objects.filter(createur=request.user)
    
    #ForeignKey drop list
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_personne":
            kwargs["queryset"] = Personne.objects.filter(createur=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    exclude = ('createur',)#to not be able to change it manually
    @admin.display(description='Employé')
    def employe(obj):
        return obj.id_employe
    list_display = (nom_client, employe, 'adr_entreprise', 'num_contrat', 'num_licence', 'statut', 'createur')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.createur = request.user
        obj.save()
    
    def get_queryset(self, request):
        queryset = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        print(Client.objects.filter(createur=request.user))
        return Client.objects.filter(createur=request.user)
    
    #ForeignKey drop list
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_personne":
            kwargs["queryset"] = Personne.objects.filter(createur=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

        
#mettre en place vérificateur pr champ tva + tel
admin.site.register(Integrateur, IntegrateurAdmin)