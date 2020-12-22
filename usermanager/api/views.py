from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from .models import Seller, Bill, Client
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view
import datetime
# Create your views here.


def register(request):
    if(request.method == 'GET'):
        return render(request, "users/ajouter_utilisateur.html",{'status':False})
    elif(request.method == 'POST'):

        date_birth = [int(i) for i in request.POST.get('date').split("/")]

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        username = request.POST.get('identifiant')
        email = request.POST.get('email')
        date_naissance = datetime.date(
            date_birth[2], date_birth[1], date_birth[0])
        mot_de_passe =make_password(request.POST.get('mot_de_passe'))

       
        if(request.POST.get('profile') == "seller"):
            user = User(password=mot_de_passe, username=username, last_name=nom, 
                        email=email,first_name=prenom,)
            user.save()
            seller = Seller(user=user, date_naissance=datetime.date(
                date_birth[2], date_birth[1], date_birth[0]), gain=0)
            seller.save()
            return render(request, "users/ajouter_utilisateur.html",{'status':True})
        elif(request.POST.get('profile') == "client"):
            user = User(password=mot_de_passe, username=username, last_name=nom, 
                        email=email,first_name=prenom,)
            user.save()
            
            client = Client(user_id=user, date_naissance=datetime.date(
                date_birth[2], date_birth[1], date_birth[0]),balance=0,total_spent=0)
            client.save()
            
            return render(request, "users/ajouter_utilisateur.html",{'status':True})
   
@api_view(["GET","POST"])
def login(request):
    if(request.method=="GET"):
          return render(request, "users/login.html",{'status':True})
    elif(request.method=="POST"):
         username=request.POST.get('username')
         print(username)
        
         password=request.POST.get('password')
         user=User.objects.filter(username=username).first()
         if(user):
            success=check_password(password,user.password)
            if(success):
                token=Token.objects.filter(user_id=user.id)
                if(token):
                    return Response({"token":"token {}".format(token.first().key)},status=status.HTTP_200_OK)
                else:
                    token=Token.objects.create(user_id=user.id) 
                    return Response({"token":"token {}".format(token.first().key)},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Mot de passe incorrect"},status=status.HTTP_404_NOT_FOUND)            
         else:

             return Response({"message":"L'utilisateur n'existe pas"},status=status.HTTP_404_NOT_FOUND)