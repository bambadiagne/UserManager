import datetime

from rest_framework.authtoken.models import Token
from api.models import Client, Seller
from re import match

from django.contrib.auth.models import User


def email_validator(email: str):
    return match(r"[^@]+@[^@]+\.[^@]+", email)


def password_validator(password: str):
    return len(password) >= 8


def user_form_validation(request):
    date = request.data['user_form']['date']

    nom = request.data['user_form']['nom']
    prenom = request.data['user_form']['prenom']
    username = request.data['user_form']['identifiant']
    email = request.data['user_form']['email']
    mot_de_passe = request.data['user_form']['mot_de_passe']
    confirmation = request.data['user_form']["confirmation"]
    if(nom and prenom and username and email and mot_de_passe and date):
        date_birth = [int(i) for i in date.split("/")]

        if(email_validator(email)):
            if(password_validator(mot_de_passe)):
                if(mot_de_passe == confirmation):
                    if(request.data['user_form']['profile'] in ["seller", "client"]):
                        if(not User.objects.filter(username=username).first()):
                            return (True, {"nom": nom, "prenom": prenom, "username": username, "email": email, "mot_de_passe": mot_de_passe, "date_birth": date_birth})
                        return (False, "nom d'utilisateur déjà existant")
                    return (False, "Profile inconnu")
                return (False, "Les mots de passe sont differents")
            return (False, "La longueur du mot de passe doit etre superieur ou egale à 8")
        return (False, "Format d'email non valide")
    return (False, "Un de vos champs est nul")


def ticket_form_validation(request):
    origin = request.data['ticket_form']["origin"]
    destination = request.data['ticket_form']["destination"]
    time = request.data['ticket_form']["time"]
    total_places = request.data['ticket_form']["total_places"]
    available_places = request.data['ticket_form']["available_places"]
    price = request.data['ticket_form']["price"]
    date = request.data['ticket_form']["date"]
    if(origin and destination and price and total_places and available_places and time):
        date_birth = [int(i) for i in date.split("/")]
        if(total_places.isdigit() and available_places.isdigit()):
            if(time.upper() in ["AM", "PM"]):
                date = datetime.date(
                    date_birth[2], date_birth[1], date_birth[0])

                return (True, {"origin": origin, "destination": destination, "time": time, "available_places": available_places, "total_places": total_places, "date": date, "price": price})
            return (False, "La valeur de time doit etre AM ou PM")
        return (False, "total_places et available_places doivent être des nombres")
    return (False, "Formulaire invalide:Un de vos champs est nul")


def is_seller_or_client(user_id):
    client = Client()
    try:
        client = Client.objects.get(user_id=user_id)
    except Client.DoesNotExist:
        client = None
    if(client):
        return ("client", client)
    try:
        seller = Seller.objects.get(user_id=user_id)
    except Seller.DoesNotExist:
        seller = None
    if(seller):
        return ('seller', seller)
    return "Aucun utilisateur trouvé"


def get_user_by_token(request):
    token_key = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    user_id = Token.objects.filter(key=token_key).first().user_id

    user = is_seller_or_client(user_id)
    return user
