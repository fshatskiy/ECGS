from django.contrib import admin
from .models import Resultat, CustomUser, Integrateur, Employe, Client, Contrat, Contrat_detail, Licence
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
# Register your models here.


#je crois que je devrais ajouter des autorisations pour cette page car je ne peux rien y voir, sauf lorsque
#je vais encore sur /admin/



# new custom user
@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            #if client, sans demande de mdp lors de l'enregistrement
            'fields': ('nom', 'prenom', 'email', 'password1', 'password2', 'tel', 'entreprise', 'is_active', 'is_staff', 'groups'),# Création d'un nouveau utilisateur via "Utilisateurs  +ADD"
        }),
        )
    #exclude = ('id_utilisateur', )
    list_display = ('nom', 'prenom', 'email', 'entreprise', 'fonction', 'is_staff', 'created_date')#
    list_filter = ('entreprise', 'groups', 'is_staff', 'date_joined')
    search_fields = ('email', 'nom', 'prenom', 'tel', 'entreprise')
    ordering = ('email',)
    
    # permet de cacher à tous les utilisateurs sauf admin, la boxcase de "is superuser"
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        
        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            perm_fields = ('is_active', 'is_staff', 'groups')
            
        return [(None, {'fields': ('email', 'password')}),
                (_('Personal info'), {'fields': ('nom', 'prenom', 'email', 'tel', 'entreprise')}),
                (_('Permissions'), {'fields': perm_fields})]
    
    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            print("here2")
            #print(obj.id_utilisateur, "obj.id_utilisateur")
            obj.modified_by = str(request.user)# request.user est une adr email, str() le force à etre charField
            obj.modified_date=datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => CustomUserAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date=datetime.now()
            print(obj.created_by, "obj.created_by de save_model => CustomUserAdmin")
        print("here4")
        obj.save()
        
        # permet à l'user de voir uniquement les utilisateurs qu'il a créées    
    def get_queryset(self, request):
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return CustomUser.objects.all()
        print("here33")
        print("CustomUserADMIN filtre")
        return CustomUser.objects.filter(created_by=request.user)
    
    
    """ def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['entreprise', 'date_joined', 'is_active', 'is_staff', 'is_superuser']
        else:
            return ['date_joined', 'is_active', 'is_staff'] """ 

#admin.site.unregister(CustomUser, CustomUserAdmin)
#admin.site.register(CustomUser, CustomUserAdmin)

#custom colonnes - essayer d'utiliser : Integrateur.nom
""" @admin.display(description='Nom intégrateur')
def nom_int(obj):
    return "%s %s"%(obj.id_utilisateur.nom, obj.id_utilisateur.prenom)

@admin.display(description='Entreprise')
def int_entr(obj):
    return obj.id_utilisateur.entreprise

@admin.display(description='Nom employé')
def nom_empl(obj):
    return "%s %s"%(obj.id_utilisateur.nom, obj.id_utilisateur.prenom)

@admin.display(description='Entreprise')
def empl_entr(obj):
    return obj.id_utilisateur.entreprise

@admin.display(description='Nom client')
def nom_client(obj):
    return "%s %s"%(obj.id_utilisateur.nom, obj.id_utilisateur.prenom) """

@admin.register(Resultat)
@admin.register(Licence)
@admin.register(Integrateur)


class IntegrateurAdmin(admin.ModelAdmin):    
    
    #list_display = ('adr_entreprise', 'lieu_fonction', 'tel_contact')
    
    #ajouter modified_by
    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            print("here2")
            #print(obj.id_utilisateur, "obj.id_utilisateur")
            obj.modified_by = str(request.user)# request.user est une adr email, str() le force à etre charField
            obj.modified_date=datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => IntegrateurAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date=datetime.now()
            print(obj.created_by, "obj.created_by de save_model => IntegrateurAdmin")
        print("here4")
        obj.save()
    
    # permet à l'user de voir uniquement les utilisateurs qu'il a créées    
    def get_queryset(self, request):
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return Integrateur.objects.all()
        print("here33")
        print("INTEGRATEURADMIN filtre")
        return Integrateur.objects.filter(created_by=request.user)
        
    #ne sert à rien ? car lorsque je me co en tant qu'int, je n'ai pas besoin de créer d'autres int.
    """ def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here111int")
        if db_field.name == "utilisateur" and request.user.is_superuser:
            print("here222int")
            kwargs["queryset"] = CustomUser.objects.all()
        elif db_field.name == "utilisateur" and not request.user.is_superuser:
            print("here333int")
            kwargs["queryset"] = CustomUser.objects.filter(created_by=request.user)#employe id_utilisateur
        print("here444int")
        return super().formfield_for_foreignkey(db_field, request, **kwargs) """
        
    
    
    """def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__date_joined']
        else:
            return []
        
    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__nom', 'id_utilisateur__prenom', 'id_utilisateur__mail', 'id_utilisateur__tel', 'id_utilisateur__entreprise', 'id_utilisateur__fonction']
        else:
            return []  """

    
    

