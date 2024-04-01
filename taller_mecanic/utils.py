import importlib
from django.contrib.auth.hashers import make_password, check_password
from passlib.hash import bcrypt
from django.db import connection,connections
from django.http import JsonResponse
from . import models, parametres
import bcrypt
from datetime import datetime
from django.urls import reverse
import json
from decimal import Decimal

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
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat, c.nif
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
            "ciutat": row[14],
            "nif": row[15],
            "url_reparacio": reverse('reparacio', kwargs={'id_reparacio': row[0]})
        }
        print('ROW DICT: ',row_dict)
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
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat, c.nif
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
            "ciutat": row[14],
            "nif": row[15],
            "url_reparacio": reverse('reparacio', kwargs={'id_reparacio': row[0]})
        }
        print('ROW DICT: ',row_dict)
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

def filtrar_reparacions(request, f_data_alta, f_estat, f_marca_model, f_matricula, f_client, f_poblacio, f_pagada, f_nif):
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
            c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat, c.nif
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
                                        and ('' = UPPER(%s) OR UPPER(c.nif) like %s)
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
                c.nom, c.cognoms, c.telefon, u.nom AS nom_usuari, tu.nom AS tipus_usuari, c.ciutat, c.nif
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
                                            and ('' = UPPER(%s) OR UPPER(c.nif) like %s)
                ORDER BY r.data_alta DESC
                """
    else:
        return None
    
    with connection.cursor() as cursor:
        print("Consulta SQL con parámetros sustituidos:")
        print(cursor.mogrify(query, [f_data_alta, f_data_alta,tupla_valores,tupla_valores, f_marca_model+'%', f_marca_model+'%', f_matricula+'%', f_matricula+'%', f_client+'%', f_client+'%', '%'+f_client+'%', '%'+f_poblacio+'%', '%'+f_poblacio+'%', f_nif+'%', f_nif+'%']))

        cursor.execute(query, [f_data_alta,f_data_alta,tupla_valores,tupla_valores, f_marca_model+'%', f_marca_model+'%', f_matricula+'%', f_matricula+'%', f_client+'%', f_client+'%', '%'+f_client+'%', '%'+f_poblacio+'%', '%'+f_poblacio+'%', f_nif+'%', f_nif+'%'])
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
            "ciutat": row[14],
            "nif": row[15],
            "url_reparacio": reverse('reparacio', kwargs={'id_reparacio': row[0]})
        }
        data.append(row_dict)

    return JsonResponse({'success' : True, 'data': data})

#Retorna tots els vehicles
def get_vehicles():
    query = """
        SELECT v.*, mm.nom 
        FROM vehicle v LEFT JOIN marca_model mm ON v.id_marca_model = mm.id 
        ORDER BY mm.nom
    """
    with connection.cursor() as cursor:
        print("Consulta SQL con parámetros sustituidos:")
        print(cursor.mogrify(query))
        
        cursor.execute(query)
        results = cursor.fetchall()

    data = []
    
    for row in results:
        row_dict = {
            "id": row[0],
            "matricula": row[1],
            "kms": row[2],
            "id_client": row[3],
            "id_marca_model": row[4],
            "nom": row[5]
        }
        data.append(row_dict)
    return data


    '''
    
    
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
    '''

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
    
#Retorna el preu del pack indicat per paràmetre
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

#Retorna tots els packs
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


#Retorna tots els clients
def get_clients():
    query = """
        SELECT * 
        FROM clients
        order by nom,cognoms
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    data = []
    for row in results:
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        packs = models.Clients(*row)
        data.append(packs)
    return data


#Retorna els vehcicles del client passat per paràmetre
def get_dades_vehicle(id_client):
    query = """
        SELECT v.*, mm.nom 
        FROM vehicle v LEFT JOIN marca_model mm ON v.id_marca_model = mm.id 
        WHERE v.id_client = %s
        ORDER BY mm.nom
    """

    with connection.cursor() as cursor:

        print("Consulta SQL con parámetros sustituidos:")
        print(cursor.mogrify(query, [id_client]))
        
        cursor.execute(query, [id_client])
        results = cursor.fetchall()

    data = []
    
    for row in results:
        row_dict = {
            "id": row[0],
            "matricula": row[1],
            "kms": row[2],
            "id_client": row[3],
            "id_marca_model": row[4],
            "nom": row[5]
        }
        data.append(row_dict)

    return JsonResponse({'success' : True, 'vehicles': data})

