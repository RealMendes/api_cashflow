from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db = SQLAlchemy(app)
    ma = Marshmallow(app)
    mi = Migrate(app, db)

    api = Api(app, version='1.0', title='CashFlow', description='Financial control API')

    from .models import account_model
    from .views import account_view

    from .models import transaction_model
    from .views import transaction_view

    from .models import user_model
    from .views import user_view

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
