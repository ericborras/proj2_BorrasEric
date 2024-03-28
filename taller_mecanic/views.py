from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from . import utils

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        usuari = request.POST.get('usuari')
        password = request.POST.get('password')

        return utils.existeix_usuari(request,usuari, password)

        
    return render(request, 'index.html')

def reparacions(request):
    return render(request, 'reparacions.html', {'dades_usuari':request.session['dades_usuari']})

def tanca_sessio(request):
    request.session.flush()

    return redirect('login')