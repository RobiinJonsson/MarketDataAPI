"""
Frontend Utilities

This module contains utility functions for frontend operations.
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def get_frontend_template_path(template_name: str) -> str:
    """
    Get the full path to a frontend template file.
    
    Args:
        template_name: Name of the template file
        
    Returns:
        str: Full path to the template
    """
    from flask import current_app
    
    template_dir = current_app.template_folder
    return os.path.join(template_dir, template_name)


def validate_frontend_templates() -> dict:
    """
    Validate that required frontend templates exist.
    
    Returns:
        dict: Validation results with template status
    """
    required_templates = ["index.html", "admin.html"]
    results = {
        "valid": True,
        "templates": {},
        "missing": []
    }
    
    try:
        from flask import current_app
        
        template_dir = current_app.template_folder
        
        for template in required_templates:
            template_path = os.path.join(template_dir, template)
            exists = os.path.exists(template_path)
            
            results["templates"][template] = {
                "exists": exists,
                "path": template_path
            }
            
            if not exists:
                results["missing"].append(template)
                results["valid"] = False
                
    except Exception as e:
        logger.error(f"Error validating frontend templates: {str(e)}")
        results["valid"] = False
        results["error"] = str(e)
        
    return results


def get_frontend_assets_info() -> dict:
    """
    Get information about frontend assets.
    
    Returns:
        dict: Frontend assets information
    """
    try:
        from flask import current_app
        
        static_dir = current_app.static_folder
        assets_info = {
            "static_folder": static_dir,
            "assets": []
        }
        
        if static_dir and os.path.exists(static_dir):
            assets_dir = os.path.join(static_dir, "assets")
            if os.path.exists(assets_dir):
                assets_info["assets"] = [
                    f for f in os.listdir(assets_dir) 
                    if os.path.isfile(os.path.join(assets_dir, f))
                ]
        
        return assets_info
        
    except Exception as e:
        logger.error(f"Error getting frontend assets info: {str(e)}")
        return {"error": str(e)}


def build_frontend_status() -> dict:
    """
    Build comprehensive frontend status information.
    
    Returns:
        dict: Complete frontend status
    """
    return {
        "templates": validate_frontend_templates(),
        "assets": get_frontend_assets_info(),
        "status": "operational"
    }