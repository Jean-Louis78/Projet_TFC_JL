from io import BytesIO
import json
from django.shortcuts import  get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
import os
from Accounts.models import Custommer_User
from .models import *
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import datetime



# Create your views here.
# ===============================================================================================================================================
#                                                                    PRODUITS
# ===============================================================================================================================================
def index(request):
    produit=Produit.objects.all()
    commandes = Commande.objects.filter(etat_cmd = 'En Attente').count
    
    if request.method == "POST":
        search = request.POST.get('search')
        produit = produit.filter(
            Q(designation__icontains = search)
            )
    
    context={
        "produit": produit,
        'commandes': commandes
        }
    return render(request, 'BASE/base.html', context)

def detail_produit(request, slug):
    produit= get_object_or_404(Produit, slug=slug)
    context={"produit":produit}
    return render(request, 'PRODUCTS/detail_produit.html', context)

def add_product(request):
    categories = Categorie_Produit.objects.all().order_by('id_cat')
    if request.method == "POST":
        designation = request.POST.get('designation')
        slug = request.POST.get('slug')
        cat = request.POST.get('categorie')
        prix_unitaire = request.POST.get('prix-unitaire')
        image = request.FILES["photo"]
        description = request.POST.get('description')

        categorie = get_object_or_404(Categorie_Produit, pk=cat)
        product_price = prix_unitaire.replace(',', '.').strip()
        if Produit.objects.filter(
            designation=designation, 
            slug=slug,
            categorie=categorie,
            prix_unitaire=product_price,
            image=image,
            description=description
            ):
            messages.error(request, "Existe déjà")
        else:
            products = Produit.objects.create(
                designation=designation, 
                slug=slug,
                categorie=categorie,
                prix_unitaire=product_price,
                image=image,
                description=description
                )
            products.save()
            messages.success(request, "Ajouté avec succès")
    return render(request, 'PRODUCTS/add-product.html',{'categories':categories})

def update_product(request, id_prod):
    produit = get_object_or_404(Produit, id_prod=id_prod)
    categories = Categorie_Produit.objects.all().order_by('id_cat')
    context = {
        'produits':produit,
        'categories':categories
    }
    return render(request, 'PRODUCTS/update-product.html', context)

def record_update_product(request, id_prod):
    if request.method == 'POST':
        designation = request.POST.get('designation')
        slug = request.POST.get('slug')
        cat = request.POST.get('categorie')
        prix_unitaire = request.POST.get('prix-unitaire')
        image = request.FILES.get('photo')
        description = request.POST.get('description')

        categorie = get_object_or_404(Categorie_Produit, pk=cat)
        getproduit = Produit.objects.get(id_prod=id_prod)
        product_price = prix_unitaire.replace(',', '.').strip()

        if Produit.objects.filter(
            id_prod = id_prod,
            designation=designation, 
            slug=slug,
            categorie=categorie,
            prix_unitaire=product_price,
            image=image,
            description=description
            ):
            messages.error(request, "Existe déjà")
        else:
            if image:
                form = Produit(
                    id_prod = id_prod,
                    designation=designation, 
                    slug=slug,
                    categorie=categorie,
                    prix_unitaire=product_price,
                    image=image,
                    description=description,
                    date_ajout=getproduit.date_ajout 
                )
                form.save()
                messages.success(request, "Modifié avec succès")
                return redirect('display-product')
            else:
                form = Produit(
                    id_prod = id_prod,
                    designation=designation, 
                    slug=slug,
                    categorie=categorie,
                    prix_unitaire=product_price,
                    image=getproduit.image,
                    description=description,
                    date_ajout=getproduit.date_ajout 
                )
                form.save()
                messages.success(request, "Modifié avec succès")
                return redirect('display-product')
    return render(request, 'PRODUCTS/update-product.html')

def delete_product(request, id_prod):
    obj=Produit.objects.get(id_prod=id_prod)
    if obj:
        obj.delete()
        messages.success(request, "Effacé avec succès")
        return redirect('display-product')
    else:
        return redirect('page-404')
# ===============================================================================================================================================

# ============================================================================================================================================
#                                                   APPROVISIONNEMENT
# ======================================================================================================================================
@transaction.atomic
def create_approvisionnement(request):
    produit=Produit.objects.all()
    approv=Approvisionnement.objects.all().order_by('-date_approv')
    context={
        'produit': produit,
        'approvisionnements':approv
        }
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite_approv = request.POST.get('quantite_approv')

        produit = get_object_or_404(Produit, pk=produit_id)

        with transaction.atomic():
            approvisionnement = Approvisionnement.objects.create(
                produit=produit,
                quantite_approv=int(quantite_approv)
            )

            stock, created = Stock.objects.get_or_create(produit=produit)
            stock.stock_dispo += int(approvisionnement.quantite_approv)
            stock.save()
            messages.success(request, "Approvisionnement effectué avec succès")

    return render(request, 'BASE/Approvisionnement.html', context)
