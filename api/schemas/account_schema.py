from api import ma
from ..models import account_model
from marshmallow import fields
from ..schemas import transaction_schema


class AccountSchema(ma.SQLAlchemyAutoSchema):
    transactions = ma.Nested(transaction_schema.TransactionSchema, many=True)

    class Meta:
        model = account_model.Account
        load_instance = True

    description = fields.String(required=True)
    balance = fields.Float(required=True)
    user_id = fields.Integer(required=True)
