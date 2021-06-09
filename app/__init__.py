from flask import Flask
from app.api.database import DB, MA
from app.api import rest_api
from app.constants import SQLALCHEMY_DATABASE_URI_FORMAT
from flask_cors import CORS

def create_app() -> (Flask):
    app = Flask(__name__)
    app.app_context().push()

    app.config['DEBUG'] = True
    app.config['SQLALCHEMY'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_FORMAT
    app.config['SERVER_NAME'] = 'server_name'
    app.secret_key = 'abcdefghijklmnopqrstuvwxyz'

    DB.init_app(app)
    DB.create_all()
    MA.init_app(app)
    rest_api.init_app(app)
    CORS(app)

    return app