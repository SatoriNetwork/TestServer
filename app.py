# app.py
from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db  # Import db from extensions.py

def create_flask_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app

def init_database(app):
    db.init_app(app)

def create_api(app):
    return Api(app, title='Proposal API', version='1.0', description='API for managing proposals and votes')

def register_api_routes(api):
    from api import register_routes
    register_routes(api)

def create_app(config_class=Config):
    try:
        # 1. Create the Flask app
        app = create_flask_app(config_class)
        
        # 2. Initialize the database
        init_database(app)
        
        # 3. Create the API
        api = create_api(app)
        
        # 4. Register API routes
        register_api_routes(api)
        
        return app
    except Exception as e:
        print(f"Error creating app: {e}")
        return None

# This create_app function is typically called in main.py or wherever you start your application