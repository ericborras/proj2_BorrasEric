from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from . import utils, models, parametres
from django.core.paginator import Paginator
import json

def index(request):
    utils.obrir_factura(1)
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
        f_nif = request.POST.get('f_nif')

        return utils.filtrar_reparacions(request, f_data_alta, f_estat, f_marca_model, f_matricula, f_client, f_poblacio, f_pagada, f_nif)

        
    return render(request, 'reparacions.html')


def nova_reparacio(request):
    vehicles = utils.get_vehicles()
    definicio_tipus_linia = utils.get_definicio_tipus_linia()
    packs = utils.get_packs()
    clients = utils.get_clients()
    marca_models = utils.get_marca_models()

    return render(request, 'nova_reparacio.html', {'dades_usuari':request.session['dades_usuari'], 'vehicles':vehicles, 'definicio_tipus_linia':definicio_tipus_linia, 'packs':packs, 'clients':clients, 'marca_models':marca_models})

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

def get_dades_vehicle(request):
    if request.method == 'POST':
        id_client = request.POST.get('id_client')
        return utils.get_dades_vehicle(id_client)

    return render(request, 'index.html')

def get_vehicle(request):
    if request.method == 'POST':
        id_vehicle = request.POST.get('id_vehicle')
        return utils.get_vehicle(id_vehicle)
    
    return render(request, 'index.html')

def get_vehicles(request):
    if(request.method == 'POST'):
        
        vehicles = utils.get_vehicles()
        vehicles_json = json.dumps([{
            'id': vehicle.id,
            'matricula': vehicle.matricula,
            'kms': float(vehicle.kms),  # Convertir Decimal a float aquí
            'nom': vehicle.id_marca_model.nom
        } for vehicle in vehicles])
        return JsonResponse({'success': True, 'vehicles': vehicles_json})
    
    return JsonResponse({'success' : False})


def add_reparacio(request):
    if(request.method == 'POST'):
        id_vehicle = request.POST.get('id_vehicle')
        return utils.add_reparacio(request, id_vehicle)
    return render(request, 'index.html')


def reparacio(request, id_reparacio):
    vehicle = utils.get_vehicle_reparacio(id_reparacio)
    definicio_tipus_linia = utils.get_definicio_tipus_linia()
    packs = utils.get_packs()
    client = utils.get_client_reparacio(id_reparacio)
    packs_json = utils.get_packs_json()
    linies_reparacio = utils.get_linies_reparacio(id_reparacio)
    estat_reparacio = utils.get_estat_reparacio(id_reparacio)
    te_factura = utils.get_es_reparacio_factura(id_reparacio)
    #return render(request, 'nova_reparacio.html', {'dades_usuari':request.session['dades_usuari'], 'vehicles':vehicles, 'definicio_tipus_linia':definicio_tipus_linia, 'packs':packs, 'clients':clients})

    reparacio = get_object_or_404(models.Reparacio, pk=id_reparacio)
    return render(request, 'editar_reparacio.html', {'dades_usuari':request.session['dades_usuari'], 'vehicle':vehicle, 'definicio_tipus_linia':definicio_tipus_linia, 'packs':packs, 'client':client, 'reparacio': reparacio, "packs_json":packs_json, 'linies_reparacio':linies_reparacio,'estat_reparacio':estat_reparacio, 'te_factura':te_factura})

def add_vehicle(request):
    if(request.method == 'POST'):
        kms = request.POST.get('kms')
        matricula = request.POST.get('matricula')
        marca_model = request.POST.get('marca_model')
        client = request.POST.get('client')
        return utils.add_vehicle(request, kms, matricula, marca_model, client)
    
    return render(request, 'index.html')


