from api import ma
from ..models import user_model
from marshmallow import fields
from ..schemas import account_schema


class UserSchema(ma.SQLAlchemyAutoSchema):
    accounts = fields.Nested(account_schema.AccountSchema, many=True)

    class Meta:
        model = user_model.User
        load_instance = True

    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
