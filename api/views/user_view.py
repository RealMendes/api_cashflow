from flask import request
from flask_restx import Resource, fields
from marshmallow import ValidationError
from http import HTTPStatus
from api import api
from ..views import helper
from ..schemas.user_schema import UserSchema
from ..services.user_service import UserService

user_service = UserService()

user_namespace = api.namespace('users', description='User operations')

user_input_model = api.model('UserInput', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),

})

user_output_model = api.model('UserOutput', {
    'username': fields.String(description='Username'),
    'password': fields.String(description='Password'),

})


@user_namespace.route('/create-account')
class UserCreateAcoount(Resource):

    @api.expect(user_input_model)
    @api.response(HTTPStatus.CREATED, 'User registered successfully.')
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    def post(self):
        """
        Register a new user.
        """
        try:
            user_data = UserSchema().load(request.json)
            user_service.create_user(user_data)
            return {"message": "User registered successfully."}, HTTPStatus.CREATED
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST


@user_namespace.route('/list/<int:user_id>')
class UserList(Resource):

    @api.response(HTTPStatus.OK, 'User details retrieved successfully.', user_output_model)
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    def get(self, user_id):
        """
        Retrieve user details by ID.
        """
        try:
            user = user_service.get_user_by_id(user_id)
            return UserSchema().dump(user), HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST

    @api.response(HTTPStatus.OK, 'User deleted successfully.')
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    def delete(self, user_id):
        """
        Delete user by ID.
        """
        try:
            user = user_service.delete_user_by_id(user_id)
            return {"message": "User deleted successfully."}, HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST


@user_namespace.route('/authenticate')
class UserAuthentication(Resource):

    @api.response(HTTPStatus.OK, 'Authentication successful.')
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    def post(self):
        """
        Authenticate user.
        """
        try:
            return helper.auth()
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
