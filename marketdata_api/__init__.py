from flask import Flask
from marketdata_api.config import FLASK_ENV, Config
from marketdata_api.database.base import init_db
import logging
from logging.handlers import RotatingFileHandler
import os
import glob

def create_app():
    app = Flask(__name__,
                template_folder="../frontend/templates",
                static_folder="../frontend/static")
    app.config["ENV"] = FLASK_ENV
    app.config["ROOT_PATH"] = Config.ROOT_PATH

    # Set up logging and register cleanup
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Improved file handler with larger buffer and delay
    debug_handler = RotatingFileHandler(
        'logs/debug.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        delay=True,  # Don't create file until first write
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
    root_logger.addHandler(console_handler)    # Initialize database and create tables
    app.logger.info("Initializing database...")
    init_db()
    app.logger.info("Database initialization complete")
    from marketdata_api.routes.schema import schema_bp
    from marketdata_api.routes.swagger import swagger_bp  # Import the Swagger API blueprint
    from marketdata_api.routes.docs import docs_bp  # Import the Docs API blueprint
    from marketdata_api.routes.common_routes import frontend_bp  # Import the frontend blueprint
    # Import the new refactored routes registration function
    from marketdata_api.routes import register_routes
    
    app.register_blueprint(schema_bp)
    app.register_blueprint(swagger_bp)  # Register the Swagger API blueprint
    app.register_blueprint(docs_bp)  # Register the Docs API blueprint
    app.register_blueprint(frontend_bp)  # Register the frontend blueprint
    
    # Register all the refactored CRUD routes
    register_routes(app)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=(FLASK_ENV == "development"))