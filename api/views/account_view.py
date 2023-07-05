from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from http import HTTPStatus
from api import api
from . import helper

from ..schemas.account_schema import AccountSchema
from ..services.account_service import AccountService

account_service = AccountService()

class AccountDetail(Resource):
    @staticmethod
    @helper.token_required
    def get(current_user, **kwargs):
        account_id = kwargs['account_id']
        try:
            account = account_service.get_account(account_id)
            return AccountSchema().dump(account), HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {'message': "Something is wrong", 'errors': err}, HTTPStatus.BAD_REQUEST

    @staticmethod
    @helper.token_required
    def delete(current_user, **kwargs):
        account_id = kwargs['account_id']
        try:
            account_service.delete_account(account_id)
            return {"message": "Successfully deleted account."}, HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {'message': "Something is wrong", 'errors': err}, HTTPStatus.BAD_REQUEST


api.add_resource(AccountDetail, "/accounts/<int:account_id>")
