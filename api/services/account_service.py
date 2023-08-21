from api import db
from ..models.account_model import Account
from marshmallow import ValidationError

INPUT = 1
OUTPUT = 2
RESERVE = 3


class AccountService:
    @staticmethod
    def create_account(user_id):
        account = Account(
            description='',
            balance=0,
            reserve=0,
            user_id=user_id
        )
        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def get_account(account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            raise ValidationError("Account not found")
        return account

    @staticmethod
    def update_account(account_id, account_data):
        account = AccountService.get_account(account_id)

        account_dict = account_data.to_dict()
        for key, value in account_dict.items():
            if value is not None:
                setattr(account, key, value)

        db.session.commit()
        return account

    @staticmethod
    def delete_account(account_id):
        account = AccountService.get_account(account_id)
        db.session.delete(account)
        db.session.commit()

    @staticmethod
    def get_balance(account_id):
        account = AccountService.get_account(account_id)
        return account.balance

    @staticmethod
    def update_balance(account_id, transaction, operation_type, previous_value=None):
        account = AccountService.get_account(account_id)
        balance = account.balance
        reserve = account.reserve

        if operation_type == "create":
            if transaction.kind == INPUT:
                account.balance = balance + transaction.value
            elif transaction.kind == OUTPUT:
                account.balance = balance - transaction.value
            elif transaction.kind == RESERVE:
                account.reserve = reserve + transaction.value
        elif operation_type == "edit":
            if transaction.kind == INPUT:
                account.balance = balance - previous_value + transaction.value
            elif transaction.kind == OUTPUT:
                account.balance = balance + previous_value - transaction.value
            elif transaction.kind == RESERVE:
                raise ValidationError("You can't edit a reserve transaction")

        db.session.commit()

    @staticmethod
    def delete_balance_reserve(account_id, transaction):
        account = AccountService.get_account(account_id)
        balance = account.balance
        reserve = account.reserve
        if transaction.kind == INPUT:
            account.balance = balance - transaction.value
        elif transaction.kind == OUTPUT:
            account.balance = balance + transaction.value
        elif transaction.kind == RESERVE:
            account.reserve = reserve - transaction.value

        db.session.commit()
