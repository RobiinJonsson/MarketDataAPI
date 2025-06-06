"""Routes package initialization"""

from flask import Flask
from .common_routes import common_bp
from .instrument_routes import instrument_bp
from .entity_routes import entity_bp
from .cfi_routes import cfi_bp
# Import any other route modules here

def register_routes(app: Flask) -> None:
    """Register all API route blueprints with the Flask app"""
    app.register_blueprint(common_bp)
    app.register_blueprint(instrument_bp)
    app.register_blueprint(entity_bp)
    app.register_blueprint(cfi_bp)
    # Register any other blueprints here
