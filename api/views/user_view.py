from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from http import HTTPStatus
from api import api
from ..views import helper
from ..schemas.user_schema import UserSchema
from ..services.user_service import UserService

user_service = UserService()


class UserCreateAcoount(Resource):

    def post(self):
        try:
            user_data = UserSchema().load(request.json)
            user_service.create_user(user_data)
            return {"message": "User registered successfully."}, HTTPStatus.CREATED
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST


class UserList(Resource):

    def get(self, user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            return UserSchema().dump(user), HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST

    def delete(self, user_id):
        try:
            user = user_service.delete_user_by_id(user_id)
            return {"message": "User deleted successfully."}, HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST


class UserAuthentication(Resource):
    def post(self):

        try:
            return helper.auth()
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST


api.add_resource(UserCreateAcoount, '/users/create-account')
api.add_resource(UserList, "/users/list/<int:user_id>")
api.add_resource(UserAuthentication, "/users/authenticate")
