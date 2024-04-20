from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Livreur)
class TabLivreur(admin.ModelAdmin):
    list_display = ('id_liv', 'nom', 'postnom', 'prenom', 'adresse', 'telephone', 'email', 'date_ajout')
    list_filter = ('date_ajout',)

@admin.register(Categorie_Produit)
class TabCategorie(admin.ModelAdmin):
    list_display = ('id_cat', 'designation')

@admin.register(Produit)
class TabProduit(admin.ModelAdmin):
    list_display = ('id_prod', 'designation', 'categorie', 'prix_unitaire', 'date_ajout')
    list_filter = ('categorie',)

@admin.register(Vente)
class TabVente(admin.ModelAdmin):
    list_display = ('id_Vente', 'user', 'produit', 'quantite', 'prix_total', 'date_vente')
    list_filter = ('date_vente',)

@admin.register(Approvisionnement)
class TabCApprovisionnement(admin.ModelAdmin):
    list_display = ('id_approv', 'produit', 'quantite_approv', 'date_approv')
    list_filter = ('date_approv',)

@admin.register(Stock)
class TabStock(admin.ModelAdmin):
    list_display = ('id_stock', 'produit', 'stock_dispo')
    list_filter = ('produit',)

@admin.register(Commande)
class TabCommande(admin.ModelAdmin):
    list_display = ('id_cmd', 'livreur', 'vente', 'etat_cmd', 'date_ajout')
    list_filter = ('date_ajout',)

@admin.register(Livraison)
class TabLivraison(admin.ModelAdmin):
    list_display = ('id', 'commande', 'etat_livraison', 'date_livraison')
    list_filter = ('etat_livraison',)