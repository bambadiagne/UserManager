from django.urls import path
from . import views

urlpatterns = [
    path('add',views.addUser,name='addUser'),
    path('update/<int:id>', views.modifyUser, name = 'modifyUser'),
    path('<int:id>', views.deleteUser, name = 'deleteUser'),
    
]
