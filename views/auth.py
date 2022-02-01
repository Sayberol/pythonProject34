from flask import request
from flask_restx import Namespace, Resource, abort
from marshmallow import Schema, fields

auth_ns = Namespace('auth')


class LoginValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        ...

    def put(self):
        ...