from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    init_app(app)

    # Register routes
    from .cuatom_auth_router import auth_bp
    from .core_ams_routers import bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp, url_prefix='/auth_bp')

    return app
