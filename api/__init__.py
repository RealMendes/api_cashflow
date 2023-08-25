from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api

db = SQLAlchemy()
ma = Marshmallow()
mi = Migrate()
api = Api(version='1.0', title='CashFlow', description='Financial control API')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    ma.init_app(app)
    mi.init_app(app, db)
    api.init_app(app)

    from .models import account_model
    from .views import account_view

    from .models import transaction_model
    from .views import transaction_view

    from .models import user_model
    from .views import user_view

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
