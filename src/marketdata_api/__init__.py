import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from marketdata_api.config import FLASK_ENV, Config, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES
from marketdata_api.database import init_database


def create_app(config_override=None):
    app = Flask(
        __name__, template_folder="../../frontend-modern/dist", static_folder="../../frontend-modern/dist/assets"
    )
    app.config["ENV"] = FLASK_ENV
    app.config["ROOT_PATH"] = Config.ROOT_PATH
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Configure JSON serialization to handle NaN values
    import json
    import math
    
    def default_json_handler(obj):
        """Handle special values in JSON serialization"""
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
        raise TypeError(f"Object {obj} is not JSON serializable")
    
    app.json.default = default_json_handler
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["1000 per hour", "100 per minute"],
        storage_uri="memory://",
        strategy="fixed-window"
    )

    # Apply test configuration if provided
    if config_override:
        app.config.update(config_override)

    # Enable CORS for all routes with comprehensive configuration
    # In development, be more permissive with origins
    if FLASK_ENV == "development":
        CORS(app, 
             origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
             allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
             supports_credentials=True,
             expose_headers=["Content-Range", "X-Content-Range"])
    else:
        CORS(app, 
             origins=["http://localhost:3000"],  # Restrict in production
             allow_headers=["Content-Type", "Authorization"],
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             supports_credentials=False)

    # Set up logging and register cleanup
    logs_dir = os.path.join(Config.ROOT_PATH, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

    # Simple file handler without rotation to avoid numbered backups
    debug_handler = logging.FileHandler(
        os.path.join(logs_dir, "debug.log"), mode="a", encoding="utf-8"  # Append mode
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # Console handler for info level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Clear existing handlers to prevent duplicates
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Set root logger
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(debug_handler)
    root_logger.addHandler(console_handler)

    # Configure specific loggers for development
    # Suppress SQLite engine creation spam but keep other important messages
    sqlite_logger = logging.getLogger('marketdata_api.database.sqlite.sqlite_database')
    sqlite_logger.setLevel(logging.WARNING)
    
    # Reduce rate limiter warnings in development (but keep errors)
    rate_limiter_logger = logging.getLogger('marketdata_api.auth.rate_limiting')
    rate_limiter_logger.setLevel(logging.ERROR)
    
    # Keep HTTP request logging (werkzeug) at INFO level for development visibility
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    
    # Also ensure Flask's built-in logger shows HTTP requests in development
    if FLASK_ENV == "development":
        app.logger.setLevel(logging.INFO)
        # Enable werkzeug access logs
        werkzeug_access_logger = logging.getLogger('werkzeug._internal')
        werkzeug_access_logger.setLevel(logging.INFO)

    # Initialize database and create tables (skip during testing)
    if not app.config.get("TESTING"):
        from marketdata_api.config import DatabaseConfig
        db_type = DatabaseConfig.get_database_type()
        app.logger.info(f"Initializing database... (Database Type: {db_type.upper()})")
        init_database()
        app.logger.info("Database initialization complete")

    from marketdata_api.api.resources.frontend import create_frontend_blueprint  # Import frontend blueprint function
    from marketdata_api.api import (  # Import the consolidated API blueprint
        create_swagger_blueprint,
    )

    # Register the consolidated Swagger blueprint (all API endpoints)
    # This provides: instruments, legal entities, transparency, MIC, schema, files, system, docs, frontend
    # AND the SwaggerUI at /api/v1/swagger/
    swagger_bp = create_swagger_blueprint()
    app.register_blueprint(swagger_bp)

    # Create and register the frontend blueprint (non-API routes for serving templates)
    frontend_bp = create_frontend_blueprint()
    app.register_blueprint(frontend_bp)  # Register the frontend blueprint

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=(FLASK_ENV == "development"))
