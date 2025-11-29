"""Authentication decorators for API endpoint protection"""

from functools import wraps
from typing import List, Optional, Union
from flask import request, jsonify, g, current_app
import logging

from ..services.core.auth_service import auth_service

logger = logging.getLogger(__name__)


def require_auth(f):
    """
    Decorator to require authentication for an endpoint.
    Verifies JWT token and sets g.current_user.
    Skips authentication for SQLite (development mode).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip authentication for SQLite (development mode)
        if not auth_service.is_authentication_enabled():
            logger.debug("Authentication disabled for SQLite development mode")
            g.current_user = None
            return f(*args, **kwargs)
        
        try:
            # Get token from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Missing Authorization header'
                }), 401
            
            # Extract token from "Bearer <token>" format
            if not auth_header.startswith('Bearer '):
                return jsonify({
                    'error': 'Invalid authentication format',
                    'message': 'Authorization header must start with "Bearer "'
                }), 401
            
            token = auth_header.split(' ')[1]
            
            # Verify token
            payload = auth_service.verify_token(token)
            
            # Set current user in Flask g object
            g.current_user = {
                'id': payload.get('user_id'),
                'username': payload.get('username'),
                'email': payload.get('email'),
                'roles': payload.get('roles', []),
                'permissions': payload.get('permissions', [])
            }
            
            logger.debug(f"Authenticated user: {g.current_user['username']}")
            return f(*args, **kwargs)
            
        except ValueError as e:
            logger.warning(f"Authentication failed: {e}")
            return jsonify({
                'error': 'Authentication failed',
                'message': str(e)
            }), 401
        except Exception as e:
            logger.error(f"Unexpected authentication error: {e}")
            return jsonify({
                'error': 'Authentication error',
                'message': 'An unexpected error occurred'
            }), 500
    
    return decorated_function


def require_role(required_roles: Union[str, List[str]]):
    """
    Decorator to require specific role(s) for an endpoint.
    Must be used after @require_auth.
    
    Args:
        required_roles: Single role string or list of roles (OR logic)
    """
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Check if user is authenticated (should be set by @require_auth)
                if not hasattr(g, 'current_user') or not g.current_user:
                    return jsonify({
                        'error': 'Authentication required',
                        'message': 'User must be authenticated to access this resource'
                    }), 401
                
                user_roles = g.current_user.get('roles', [])
                
                # Check if user has any of the required roles
                has_required_role = any(role in user_roles for role in required_roles)
                
                if not has_required_role:
                    logger.warning(f"Access denied for user {g.current_user['username']}: "
                                 f"requires {required_roles}, has {user_roles}")
                    return jsonify({
                        'error': 'Insufficient permissions',
                        'message': f'This operation requires one of these roles: {", ".join(required_roles)}'
                    }), 403
                
                logger.debug(f"Role check passed for user {g.current_user['username']}: "
                           f"has {user_roles}, required {required_roles}")
                return f(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Role check error: {e}")
                return jsonify({
                    'error': 'Authorization error',
                    'message': 'An unexpected error occurred during authorization'
                }), 500
        
        return decorated_function
    return decorator


def require_permission(required_permissions: Union[str, List[str]]):
    """
    Decorator to require specific permission(s) for an endpoint.
    Must be used after @require_auth.
    
    Args:
        required_permissions: Single permission string or list of permissions (OR logic)
    """
    if isinstance(required_permissions, str):
        required_permissions = [required_permissions]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Check if user is authenticated
                if not hasattr(g, 'current_user') or not g.current_user:
                    return jsonify({
                        'error': 'Authentication required',
                        'message': 'User must be authenticated to access this resource'
                    }), 401
                
                user_permissions = g.current_user.get('permissions', [])
                
                # Check if user has any of the required permissions
                has_required_permission = any(perm in user_permissions for perm in required_permissions)
                
                if not has_required_permission:
                    logger.warning(f"Access denied for user {g.current_user['username']}: "
                                 f"requires {required_permissions}, has {user_permissions}")
                    return jsonify({
                        'error': 'Insufficient permissions',
                        'message': f'This operation requires one of these permissions: {", ".join(required_permissions)}'
                    }), 403
                
                logger.debug(f"Permission check passed for user {g.current_user['username']}: "
                           f"has {user_permissions}, required {required_permissions}")
                return f(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Permission check error: {e}")
                return jsonify({
                    'error': 'Authorization error',
                    'message': 'An unexpected error occurred during authorization'
                }), 500
        
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorator to require admin role.
    Convenience decorator equivalent to @require_role(['admin']).
    Must be used after @require_auth.
    """
    @wraps(f)
    @require_role(['admin'])
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    
    return decorated_function


def user_or_admin(f):
    """
    Decorator to require user or admin role.
    Must be used after @require_auth.
    """
    @wraps(f)
    @require_role(['user', 'admin'])
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    
    return decorated_function


def method_based_auth(read_permissions: List[str] = None, write_permissions: List[str] = None):
    """
    Decorator to apply different authentication based on HTTP method.
    GET requests require read permissions, POST/PUT/DELETE require write permissions.
    
    Args:
        read_permissions: Permissions required for GET requests (default: ['user', 'admin'])
        write_permissions: Permissions required for POST/PUT/DELETE requests (default: ['admin'])
    """
    if read_permissions is None:
        read_permissions = ['user', 'admin']
    if write_permissions is None:
        write_permissions = ['admin']
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First ensure user is authenticated
            auth_result = require_auth(lambda: None)()
            if auth_result is not None:  # Auth failed
                return auth_result
            
            # Apply role-based logic based on method
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                # Read operations - allow user or admin
                role_check = require_role(read_permissions)(lambda: None)()
            else:
                # Write operations - require admin only
                role_check = require_role(write_permissions)(lambda: None)()
            
            if role_check is not None:  # Role check failed
                return role_check
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_user() -> Optional[dict]:
    """
    Utility function to get current user from Flask g.
    Returns None if no user is authenticated.
    """
    return getattr(g, 'current_user', None)


def is_admin() -> bool:
    """
    Utility function to check if current user is an admin.
    """
    user = get_current_user()
    return user and 'admin' in user.get('roles', [])


def has_permission(permission: str) -> bool:
    """
    Utility function to check if current user has a specific permission.
    """
    user = get_current_user()
    return user and permission in user.get('permissions', [])


def has_role(role: str) -> bool:
    """
    Utility function to check if current user has a specific role.
    """
    user = get_current_user()
    return user and role in user.get('roles', [])