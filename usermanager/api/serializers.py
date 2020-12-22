from django.db.models import fields
from rest_framework import serializers
from .models import Ticket,Client,Seller

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ["origin","destination","date","time","total_places","available_places","price"]
        
class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Client
        fields=["solde","total_spent"]

