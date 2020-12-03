from django.urls import path
from . import views

urlpatterns = [
    path('vendeurs',views.afficher_vendeurs,name='vendeurs'),
    path('clients',views.afficher_clients,name='clients'),
    path('ajouter',views.ajouter_utilisateur,name='addUser'),
    path('modifier/<int:id>', views.modifier_utilisateur, name = 'modifyUser'),
    path('delete/<int:id>', views.supprimer_utilisateur, name = 'deleteUser'),
    
]
