from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import Seller, Bill, Client, Ticket, is_seller_or_client
from .serializers import BillSerializer, ClientSerializer, SellerSerializer, TicketSerializer
from re import match
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db.models import F
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
        mot_de_passe = request.POST.get('mot_de_passe')

        if(nom and prenom and username and email and mot_de_passe):
            if(match(r"[^@]+@[^@]+\.[^@]+", email)):
                if(len(mot_de_passe) >= 8):
                    already_exists = User.objects.filter(
                        username=username).first()
                    if(request.POST.get('profile') == "seller"):
                        if(already_exists):
                            return render(request, "users/ajouter_utilisateur.html", {"message": "Utilisateur deja existant", 'status': False})
                        mot_de_passe = make_password(mot_de_passe)
                        user = User(password=mot_de_passe, username=username, last_name=nom,
                                    email=email, first_name=prenom,)
                        user.save()
                        seller = Seller(user=user, date_naissance=datetime.date(
                            date_birth[2], date_birth[1], date_birth[0]), gain=0)
                        seller.save()
                        return render(request, "users/ajouter_utilisateur.html", {'status': True})
                    elif(request.POST.get('profile') == "client"):
                        if(already_exists):
                            return render(request, "users/ajouter_utilisateur.html", {"message": "Utilisateur deja existant", 'status': False})
                        mot_de_passe = make_password(mot_de_passe)
                        user = User(password=mot_de_passe, username=username, last_name=nom,
                                    email=email, first_name=prenom)
                        user.save()

                        client = Client(user=user, date_naissance=datetime.date(
                            date_birth[2], date_birth[1], date_birth[0]), balance=0, total_spent=0)
                        client.save()

                        return render(request, "users/ajouter_utilisateur.html", {'status': True, 'message': "Compte cree avec succès"})
                    else:
                        return render(request, "users/ajouter_utilisateur.html", {"message": "Profile inconnu", "status": "False"})
                else:
                    return render(request, "users/ajouter_utilisateur.html", {"message": "La longueur du mot de passe doit etre superieur ou egale à 8", "status": False})
            else:
                return render(request, "users/ajouter_utilisateur.html",
                       {"message": "Format d'email non valide", "status": False})
        else:
            return render(request, "users/ajouter_utilisateur.html", {"message": "Un de vos champs est nul", "status": False})


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
def get_info_user(request, id):
    user = is_seller_or_client(id)
    if(user[0] == "client"):
        return Response(ClientSerializer(user[1]).data, status=status.HTTP_200_OK)
    elif(user[0] == "seller"):
        return Response(SellerSerializer(user[1]).data, status=status.HTTP_200_OK)
    return Response({"message": "Aucun utilisateur trouvé"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_all_client_bill(request):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    user_id = Token.objects.filter(key=token_key).first().user_id
    user = is_seller_or_client(user_id)
    if(user[0] == "client"):
        all_bill = Bill.objects.filter(client_id=user[1].id)
        if(all_bill):
            return Response(BillSerializer(all_bill, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Vous n'avez pas de factures"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Connectez-vous etant que client!!!"}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
def get_single_client_bill(request, id):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    user_id = Token.objects.filter(key=token_key).first().user_id
    user = is_seller_or_client(user_id)
    if(user[0] == "client"):
        try:
            bill = Bill.objects.get(id=id)
        except Bill.DoesNotExist:
            bill = None
        if(bill):
            return Response(BillSerializer(bill).data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Facture inexistante"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "Connectez-vous etant que client"}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def buy_ticket(request, id):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    user_id = Token.objects.filter(key=token_key).first().user_id

    user = is_seller_or_client(user_id)
    if(user[0] == "client"):
        number = int(request.POST.get('number'))
        client_ticket = Ticket.objects.get(pk=id)
        if(client_ticket):
            if(client_ticket.available_places >= int(number)):
                total_price = client_ticket.price*number
                Bill.objects.create(
                    total_paid=total_price, client_id=user[1].id, seller_id=client_ticket.seller_id, ticket_id=client_ticket.id)
                Client.objects.filter(id=user[1].id).update(
                    balance=F("balance")-total_price, total_spent=F("total_spent")+total_price)
                Seller.objects.filter(id=client_ticket.seller_id).update(
                    gain=F("gain")+0.12*total_price)
                Ticket.objects.filter(id=id).update(
                    available_places=F("available_places")-number)
                return Response({"message": "Billet(s) achetés avec succès"}, status=status.HTTP_200_OK)

            else:
                return Response({"message": "Nombre de tickets insuffisants"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"message": "Un billet ne peut qu'etre acheté par un client"}, status=status.HTTP_401_UNAUTHORIZED)


class TicketViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id

        user = is_seller_or_client(user_id)

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

    def retrieve(self, request, pk):

        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id
        user = is_seller_or_client(user_id)
        if(user[0] == "client"):
            try:
                client_ticket = Ticket.objects.get(id=pk)
            except Ticket.DoesNotExist:
                return Response({"message": "Billet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            ticket_serializer = TicketSerializer(client_ticket)
            return Response(ticket_serializer.data, status=status.HTTP_200_OK)
        if(user[0] == "seller"):
            try:
                seller_ticket = Ticket.objects.get(seller_id=user[1].id, id=pk)
            except Ticket.DoesNotExist:
                return Response({"message": "Billet non trouvé"}, status=status.HTTP_404_NOT_FOUND)
            ticket_serializer = TicketSerializer(seller_ticket)
            return Response(ticket_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id

        user = is_seller_or_client(user_id)
        if(user[0] == "seller"):
            if(request.method == "POST"):
                if(request.POST.get('date')):
                    origin = request.POST.get("origin")
                    destination = request.POST.get("destination")
                    date_birth = [int(i)
                                  for i in request.POST.get('date').split("/")]
                    date = datetime.date(
                        date_birth[2], date_birth[1], date_birth[0])
                    time = request.POST.get("time")
                    total_places = request.POST.get("total_places")
                    available_places = request.POST.get("available_places")
                    price = request.POST.get("price")
                    if(origin and destination and price and total_places and available_places and time):
                        if(total_places.isdigit() and available_places.isdigit()):
                            if(time.upper() in ["AM", "PM"]):
                                Ticket.objects.create(origin=origin, destination=destination, date=date, time=time,
                                                      total_places=total_places, available_places=available_places, price=price, seller_id=user[1].id)
                                return Response({"message": "Billet crée avec succès"},
                                                status=status.HTTP_200_OK)
                            else:
                                return Response({"message": "La valeur de time doit etre AM ou PM"}, status=status.HTTP_404_NOT_FOUND)
                        else:
                            return Response({"message": "total_places et available_places ne sont pas des nombres"}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"message": "Formulaire invalide:Un de vos champs est nul"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Impossible,Vous n'etes pas vendeur"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id

        user = is_seller_or_client(user_id)
        if(user[0] == "seller"):
            try:
                ticket_deleted = Ticket.objects.get(id=pk)
            except Ticket.DoesNotExist:
                return Response({"message": "Ce billet n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
            ticket_deleted.delete()
            return Response({"message": "Le billet a été bien supprimé"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Impossible,Vous n'etes pas vendeur"}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        user_id = Token.objects.filter(key=token_key).first().user_id

        user = is_seller_or_client(user_id)
        if(user[0] == "seller"):
            try:
                Ticket.objects.get(id=pk)
            except Ticket.DoesNotExist:
                return Response({"message": "Ce billet n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
            if(request.POST.get('date')):
                origin = request.POST.get("origin")
                destination = request.POST.get("destination")
                date_birth = [int(i)
                              for i in request.POST.get('date').split("/")]
                date = datetime.date(
                    date_birth[2], date_birth[1], date_birth[0])
                time = request.POST.get("time")
                total_places = request.POST.get("total_places")
                available_places = request.POST.get("available_places")
                price = request.POST.get("price")
                if(origin and destination and price and total_places and available_places and time):
                    if(total_places.isdigit() and available_places.isdigit()):
                        if(time.upper() in ["AM", "PM"]):
                            Ticket.objects.update(origin=origin, destination=destination, date=date, time=time,
                                                  total_places=total_places, available_places=available_places, price=price, seller_id=user[1].id)
                            return Response({"message": "Billet mis à jour avec succès"},
                                            status=status.HTTP_200_OK)
                        else:
                            return Response({"message": "La valeur de time doit etre AM ou PM"}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"message": "total_places et available_places ne sont pas des nombres"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"message": "Formulaire invalide:Un de vos champs est nul"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Impossible,Vous n'etes pas vendeur"}, status=status.HTTP_401_UNAUTHORIZED)
