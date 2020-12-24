from django.urls import path,include
from . import views
from rest_framework import routers
router=routers.DefaultRouter()
router.register('tickets',views.TicketViewSet,basename='/')
urlpatterns = [
    path('register',views.register),
    path('login',views.login),
    path('info/<int:id>',views.getInfoUser),
    path('', include(router.urls),name='tickets'),
  
]
