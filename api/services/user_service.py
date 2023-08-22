from api import db
from ..models.user_model import User
from marshmallow import ValidationError
from .account_service import AccountService


class UserService:
    def create_user(self, user):
        user_bd = User(
            username=user.username,
            email=user.email,
            password=user.password
        )
        user_bd.hash_password()
        db.session.add(user_bd)
        db.session.commit()

        id_user = user_bd.id
        AccountService.create_account(id_user)

    def get_user_by_id(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise ValidationError("User not found")
        return user

    def get_user_by_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise ValidationError("User not found")
        return user

    def delete_user_by_id(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise ValidationError("User not found")
        db.session.delete(user)
        db.session.commit()
        return user

    def get_users(self):
        users = User.query.all()
        return users

    def user_by_username(username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise ValidationError("User not found")
        return user

    def update_user_by_id(self, user_id, user_data):
        user = self.get_user_by_id(user_id)

        user_dict = user_data.to_dict()
        for key, value in user_dict.items():
            if value is not None and key != "password":
                setattr(user, key, value)

        new_password = user_data.password
        if new_password:
            user.password = new_password
            user.hash_password()

        db.session.commit()
        return user
