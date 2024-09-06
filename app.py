from flask import Flask
from flask_restx import Api
from config import Config
from models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    api = Api(app, title='Proposal API', version='1.0', description='API for managing proposals and votes.')

    from api import register_routes
    register_routes(api)

    return app