from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import Seller, Bill, Client, Ticket, isSellerOrClient
from .serializers import ClientSerializer, SellerSerializer, TicketSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

import datetime
# Create your views here.


def register(request):
    if(request.method == 'GET'):
        return render(request, "users/ajouter_utilisateur.html", {'status': False})
    elif(request.method == 'POST'):

        date_birth = [int(i) for i in request.POST.get('date').split("/")]

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        username = request.POST.get('identifiant')
        email = request.POST.get('email')
        date_naissance = datetime.date(
            date_birth[2], date_birth[1], date_birth[0])
        mot_de_passe = make_password(request.POST.get('mot_de_passe'))

        if(request.POST.get('profile') == "seller"):
            user = User(password=mot_de_passe, username=username, last_name=nom,
                        email=email, first_name=prenom,)
            user.save()
            seller = Seller(user=user, date_naissance=datetime.date(
                date_birth[2], date_birth[1], date_birth[0]), gain=0)
            seller.save()
            return render(request, "users/ajouter_utilisateur.html", {'status': True})
        elif(request.POST.get('profile') == "client"):
            user = User(password=mot_de_passe, username=username, last_name=nom,
                        email=email, first_name=prenom,)
            user.save()

            client = Client(user=user, date_naissance=datetime.date(
                date_birth[2], date_birth[1], date_birth[0]), balance=0, total_spent=0)
            client.save()

            return render(request, "users/ajouter_utilisateur.html", {'status': True})


@api_view(["GET", "POST"])
def login(request):
    if(request.method == "GET"):
        return render(request, "users/login.html", {'status': False})
    elif(request.method == "POST"):
        username = request.POST.get('username')

        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if(user):
            success = check_password(password, user.password)
            if(success):
                token = Token.objects.filter(user_id=user.id)
                if(token):
                    return Response({"token": "Token {}".format(token.first().key)}, status=status.HTTP_200_OK)
                else:
                    token = Token.objects.create(user_id=user.id)
                    return Response({"token": "Token {}".format(token.key)}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Mot de passe incorrect"}, status=status.HTTP_404_NOT_FOUND)
        else:

            return Response({"message": "L'utilisateur n'existe pas"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getInfoUser(request, id):
    user = isSellerOrClient(id)
    if(user[0] == "client"):
        return Response(ClientSerializer(user[1]).data, status=status.HTTP_200_OK)
    elif(user[0] == "seller"):
        return Response(SellerSerializer(user[1]).data, status=status.HTTP_200_OK)
    return Response({"message": "Aucun utilisateur trouvé"}, status=status.HTTP_404_NOT_FOUND)


class TicketViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id
        
        user = isSellerOrClient(user_id)
          
        if(user[0] == "client"):
            try:
                client_tickets = Ticket.objects.filter(available_places__gt=0)
            except Ticket.DoesNotExist:
                client_tickets = None
            if(client_tickets):
                return Response(TicketSerializer(client_tickets, many=True).data, status=status.HTTP_200_OK)
        elif(user[0] == "seller"):
            try:
                seller_tickets = Ticket.objects.filter(seller_id=user[1].id)
            except Ticket.DoesNotExist:
                seller_tickets = None
            if(seller_tickets):
        
                return Response(TicketSerializer(seller_tickets, many=True).data, status=status.HTTP_200_OK)

        return Response({"message": "Billets non disponibles"}, status=status.HTTP_404_NOT_FOUND)
    def retrieve(self, request,pk):
        
        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id
        
        user=isSellerOrClient(user_id)
        print(pk)
        print(user)
        if(user[0]=="client"):
            try:
                client_ticket=Ticket.objects.get(id=pk)
                print(client_ticket)
            except Ticket.DoesNotExist:
                return Response({"message":"Billet non trouvé"},status=status.HTTP_404_NOT_FOUND)
            ticket_serializer=TicketSerializer(client_ticket)
            return Response(ticket_serializer.data,status=status.HTTP_200_OK)    
        if(user[0]=="seller"):
            try:
                seller_ticket=Ticket.objects.get(seller_id=user[1].id,id=pk)
                print(seller_ticket)
            except Ticket.DoesNotExist:
                return Response({"message":"Billet non trouvé"},status=status.HTTP_404_NOT_FOUND)
            ticket_serializer=TicketSerializer(seller_ticket)
            return Response(ticket_serializer.data,status=status.HTTP_200_OK)        