"""
Response Builder Utilities

Common utilities for building standardized API responses.
Extracted from various route files for consistency across the application.
"""

from typing import Any, Dict, List, Optional
from ...constants import ResponseFields


def build_success_response(data: Any, message: str = "Success", **kwargs) -> Dict[str, Any]:
    """
    Build a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        **kwargs: Additional response fields
        
    Returns:
        dict: Standardized success response
    """
    response = {
        ResponseFields.STATUS: "success",
        ResponseFields.MESSAGE: message,
        ResponseFields.DATA: data,
    }
    response.update(kwargs)
    return response


def build_error_response(error: str, details: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Build a standardized error response.
    
    Args:
        error: Error message
        details: Additional error details
        **kwargs: Additional response fields
        
    Returns:
        dict: Standardized error response
    """
    response = {
        ResponseFields.STATUS: "error",
        ResponseFields.ERROR: error,
    }
    if details:
        response["details"] = details
    response.update(kwargs)
    return response


def build_paginated_response(items: List[Any], total_count: int, page: int = 1, 
                            per_page: int = 20, message: str = "Success") -> Dict[str, Any]:
    """
    Build a standardized paginated response.
    
    Args:
        items: List of items for current page
        total_count: Total number of items across all pages
        page: Current page number
        per_page: Items per page
        message: Response message
        
    Returns:
        dict: Standardized paginated response
    """
    return {
        ResponseFields.STATUS: "success",
        ResponseFields.MESSAGE: message,
        ResponseFields.DATA: items,
        ResponseFields.META: {
            ResponseFields.PAGE: page,
            ResponseFields.PER_PAGE: per_page,
            ResponseFields.TOTAL: total_count,
            "has_next": (page * per_page) < total_count,
            "has_prev": page > 1,
        },
    }


def build_validation_error_response(errors: List[str]) -> Dict[str, Any]:
    """
    Build a standardized validation error response.
    
    Args:
        errors: List of validation error messages
        
    Returns:
        dict: Standardized validation error response
    """
    return {
        ResponseFields.STATUS: "error",
        ResponseFields.ERROR: "Validation failed",
        "validation_errors": errors,
    }


def extract_pagination_params(args: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract and validate pagination parameters from request arguments.
    
    Args:
        args: Request arguments dictionary
        
    Returns:
        dict: Validated pagination parameters
    """
    try:
        page = max(1, int(args.get('page', 1)))
        per_page = min(1000, max(1, int(args.get('per_page', 20))))
        limit = args.get('limit', type=int)
        offset = max(0, int(args.get('offset', 0)))
        
        return {
            'page': page,
            'per_page': per_page,
            'limit': limit,
            'offset': offset,
        }
    except (ValueError, TypeError):
        return {
            'page': 1,
            'per_page': 20,
            'limit': None,
            'offset': 0,
        }