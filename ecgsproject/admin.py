from django.contrib import admin
from .models import Resultat, CustomUser, Integrateur, Employe, Client, Contrat, Contrat_detail, Licence
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
# Register your models here.


#je crois que je devrais ajouter des autorisations pour cette page car je ne peux rien y voir, sauf lorsque
#je vais encore sur /admin/



# new custom user
@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        )
    #exclude = ('id_utilisateur', )
    list_display = ('nom', 'prenom', 'email', 'is_staff')#
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
    
    """ def save_model(self, request, obj, form, change):
        if not change:
            obj.id_utilisateur = request.user
        obj.save()
    
    #ces deux fonctions permettent à l'utilisateur de voir uniquement les utilisateurs créés par lui même    
    def get_queryset(self, request):
        queryset = super(CustomUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return CustomUser.objects.all()
        print(CustomUser.objects.filter(email=request.user))
        return CustomUser.objects.filter(email=request.user) """
    
    """ def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['entreprise', 'date_joined', 'is_active', 'is_staff', 'is_superuser']#
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
@admin.register(Contrat)
@admin.register(Contrat_detail)
@admin.register(Licence)
@admin.register(Integrateur)


class IntegrateurAdmin(admin.ModelAdmin):    
    """list_display = (nom_int, int_entr, 'adr_entreprise', 'lieu_fonction')
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__date_joined']
        else:
            return []
        
    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ['id_utilisateur__nom', 'id_utilisateur__prenom', 'id_utilisateur__mail', 'id_utilisateur__tel', 'id_utilisateur__entreprise', 'id_utilisateur__fonction']
        else:
            return [] 
"""
    
    

""" 
class CustomUserAdmin(admin.ModelAdmin):
    exclude = ('id_utilisateur',)#to not be able to change it manually
    list_display = ('nom', 'prenom', 'email', 'tel', 'entreprise', 'fonction', 'date_joined', 'id_utilisateur')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.id_utilisateur = request.user
        obj.save()
    
    # permet à l'utilisateur de voir uniquement les CustomUsers qu'il a créées
    def get_queryset(self, request):
        if request.user.is_superuser:
            return CustomUser.objects.all()
        print(CustomUser.objects.filter(id_utilisateur=request.user))
        return CustomUser.objects.filter(id_utilisateur=request.user)
    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['entreprise', 'date_joined']
        else:
            return ['date_joined'] """
    

@admin.register(Employe)

class EmployeAdmin(admin.ModelAdmin):
    #exclude = ('id_integrateur', 'id_utilisateur',)#to not be able to change it manually
    """ list_display = (nom_empl, empl_entr, 'lieu_fonction', 'id_integrateur')
    
    
        def save_model(self, request, obj, form, change):
        if not change:
            obj.id_utilisateur = request.user
        obj.save()"""
        
    # permet à l'utilisateur de voir uniquement les CustomUsers qu'il a  créées
    """ def get_queryset(self, request):
        queryset = super(EmployeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return Employe.objects.all()
        print(Employe.objects.filter(id_utilisateur=request.user))
        return Employe.objects.filter(id_utilisateur=request.user)  """
    
    """ def get_queryset(self, request):
        if request.user.is_superuser:
            return Employe.objects.all()
        print(Employe.objects.filter(id_integrateur=request.user))
        return Employe.objects.filter(id_integrateur=request.user) """
    
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
    """ def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_utilisateur":
            kwargs["queryset"] = CustomUser.objects.filter(id_utilisateur=request.user)#employe id_utilisateur
        return super().formfield_for_foreignkey(db_field, request, **kwargs) """
    
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """exclude = ('id_utilisateur',)#to not be able to change it manually
    @admin.display(description='Employé')
    def employe(obj):
        return obj.id_employe 
    list_display = (nom_client, 'id_employe', 'adr_entreprise', 'num_contrat', 'num_licence', 'statut', 'id_utilisateur') """
    
    """ def save_model(self, request, obj, form, change):
        if not change:
            obj.id_utilisateur = request.user
        obj.save()
    
    # permet à l'utilisateur de voir uniquement les CustomUsers qu'il a  créées
    def get_queryset(self, request):
        queryset = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        print(Client.objects.filter(id_utilisateur=request.user))
        return Client.objects.filter(id_utilisateur=request.user)
    
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
    
    #ForeignKey drop list
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_utilisateur":
            kwargs["queryset"] = CustomUser.objects.filter(id_utilisateur=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs) """
    