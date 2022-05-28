from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from helpers.decorators import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = directors_schema.dump(rs)
        return res, 200
    @admin_required
    def post(self):
        data = request.json
        director = director_service.create(data)
        return '', 201, {"location": f'/directors/{director.id}'}


@director_ns.route('/<int:did>')
@director_ns.doc(params={'did': 'director id'})
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        r = director_service.get_one(did)
        sm_d = director_schema.dump(r)
        return sm_d, 200

    @admin_required
    def delete(self, did):
        director_service.delete(did)
        return '', 204

    @admin_required
    def put(self, did):
        data = request.json
        if 'id' not in data:
            data['id'] = did
        director_service.update(data)
        return '', 204
