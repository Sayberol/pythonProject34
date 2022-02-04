import base64
import calendar
import datetime
import hashlib
import hmac

from flask import request
from flask_restx import abort
import jwt
from config import SECRET_HERE, JWT_ALGORITHM
from models import User


def login_required(func):
    def wrapper(*args, **kwargs):
        decoded_jwt = auth_check()
        if decoded_jwt:
            role = decoded_jwt.get("role")
            if role == "admin":
                return func(*args, **kwargs)
            abort(401)
    return wrapper


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_tiken = jwt.encode(data, SECRET_HERE, algorithm=JWT_ALGORITHM)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET_HERE, algorithm=JWT_ALGORITHM)
    return {'access_token': access_tiken, 'refresh_token': refresh_token}


def get_hash(self):
    return hashlib.md5(self.password.encode('utf-8')).hexdigest()


def login_user(req_json):
    user_name = req_json.get("username")
    user_pass = req_json.get("password")
    if user_pass and user_pass:
        user = User.get_filter({"username": user_name})
        if user:
            pass_hashed = user[0].role
            req_json["role"] = user[0].role
            if get_hash(pass_hashed):
                return generate_token(req_json)
    return False

def refresh_user_token(req_json):
    refresh_token = req_json.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    return False