""" 
class CustomUserAdmin(admin.ModelAdmin):
    exclude = ('id_utilisateur',)#to not be able to change it manually
    list_display = ('nom', 'prenom', 'email', 'tel', 'entreprise', 'fonction', 'date_joined', 'id_utilisateur')
    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['entreprise', 'date_joined']
        else:
            return ['date_joined'] """
    

@admin.register(Employe)

class EmployeAdmin(admin.ModelAdmin):
    #exclude = ('id_integrateur', 'id_utilisateur',)#to not be able to change it manually
    """ 
    # affichage dans le portail qui remplace le def __str__(self):
    list_display = ('utilisateur', 'lieu_fonction', 'integrateur') """
    #exclude = ('integrateur',)
    
    
    #obj.integrateur du model "employe" bon ?
    #ajouter modified_by
    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            #print(obj.id_utilisateur, "obj.id_utilisateur")
            print("here2")
            obj.modified_by = str(request.user)
            obj.modified_date=datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => EmployeAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date=datetime.now()
            #print(obj.created_by, "obj.created_by de save_model => EmployeAdmin")
        """ print(request.user, " : integrateur = request.user")
        obj.integrateur_id = request.user
        print(request.user.tva_integrateur, " : integrateur = request.user.tva_integrateur")
        print("here4") """
        obj.save()
        
    # permet à l'utilisateur de voir uniquement les utilisateurs qu'il a créés    
    def get_queryset(self, request):
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return Employe.objects.all()
        print("here33")
        print("EMPLOYEADMIN filtre")
        return Employe.objects.filter(created_by=request.user)
    
    # permet à l'utilisateur de voir dans le droplist uniquement les utilisateurs qu'il a créés    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here111empl")
        if db_field.name == "utilisateur" and request.user.is_superuser:
            print("here222empl")
            kwargs["queryset"] = CustomUser.objects.all()
        elif db_field.name == "utilisateur" and not request.user.is_superuser:
            print("here333empl")
            kwargs["queryset"] = CustomUser.objects.filter(created_by=request.user)#employe id_utilisateur
        print("here444empl")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    #fonction permettant à n'afficher que l'integrateur 
    """ def formfield_for_foreignkey2(self, db_field, request, **kwargs):
        print("here111empl2")
        if db_field.name == "integrateur" and not request.user.is_superuser:
            print("here222empl2")
            kwargs["queryset"] = Integrateur.objects.filter(utilisateur=request.user)
        print("here333empl2")
        return super().formfield_for_foreignkey(db_field, request, **kwargs) """
        
    # permet à l'utilisateur de voir uniquement les CustomUsers qu'il a  créées
    
    
    """ def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__entreprise', 'id_utilisateur__date_joined']
        else:
            return ['id_utilisateur__date_joined']
        
    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__nom', 'id_utilisateur__prenom', 'id_utilisateur__mail', 'id_utilisateur__tel', 'id_utilisateur__entreprise', 'id_utilisateur__fonction']
        else:
            return [] """
    
    #ForeignKey drop list
    
    
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """exclude = ('id_utilisateur',)#to not be able to change it manually
    @admin.display(description='Employé')
    def employe(obj):
        return obj.id_employe 
    list_display = (nom_client, 'id_employe', 'adr_entreprise', 'num_contrat', 'num_licence', 'statut', 'id_utilisateur') """
    
    
    # permet à l'utilisateur de voir uniquement les CustomUsers qu'il a  créées
    """
    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__entreprise', 'statut', 'id_utilisateur']
        else:
            return ['id_utilisateur__date_joined', 'statut']
        
    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__nom', 'id_utilisateur__prenom', 'id_utilisateur__mail', 'id_utilisateur__tel', 'id_utilisateur__entreprise', 'id_utilisateur__fonction', 'id_utilisateur__id_utilisateur', 'id_utilisateur__date_joined']
        else:
            return ['id_utilisateur__nom', 'id_utilisateur__prenom', 'id_utilisateur__mail', 'id_utilisateur__tel', 'id_utilisateur__date_joined', 'id_utilisateur__fonction',]
    
    """
    
    
    @admin.register(Contrat)
    class ContratAdmin(admin.ModelAdmin):
        exclude = ('id_contrat',)
        list_display = ('num_contrat', 'client', 'date_creation')
    
    
    @admin.register(Contrat_detail)
    class Contrat_detailAdmin(admin.ModelAdmin):
        exclude = ('id_contrat_detail',)
        list_display = ('contrat', 'statut')