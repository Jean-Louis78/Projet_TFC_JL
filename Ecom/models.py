from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here. 
    
class Livreur(models.Model):
    id_liv=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=50)
    postnom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    telephone=PhoneNumberField()
    email=models.EmailField(max_length=254, null=False)
    adresse=models.CharField(max_length=200)
    password=models.CharField(max_length=15)
    date_ajout=models.DateTimeField(auto_now_add=True, editable=False)
    photo=models.ImageField(upload_to='Photo_Livreur/', blank=True)

    class Meta:
        db_table = 'tLivreur'
        managed = True
        verbose_name = 'Livreur'
        verbose_name_plural = 'Livreurs'
        ordering = ['date_ajout']
    
    def __str__(self) -> str:
        return (f"{self.nom} {self.postnom} {self.prenom}")

class Categorie_Produit(models.Model):
    id_cat=models.AutoField(primary_key=True)
    designation=models.CharField(max_length=50)

    class Meta:
        db_table = 'tCategorie'
        managed = True
        verbose_name = 'Catégorie Produit'
        verbose_name_plural = 'Catégories Produit'
        ordering = ['id_cat']

    def __str__(self) -> str:
        return self.designation

class Produit(models.Model):
    id_prod=models.AutoField(primary_key=True)
    designation=models.CharField(max_length=50)
    slug= models.SlugField(max_length=50)
    categorie=models.ForeignKey(Categorie_Produit, on_delete=models.CASCADE)
    prix_unitaire=models.FloatField(default=0.0)
    description=models.TextField()
    date_ajout=models.DateTimeField(auto_now_add=True, editable=False)
    image=models.ImageField(upload_to='images_produits/', blank=True)

    class Meta:
        db_table = 'tproduit'
        managed = True
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['date_ajout']
        
    def __str__(self) -> str:
        return self.designation    

class Vente(models.Model):
    id_Vente=models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit=models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite=models.PositiveIntegerField(default=1)
    prix_total=models.FloatField(editable=False)
    date_vente=models.DateTimeField(editable=False, auto_now_add=True)    

    def save(self, *args, **kwargs):
        self.prix_total = self.produit.prix_unitaire * float(self.quantite)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.produit.designation} :  ({self.quantite})")

    class Meta:
        db_table = 'tVente'
        managed = True
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['date_vente']
    
class Commande(models.Model):
    id_cmd=models.AutoField(primary_key=True)
    vente=models.ForeignKey(Vente, verbose_name=("Vente"), on_delete=models.CASCADE)    
    livreur=models.ForeignKey(Livreur, on_delete=models.CASCADE, default=None, blank=True, null=True)
    etat_cmd=models.CharField(max_length=20, default='En Attente')
    date_ajout=models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'tCommande'
        managed = True
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['date_ajout']

    def __str__(self):
        return (f"{self.vente.user.first_name} {self.vente.user.last_name} {self.vente.user.username}")

class Approvisionnement(models.Model):
    id_approv=models.AutoField(primary_key=True)
    produit=models.ForeignKey(Produit, verbose_name=("Produit"), on_delete=models.CASCADE)
    quantite_approv=models.PositiveIntegerField()
    date_approv=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tApprovisionnement'
        managed = True
        verbose_name = 'Approvisionnement'
        verbose_name_plural = 'Approvisionnements'
        ordering = ['date_approv']
    
class Stock(models.Model):
    id_stock=models.AutoField(primary_key=True)
    produit=models.OneToOneField(Produit, on_delete=models.CASCADE)
    stock_dispo=models.IntegerField()

    def save(self, *args, **kwargs):
        approvisionnement=Approvisionnement.objects.filter(produit=self.produit)
        total_approv=approvisionnement.aggregate(models.Sum('quantite_approv'))['quantite_approv__sum'] or 0
        vente=Vente.objects.filter(produit=self.produit)
        total_vente=vente.aggregate(models.Sum('quantite'))['quantite__sum'] or 0
        self.stock_dispo = total_approv - total_vente
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tSock'
        managed = True
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['id_stock']

class Livraison(models.Model):
    id=models.AutoField(primary_key=True)
    commande=models.ForeignKey(Commande, on_delete=models.CASCADE)
    etat_livraison=models.CharField(max_length=20, default='En Attente')
    date_livraison=models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        db_table = 'tLivraison'
        managed = True
        verbose_name = 'Livraison'
        verbose_name_plural = 'Livraisons'
        ordering = ['id']

    def __str__(self):
        return (f"{self.commande.vente.user.first_name} {self.commande.vente.user.last_name} {self.commande.vente.user.username}")
