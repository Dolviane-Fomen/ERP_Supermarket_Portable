from django.contrib import admin
from .models import (
    Agence, Compte, Employe, Client, Fournisseur, Famille, TypeVente, Article,
    Caisse, SessionCaisse, FactureVente, LigneFactureVente
)

# Configuration de l'interface d'administration

@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display = ['nom_agence', 'adresse']
    search_fields = ['nom_agence', 'adresse']
    list_filter = ['nom_agence']

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ['numero_compte', 'nom', 'prenom', 'user', 'agence', 'actif']
    search_fields = ['numero_compte', 'nom', 'prenom', 'user__username']
    list_filter = ['agence', 'actif']
    raw_id_fields = ['user', 'agence']

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ['compte', 'poste', 'date_embauche']
    search_fields = ['compte__nom', 'compte__prenom', 'poste']
    list_filter = ['poste', 'date_embauche']
    raw_id_fields = ['compte']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['intitule', 'telephone', 'email', 'agence']
    search_fields = ['intitule', 'telephone', 'email']
    list_filter = ['agence']

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ['intitule', 'telephone', 'email', 'agence']
    search_fields = ['intitule', 'telephone', 'email']
    list_filter = ['agence']

@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
    list_display = ['intitule', 'code']
    search_fields = ['intitule', 'code']

@admin.register(TypeVente)
class TypeVenteAdmin(admin.ModelAdmin):
    list_display = ['intitule', 'prix', 'article']
    search_fields = ['intitule', 'article__designation']
    list_filter = ['article__categorie']
    raw_id_fields = ['article']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['reference_article', 'designation', 'categorie', 'prix_vente', 'stock_actuel', 'agence']
    search_fields = ['reference_article', 'designation']
    list_filter = ['categorie', 'agence']
    raw_id_fields = ['categorie', 'agence']

@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    list_display = ['numero_caisse', 'nom_caisse', 'solde_actuel', 'agence']
    search_fields = ['numero_caisse', 'nom_caisse']
    list_filter = ['agence']

@admin.register(SessionCaisse)
class SessionCaisseAdmin(admin.ModelAdmin):
    list_display = ['caisse', 'employe', 'date_ouverture', 'date_fermeture', 'statut', 'agence']
    search_fields = ['caisse__nom_caisse', 'employe__compte__nom']
    list_filter = ['statut', 'date_ouverture', 'agence']
    raw_id_fields = ['caisse', 'employe', 'utilisateur', 'agence']

class LigneFactureVenteInline(admin.TabularInline):
    model = LigneFactureVente
    extra = 1
    fields = ['article', 'designation', 'quantite', 'prix_unitaire', 'prix_total']

@admin.register(FactureVente)
class FactureVenteAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'client', 'nom_vendeuse', 'nette_a_payer', 'date', 'en_attente', 'agence']
    search_fields = ['numero_ticket', 'client__intitule', 'nom_vendeuse']
    list_filter = ['en_attente', 'date', 'agence']
    raw_id_fields = ['client', 'caisse', 'vendeur', 'agence']
    inlines = [LigneFactureVenteInline]
    readonly_fields = ['numero_ticket']


# Configuration du site d'administration
admin.site.site_header = "ERP Supermarket - Administration"
admin.site.site_title = "ERP Supermarket Admin"
admin.site.index_title = "Gestion de l'ERP Supermarket"