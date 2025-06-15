#!/usr/bin/env python
"""
Validation script for MarketDataAPI refactoring

This script validates that the refactored routes are working correctly,
all imports are resolvable, and the API endpoints are accessible.
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def safe_print(message):
    """Print message with encoding safety for Windows terminals."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

def validate_imports():
    """Validate that all route modules can be imported"""
    try:
        # Test core route imports
        from marketdata_api.routes import (
            common_routes, instrument_routes, entity_routes, 
            cfi_routes, transparency_routes, schema, docs
        )
        safe_print("All route modules imported successfully")
        
        # Test swagger import
        from marketdata_api.routes.swagger import swagger_bp, api
        safe_print("Swagger module imported successfully")
        
        # Test route registration
        from marketdata_api.routes import register_routes
        safe_print("Route registration function imported successfully")
        
        return True
        
    except ImportError as e:
        safe_print(f"Import error: {e}")
        return False

def validate_service_layers():
    """Validate that service layers can be imported"""
    try:
        from marketdata_api.services import (
            instrument_service, legal_entity_service, transparency_service
        )
        safe_print("All service modules imported successfully")
        return True
        
    except ImportError as e:
        safe_print(f"Service import error: {e}")
        return False

def validate_flask_app_creation():
    """Validate that the Flask app can be created with all routes"""
    try:
        from flask import Flask
        from marketdata_api.routes import register_routes
        
        app = Flask(__name__)
        register_routes(app)
        
        # Check that blueprints are registered
        blueprint_names = [bp.name for bp in app.iter_blueprints()]
        expected_blueprints = [
            'common', 'frontend', 'instrument', 'entity', 
            'cfi', 'transparency', 'schema', 'docs'
        ]
        
        missing_blueprints = [bp for bp in expected_blueprints if bp not in blueprint_names]
        if missing_blueprints:
            safe_print(f"Missing blueprints: {missing_blueprints}")
            return False
            
        safe_print(f"Flask app created with all blueprints: {blueprint_names}")
        return True
        
    except Exception as e:
        safe_print(f"Flask app creation error: {e}")
        return False

def validate_documentation_structure():
    """Validate that documentation files exist"""
    docs_dir = project_root / 'docs'
    
    required_files = [
        'README.md',
        'api/transparency.md',
        'api/schemas.md',
        'api/instruments.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = docs_dir / file_path
        if not full_path.exists():
            missing_files.append(str(full_path))
    
    if missing_files:
        safe_print(f"Missing documentation files: {missing_files}")
        return False
    
    safe_print("All required documentation files exist")
    return True

def main():
    """Run all validation checks"""
    safe_print("Validating MarketDataAPI refactoring...")
    safe_print(f"Project root: {project_root}")
    
    checks = [
        ("Route Imports", validate_imports),
        ("Service Imports", validate_service_layers),
        ("Flask App Creation", validate_flask_app_creation),
        ("Documentation Structure", validate_documentation_structure)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        safe_print(f"\n-> Running {check_name} validation...")
        if check_func():
            passed += 1
        else:
            safe_print(f"X {check_name} validation failed")
    
    safe_print(f"\nValidation Results: {passed}/{total} checks passed")
    
    if passed == total:
        safe_print("All validations passed! The refactoring is successful.")
        return True
    else:
        safe_print("Some validations failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
