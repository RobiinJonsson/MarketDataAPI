"""
Common API utilities for Flask-RESTX resources.

This module provides common functionality used across all API resources,
including error handling, validation, and response formatting.
"""

import logging
from functools import wraps
from typing import Any, Dict

from flask import request
from flask_restx import abort

from ...constants import ErrorMessages, HTTPStatus, ResponseFields

logger = logging.getLogger(__name__)


def handle_api_errors(f):
    """
    Decorator to standardize error handling across all API endpoints.
    
    Args:
        f: Function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {f.__name__}: {str(e)}")
            return {
                ResponseFields.ERROR: ErrorMessages.INVALID_REQUEST_BODY,
                "details": str(e),
            }, HTTPStatus.BAD_REQUEST
        except KeyError as e:
            logger.error(f"Missing required field in {f.__name__}: {str(e)}")
            return {
                ResponseFields.ERROR: f"Missing required field: {str(e)}",
            }, HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}", exc_info=True)
            return {
                ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                "details": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
    return wrapper


def validate_pagination_params():
    """
    Validate and normalize pagination parameters from request.
    
    Returns:
        Dict containing validated pagination parameters
    """
    try:
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(1000, max(1, int(request.args.get('per_page', 20))))
        limit = request.args.get('limit', type=int)
        offset = max(0, int(request.args.get('offset', 0)))
        
        return {
            'page': page,
            'per_page': per_page,
            'limit': limit,
            'offset': offset,
        }
    except (ValueError, TypeError) as e:
        abort(HTTPStatus.BAD_REQUEST, f"Invalid pagination parameters: {str(e)}")


def validate_filter_params(allowed_filters: Dict[str, Any]):
    """
    Validate filter parameters against allowed filters.
    
    Args:
        allowed_filters: Dictionary of allowed filter names and their validation functions
        
    Returns:
        Dict of validated filter parameters
    """
    filters = {}
    
    for param_name, validator in allowed_filters.items():
        value = request.args.get(param_name)
        if value is not None:
            try:
                if validator:
                    filters[param_name] = validator(value)
                else:
                    filters[param_name] = value
            except (ValueError, TypeError) as e:
                abort(HTTPStatus.BAD_REQUEST, f"Invalid {param_name}: {str(e)}")
    
    return filters


def format_success_response(data: Any, message: str = "Success", **kwargs):
    """
    Format a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        **kwargs: Additional response fields
        
    Returns:
        Formatted response dictionary
    """
    response = {
        ResponseFields.STATUS: "success",
        ResponseFields.MESSAGE: message,
        "data": data,
    }
    response.update(kwargs)
    return response


def format_error_response(error: str, details: str = None, **kwargs):
    """
    Format a standardized error response.
    
    Args:
        error: Error message
        details: Additional error details
        **kwargs: Additional response fields
        
    Returns:
        Formatted error response dictionary
    """
    response = {
        ResponseFields.STATUS: "error",
        ResponseFields.ERROR: error,
    }
    if details:
        response["details"] = details
    response.update(kwargs)
    return response


def validate_json_request(required_fields: list = None):
    """
    Validate JSON request body and check for required fields.
    
    Args:
        required_fields: List of required field names
        
    Returns:
        Parsed JSON data
        
    Raises:
        ValueError: If validation fails
    """
    data = request.get_json()
    if not data:
        raise ValueError("Request body must be valid JSON")
    
    if required_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return data


# Common validation functions
def validate_isin(isin: str) -> str:
    """Validate ISIN format."""
    if not isin or len(isin) != 12:
        raise ValueError("ISIN must be exactly 12 characters")
    return isin.upper()


def validate_cfi_code(cfi: str) -> str:
    """Validate CFI code format."""
    if not cfi or len(cfi) != 6:
        raise ValueError("CFI code must be exactly 6 characters")
    return cfi.upper()


def validate_mic_code(mic: str) -> str:
    """Validate MIC code format."""
    if not mic or len(mic) != 4:
        raise ValueError("MIC code must be exactly 4 characters")
    return mic.upper()


def validate_currency_code(currency: str) -> str:
    """Validate currency code format."""
    if not currency or len(currency) != 3:
        raise ValueError("Currency code must be exactly 3 characters")
    return currency.upper()