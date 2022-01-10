from django.contrib import admin
from .models import (
    Resultat,
    CustomUser,
    Integrateur,
    Employe,
    Client,
    Contrat,
    Contrat_detail,
    Licence,
)
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django import forms

# Register your models here.


# je crois que je devrais ajouter des autorisations pour cette page car je ne peux rien y voir, sauf lorsque
# je vais encore sur /admin/



# new custom user
@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                # if client, sans demande de mdp lors de l'enregistrement
                "fields": (
                    "nom",
                    "prenom",
                    "email",
                    "password1",
                    "password2",
                    "tel",
                    "entreprise",
                    "is_active",
                    "is_staff",
                    "groups",
                ),  # Création d'un nouveau utilisateur via "Utilisateurs  +ADD"
            },
        ),
    )
    # exclude = ('id_utilisateur', )
    list_display = (
        "nom",
        "prenom",
        "entreprise",
        "email",
        "fonction",
        "tel",
        "is_staff",
        "created_date",
        "created_by",
    )  #
    list_filter = (
        "entreprise",
        "groups",
        "is_staff",
        "date_joined",
    )
    search_fields = (
        "email",
        "nom",
        "prenom",
        "tel",
        "entreprise",
    )
    ordering = ("email",)

    # permet de cacher à tous les utilisateurs sauf admin, la boxcase de "is superuser"
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        else:
            perm_fields = ("is_active", "is_staff", "groups")

        return [
            (None, {"fields": ("email", "password")}),
            (
                _("Personal info"),
                {"fields": ("nom", "prenom", "tel", "entreprise")},
            ),  # email enlevé | champs lors de la modification d'un utilisateur
            (_("Permissions"), {"fields": perm_fields}),
        ]

    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            print("here2")
            # print(obj.id_utilisateur, "obj.id_utilisateur")
            obj.modified_by = str(
                request.user
            )  # request.user est une adr email, str() le force à etre charField
            obj.modified_date = datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => CustomUserAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date = datetime.now()
            print(obj.created_by, "obj.created_by de save_model => CustomUserAdmin")
        print("here4")
        obj.save()

        # permet à l'user de voir uniquement les utilisateurs qu'il a créées DANS UTILISATEURS : pour tout le monde

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


# admin.site.unregister(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUser, CustomUserAdmin)

# custom colonnes - essayer d'utiliser : Integrateur.nom
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


