from ..models.transaction_model import Transaction
from api import db
from marshmallow import ValidationError
from ..services.account_service import AccountService

_ACCOUNT = AccountService()

CREATE = "create"
EDIT = "edit"
DELETE = "delete"


class TransactionService:
    def create_transaction(self, transaction):
        transaction_db = Transaction(
            name=transaction.name,
            description=transaction.description,
            value=transaction.value,
            kind=transaction.kind,
            account_id=transaction.account_id
        )
        db.session.add(transaction_db)
        _ACCOUNT.update_balance(transaction.account_id, transaction, CREATE)
        db.session.commit()
        return transaction_db

    @staticmethod
    def get_all_transactions_ids(account_id):
        transactions = db.session.query(Transaction).filter_by(account_id=account_id).all()
        transaction_ids = [transaction.id for transaction in transactions]
        return transaction_ids

    def get_by_transaction(self, transaction_id):
        transaction = Transaction.query.filter_by(id=transaction_id).first()
        if transaction is None:
            raise ValidationError("Transaction not found")
        return transaction

    def update_transaction(self, transaction_id, transaction_data):
        transaction = self.get_by_transaction(transaction_id)

        transaction_dict = transaction_data.to_dict()

        if transaction.kind != transaction_dict["kind"] or transaction.value != transaction_dict["value"]:
            _ACCOUNT.update_balance(transaction.account_id, transaction, EDIT, transaction_dict["value"],
                                    transaction_dict["kind"])

        for key, value in transaction_dict.items():
            if value is not None:
                setattr(transaction, key, value)

        db.session.commit()

        return transaction

    def delete_transaction(self, transaction_id):
        transaction = self.get_by_transaction(transaction_id)
        account_id = transaction.account_id
        _ACCOUNT.update_balance(account_id, transaction, DELETE)
        db.session.delete(transaction)
        db.session.commit()
