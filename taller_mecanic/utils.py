from django.contrib.auth.hashers import make_password, check_password
from passlib.hash import bcrypt
from django.db import connection
from django.http import JsonResponse
from . import models
import bcrypt

#Funció que comprova si el hash i login de l'usuari existeix a la base de dades
def existeix_usuari(request, login, password):
    #Montem la consulta
    query = """
        SELECT * 
        FROM usuari 
        WHERE login = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [login])
        row = cursor.fetchone()

    if row:
        hash_almacenado = row[2].encode()
        if bcrypt.checkpw(password.encode(), hash_almacenado):
            # Crea una instancia de modelo Usuari con los datos de la fila obtenida
            usuari = models.Usuari(*row)

            #print("PRINT: ",usuari.to_json())
            request.session['dades_usuari'] = usuari.to_json()
            #usuari_json = usuari.to_json()
            return JsonResponse({'success' : True, 'redirect_url': '/reparacions/'})
        else:
            return JsonResponse({'success' : False})
    else:
        return JsonResponse({'success' : False})

