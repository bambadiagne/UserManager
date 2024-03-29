from django.urls import path
from . import views

urlpatterns = [
    path('vendeurs', views.afficher_vendeurs, name='vendeurs'),
    path('confirmer/<str:id>', views.confirmation_suppression, name='confirmation'),
    path('clients', views.afficher_clients, name='clients'),
    path('ajouter', views.ajouter_utilisateur, name='addUser'),
    path('modifier/<str:id>', views.modifier_utilisateur, name='modifyUser'),
    path('supprimer/<str:id>', views.supprimer_utilisateur, name='deleteUser'),

]
