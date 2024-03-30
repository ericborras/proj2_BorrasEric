from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login'),
    path('reparacions/', views.reparacions, name='reparacions'),
    path('tanca_sessio/', views.tanca_sessio, name='tanca_sessio'),
    path('filtrar_reparacions/', views.filtrar_reparacions, name='filtrar_reparacions'),
    path('nova_reparacio', views.nova_reparacio, name="nova_reparacio"),
    path('get_client/', views.get_client, name="get_client"),
    path('get_preu_pack/', views.get_preu_pack, name="get_preu_pack")
]