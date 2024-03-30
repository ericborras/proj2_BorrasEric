from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from . import utils
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        usuari = request.POST.get('usuari')
        password = request.POST.get('password')

        return utils.existeix_usuari(request,usuari, password)

        
    return render(request, 'index.html')

def reparacions(request):
    '''
    Saber el rol de l'usuari:
        -Mecanic (id 2)
            Usuaris mecànics han de poder veure totes les reparacions obertes.
        -Recepció (id 1)
            Usuaris recepció han de poder veure totes les reparacions (per defecte les tancades i
            pendents de facturar), però han de poder veure també la resta.
    '''
    #print(request.session['dades_usuari'])
    estats_reparacio = utils.get_estats_reparacio()
    if(request.session['dades_usuari']['id_tipus_usuari'] == 2):
        reparacions = utils.reparacions_mecanic(request)
        
    elif(request.session['dades_usuari']['id_tipus_usuari'] == 1):
        reparacions = utils.reparacions_recepcio(request)

    #print(reparacions)
    return render(request, 'reparacions.html', {'dades_usuari':request.session['dades_usuari'], 'reparacions':reparacions, 'estats_reparacio':estats_reparacio})

def tanca_sessio(request):
    request.session.flush()
    return redirect('login')

def filtrar_reparacions(request):
    if request.method == 'POST':
        f_data_alta = request.POST.get('f_data_alta')
        
        f_estat = request.POST.get('f_estat')
        print("F_ESTAT: ",f_estat)
        f_marca_model = request.POST.get('f_marca_model')
        f_matricula = request.POST.get('f_matricula')
        f_client = request.POST.get('f_client')
        f_poblacio = request.POST.get('f_poblacio')
        f_pagada = request.POST.get('f_pagada')

        return utils.filtrar_reparacions(request, f_data_alta, f_estat, f_marca_model, f_matricula, f_client, f_poblacio, f_pagada)

        
    return render(request, 'reparacions.html')


def nova_reparacio(request):
    vehicles = utils.get_vehicles()
    definicio_tipus_linia = utils.get_definicio_tipus_linia()
    packs = utils.get_packs()
    clients = utils.get_clients()

    return render(request, 'nova_reparacio.html', {'dades_usuari':request.session['dades_usuari'], 'vehicles':vehicles, 'definicio_tipus_linia':definicio_tipus_linia, 'packs':packs, 'clients':clients})

def get_client(request):
    if request.method == 'POST':
        id_vehicle = request.POST.get('id_vehicle')

        return utils.get_client(id_vehicle)
    
    return render(request, 'index.html')


def get_preu_pack(request):
    if request.method == 'POST':
        id_pack = request.POST.get('id_pack')

        return utils.get_pack(id_pack)
    
    return render(request, 'index.html')
