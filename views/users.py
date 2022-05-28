from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from helpers.decorators import admin_required
from implemented import user_service


user_ns = Namespace('users')
users_schema = UserSchema(many=True)
user_schema = UserSchema()


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        return users_schema.dump(all_users), 200

    def post(self):
        data = request.json
        new_user = user_service.create(data)
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:uid>')
@user_ns.doc(params={'uid': 'user id'})
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        return user_schema.dump(user), 200

    def delete(self, uid):
        user_service.delete(uid)
        return '', 204

    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204


