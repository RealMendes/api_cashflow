from flask import request
from flask_restful import Resource
from http import HTTPStatus
from api import api
from . import helper
from ..schemas.transaction_schema import TransactionSchema
from ..services.transaction_service import TransactionService
from ..services.account_service import AccountService
from marshmallow import ValidationError

transaction_service = TransactionService()
account_service = AccountService()


class TransactionList(Resource):
    @staticmethod
    @helper.token_required
    def post(current_user, **kwargs):
        account_id = kwargs['account_id']
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


class TransactionListAll(Resource):
    @staticmethod
    @helper.token_required
    def get(current_user, **kwargs):
        account_id = kwargs['account_id']
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


class TransactionDetail(Resource):
    @staticmethod
    @helper.token_required
    def get(current_user, **kwargs):
        transaction_id = kwargs['transaction_id']
        try:
            transaction = transaction_service.get_by_transaction(transaction_id)
            return TransactionSchema().dump(transaction), HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST

    @staticmethod
    @helper.token_required
    def put(current_user, **kwargs):
        transaction_id = kwargs['transaction_id']
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

    @staticmethod
    @helper.token_required
    def delete(current_user, **kwargs):
        transaction_id = kwargs['transaction_id']
        try:
            transaction_service.delete_transaction(transaction_id)
            return {"message": "Successfully deleted transaction."}, HTTPStatus.OK
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as err:
            return {"message": "Something went wrong", "errors": str(err)}, HTTPStatus.BAD_REQUEST


api.add_resource(TransactionList, "/transactions/<int:account_id>")
api.add_resource(TransactionDetail, "/transactions/<int:transaction_id>")
api.add_resource(TransactionListAll, "/transactions/<int:account_id>/for-account")