# ===========================================================================================================================================



#============================================================================================================================================
#                                                                       VENTE
#============================================================================================================================================

def sales(request):
    vente = Vente.objects.all().order_by('-date_vente')
    context = {
        'ventes': vente
    }
    return render(request, 'BASE/ventes.html', context)
#===============================================================================================================================================



#===============================================================================================================================================
#                                                               PANIER
#===============================================================================================================================================
def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'slug': request.GET['pid']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data-obj'] = cart_data

        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = item['price']
            product_price = price.replace(',', '.').strip()
            cart_total_amount += int(item['qty']) * float(product_price)
        return render(request, 'CART/shopping_cart.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'total_amount':cart_total_amount})
    else:
        messages.warning(request, "Il n'y a rien dans votre panier")
        return redirect('index')
    
def checkout(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = item['price']
            product_price = price.replace(',', '.').strip()
            cart_total_amount += int(item['qty']) * float(product_price)
        return render(request, 'PAYMENT/company_invoice.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'total_amount':cart_total_amount})
    else:
        messages.warning(request, "Il n'y a rien dans votre panier")
        return redirect('index')

def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = item['price']
            product_price = price.replace(',', '.').strip()
            cart_total_amount += int(item['qty']) * float(product_price)
    
    context = render_to_string("CART/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = item['price']
            product_price = price.replace(',', '.').strip()
            cart_total_amount += int(item['qty']) * float(product_price)
    
    context = render_to_string("CART/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})
#================================================================================================================================================================



# ===============================================================================================================================================================
#                                                                       COMMANDE
# ===============================================================================================================================================================

def orders(request):
    order = Commande.objects.all().order_by('-date_ajout','etat_cmd')
    if request.method == "POST":
        search = request.POST.get('search')
        order = order.filter(
            Q(etat_cmd__icontains = search)
        )
    context = {
        'commandes': order
    }
    return render(request, 'BASE/Orders.html', context)

def get_order(request, id_cmd):
    order = Commande.objects.get(id_cmd = id_cmd)
    livreur = Livreur.objects.all()
    context = {
        'commande': order,
        'livreurs': livreur
    }
    return render(request, 'BASE/update_order.html', context)

@transaction.atomic
def update_order(request, id_cmd):
    if request.method == "POST":
        etat = request.POST.get('etat')
        liv = request.POST.get('livreur')

        order = Commande.objects.get(id_cmd = id_cmd)
        deliver = get_object_or_404(Livreur, id_liv = liv)
        with transaction.atomic():
                commande = Commande(
                    id_cmd = id_cmd,
                    vente = order.vente,
                    livreur = deliver,
                    etat_cmd = etat,
                    date_ajout = order.date_ajout
                )
                commande.save()
                if commande.etat_cmd == 'Annulé':
                    messages.success(request, "Commande Annulée")
                    return redirect('commande')
                elif commande.etat_cmd == 'Confirmé' and commande.livreur != None:
                    livraison, created = Livraison.objects.get_or_create(commande = commande)
                    livraison.save()
                    messages.success(request, "Commande Confirmée")
                    return redirect('commande')
                
                livraison, created = Livraison.objects.get_or_create(commande = commande)
                livraison.save()
                messages.success(request, "Commande Confirmée")
                return redirect('commande')
    return render(request, 'BASE/update_order.html')
# =================================================================================================================================================================



# =================================================================================================================================================================
#                                              ADMINISTRATION
# =================================================================================================================================================================
def administration(request):
    ventes = Vente.objects.all().count
    commandes = Commande.objects.all().count
    users = Custommer_User.objects.filter(is_superuser = 0).count
    context = {
        'ventes': ventes,
        'commandes': commandes,
        'users': users
               }
    return render(request, 'BASE/index.html', context)

def display_products(request):
    produit = Produit.objects.all().order_by('-date_ajout')
    return render(request, 'PRODUCTS/products.html', {'products':produit})

def page_not_found(request):
    return render(request, 'BASE/pages-error-404.html')
# ====================================================================================================================================================================


# ====================================================================================================================================================================
#                                                  LIVREUR
# ====================================================================================================================================================================
def delivers(request):
    list_delivers = Livreur.objects.all().order_by('-date_ajout')
    if request.method == "POST":
        nom = request.POST.get('nom')
        postnom = request.POST.get('postnom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        password = request.POST.get('password')
        image = request.FILES['photo']

        search = request.POST.get('search')

        livreur = Livreur.objects.create(
            nom = nom,
            postnom = postnom,
            prenom =  prenom,
            telephone = telephone,
            email = email,
            adresse = adresse,
            password = password,
            photo = image
            )
        livreur.save()
        list_delivers = list_delivers.filter(
            Q(nom__icontains = search)|
            Q(postnom__icontains = search)|
            Q(prenom__icontains = search)|
            Q(telephone__icontains = search)|
            Q(email__icontains = search)
        )
    
    context = {'livreurs':list_delivers}
    return render(request, 'DELIVERY/livreurs.html', context)

def deliver_details(request, id_liv):
    deliver = get_object_or_404(Livreur, id_liv=id_liv)
    context = {'livreur': deliver}
    return render(request, 'DELIVERY/livreur-details.html', context)

def deliver_connection(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password=request.POST.get("password")
        try:
            if Livreur.objects.get(email = email, password = password):
                return redirect('livraison')
        except:
            messages.error(request, "Impossible")
            return redirect('deliver_login')
    return render(request, 'USER/login-deliver.html')
# =====================================================================================================================================================================


# =====================================================================================================================================================================
#                                               CATEGORIES
# =====================================================================================================================================================================
def add_categorie(request):
    categories = Categorie_Produit.objects.all().order_by('id_cat')
    if request.method == "POST":
        designation_cat = request.POST.get('designation-cat')
        categorie_prod = Categorie_Produit.objects.create(
            designation = designation_cat
        )
        categorie_prod.save()
    return render(request, 'BASE/category.html',{'categories':categories})

def get_categorie(request, id_cat):
    categorie = Categorie_Produit.objects.get(id_cat = id_cat)
    context = {
        'categorie': categorie
    }
    return render(request, 'BASE/update-categorie.html', context)

def update_categorie(request, id_cat):
    if request.method == "POST":
        designation_cat = request.POST.get('designation-cat')

        categorie_prod = Categorie_Produit(
            id_cat = id_cat,
            designation = designation_cat
        )
        categorie_prod.save()
        messages.success(request, "Modification Réussie")
        return redirect('add-category')
    return render(request, 'BASE/update-categorie.html')

def delete_categorie(request, id_cat):
    categorie = Categorie_Produit.objects.get(id_cat = id_cat)
    categorie.delete()
    messages.success(request, "Effacé avec succès")
    return redirect('add-category')
# =======================================================================================================================================================================

def stock_view(request):
    stock = Stock.objects.all().order_by('id_stock')
    context = {
        'stocks':stock
    }
    return render(request, 'BASE/stock.html', context)


# =======================================================================================================================================================
#                                               LIVRAISON
# =======================================================================================================================================================
def livraison(request):
    livraisons = Livraison.objects.all().order_by('-date_livraison')
    context = {
        'livraisons': livraisons
    }
    return render(request, 'DELIVERY/livraison.html', context)

def get_livraison(request, id):
    getlivraison = get_object_or_404(Livraison, id = id)
    context = {
        'livraison':getlivraison
    }
    return render(request, 'DELIVERY/confirmer_livraison.html', context)

def confirmer_livraison(request, id):
    if request.method == "POST":
        etat = request.POST.get('etat')
        livraison = get_object_or_404(Livraison, id = id)

        form = Livraison(
            id = id,
            commande = livraison.commande,
            etat_livraison = etat,
            date_livraison = datetime.now()
        )
        form.save()
        messages.success(request, "Opération réussie")
        return redirect('livraison')
    return render(request, 'DELIVERY/confirmer_livraison.html')
# ===============================================================================================================================================

def invoice(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price = item['price']
            product_price = price.replace(',', '.').strip()
            cart_total_amount += int(item['qty']) * float(product_price)
        return render(request, 'invoice.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'total_amount':cart_total_amount})
    else:
        messages.error(request, "Vous n'avez pas encore effectué un achat")
        return redirect('index')

def restart(request):
    request.session.flush()
    return redirect('index')
 # ========================================================================================================================================

def payment_success(request):
    body = json.loads(request.body)
    print('BODY:', body)
    return JsonResponse('Paiement Effectué avec succès', safe=False)

@transaction.atomic
def create_vente(request):
    if request.method == 'POST':
        client = request.user
        product = request.POST.get('produit_vente')
        quantite_qty = request.POST.get('quantite_vente')
        produit = Produit.objects.get(id_prod = product)
        with transaction.atomic():
            vente = Vente.objects.create(
                    user=client,
                    produit=produit,
                    quantite=int(quantite_qty)
                )
            stock, created = Stock.objects.get_or_create(produit=produit)
            if stock.stock_dispo > 0 :
                if stock.stock_dispo > int(vente.quantite):
                    stock.stock_dispo -= int(vente.quantite)
                    stock.save()

                    commande, created = Commande.objects.get_or_create(vente = vente)
                    commande.save()
                    messages.success(request, "Success")
                    return redirect('cart')
                else:
                    messages.warning(request, "Stock Insuffisant")
                    return redirect('cart')
    return render(request, 'CART/shopping_cart.html')
# ====================================================================================

# def search(request):
#     queryset = 
#     if request.method == "POST":
#         search = request.POST.get('search')
#         queryset = queryset.
#     return render(request, 'BASE/base.html', context)