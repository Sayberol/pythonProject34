from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        ent = User(**req_json)
        with db.session.begin():
            db.session.add(ent)
        return "", 201


@user_ns.route('/<int:bid>')
class UserView(Resource):
    def get(self, bid):
        b = db.session.query(User).get(bid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        user = User.query.get(bid)
        if not user:
            return "", 404
        else:
            db.session.update(user)
            db.session.commit()
            return "", 204

