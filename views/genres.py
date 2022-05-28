from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from helpers.decorators import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = genres_schema.dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        genre = genre_service.create(data)
        return '', 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:gid>')
@genre_ns.doc(params={'gid': 'genre id'})
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = genre_schema.dump(r)
        return sm_d, 200

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return '', 204

    @admin_required
    def put(self, gid):
        data = request.json
        if 'id' not in data:
            data['id'] = gid
        genre_service.update(data)
        return '', 204



