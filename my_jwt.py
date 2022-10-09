from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta


def expire_date(minutes: int):
    now = datetime.now()
    new_date = now + timedelta(minutes=minutes) + timedelta(hours=5)
    return new_date


def write_token(ident):
    token = encode(payload={"id":ident, "exp": expire_date(15)}, key=getenv('SECRET'), algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(request):
    response = "Error"
    try:
        token = request.headers['Authorization']
        decoded = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        response = "OK"
    except exceptions.DecodeError:
        response = "Invalid Token"
    except exceptions.ExpiredSignatureError:
        response = "Token Expired"
    finally:
        return response

 
