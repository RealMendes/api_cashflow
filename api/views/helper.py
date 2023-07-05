import datetime
from functools import wraps
from http import HTTPStatus

import jwt
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from flask import request, jsonify
from api import app
from ..services.user_service import UserService


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        raise ValidationError("Could not verify")

    username = auth.username
    user = UserService.user_by_username(username)
    if not user:
        raise ValidationError("Could not found user")

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    else:
        raise ValidationError("Could not verify, wrong password")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {"message": "Validation error, token is missing"}, HTTPStatus.BAD_REQUEST

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = UserService.user_by_username(data['username'])
        except jwt.DecodeError as e:
            return {"message": "Validation error", "errors": e.messages}, HTTPStatus.BAD_REQUEST

        kwargs['current_user'] = current_user
        return f(*args, **kwargs)

    return decorated