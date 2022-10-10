import sqlite3
import requests
import json
import rsa
import hashlib


DBname = "MELI.db"


def getDB():
    con = sqlite3.connect(DBname)
    return con

def create_tables():
    db = getDB()
    cur = db.cursor()
    #Sentencia de creación de clientes
    table = """CREATE TABLE IF NOT EXISTS clients(
                id INTEGER NOT NULL PRIMARY KEY,
                fec_alta,
                user_name UNIQUE NOT NULL,
                codigo_zip,
                credit_card_num,
                credit_card_ccv,
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
                fec_birthday)"""
    cur.execute(table)
    db.commit()
    #Ahora crear la tabla de usuarios       
    table_users = """CREATE TABLE IF NOT EXISTS users(
                id INTEGER NOT NULL PRIMARY KEY,
                username NOT NULL UNIQUE,
                password NOT NULL)"""
    cur.execute(table_users)
    db.commit()
    return True


def populate_tables():
    db = getDB()
    cur = db.cursor() 
    #Descargar data desde el API inicial
    r = requests.get('https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios')
    json_construido = json.loads(r.text) 
    publicKeyPkcs1PEM = open('publicKey.pem','r').read()
    publicKeyReloaded = rsa.PublicKey.load_pkcs1(publicKeyPkcs1PEM.encode('utf8')) 
    for i in json_construido:
        #Sentencia de inserción de valores
        sql_sentence="INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values=[i['id'],
                i['fec_alta'],
                i['user_name'],
                i['codigo_zip'],
                rsa.encrypt(i['credit_card_num'].encode(),publicKeyReloaded),
                rsa.encrypt(i['credit_card_ccv'].encode(),publicKeyReloaded),
                i['cuenta_numero'],
                i['direccion'],
                i['geo_latitud'],
                i['geo_longitud'],
                i['color_favorito'],
                i['foto_dni'],
                i['ip'],
                i['auto'],
                i['auto_modelo'],
                i['auto_tipo'],
                i['auto_color'],
                i['cantidad_compras_realizadas'],
                i['avatar'],
                i['fec_birthday']]
        try:
            cur.execute(sql_sentence,values)
        except Exception as e:
            print(e)
    db.commit()
    sql_sentence_users = "INSERT INTO users VALUES (?, ?, ?)"
    '''
    #Ejemplo comando crear usuario
    values_users = [1, "juan.rodriguez", hashlib.sha256("PASSWORDSECURE".encode('utf-8')).hexdigest()]
    try:
        cur.execute(sql_sentence_users,values_users)
    except Exception as e:
        print(e)
    
    db.commit()
    '''
    return True