@admin.register(Integrateur)
class IntegrateurAdmin(admin.ModelAdmin):
    
    list_display = ["get_nom", "get_prenom", "get_entreprise", "get_email", "get_tel", "tva_integrateur"]
    
    
    def get_nom(self, obj):
        return obj.utilisateur.nom
    get_nom.admin_order_field  = 'utilisateur__nom'  #Allows column order sorting
    get_nom.short_description = 'Nom'  #Renames column head
    
    def get_prenom(self, obj):
        return obj.utilisateur.prenom
    get_prenom.admin_order_field  = 'utilisateur__prenom'  #Allows column order sorting
    get_prenom.short_description = 'Prenom'  #Renames column head
    
    def get_entreprise(self, obj):
        return obj.utilisateur.entreprise
    get_entreprise.admin_order_field  = 'utilisateur__entreprise'  #Allows column order sorting
    get_entreprise.short_description = 'Entreprise'  #Renames column head
    
    def get_email(self, obj):
        return obj.utilisateur.email
    get_email.admin_order_field  = 'utilisateur__email'  #Allows column order sorting
    get_email.short_description = 'Email'  #Renames column head
    
    def get_tel(self, obj):
        return obj.utilisateur.tel
    get_tel.admin_order_field  = 'utilisateur__tel'  #Allows column order sorting
    get_tel.short_description = 'Téléphone'  #Renames column head

    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            print("here2")
            # print(obj.id_utilisateur, "obj.id_utilisateur")
            obj.modified_by = str(
                request.user
            )  # request.user est une adr email, str() le force à etre charField
            obj.modified_date = datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => IntegrateurAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date = datetime.now()
            print(obj.created_by, "obj.created_by de save_model => IntegrateurAdmin")
        print("here4")
        obj.save()

    # permet à l'user de voir uniquement les utilisateurs qu'il a créées    , osef car integrateur : il n'a pas accès aux integrateurs de toute facon
    """ def get_queryset(self, request):
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return Integrateur.objects.all()
        print("here33")
        print("INTEGRATEURADMIN filtre")
        return Integrateur.objects.filter(created_by=request.user) """

    # ne sert à rien ? car lorsque je me co en tant qu'int, je n'ai pas besoin de créer d'autres int.
    """ def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here111int")
        if db_field.name == "integrateur" and request.user.is_superuser:
            print("here222int")
            kwargs["queryset"] = Integrateur.objects.all()
        elif db_field.name == "integrateur" and not request.user.is_superuser:
            print("here333int")
            kwargs["queryset"] = Integrateur.objects.filter(created_by=request.user)#employe id_utilisateur
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

"""Cleaning data and raising errors for Employe Model"""
""" class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__'
    def equals_entreprise(self):
        entreprise = self.cleaned_data['entreprise']
        if Employe.utilisateur.entreprise != Employe.integrateur.utilisateur.entreprise:
            raise forms.ValidationError("Le nom de l'entreprise ne correspond pas avec celui de votre intégrateur")
        return entreprise """


@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    # readonly_fields = ('integrateur',)#to not be able to change it manually

    list_display = ["get_nom", "get_prenom", "get_entreprise", "get_email", "get_tel", "created_by" ]
    
    #form = EmployeForm #lien vers le formulaire
    
    def get_nom(self, obj):
        return obj.utilisateur.nom
    get_nom.admin_order_field  = 'utilisateur__nom'  #Allows column order sorting
    get_nom.short_description = 'Nom'  #Renames column head
    
    def get_prenom(self, obj):
        return obj.utilisateur.prenom
    get_prenom.admin_order_field  = 'utilisateur__prenom'  #Allows column order sorting
    get_prenom.short_description = 'Prenom'  #Renames column head

    def get_email(self, obj):
        return obj.utilisateur.email
    get_email.admin_order_field  = 'utilisateur__email'  #Allows column order sorting
    get_email.short_description = 'Email'  #Renames column head
    
    def get_entreprise(self, obj):
        return obj.utilisateur.entreprise
    get_entreprise.admin_order_field  = 'utilisateur__entreprise'  #Allows column order sorting
    get_entreprise.short_description = 'Entreprise'  #Renames column head
    
    def get_tel(self, obj):
        return obj.utilisateur.tel
    get_tel.admin_order_field  = 'utilisateur__tel'  #Allows column order sorting
    get_tel.short_description = 'Téléphone'  #Renames column head
    
    # Save models
    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            # print(obj.id_utilisateur, "obj.id_utilisateur")
            print("here2")
            """ if obj.utilisateur.entreprise != obj.integrateur.utilisateur.entreprise:
                print("erreur modif equald entreprises : ", obj.utilisateur.entreprise, obj.integrateur.utilisateur.entreprise) """
            #obj.utilisateur.entreprise = obj.integrateur.utilisateur.entreprise
            #print("MODIF j'oblige a mettre la meme entr : ", obj.utilisateur.entreprise, obj.integrateur.utilisateur.entreprise)
            obj.modified_by = str(request.user)
            obj.modified_date = datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => EmployeAdmin")
        if not change:
            print("here3")
            """ if obj.utilisateur.entreprise != obj.integrateur.utilisateur.entreprise:
                print("erreur equald entreprises : ", obj.utilisateur.entreprise, obj.integrateur.utilisateur.entreprise) """
            #obj.utilisateur.entreprise = obj.integrateur.utilisateur.entreprise
            #print("CREATION j'oblige a mettre la meme entr : ", obj.utilisateur.entreprise, obj.integrateur.utilisateur.entreprise)
            obj.created_by = request.user
            obj.created_date = datetime.now()
            # print(obj.created_by, "obj.created_by de save_model => EmployeAdmin")
        """ print(request.user, " : integrateur = request.user")
        obj.integrateur_id = request.user
        print(request.user.tva_integrateur, " : integrateur = request.user.tva_integrateur")
        print("here4") """
        """ obj.utilisateur.entreprise = obj.integrateur.utilisateur.entreprise
        print("FIN j'oblige a mettre la meme entr : ", obj.utilisateur.entreprise, obj.integrateur.utilisateur.entreprise) """
        obj.save()

    # permet à l'utilisateur de voir uniquement les utilisateurs qu'il a créés
    # Filter the employees in "Employee" list
    def get_queryset(self, request):
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return Employe.objects.all()
        print("here33")
        print("EMPLOYEADMIN filtre")
        return Employe.objects.filter(created_by=request.user)

    # permet à l'utilisateur de voir dans le droplist uniquement les utilisateurs qu'il a créés
    # Filter the "Utilisateur" field droplist to show only the users created by request.user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here111empl")
        if db_field.name == "utilisateur" and request.user.is_superuser:
            print("here222empl")
            kwargs["queryset"] = CustomUser.objects.all()
        elif db_field.name == "utilisateur" and not request.user.is_superuser:
            print("here333empl")
            kwargs["queryset"] = CustomUser.objects.filter(
                created_by=request.user
            )  # employe id_utilisateur
        elif db_field.name == "integrateur" and not request.user.is_superuser:
            print("here333empl")
            print("test création Employe :", Integrateur.objects.filter(utilisateur=request.user))
            kwargs["queryset"] = Integrateur.objects.filter(utilisateur=request.user)
        print("here444empl")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # trouver comment choisir automatiquement request.user au champ integrateur même s'il est caché/read-only. Si r-o, alors il ne tient plus compte du initial
    """ def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("droplistforfk enter")
        if db_field.name == "integrateur":
            kwargs["initial"] = Integrateur.objects.filter(
                utilisateur=request.user
            )  # choix initial (le "-------" est remplacé)
            print("2e fonction bon")
            return db_field.formfield(**kwargs)
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

    # ForeignKey drop list



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["get_nom", "get_prenom", "get_entreprise", "get_email", "get_tel", "tva_cli", "employe", "get_empl_entreprise", "created_by"]
    
    def get_nom(self, obj):
        return obj.utilisateur.nom
    get_nom.admin_order_field  = 'utilisateur__nom'  #Allows column order sorting
    get_nom.short_description = 'Nom'  #Renames column head
    
    def get_prenom(self, obj):
        return obj.utilisateur.prenom
    get_prenom.admin_order_field  = 'utilisateur__prenom'  #Allows column order sorting
    get_prenom.short_description = 'Prenom'  #Renames column head

    def get_email(self, obj):
        return obj.utilisateur.email
    get_email.admin_order_field  = 'utilisateur__email'  #Allows column order sorting
    get_email.short_description = 'Email'  #Renames column head
    
    def get_entreprise(self, obj):
        return obj.utilisateur.entreprise
    get_entreprise.admin_order_field  = 'utilisateur__entreprise'  #Allows column order sorting
    get_entreprise.short_description = 'Entreprise'  #Renames column head
    
    def get_empl_entreprise(self, obj):
        return obj.employe.utilisateur.entreprise
    get_empl_entreprise.admin_order_field  = 'employe__utilisateur__entreprise'  #Allows column order sorting
    get_empl_entreprise.short_description = 'Entreprise de l\'employé'  #Renames column head
    
    def get_tel(self, obj):
        return obj.utilisateur.tel
    get_tel.admin_order_field  = 'utilisateur__tel'  #Allows column order sorting
    get_tel.short_description = 'Téléphone'  #Renames column head
    
    # Save models
    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            # print(obj.id_utilisateur, "obj.id_utilisateur")
            print("here2")
            obj.modified_by = str(request.user)
            obj.modified_date = datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => EmployeAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date = datetime.now()
            # print(obj.created_by, "obj.created_by de save_model => EmployeAdmin")
        
        obj.save()
        
