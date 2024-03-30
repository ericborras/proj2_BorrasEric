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
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat
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
            "tipus_usuari": row[13],
            "ciutat": row[14]
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
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat
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
            "tipus_usuari": row[13],
            "ciutat": row[14]
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

def filtrar_reparacions(request, f_data_alta, f_estat, f_marca_model, f_matricula, f_client, f_poblacio, f_pagada):
    if(request.session['dades_usuari']['id_tipus_usuari'] == 2):
        #Mecànic
        valores_lista = "0"
        if(len(f_estat)==0):
            f_estat = ""
        else:
            valores_lista = f_estat.split(',')

        # Convierte cada cadena en un número entero
        valores_enteros = [int(valor) for valor in valores_lista]

        # Crea una tupla con los números convertidos
        tupla_valores = tuple(valores_enteros)

        query = """
            SELECT r.id, DATE_FORMAT(r.data_alta, '%%d/%%m/%%Y') AS data_alta, r.id_estat_reparacio, r.id_usuari, r.id_vehicle, er.nom AS estat_reparacio, v.matricula, 
            v.id_marca_model, 
            CASE 
            WHEN LENGTH(mm.nom) > 50 THEN CONCAT(LEFT(mm.nom, 47), '...') 
            ELSE mm.nom 
            END AS marca_model,
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat
            FROM reparacio r LEFT JOIN estat_reparacio er ON r.id_estat_reparacio = er.id
                                LEFT JOIN vehicle v ON r.id_vehicle = v.id
                                LEFT JOIN marca_model mm ON v.id_marca_model = mm.id
                                LEFT JOIN clients c ON v.id_client = c.id
                                LEFT JOIN usuari u ON r.id_usuari = u.id
                                LEFT JOIN tipus_usuari tu ON u.id_tipus_usuari = tu.id
            WHERE r.id_estat_reparacio = 1 and (''=%s OR DATE_FORMAT(r.data_alta, '%%Y-%%m-%%d')=%s)
                                        and ('' in %s OR r.id_estat_reparacio in %s)
                                        and ('' = UPPER(%s) OR UPPER(mm.nom) like %s)
                                        and ('' = UPPER(%s) OR UPPER(v.matricula) like %s)
                                        and ('' = UPPER(%s) OR UPPER(c.nom) like %s OR UPPER(c.cognoms) like %s)
                                        and ('' = UPPER(%s) OR UPPER(c.ciutat) like %s)
            ORDER BY r.data_alta DESC
            """
        
    elif(request.session['dades_usuari']['id_tipus_usuari'] == 1):
        #Recepcio
        #Mecànic
        valores_lista = "0"
        if(len(f_estat)==0):
            f_estat = ""
        else:
            valores_lista = f_estat.split(',')

        # Convierte cada cadena en un número entero
        valores_enteros = [int(valor) for valor in valores_lista]

        # Crea una tupla con los números convertidos
        tupla_valores = tuple(valores_enteros)
        query = """
                SELECT r.id, DATE_FORMAT(r.data_alta, '%%d/%%m/%%Y') AS data_alta, r.id_estat_reparacio, r.id_usuari, r.id_vehicle, er.nom AS estat_reparacio, v.matricula, 
                v.id_marca_model, 
                CASE 
                WHEN LENGTH(mm.nom) > 50 THEN CONCAT(LEFT(mm.nom, 47), '...') 
                ELSE mm.nom 
                END AS marca_model,
                c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat
                FROM reparacio r LEFT JOIN estat_reparacio er ON r.id_estat_reparacio = er.id
                                    LEFT JOIN vehicle v ON r.id_vehicle = v.id
                                    LEFT JOIN marca_model mm ON v.id_marca_model = mm.id
                                    LEFT JOIN clients c ON v.id_client = c.id
                                    LEFT JOIN usuari u ON r.id_usuari = u.id
                                    LEFT JOIN tipus_usuari tu ON u.id_tipus_usuari = tu.id
                WHERE (''=%s OR DATE_FORMAT(r.data_alta, '%%Y-%%m-%%d')=%s)
                                            and ('' in %s OR r.id_estat_reparacio in %s)
                                            and ('' = UPPER(%s) OR UPPER(mm.nom) like %s)
                                            and ('' = UPPER(%s) OR UPPER(v.matricula) like %s)
                                            and ('' = UPPER(%s) OR UPPER(c.nom) like %s OR UPPER(c.cognoms) like %s)
                                            and ('' = UPPER(%s) OR UPPER(c.ciutat) like %s)
                ORDER BY r.data_alta DESC
                """
    else:
        return None
    
    with connection.cursor() as cursor:
        print("Consulta SQL con parámetros sustituidos:")
        print(cursor.mogrify(query, [f_data_alta, f_data_alta,tupla_valores,tupla_valores, f_marca_model+'%', f_marca_model+'%', f_matricula+'%', f_matricula+'%', f_client+'%', f_client+'%', '%'+f_client+'%', '%'+f_poblacio+'%', '%'+f_poblacio+'%']))

        cursor.execute(query, [f_data_alta,f_data_alta,tupla_valores,tupla_valores, f_marca_model+'%', f_marca_model+'%', f_matricula+'%', f_matricula+'%', f_client+'%', f_client+'%', '%'+f_client+'%', '%'+f_poblacio+'%', '%'+f_poblacio+'%'])
        results = cursor.fetchall()

    data = []
    
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
            "tipus_usuari": row[13],
            "ciutat": row[14]
        }
        data.append(row_dict)

    return JsonResponse({'success' : True, 'data': data})

def get_vehicles():
    query = """
            SELECT * FROM vehicle
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    data = []
    #print("RESULTS: ",len(results))
    for row in results:
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        vehicle = models.Vehicle(*row)
        data.append(vehicle)
    return data

def get_definicio_tipus_linia():
    query = """
            SELECT * FROM definicio_tipus_linia order by nom
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    data = []
    #print("RESULTS: ",len(results))
    for row in results:
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        dtl = models.DefinicioTipusLinia(*row)
        data.append(dtl)
    return data

def get_client(id_vehicle):
    #Montem la consulta
    query = """
        SELECT c.* 
        FROM clients c LEFT JOIN vehicle v ON c.id = v.id_client
        WHERE v.id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [id_vehicle])
        row = cursor.fetchone()

    if row:
        
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        client = models.Clients(*row)

        #print("PRINT: ",usuari.to_json())
        client_json = client.to_json()
            
        return JsonResponse({'success' : True, 'client': client_json})
    else:
        return JsonResponse({'success' : False})
    

def get_pack(id_pack):
    #Montem la consulta
    query = """
        SELECT preu 
        FROM packs_def
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [id_pack])
        row = cursor.fetchone()

    if row:
        
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        preu = row[0]

        return JsonResponse({'success' : True, 'preu': preu})
    else:
        return JsonResponse({'success' : False})
    
def get_packs():
    query = """
        SELECT * 
        FROM packs_def
        order by nom
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    data = []
    #print("RESULTS: ",len(results))
    for row in results:
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        packs = models.PacksDef(*row)
        data.append(packs)
    return data
