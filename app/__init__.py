from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database with the app
    db.init_app(app)

    # Import and register routes
    from . import routes
    app.register_blueprint(routes.bp)

    # Import models
    from . import model

    return app