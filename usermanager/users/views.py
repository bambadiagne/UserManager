from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
import datetime
from api.models import Seller,Client
from api.utils import is_seller_or_client,user_form_validation
from rest_framework.authtoken.models import Token

def afficher_vendeurs(request):
    vendeurs = Seller.objects.all()
    vendeurs=[User.objects.filter(id=vendeur.user_id).first() for vendeur in vendeurs]
    return render(request, "users/vendeurs.html", {'vendeurs': vendeurs})


def afficher_clients(request):

    clients = Client.objects.all()
    clients=[User.objects.filter(id=vendeur.user_id).first() for vendeur in clients]
    return render(request, "users/clients.html", {'clients': clients})


def supprimer_utilisateur(request, id):
    
    user=is_seller_or_client(id)
    user[1].delete()
    User.objects.filter(id=user[1].user_id).first().delete()      
    user_token=Token.objects.filter(user_id=user[1].user_id).first()

    if(user_token):
        user_token.delete()
    
    return redirect('/users/clients')
   
def confirmation_suppression(request,id):
        return render(request,'users/confirmation.html',{'id':id})
def modifier_utilisateur(request, id):
    user = User.objects.get(id=id)
    
    if(request.method == 'POST'):
        user_form=user_form_validation(request)
        if(user_form[0] and user.username!=user_form[1]["username"]):
            User.objects.filter(id=id).update(password=make_password(user_form[1]["mot_de_passe"]),username=user_form[1]["username"], last_name=user_form[1]["nom"],
                                    email=user_form[1]["email"], first_name=user_form[1]["prenom"])    
            if(request.POST.get('profile')=='seller'):        
                
                seller = Seller(user=user, date_naissance=datetime.date(
                            user_form[1]["date_birth"][2], user_form[1]["date_birth"][1], user_form[1]["date_birth"][0]))
                seller.save()
                return render(request, "users/vendeurs.html")
            elif(request.POST.get('profile') == "client"):
                client = Client(user=user, date_naissance=datetime.date(
                            user_form[1]["date_birth"][2], user_form[1]["date_birth"][1], user_form[1]["date_birth"][0]))
                client.save()
                return render(request, "users/clients.html")
        return             
        
          
    return render(request, 'users/modifier_utilisateur.html', {'id': id, 'client': user})


def ajouter_utilisateur(request):
    return render(request, 'users/ajouter_utilisateur.html')
