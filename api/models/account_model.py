from api import db
from .user_model import User

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    reserve = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(User, backref=db.backref("accounts", lazy="dynamic"))

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "balance": self.balance,
            "reserve": self.reserve
        }
