import os

from flask import Blueprint, current_app, jsonify, send_from_directory

docs_bp = Blueprint("docs", __name__, url_prefix="/docs")


@docs_bp.route("/")
def docs_index():
    """Serve the main documentation index"""
    return send_from_directory(os.path.join(current_app.root_path, "..", "..", "docs"), "README.md")


@docs_bp.route("/api")
def api_docs():
    """Serve API documentation index"""
    return send_from_directory(
        os.path.join(current_app.root_path, "..", "..", "docs", "api"), "README.md"
    )


@docs_bp.route("/development")
def dev_docs():
    """Serve development documentation index"""
    return send_from_directory(
        os.path.join(current_app.root_path, "..", "..", "docs", "development"), "README.md"
    )


@docs_bp.route("/openapi")
def openapi_spec():
    """Serve the OpenAPI specification"""
    return send_from_directory(
        os.path.join(current_app.root_path, "..", "..", "docs", "openapi"),
        "openapi.yaml",
        mimetype="text/yaml",
    )


@docs_bp.route("/openapi-legacy")
def openapi_spec_legacy():
    """Serve the legacy OpenAPI specification (for comparison)"""
    return send_from_directory(
        os.path.join(current_app.root_path, "..", "..", "docs"),
        "openapi.yaml.backup",
        mimetype="text/yaml",
    )


@docs_bp.route("/test")
def test_docs():
    """Test route to verify docs blueprint is working"""
    return jsonify(
        {
            "status": "success",
            "message": "Documentation routes are working",
            "available_endpoints": [
                "/docs/ - Main documentation index",
                "/docs/api - API documentation",
                "/docs/development - Development documentation",
                "/docs/openapi - Generated OpenAPI specification",
                "/docs/openapi-legacy - Legacy OpenAPI specification",
            ],
        }
    )


@docs_bp.route("/status")
def docs_status():
    """Check status of documentation files"""
    import os

    from flask import current_app

    docs_root = os.path.join(current_app.root_path, "..", "docs")

    files_status = {}

    # Check for key documentation files
    check_files = ["README.md", "openapi/openapi.yaml", "openapi.yaml.backup", "api/README.md"]

    for file_path in check_files:
        full_path = os.path.join(docs_root, file_path)
        files_status[file_path] = {"exists": os.path.exists(full_path), "path": full_path}

    return jsonify({"status": "success", "docs_root": docs_root, "files": files_status})


@docs_bp.route("/regenerate")
def regenerate_docs():
    """Regenerate documentation from swagger definitions"""
    try:
        import subprocess
        import sys
        from pathlib import Path

        # Only allow in development/testing mode
        if not current_app.config.get("TESTING") and not current_app.config.get("DEBUG"):
            return (
                jsonify({"error": "Documentation regeneration only available in development mode"}),
                403,
            )

        # Run the generation script
        script_path = Path(current_app.root_path).parent / "scripts" / "generate_docs.py"
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)

        return jsonify(
            {
                "status": "success" if result.returncode == 0 else "error",
                "message": (
                    "Documentation regeneration completed"
                    if result.returncode == 0
                    else "Documentation regeneration failed"
                ),
                "output": result.stdout,
                "errors": result.stderr if result.stderr else None,
                "return_code": result.returncode,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Failed to regenerate documentation: {str(e)}"}), 500
