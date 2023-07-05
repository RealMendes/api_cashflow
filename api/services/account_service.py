from api import db
from ..models.account_model import Account
from marshmallow import ValidationError


class AccountService:
    def create_account(user_id):
        account_bd = Account(
            description='',
            balance=0,
            reserve=0,
            user_id=user_id
        )
        db.session.add(account_bd)
        db.session.commit()
        return account_bd

    def get_account(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            raise ValidationError("Account not found")
        return account

    def update_account(self, account_id, account_data):
        account = self.get_account(account_id)

        account_dict = account_data.to_dict()
        for key, value in account_dict.items():
            if value is not None:
                setattr(account, key, value)

        db.session.commit()
        return account

    def delete_account(self, account_id):
        self.get_account(account_id)
        account = Account.query.get(account_id)
        db.session.delete(account)
        db.session.commit()

    def get_balance(self, account_id):
        account = self.get_account(account_id)
        return account.balance

    def update_balance(self, account_id, transaction, operation_type, previous_value=None, type_transaction=None):
        account = self.get_account(account_id)
        balance = account.balance

        if operation_type == "create":
            if transaction.kind == "1":
                account.balance = balance + transaction.value
            elif transaction.kind == "2":
                account.balance = balance - transaction.value
        elif operation_type == "edit":
            if transaction.kind == "1":
                account.balance = balance - previous_value + transaction.value
            elif transaction.kind == "2":
                account.balance = balance + previous_value - transaction.value
        elif operation_type == "delete":
            if transaction.kind == "1":
                account.balance = balance - transaction.value
            elif transaction.kind == "2":
                account.balance = balance + transaction.value

        db.session.commit()
