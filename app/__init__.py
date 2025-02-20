from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_restx import Api

# Initialize SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)

api = Api(
    app,
    version='1.0',
    title='Flask API with JWT and Swagger',
    description='A simple API demonstrating JWT authentication and Swagger documentation',
    doc='/swagger',  # Swagger UI documentation URL
    security='Bearer',  # Define Bearer token security globally for Swagger
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    default='Default',  # Default namespace
    default_label='API Endpoints'
)

def init_app(app):
    db.init_app(app)

def create_app():
    # Initialize the Flask app

    app.config.from_object(Config)

    # Initialize the database
    init_app(app)

    # Register routes
    from .cuatom_auth_router import auth
    from .core_ams_routers import bp
    app.register_blueprint(bp)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
