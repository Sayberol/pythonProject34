from flask import request
from flask_restx import abort
import jwt
from lesson19_project_easy_source.config import SECRET_HERE


def login_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, SECRET_HERE, algorithms=[algo])
        except:
            abort(401)
        return func(*args, **kwargs)

    return wrapper
