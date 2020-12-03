from django.shortcuts import render
from .models import Utilisateur
def allUsers(request):
    utilisateurs=Utilisateur.objects.all()
    return render(request,{'utilisateurs':utilisateurs})
def deleteUser(request,id):
    pass
def modifyUser(request,id):
    pass
def addUser(request):
    pass