# permet à l'utilisateur de voir uniquement les contrats qu'il a créés
    def get_queryset(self, request):
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return Client.objects.all()
        else:
            # Affiche les clients créés par les employés provenant d'un MEME intégrateur
            for i in Employe.objects.filter(created_by = request.user):
                print("employés : ", i.utilisateur.email)
                mail = i.utilisateur.email
                e = Client.objects.filter(created_by = mail)
                print("clients : ", e)
            print("clients créés par les employeurs d'un même intégrateur : ", Client.objects.filter(created_by = mail))
            return Client.objects.filter(created_by=mail)
        #AFFICHER LES CLIENTS CREES PAR LES EMPLOYES CONNECTES MNT
    

    # permet à l'utilisateur de voir dans le droplist uniquement les utilisateurs qu'il a créés
    # Filter the "Utilisateur" field droplist to show only the users created by request.user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here111empl")
        if db_field.name == "employe" and request.user.is_superuser:
            print("here222empl")
            kwargs["queryset"] = Employe.objects.all()
        elif db_field.name == "employe" and not request.user.is_superuser:
            #emails = Integrateur.objects.all()
            #for integrateur in emails:
            #    print("emails : ", integrateur.utilisateur)
            print("here333empl")
            test = request.user
            print("test :", Employe.objects.filter(utilisateur=request.user))
            kwargs["queryset"] = Employe.objects.filter(utilisateur=request.user)  # employe id_utilisateur
        elif db_field.name == "utilisateur" and not request.user.is_superuser:
            #emails = Integrateur.objects.all()
            #for integrateur in emails:
            #    print("emails : ", integrateur.utilisateur)
            print("here333empl")
            test = request.user
            print("test :", CustomUser.objects.filter(created_by=request.user))
            kwargs["queryset"] = CustomUser.objects.filter(created_by=request.user)
        print("here444empl")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




    """exclude = ('id_utilisateur',)#to not be able to change it manually
    @admin.display(description='Employé')
    def employe(obj):
        return obj.id_employe
    list_display = (nom_client, 'id_employe', 'adr_entreprise', 'num_contrat', 'num_licence', 'statut', 'id_utilisateur')"""

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