def add_feina_mecanic(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        desc = request.POST.get('desc')
        qt = request.POST.get('qt')
        config = parametres.Configuracio('config.json')
        preu = config.get_valor('preu_ma_obra')
        return utils.add_feina_mecanic(request, id_reparacio, desc, qt, preu)
    
    return render(request, 'index.html')


def editar_feina_mecanic(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        id_linia_reparacio = request.POST.get('id_linia_reparacio')
        desc = request.POST.get('desc')
        qt = request.POST.get('qt')
        config = parametres.Configuracio('config.json')
        preu = config.get_valor('preu_ma_obra')

        return utils.editar_feina_mecanic(request, id_reparacio, id_linia_reparacio, desc, qt, preu)

    return render(request, 'index.html')

def eliminar_feina_mecanic(request):
    if(request.method == 'POST'):
        id_linia_reparacio = request.POST.get('id_linia_reparacio')

        return utils.eliminar_feina_mecanic(request, id_linia_reparacio)

    return render(request, 'index.html')      

def add_pesa_recanvi(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        pesa = request.POST.get('pesa')
        qt = request.POST.get('qt')
        codfab = request.POST.get('codfab')
        preu = request.POST.get('preu')

        print('LA QT: ',qt)
        return utils.add_pesa_recanvi(request, id_reparacio, pesa, qt, codfab, preu)

    return render(request, 'index.html')

def editar_pesa_recanvi(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        id_linia_reparacio = request.POST.get('id_linia_reparacio')
        pesa = request.POST.get('pesa')
        qt = request.POST.get('qt')
        codfab = request.POST.get('codfab')
        preu = request.POST.get('preu')

        return utils.editar_pesa_recanvi(request, id_reparacio, id_linia_reparacio, pesa, qt, preu, codfab)

    return render(request, 'index.html')

def add_altres_conceptes(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        desc = request.POST.get('desc')
        qt = request.POST.get('qt')
        preu = request.POST.get('preu')

        return utils.add_altres_conceptes(request, id_reparacio, desc, qt, preu)

    return render(request, 'index.html')

def editar_altres_conceptes(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        id_linia_reparacio = request.POST.get('id_linia_reparacio')
        desc = request.POST.get('desc')
        qt = request.POST.get('qt')
        preu = request.POST.get('preu')

        return utils.editar_altres_conceptes(request, id_reparacio, id_linia_reparacio, desc, qt, preu)

    return render(request, 'index.html')

def add_packs(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        id_pack = request.POST.get('id_pack')
        preu = request.POST.get('preu')
        desc = request.POST.get('desc')

        return utils.add_packs(request, id_reparacio, id_pack, preu, desc)

    return render(request, 'index.html')


def editar_packs(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        id_linia_reparacio = request.POST.get('id_linia_reparacio')
        desc = request.POST.get('desc')
        id_pack = request.POST.get('id_pack')
        preu = request.POST.get('preu')

        return utils.editar_packs(request, id_reparacio, id_linia_reparacio, desc, id_pack, preu)

    return render(request, 'index.html')

def rebutjar_reparacio(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')

        return utils.rebutjar_reparacio(request, id_reparacio)

    return render(request, 'index.html')

def tancar_reparacio(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')

        return utils.tancar_reparacio(request, id_reparacio)

    return render(request, 'index.html')

def genera_factura(request):
    if(request.method == 'POST'):
        id_reparacio = request.POST.get('id_reparacio')
        descomptes = json.loads(request.POST.get('descomptes'))
        return utils.genera_factura(request, id_reparacio, descomptes)

    return render(request, 'index.html')

def get_parametres(request):
    #Obtenir els paràmetres del fitxer parametres.py
    config = parametres.Configuracio('config.json')
    valor_iva = config.get_valor('iva')
    valor_preu_ma_obra = config.get_valor('preu_ma_obra')
    num_fact = utils.get_num_fact()


    return render(request, 'parametres.html', {'dades_usuari':request.session['dades_usuari'], 'iva':valor_iva, 'preu_ma_obra':valor_preu_ma_obra, 'num_fact':num_fact})


def guarda_canvis_props(request):
    if(request.method == 'POST'):
        ma_obra = request.POST.get('ma_obra')
        iva = request.POST.get('iva')

        return utils.guarda_canvis_props(request, ma_obra, iva)

    return render(request, 'index.html')


def guarda_canvis_factura(request):
    if(request.method == 'POST'):
        num_fact = request.POST.get('num_fact')

        return utils.guarda_canvis_factura(request, num_fact)

    return render(request, 'index.html')

 