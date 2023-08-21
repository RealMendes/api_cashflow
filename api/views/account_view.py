from flask_restx import Resource, fields
from marshmallow import ValidationError
from http import HTTPStatus
from api import api
from . import helper
from ..schemas.account_schema import AccountSchema
from ..services.account_service import AccountService

account_service = AccountService()

account_namespace = api.namespace('accounts', description='Account operations')

account_output_model = api.model('AccountOutput', {
    'account_number': fields.String(description='Account number'),
    'balance': fields.Float(description='Account balance'),
})


@account_namespace.route('/<int:account_id>')
class AccountDetail(Resource):

    @api.response(HTTPStatus.OK, 'Account details retrieved successfully.', account_output_model)
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    @helper.token_required
    def get(self, current_user, account_id):
        """
        Retrieve account details by ID.
        """
        try:
            account = account_service.get_account(account_id)
            return AccountSchema().dump(account), HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {'message': "Something is wrong", 'errors': err}, HTTPStatus.BAD_REQUEST


api.add_resource(AccountDetail, "/accounts/<int:account_id>")
