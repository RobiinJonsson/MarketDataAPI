"""Routes package initialization"""

from flask import Flask
import logging

logger = logging.getLogger(__name__)

def register_routes(app: Flask) -> None:
    """Register all API route blueprints with the Flask app"""
    try:
        # Import blueprints individually to avoid conflicts
        from .common_routes import common_bp
        from .instrument_routes import instrument_bp
        from .entity_routes import entity_bp
        from .transparency_routes import transparency_bp
       
        
        # Register blueprints with error handling
        blueprints = [
            (common_bp, "common"),
            (instrument_bp, "instrument"),
            (entity_bp, "entity"),
            (transparency_bp, "transparency"),
        ]
        
        for blueprint, name in blueprints:
            try:
                # Check if blueprint is already registered using the blueprint's actual name
                if blueprint.name not in app.blueprints:
                    app.register_blueprint(blueprint)
                    logger.info(f"Registered {name} blueprint successfully")
                else:
                    logger.info(f"{name} blueprint already registered, skipping")
            except ValueError as e:
                logger.error(f"Error registering {name} blueprint: {e}")
                continue
                   
    except Exception as e:
        logger.error(f"Error during route registration: {e}")
        raise
