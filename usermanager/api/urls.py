from django.urls import path, include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('tickets', views.TicketViewSet, basename='/')
urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('info/<int:id>', views.get_info_user),
    path('buy/<int:id>', views.buy_ticket),
    path('bill', views.get_all_client_bill),
    path('bill/<int:id>', views.get_single_client_bill),
    path('', include(router.urls), name='tickets'),

]
