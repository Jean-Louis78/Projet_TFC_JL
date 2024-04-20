from django.db.models.signals import *
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Vente)
def create_commande(sender, instance, created, **kwargs):
    if created:
        Commande.objects.create(vente=instance)

@receiver(post_save, sender=Approvisionnement)
def update_stock_on_approvisionnement(sender, instance, created, **kwargs):
    if created and instance.quantite_approv > 0:
        stock, created = Stock.objects.get_or_create(produit=instance.produit)
        stock.stock_dispo += instance.quantite_approv
        stock.save()

@receiver(pre_save, sender=Vente)
def update_stock_on_sale(sender, instance, **kwargs):
    if instance.quantite > 0:
        stock = Stock.objects.get(produit=instance.produit)
        if stock.stock_dispo > 0 and stock.stock_dispo >= instance.quantite:
            stock.stock_dispo -= instance.quantite
            stock.save()
        else:
            raise ValueError('Stock épuisé')
        
    else:
        raise ValueError('Quantité de vente invalide')