def get_vehicle(id_vehicle):
    #Montem la consulta
    query = """
        SELECT * 
        FROM vehicle
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [id_vehicle])
        row = cursor.fetchone()

    if row:
        
        vehicle = models.Vehicle(*row)
        vehicle_json = vehicle.to_json()
            
        return JsonResponse({'success' : True, 'vehicle': vehicle_json})

    else:
        return JsonResponse({'success' : False})
    
def add_reparacio(request, id_vehicle):

    try:

        cursor = connections['default'].cursor()

        # Ejecutar la consulta SQL
        cursor.execute("INSERT INTO reparacio (data_alta, id_estat_reparacio, id_usuari, id_vehicle) VALUES (%s, %s, %s, %s)", [datetime.now().date(), 1, request.session['dades_usuari']['id_tipus_usuari'], id_vehicle])

        # Obtener el último ID insertado
        id_reparacio = cursor.lastrowid

        url_reparacio = reverse('reparacio', kwargs={'id_reparacio': id_reparacio})

        #query = "INSERT INTO reparacio (data_alta, id_estat_reparacio, id_usuari, id_vehicle) VALUES (%s, %s, %s, %s)"
        #q_parametres = (datetime.now().date(), 1, request.session['dades_usuari']['id_tipus_usuari'], id_vehicle)
        #print('DATA ACTUAL: ',datetime.now().date())
        #print('TIPUS USUARI DE LA SESSIÓ: ',request.session['dades_usuari']['id_tipus_usuari'])
        # Ejecutar la consulta raw
        #n_reparacio = models.Reparacio.objects.raw(query, q_parametres)
        #print('REPARACIO GUARDADA: OK?: ',n_reparacio)

        #reparacio = models.Reparacio(data_alta=datetime.now().date(), id_estat_reparacio=1, id_usuari=request.session['dades_usuari']['id_tipus_usuari'], id_vehicle=id_vehicle)
        #print('REPARACIO: ',reparacio)
        #reparacio.save()

        return JsonResponse({'success': True, 'id_reparacio': id_reparacio, "url_reparacio":url_reparacio})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def get_vehicle_reparacio(id_reparacio):
    #Montem la consulta
    query = """
        SELECT v.*, mm.nom 
        FROM reparacio r LEFT JOIN vehicle v ON r.id_vehicle = v.id
                            LEFT JOIN marca_model mm on v.id_marca_model = mm.id
        WHERE r.id = %s 
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [id_reparacio])
        row = cursor.fetchone()

    if row:
        row_dict = {
            "id": row[0],
            "matricula": row[1],
            "kms": row[2],
            "id_client": row[3],
            "id_marca_model": row[4],
            "nom": row[5]
        }
        return row_dict
    else:
        return {}
    
def get_client_reparacio(id_reparacio):
    query = """
        SELECT c.*
        FROM reparacio r LEFT JOIN vehicle v ON r.id_vehicle = v.id
                            LEFT JOIN clients c ON v.id_client = c.id
        WHERE r.id = %s  
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [id_reparacio])
        row = cursor.fetchone()

    if row:
        row_dict = {
            "id": row[0],
            "nif": row[1],
            "nom": row[2],
            "cognoms": row[3],
            "telefon": row[4],
            "email": row[5],
            "direccio": row[6],
            "ciutat": row[7],
            "codi_postal": row[8],
        }
        return row_dict
    else:
        return {}
    

def get_marca_models():
    query = """
        SELECT * 
        FROM marca_model
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    data = []
    for row in results:
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        packs = models.MarcaModel(*row)
        data.append(packs)
    return data

