from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Utilisateur
from .forms import UtilisateurForm
import datetime

def afficher_vendeurs(request):
    vendeurs = Utilisateur.objects.filter(profile="vendeur")
    return render(request, "users/vendeurs.html", {'vendeurs': vendeurs})


def afficher_clients(request):

    if(request.method == 'POST'):
        user_form = UtilisateurForm(request.POST)
        if(user_form.is_valid()):
            print(request.POST)
        
            print(user_form.cleaned_data)
            
            date_birth =[int(i) for i in request.POST.get('date').split("/")]
            
            Utilisateur.objects.create(
                nom=user_form.cleaned_data['nom'],
                prenom=user_form.cleaned_data['prenom'],
                identifiant=user_form.cleaned_data["identifiant"],
                email=user_form.cleaned_data['email'],
                date_naissance=datetime.date(date_birth[2],date_birth[1],date_birth[0]),
                mot_de_passe=user_form.cleaned_data['mot_de_passe'],
                profile=user_form.cleaned_data['profile'],
           )
            return HttpResponseRedirect("/users/clients")
    
        else:
            return render(request,"users/ajouter_utilisateur.html",{"form":user_form})
  
            
    clients = Utilisateur.objects.filter(profile="client")
    return render(request, "users/clients.html", {'clients': clients})


def supprimer_utilisateur(request, id):
     client=Utilisateur.objects.get(identifiant=id)
     return render(request,'users/supprimer_utilisateur.html',{'id':id})


def modifier_utilisateur(request, id):
    pass

def ajouter_utilisateur(request):

    return render(request, 'users/ajouter_utilisateur.html',)

def ajouter_utilisateur(request):
    return render(request, 'users/ajouter_utilisateur.html')
