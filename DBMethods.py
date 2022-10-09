from urllib import response
from MELIdb import getDB

def organize(result, description):
    items = []
    items = [dict(zip([key[0] for key in description], row)) for row in result]
    return items

def insert_client():
    pass

def update_client():
    pass

def delete_client(id):
    pass

def get_user(username):
    db = getDB()
    cur = db.cursor()
    get_statement = """SELECT 
                id,
                username,
                password FROM users WHERE username = ?"""
    cur.execute(get_statement, [username])
    return cur.fetchone()

def get_client(id):
    db = getDB()
    cur = db.cursor()
    get_statement = """SELECT 
                id,
                fec_alta,
                user_name,
                codigo_zip,
                cuenta_numero,
                direccion,
                geo_latitud,
                geo_longitud,
                color_favorito,
                foto_dni,
                ip,
                auto,
                auto_modelo,
                auto_tipo,
                auto_color,
                cantidad_compras_realizadas,
                avatar,
                fec_birthday FROM clients WHERE id = ?"""
    result = cur.execute(get_statement, [id])
    response = organize(result, cur.description)
    return response



def get_payment_method(id):
    db = getDB()
    cur = db.cursor()
    get_statement = """SELECT 
                    id, 
                    credit_card_num, 
                    credit_card_ccv FROM clients WHERE id = ?"""
    result = cur.execute(get_statement, [id])
    response = organize(result, cur.description)
    return response

def get_clients():
    db = getDB()
    cur = db.cursor()
    get_statement = """SELECT 
                id,
                fec_alta,
                user_name,
                codigo_zip,
                cuenta_numero,
                direccion,
                geo_latitud,
                geo_longitud,
                color_favorito,
                foto_dni,
                ip,
                auto,
                auto_modelo,
                auto_tipo,
                auto_color,
                cantidad_compras_realizadas,
                avatar,
                fec_birthday FROM clients LIMIT 100"""
    result=cur.execute(get_statement)
    response = organize(result, cur.description)
    return response


def get_marketing():
    db = getDB()
    cur = db.cursor()
    get_statement = """SELECT 
                id,
                user_name,
                codigo_zip,
                direccion,
                geo_latitud,
                geo_longitud,
                color_favorito,
                auto,
                auto_modelo,
                auto_tipo,
                auto_color,
                cantidad_compras_realizadas,
                fec_birthday FROM clients LIMIT 100"""
    result=cur.execute(get_statement)
    response = organize(result, cur.description)
    return response


def get_marketing_id(id):
    db = getDB()
    cur = db.cursor()
    get_statement = """SELECT 
                id,
                user_name,
                codigo_zip,
                direccion,
                geo_latitud,
                geo_longitud,
                color_favorito,
                auto,
                auto_modelo,
                auto_tipo,
                auto_color,
                cantidad_compras_realizadas,
                fec_birthday FROM clients WHERE id = ?"""
    result=cur.execute(get_statement, [id])
    response = organize(result, cur.description)
    return response