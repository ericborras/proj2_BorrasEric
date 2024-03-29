from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login'),
    path('reparacions/', views.reparacions, name='reparacions'),
    path('tanca_sessio/', views.tanca_sessio, name='tanca_sessio'),
    path('filtrar_reparacions/', views.filtrar_reparacions, name='filtrar_reparacions'),
    path('nova_reparacio', views.nova_reparacio, name="nova_reparacio")
]