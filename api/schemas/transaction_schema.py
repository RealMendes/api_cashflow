from api import ma
from ..models import transaction_model
from marshmallow import fields


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = transaction_model.Transaction
        load_instance = True

    name = fields.String(required=True)
    description = fields.String(required=True)
    value = fields.Float(required=True)
    kind = fields.String(required=True)
    account_id = fields.Integer(required=False)
