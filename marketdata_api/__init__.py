from flask import Flask
from marketdata_api.config import FLASK_ENV
from marketdata_api.database.base import init_db
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__,
                template_folder="../frontend/templates",
                static_folder="../frontend/static")
    app.config["ENV"] = FLASK_ENV

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # File handler for debug level
    debug_handler = RotatingFileHandler('logs/debug.log', maxBytes=10240, backupCount=10)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # Console handler for info level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Set root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(debug_handler)
    root_logger.addHandler(console_handler)

    # Initialize database and create tables
    app.logger.info("Initializing database...")
    init_db()
    app.logger.info("Database initialization complete")

    from marketdata_api.routes.market import market_bp
    from marketdata_api.routes.schema import schema_bp
    app.register_blueprint(market_bp)
    app.register_blueprint(schema_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=(FLASK_ENV == "development"))