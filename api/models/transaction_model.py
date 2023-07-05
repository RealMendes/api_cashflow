from api import db
import enum


class TipoEnum(enum.Enum):
    input = 1
    output = 2
    reserve = 3


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    kind = db.Column(db.Enum(TipoEnum), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    account = db.relationship("Account", backref=db.backref("transactions", lazy="dynamic"))

    def to_dict(self):
        return {
            "id": self.id, "name": self.name,
            "description": self.description,
            "value": self.value, "kind": self.kind
        }
