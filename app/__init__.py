import os
from typing import Optional

from flask import Flask
from flask_jwt_extended import JWTManager

from app.core.error_handlers import error_handler_bp
from app.db.database import init_db
from app.extensions.sentry import init_sentry
from app.v1.api.routes import register_v1_routes
from config import DevelopmentConfig, ProductionConfig

jwt = JWTManager()


def create_app(db_url: Optional[str] = None, testing: Optional[bool] = False) -> Flask:
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    if testing:
        app.config["TESTING"] = testing

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or app.config["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    init_sentry(app)
    init_db(app)
    jwt.init_app(app)

    # Register blueprints
    register_v1_routes(app)

    # Register error handlers
    app.register_blueprint(error_handler_bp)

    return app
