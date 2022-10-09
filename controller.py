
from flask import Flask, request
import DBMethods
from my_jwt import *
import hashlib
import rsa
from flask import jsonify



app = Flask(__name__)

@app.route('/clients', methods=["GET"])
def get_clients():
    authenticated = validate_token(request)
    response = ""
    if authenticated == "OK":
        clients = DBMethods.get_clients()
        response = jsonify(clients)
    else:
        response = authenticated
    return response


@app.route("/client/<id>", methods=["GET"])
def get_client(id):
    authenticated = validate_token(request)
    response = ""
    if authenticated == "OK":
        client = DBMethods.get_client(id)
        print(client)
        response = jsonify(client)
    else:
        response = authenticated
    return response


@app.route("/method/<id>", methods=["GET"])
def get_payment_method(id):
    authenticated = validate_token(request)
    response = ""
    if authenticated == "OK":
        method = DBMethods.get_payment_method(id)
        privateKeyPkcs1PEM = open('privateKey.pem','r').read()
        privateKeyReloaded = rsa.PrivateKey.load_pkcs1(privateKeyPkcs1PEM.encode('utf8')) 
        method[0]['credit_card_num'] = rsa.decrypt(method[0]['credit_card_num'],privateKeyReloaded).decode("utf-8")
        method[0]['credit_card_ccv'] = rsa.decrypt(method[0]['credit_card_ccv'],privateKeyReloaded).decode("utf-8")
        response = jsonify(method)
    else:
        response = authenticated
    return response
    

@app.route("/login", methods=["POST"])
def login():
    user = DBMethods.get_user(request.json["username"])
    encoded = request.json["password"].encode('utf-8')
    hash_pass = hashlib.sha256(encoded).hexdigest()
    response = None
    if user!=None:
        if user[2] == hash_pass:
            response = jsonify({"token":write_token(user[0]).decode('utf8')})
        else:
            response = jsonify({"message":"Usuario o contraseña erróneos"})
            response.status_code=401
    else:
        response = jsonify({"message":"Usuario o contraseña erróneos"})
        response.status_code=401
    return response


@app.route('/marketing', methods=["GET"])
def get_marketing():
    authenticated = validate_token(request)
    response = ""
    if authenticated == "OK":
        clients = DBMethods.get_marketing()
        response = jsonify(clients)
    else:
        response = authenticated
    return response
    


@app.route('/marketing/<id>', methods=["GET"])
def get_marketing_id(id):
    authenticated = validate_token(request)
    response = ""
    if authenticated == "OK":
        clients = DBMethods.get_marketing_id(id)
        response = jsonify(clients)
    else:
        response = authenticated
    return response


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response