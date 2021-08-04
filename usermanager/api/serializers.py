from django.db.models import fields
from rest_framework import serializers
from .models import Ticket, Client, Seller, Bill


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ["origin", "destination", "date", "time",
                  "total_places", "available_places", "price"]


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ["balance", "total_spent"]


class SellerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seller
        fields = ["gain"]


class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ["total_paid"]