def add_vehicle(request, kms, matricula, marca_model, client):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL
        cursor.execute("INSERT INTO vehicle (matricula, kms, id_client, id_marca_model) VALUES (%s, %s, %s, %s)", [matricula, kms, client, marca_model])

        # Obtener el último ID insertado
        id_vehicle = cursor.lastrowid


        query = """
            SELECT v.id, v.matricula, mm.nom, v.kms 
            FROM vehicle v left join marca_model mm on v.id_marca_model = mm.id
            WHERE v.id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [id_vehicle])
            row = cursor.fetchone()

        if row:
            row_dict = {
                "id": row[0],
                "matricula": row[1],
                "nom": row[2],
                "kms": row[3]
            }

        return JsonResponse({'success': True, 'vehicle':row_dict})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def add_feina_mecanic(request, id_reparacio, desc, qt, preu):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("INSERT INTO linies_reparacio (id_reparacio, id_def, descripcio, quantitat, preu) VALUES (%s, 1, %s, %s, %s)", [id_reparacio, desc, qt, preu])

        # Obtener el último ID insertado
        id_feina_mecanic = cursor.lastrowid

        return JsonResponse({'success':True, 'id_linia_reparacio':id_feina_mecanic})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def editar_feina_mecanic(request, id_reparacio, id_linia_reparacio, desc, qt, preu):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update linies_reparacio set descripcio = %s, preu = %s, quantitat = %s where id = %s", [desc, preu, qt, id_linia_reparacio])

        return JsonResponse({'success':True})

    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def eliminar_feina_mecanic(request, id_linia_reparacio):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("delete from linies_reparacio where id = %s", [id_linia_reparacio])

        return JsonResponse({'success':True})
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def add_pesa_recanvi(request, id_reparacio, pesa, qt, codfab, preu):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("INSERT INTO linies_reparacio (id_reparacio, id_def, descripcio, quantitat, preu, codi_fabricant) VALUES (%s, 2, %s, %s, %s, %s)", [id_reparacio, pesa, qt, preu, codfab])

        # Obtener el último ID insertado
        id_pesa_recanvi = cursor.lastrowid

        return JsonResponse({'success':True, 'id_pesa_recanvi':id_pesa_recanvi})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def editar_pesa_recanvi(request, id_reparacio, id_linia_reparacio, pesa, qt, preu, codfab):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update linies_reparacio set descripcio = %s, preu = %s, quantitat = %s, codi_fabricant = %s where id = %s", [pesa, preu, qt, codfab, id_linia_reparacio])

        return JsonResponse({'success':True})

    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def add_altres_conceptes(request, id_reparacio, desc, qt, preu):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("INSERT INTO linies_reparacio (id_reparacio, id_def, descripcio, quantitat, preu) VALUES (%s, 4, %s, %s, %s)", [id_reparacio, desc, qt, preu])

        # Obtener el último ID insertado
        id_altres_conceptes = cursor.lastrowid

        return JsonResponse({'success':True, 'id_altres_conceptes':id_altres_conceptes})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def editar_altres_conceptes(request, id_reparacio, id_linia_reparacio, desc, qt, preu):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update linies_reparacio set descripcio = %s, preu = %s, quantitat = %s where id = %s", [desc, preu, qt, id_linia_reparacio])

        return JsonResponse({'success':True})

    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def get_packs_json():
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
        row_dict = {
            "id": row[0],
            "nom": row[1],
            "preu": str(row[2]),
        }
        data.append(row_dict)
    return json.dumps(data)


def add_packs(request, id_reparacio, id_pack, preu, desc):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("INSERT INTO linies_reparacio (id_reparacio, id_def, descripcio, quantitat, preu, id_pack) VALUES (%s, 3, %s, 1, %s, %s)", [id_reparacio, desc, preu, id_pack])

        # Obtener el último ID insertado
        id_pack = cursor.lastrowid

        return JsonResponse({'success':True, 'id_pack':id_pack})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def editar_packs(request, id_reparacio, id_linia_reparacio, desc, id_pack, preu):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update linies_reparacio set descripcio = %s, preu = %s, id_pack = %s where id = %s", [desc, preu, id_pack, id_linia_reparacio])

        return JsonResponse({'success':True})

    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def get_linies_reparacio(id_reparacio):
    query = """
            SELECT id, id_def, descripcio, preu, codi_fabricant, quantitat, id_pack, descompte
            FROM linies_reparacio
            WHERE id_reparacio = %s
            """
    
    with connection.cursor() as cursor:
        
        cursor.execute(query, [id_reparacio])
        results = cursor.fetchall()

    data = []

    for row in results:
        row_dict = {
            "id": row[0],
            "id_def": row[1],
            "descripcio": row[2],
            "preu": row[3],
            "codi_fabricant": row[4],
            "quantitat": round(row[5], 1),
            "id_pack": row[6],
            "descompte": "" if(row[7]==0) else row[7],
        }
        data.append(row_dict)
        
    return data


def get_estat_reparacio(id_reparacio):
    query = """
            SELECT er.nom
            FROM reparacio r LEFT JOIN estat_reparacio er ON r.id_estat_reparacio = er.id
            WHERE r.id = %s
            """
    with connection.cursor() as cursor:
        cursor.execute(query, [id_reparacio])
        row = cursor.fetchone()

    if row:
        estat = row[0]
        return estat
    else:
        return None
    
def rebutjar_reparacio(request, id_reparacio):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update reparacio set id_estat_reparacio = 3 where id = %s", [id_reparacio])


        return JsonResponse({'success':True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def tancar_reparacio(request, id_reparacio):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update reparacio set id_estat_reparacio = 2 where id = %s", [id_reparacio])


        return JsonResponse({'success':True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    

def genera_factura(request, id_reparacio, descomptes):
    try:
        cursor = connections['default'].cursor()
        #Actualitzar totals linies reparació
        for id_linia_reparacio, dte in descomptes.items():
            cursor.execute(
                "UPDATE linies_reparacio SET descompte = %s, preu_total = (preu * quantitat) - (preu * quantitat * %s / 100) WHERE id = %s",
                [dte, dte, id_linia_reparacio]
            )
        #Saber la suma de preu_total de les reparacions
        query = """
            SELECT SUM(preu_total) AS base
            FROM linies_reparacio
            WHERE id_reparacio = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query,[id_reparacio])
            row = cursor.fetchone()
        preu_total_linies = 0
        if row:
            preu_total_linies = row[0]
        else:
            return JsonResponse({'success': False})


        #Una vegada actualitzats, crear registre a la taula factura, amb la suma de preu_total
        data_actual = datetime.now().date()
        #Obtenir IVA i preu_ma_obra de config.json
        config = parametres.Configuracio('config.json')
        iva = config.get_valor('iva')
        #Calcular totals
        suma_base = preu_total_linies
        quota_iva = (Decimal(iva)/Decimal(100))*suma_base
        total_factura = suma_base+quota_iva

        cursor = connections['default'].cursor()
        cursor.execute("INSERT INTO factura (iva, id_reparacio, data_factura, base_imposable, quota_iva, total_factura) VALUES (%s,%s,%s,%s,%s,%s)", [iva, id_reparacio, data_actual, suma_base, quota_iva, total_factura])
        
        return JsonResponse({'success':True})

    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def get_es_reparacio_factura(id_reparacio):
    #Montem la consulta
    query = """
        SELECT count(*) as total
        from factura where id_reparacio = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [id_reparacio])
        row = cursor.fetchone()

    if row:
        
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        return row[0]
    else:
        return 0
    
def guarda_canvis_props(request, ma_obra, iva):
    try:
        config = parametres.Configuracio('config.json')

        config.modificar_valor('iva', iva)
        config.modificar_valor('preu_ma_obra', ma_obra)

        '''
        # Obtener el valor actual de 'iva'
        valor_iva = config.obtener_valor('iva')
        print("El valor actual de 'iva' es:", valor_iva)

        # Modificar el valor de 'iva' a 25
        config.modificar_valor('iva', iva)
        print("Se ha modificado el valor de 'iva' a 25")

        # Obtener el nuevo valor de 'iva'
        nuevo_valor_iva = config.obtener_valor('iva')
        print("El nuevo valor de 'iva' es:", nuevo_valor_iva)

        # Obtener el valor actual de 'preu_ma_obra'
        valor_preu_ma_obra = config.obtener_valor('preu_ma_obra')
        print("El valor actual de 'preu_ma_obra' es:", valor_preu_ma_obra)
        '''
        

        return JsonResponse({'success':True})
    except Exception as e:
        return JsonResponse({'success':False})
    
def guarda_canvis_factura(request, num_fact):
    try:
        cursor = connections['default'].cursor()
        # Ejecutar la consulta SQL -1
        cursor.execute("update comptadors set comptador = %s where concepte = 'F'", [num_fact])

        return JsonResponse({'success':True})
    except Exception as e:
        return JsonResponse({'success': False, 'msg': e})
    
def get_num_fact():
    query = """
        SELECT comptador
        from comptadors where concepte = 'F'
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()

    if row:
        
        # Crea una instancia de modelo Usuari con los datos de la fila obtenida
        return row[0]
    else:
        return -1