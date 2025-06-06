import logging
from flask import Blueprint, jsonify
from ..models.utils.cfi import CFI
from ..constants import (
    HTTPStatus, API, CFI as CFIConstants, 
    ErrorMessages, ResponseFields, Endpoints
)

# Setup logging
logger = logging.getLogger(__name__)

# Create blueprint for CFI operations
cfi_bp = Blueprint("cfi", __name__, url_prefix=API.PREFIX)

@cfi_bp.route(f"{Endpoints.CFI}/<string:cfi_code>", methods=["GET"])
def decode_cfi(cfi_code):
    """Decode a CFI code and return human-readable attributes"""
    try:
        cfi_code = cfi_code.upper()
        
        if len(cfi_code) != CFIConstants.REQUIRED_LENGTH:
            return jsonify({ResponseFields.ERROR: ErrorMessages.INVALID_CFI_LENGTH}), HTTPStatus.BAD_REQUEST
            
        cfi = CFI(cfi_code)
        result = cfi.describe()
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.error(f"Error in decode_cfi: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
