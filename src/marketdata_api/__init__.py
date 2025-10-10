import logging
import os

from flask import Flask
from flask_cors import CORS

from marketdata_api.config import FLASK_ENV, Config
from marketdata_api.database import init_database


def create_app(config_override=None):
    app = Flask(
        __name__, template_folder="../../frontend/templates", static_folder="../../frontend/static"
    )
    app.config["ENV"] = FLASK_ENV
    app.config["ROOT_PATH"] = Config.ROOT_PATH

    # Apply test configuration if provided
    if config_override:
        app.config.update(config_override)

    # Enable CORS for all routes
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

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

    # Initialize database and create tables (skip during testing)
    if not app.config.get("TESTING"):
        app.logger.info("Initializing database...")
        init_database()
        app.logger.info("Database initialization complete")

    from marketdata_api.routes.common_routes import common_bp, frontend_bp  # Import both blueprints
    from marketdata_api.routes.docs import docs_bp  # Import the Docs API blueprint
    from marketdata_api.api import (  # Import the consolidated API blueprint
        create_swagger_blueprint,
    )

    # Register the consolidated Swagger blueprint (all API endpoints)
    # This provides: instruments, legal entities, transparency, MIC, schema, files
    # AND the SwaggerUI at /api/v1/swagger/
    swagger_bp = create_swagger_blueprint()
    app.register_blueprint(swagger_bp)

    app.register_blueprint(docs_bp)  # Register the Docs API blueprint
    app.register_blueprint(common_bp)  # Register the common API blueprint
    app.register_blueprint(frontend_bp)  # Register the frontend blueprint

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=(FLASK_ENV == "development"))
