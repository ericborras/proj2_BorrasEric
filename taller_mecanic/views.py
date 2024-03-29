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
    print(request.session['dades_usuari'])
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
