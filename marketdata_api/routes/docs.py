from flask import Blueprint, send_from_directory, current_app
import os

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

@docs_bp.route('/api/<path:filename>')
def api_docs(filename):
    """Serve API documentation markdown files"""
    docs_dir = os.path.join(current_app.config['ROOT_PATH'], 'docs', 'api')
    return send_from_directory(docs_dir, filename)
