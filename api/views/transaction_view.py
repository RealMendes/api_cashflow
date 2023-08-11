from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from api import api
from . import helper
from ..schemas.transaction_schema import TransactionSchema
from ..services.transaction_service import TransactionService
from ..services.account_service import AccountService
from marshmallow import ValidationError

transaction_service = TransactionService()
account_service = AccountService()

transaction_namespace = api.namespace('transactions', description='Transaction operations')

transaction_input_model = api.model('TransactionInput', {
    'amount': fields.Float(required=True, description='Transaction amount'),
    'description': fields.String(description='Transaction description'),
    # Add other fields as needed
})

transaction_output_model = api.model('TransactionOutput', {
    'amount': fields.Float(description='Transaction amount'),
    'description': fields.String(description='Transaction description'),
    # Add other fields as needed
})


@transaction_namespace.route('/<int:account_id>')
class TransactionList(Resource):

    @api.expect(transaction_input_model)
    @api.response(HTTPStatus.CREATED, 'Transaction registered successfully.')
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    @helper.token_required
    def post(self, current_user, account_id):
        """
        Register a new transaction for an account.
        """
        try:
            transaction_data = TransactionSchema().load(request.json)
            account_service.get_account(account_id)
            transaction_data.account_id = account_id
            transaction_service.create_transaction(transaction_data)
            return {"message": "Transaction registered successfully."}, HTTPStatus.CREATED
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST


@transaction_namespace.route('/<int:transaction_id>')
class TransactionDetail(Resource):

    @api.response(HTTPStatus.OK, 'Transaction details retrieved successfully.', transaction_output_model)
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    @helper.token_required
    def get(self, current_user, transaction_id):
        """
        Retrieve transaction details by ID.
        """
        try:
            transaction = transaction_service.get_by_transaction(transaction_id)
            return TransactionSchema().dump(transaction), HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST

    @api.expect(transaction_input_model)
    @api.response(HTTPStatus.CREATED, 'Transaction changed successfully.')
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    @helper.token_required
    def put(self, current_user, transaction_id):
        """
        Change transaction details by ID.
        """
        try:
            transaction_data = TransactionSchema().load(request.json)
            account_id = transaction_data.account_id
            account_service.get_account(account_id)
            transaction_service.update_transaction(transaction_id, transaction_data)
            return {"message": "Transaction changed successfully."}, HTTPStatus.CREATED
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST

    @api.response(HTTPStatus.OK, 'Successfully deleted transaction.')
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    @helper.token_required
    def delete(self, current_user, transaction_id):
        """
        Delete transaction by ID.
        """
        try:
            transaction_service.delete_transaction(transaction_id)
            return {"message": "Successfully deleted transaction."}, HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST


@transaction_namespace.route('/<int:account_id>/for-account')
class TransactionListAll(Resource):

    @api.response(HTTPStatus.OK, 'All transactions retrieved successfully.', transaction_output_model)
    @api.response(HTTPStatus.BAD_REQUEST, 'Validation error')
    @helper.token_required
    def get(self, current_user, account_id):
        """
        Retrieve all transactions for an account.
        """
        try:
            account = account_service.get_account(account_id)
            if account is not None:
                transactions_ids = transaction_service.get_all_transactions_ids(account_id)
                transactions = []
                for transaction_id in transactions_ids:
                    transactions.append(transaction_service.get_by_transaction(transaction_id))
                serialized_transactions = TransactionSchema().dump(transactions, many=True)
                return serialized_transactions, HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST


api.add_resource(TransactionList, "/transactions/<int:account_id>")
api.add_resource(TransactionDetail, "/transactions/<int:transaction_id>")
api.add_resource(TransactionListAll, "/transactions/<int:account_id>/for-account")
