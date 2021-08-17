from django.contrib import admin
from .models import Personne, Integrateur, Employe, Client
from django.contrib.auth.models import User
# Register your models here.

""" class IntAdminSite(admin.AdminSite):
    site_header = 'Administration pour integrateurs' """

#je crois que je devrais ajouter des autorisations pour cette page car je ne peux rien y voir, sauf lorsque
#je vais encore sur /admin/

""" intadmin = IntAdminSite(name='intadmin')

class EmployeAdminSite(admin.AdminSite):
    site_header = 'Administration pour employés'

employeadmin = EmployeAdminSite(name='employeadmin') """

""" intadmin.register(Integrateur) """#???


""" class EmployeAdmin(admin.ModelAdmin):
    exclude = ('author',)#to not be able to change it manually
    list_display = ('id_employe', 'id_personne', 'id_integrateur', 'lieu_fonction', 'author')
    
    #save the "last author" who created the employee so I can filter by this informations
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(EmployeAdmin, self).save_model(request, obj, form, change)
        
    def get_queryset(self, request):
        qs = super(EmployeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user) """
    
    #def queryset(self, request):
        #return Employe.objects.filter(author=request.user)#filters by request.user
        
        
""" class ClientAdmin(admin.ModelAdmin):
    #permet d'indiquer l'auteur automatiquement et non manuellement
    exclude = ('author',)#permet d'indiquer l'auteur automatiquement et non manuellement
    list_display = ('id_client', 'id_personne', 'id_employe', 'adr_entreprise', 'num_contrat', 'num_licence', 'author')

    #def queryset(self, request):
        #qs = super(ClientAdmin, self).queryset(request)
        #if request.user.is_superuser:
            #return qs
        #return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ClientAdmin, self).save_model(request, obj, form, change)
    
    
    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user) """
    
""" def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save() """
        
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    exclude = ('author',)#to not be able to change it manually
    list_display = ('id_employe', 'id_personne', 'id_integrateur', 'lieu_fonction', 'author')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
        
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Employe.objects.all()
        print(Employe.objects.filter(author=request.user))
        return Employe.objects.filter(author=request.user)
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(id_employe__author=request.user)
        
#mettre en place vérificateur pr champ tva + tel

admin.site.register(Personne)
admin.site.register(Integrateur)
#admin.site.register(Employe)
#admin.site.register(Client, ClientAdmin)
""" admin.site.register(Contrat)
admin.site.register(Licence) """