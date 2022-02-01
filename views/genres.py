from flask import request
from flask_restx import Resource, Namespace

from lesson19_project_easy_source.models import Genre, GenreSchema
from lesson19_project_easy_source.setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        add_movie = Genre(**req_json)
        with db.session.begin():
            db.session.add(add_movie)
        return "", 201


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    def put(self, rid):
        genre = Genre.query.get(rid)
        if not genre:
            return "", 404
        else:
            db.session.update(genre)
            db.session.commit()
            return "", 204

    def delete(self, rid):
        genre = Genre.query.get(rid)
        if not genre:
            return "", 404
        else:
            db.session.delete(genre)
            db.session.commit()
            return "", 204
