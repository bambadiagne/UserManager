from django.shortcuts import render
from .models import Utilisateur


def afficher_vendeurs(request):
    vendeurs=Utilisateur.objects.filter(profile="vendeur")
    return render(request,"users/vendeurs.html",{'vendeurs':vendeurs})
def afficher_clients(request):
    clients=Utilisateur.objects.filter(profile="client")
    return render(request,"users/clients.html",{'clients':clients})

def supprimer_utilisateur(request,id):
    pass
def modifier_utilisateur(request,id):
    pass
def ajouter_utilisateur(request):
    return render(request,'users/ajouter_utilisateur.html')