"""
                                                    Inlines : permet de regrouper plusieurs models en un dans la page Django Admin.
                                                    """

"""         CONTRAT       """
class Contrat_detailInline(admin.TabularInline):
    model = Contrat_detail
    can_delete = False

class LicenceInline(admin.TabularInline):
    model = Licence
    can_delete = False

@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    inlines = [Contrat_detailInline, LicenceInline]
    
    list_display = ["get_num_contrat", "get_nom", "get_prenom", "created_by", "modified_by"]
    
    def get_num_contrat(self, obj):
        return obj.num_contrat
    get_num_contrat.admin_order_field  = 'num_contrat'  #Allows column order sorting
    get_num_contrat.short_description = 'Numéro du contrat'  #Renames column head
    
    def get_nom(self, obj):
        return obj.client.utilisateur.nom
    get_nom.admin_order_field  = 'client__utilisateur__nom'  #Allows column order sorting
    get_nom.short_description = 'Nom du client'  #Renames column head
    
    def get_prenom(self, obj):
        return obj.client.utilisateur.prenom
    get_prenom.admin_order_field  = 'client__utilisateur__prenom'  #Allows column order sorting
    get_prenom.short_description = 'Prénom du client'  #Renames column head
    
    
# Save models
    def save_model(self, request, obj, form, change):
        print("here1")
        if change:
            # print(obj.id_utilisateur, "obj.id_utilisateur")
            print("here2")
            obj.modified_by = str(request.user)
            obj.modified_date = datetime.now()
            print(obj.modified_by, "obj.modified_by de save_model => EmployeAdmin")
        if not change:
            print("here3")
            obj.created_by = request.user
            obj.created_date = datetime.now()
            # print(obj.created_by, "obj.created_by de save_model => EmployeAdmin")
        
        obj.save()

# permet à l'utilisateur de voir uniquement les contrats qu'il a créés
    def get_queryset(self, request):#obj
        print("here11")
        if request.user.is_superuser:
            print("here22")
            return Contrat.objects.all()
        #elif Integrateur.utilisateur.email == request.user:
            #emailtest = Contrat.client.employe.integrateur.utilisateur.email
            #print("here33")
        #else:
            #print("empluser", Integrateur.objects.get(utilisateur=request.user))
            #intInfo = Integrateur.objects.get(utilisateur=request.user)
            #allentrINT = Integrateur.objects.all()
            #allentrEMPL = Employe.objects.all()
            #print(allentrINT, allentrEMPL)
            """ for i in allentrINT:
                if Employe.objects.get(utilisateur=i):
                    print("ok") """
        print("here44")    
        return Contrat.objects.filter(created_by=request.user)


    # permet à l'utilisateur de voir dans le droplist uniquement les utilisateurs qu'il a créés
    # Filter the "Utilisateur" field droplist to show only the users created by request.user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("here111empl")
        if db_field.name == "client" and request.user.is_superuser:
            print("here222empl")
            kwargs["queryset"] = Client.objects.all()
        elif db_field.name == "client" and not request.user.is_superuser:
            print("here333empl")
            kwargs["queryset"] = Client.objects.filter(created_by=request.user)  # employe id_utilisateur
        print("here444empl")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)






@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ["id_resultat", "nb_h_tot_prest_ann"]