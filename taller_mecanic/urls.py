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
    path('get_preu_pack/', views.get_preu_pack, name="get_preu_pack"),
    path('get_dades_vehicle/', views.get_dades_vehicle, name="get_dades_vehicle"),
    path('get_vehicle/', views.get_vehicle, name="get_vehicle"),
    path('get_vehicles/', views.get_vehicles, name="get_vehicles"),
    path('add_reparacio/', views.add_reparacio, name="add_reparacio"),
    path('reparacio/<int:id_reparacio>/', views.reparacio, name='reparacio'),
    path('add_vehicle/', views.add_vehicle, name="add_vehicle"),
    path('add_feina_mecanic/', views.add_feina_mecanic, name="add_feina_mecanic"),
    path('editar_feina_mecanic/', views.editar_feina_mecanic, name="editar_feina_mecanic"),
    path('eliminar_feina_mecanic/', views.eliminar_feina_mecanic, name="eliminar_feina_mecanic")
]