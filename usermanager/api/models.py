from django.db import models

from django.contrib.auth.models import User



class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance= models.DateField() 
    gain=models.FloatField()
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance= models.DateField() 
    balance=models.FloatField()
    total_spent=models.FloatField()

class Ticket(models.Model):
    origin=models.CharField(max_length=70)
    destination=models.CharField(max_length=70)
    date= models.DateField()
    DAY=(("AM","AM"),("PM","PM"))
    time= models.CharField(max_length=2,choices=DAY)
    total_places=models.IntegerField()
    available_places=models.IntegerField()
    price=models.FloatField()
    seller=models.ForeignKey('Seller',on_delete=models.CASCADE)
    
class Bill(models.Model):
    total_paid=models.FloatField()
    ticket=models.ForeignKey('Ticket',on_delete=models.CASCADE)
    client=models.ForeignKey('Client',on_delete=models.CASCADE)
    seller=models.ForeignKey('Seller',on_delete=models.CASCADE)

def is_seller_or_client(id):
    client=Client()
    try:
         client=Client.objects.get(user_id=id) 
    except Client.DoesNotExist:
        client = None
    if(client):
        return ("client",client) 
    try:
         seller=Seller.objects.get(user_id=id) 
    except Seller.DoesNotExist:
        seller = None
    if(seller):
        return ('seller',seller)
    return "Aucun utilisateur trouvé"

    
    