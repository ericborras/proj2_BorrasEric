from django.contrib.auth.hashers import make_password, check_password
from passlib.hash import bcrypt
from django.db import connection
from django.http import JsonResponse
from . import models
import bcrypt, json

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

#Funció que retorna les reparacions que han de visualitzar els mecànics
def reparacions_mecanic(request):
    #Montem la consulta
    query = """
            SELECT r.id, DATE_FORMAT(r.data_alta, '%d/%m/%Y') AS data_alta, r.id_estat_reparacio, r.id_usuari, r.id_vehicle, er.nom AS estat_reparacio, v.matricula, 
            v.id_marca_model, 
            CASE 
            WHEN LENGTH(mm.nom) > 50 THEN CONCAT(LEFT(mm.nom, 47), '...') 
            ELSE mm.nom 
            END AS marca_model,
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari
            FROM reparacio r LEFT JOIN estat_reparacio er ON r.id_estat_reparacio = er.id
                                LEFT JOIN vehicle v ON r.id_vehicle = v.id
                                LEFT JOIN marca_model mm ON v.id_marca_model = mm.id
                                LEFT JOIN clients c ON v.id_client = c.id
                                LEFT JOIN usuari u ON r.id_usuari = u.id
                                LEFT JOIN tipus_usuari tu ON u.id_tipus_usuari = tu.id
            WHERE r.id_estat_reparacio = 1
            ORDER BY r.data_alta desc
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    #print("RESULTS: ",len(results))
    for row in results:
        row_dict = {
            "id": row[0],
            "data_alta": row[1],
            "id_estat_reparacio": row[2],
            "id_usuari": row[3],
            "id_vehicle": row[4],
            "estat_reparacio": row[5],
            "matricula": row[6],
            "id_marca_model": row[7],
            "marca_model": row[8],
            "nom": row[9],
            "cognoms": row[10],
            "telefon": row[11],
            "nom_usuari": row[12],
            "tipus_usuari": row[13]
        }
        data.append(row_dict)

    return data

def reparacions_recepcio(request):
    #Montem la consulta
    query = """
            SELECT r.id, DATE_FORMAT(r.data_alta, '%d/%m/%Y') AS data_alta, r.id_estat_reparacio, r.id_usuari, r.id_vehicle, er.nom AS estat_reparacio, v.matricula, 
            v.id_marca_model, 
            CASE 
            WHEN LENGTH(mm.nom) > 50 THEN CONCAT(LEFT(mm.nom, 47), '...') 
            ELSE mm.nom 
            END AS marca_model,
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari
            FROM reparacio r LEFT JOIN estat_reparacio er ON r.id_estat_reparacio = er.id
                                LEFT JOIN vehicle v ON r.id_vehicle = v.id
                                LEFT JOIN marca_model mm ON v.id_marca_model = mm.id
                                LEFT JOIN clients c ON v.id_client = c.id
                                LEFT JOIN usuari u ON r.id_usuari = u.id
                                LEFT JOIN tipus_usuari tu ON u.id_tipus_usuari = tu.id
            WHERE r.id_estat_reparacio = 2
            ORDER BY r.data_alta desc
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    #print("RESULTS: ",len(results))
    for row in results:
        row_dict = {
            "id": row[0],
            "data_alta": row[1],
            "id_estat_reparacio": row[2],
            "id_usuari": row[3],
            "id_vehicle": row[4],
            "estat_reparacio": row[5],
            "matricula": row[6],
            "id_marca_model": row[7],
            "marca_model": row[8],
            "nom": row[9],
            "cognoms": row[10],
            "telefon": row[11],
            "nom_usuari": row[12],
            "tipus_usuari": row[13]
        }
        data.append(row_dict)

    return data

#Retorna el llistat d'estats que pot tenir una reparació
def get_estats_reparacio():
    query = """
            SELECT * FROM estat_reparacio
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    data = []
    #print("RESULTS: ",len(results))
    for row in results:
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        estat_reparacio = models.EstatReparacio(*row)
        data.append(estat_reparacio)
    return data
    