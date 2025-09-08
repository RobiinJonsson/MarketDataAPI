from flask import Flask
from flask_cors import CORS
from marketdata_api.config import FLASK_ENV, Config
from marketdata_api.database import init_database
import logging
import os

def create_app():
    app = Flask(__name__,
                template_folder="../frontend/templates",
                static_folder="../frontend/static")
    app.config["ENV"] = FLASK_ENV
    app.config["ROOT_PATH"] = Config.ROOT_PATH

    # Enable CORS for all routes
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

    # Set up logging and register cleanup
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Simple file handler without rotation to avoid numbered backups
    debug_handler = logging.FileHandler(
        'logs/debug.log',
        mode='a',  # Append mode
        encoding='utf-8'
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
    
    # Initialize database and create tables
    app.logger.info("Initializing database...")
    init_database()
    app.logger.info("Database initialization complete")
    
    from marketdata_api.routes.schema import schema_bp
    from marketdata_api.swagger import create_swagger_blueprint  # Import the modular Swagger blueprint
    from marketdata_api.routes.docs import docs_bp  # Import the Docs API blueprint
    from marketdata_api.routes.common_routes import frontend_bp  # Import the frontend blueprint
    from marketdata_api.routes.file_management import file_management_bp  # Import file management blueprint
    from marketdata_api.routes.mic_routes import mic_bp  # Import MIC routes (separate from swagger)
    
    app.register_blueprint(schema_bp)
    
    # Register the modular Swagger blueprint (instruments, legal entities, transparency)
    # This provides both the API endpoints AND the SwaggerUI at /api/v1/swagger/
    swagger_bp = create_swagger_blueprint()
    app.register_blueprint(swagger_bp)
    
    # Register the separate MIC blueprint (keeps existing working MIC endpoints)
    app.register_blueprint(mic_bp)
    
    app.register_blueprint(docs_bp)  # Register the Docs API blueprint
    app.register_blueprint(frontend_bp)  # Register the frontend blueprint
    app.register_blueprint(file_management_bp)  # Register file management blueprint

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=(FLASK_ENV == "development"))