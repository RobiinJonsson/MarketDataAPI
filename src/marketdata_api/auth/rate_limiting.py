"""Rate limiting utilities with role-based limits"""

from functools import wraps
from typing import Dict, List, Union
import logging
from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from ..auth.decorators import get_current_user, has_role
from ..services.core.auth_service import auth_service

logger = logging.getLogger(__name__)


class RoleBasedRateLimiter:
    """Rate limiter that applies different limits based on user roles"""
    
    def __init__(self, limiter: Limiter):
        self.limiter = limiter
        
        # Define rate limits per role
        self.role_limits = {
            "admin": {
                "per_minute": 200,  # Higher limits for admins
                "per_hour": 5000,
                "burst": 50
            },
            "user": {
                "per_minute": 60,   # Standard limits for users  
                "per_hour": 1000,
                "burst": 20
            },
            "anonymous": {       # For unauthenticated requests (SQLite mode)
                "per_minute": 30,
                "per_hour": 500,
                "burst": 10
            }
        }
    
    def get_user_role(self) -> str:
        """Determine the current user's effective role for rate limiting"""
        # If authentication is disabled (SQLite mode), treat as anonymous
        if not auth_service.is_authentication_enabled():
            return "anonymous"
        
        current_user = get_current_user()
        if not current_user:
            return "anonymous"
        
        # Check roles in priority order (admin > user)
        if has_role("admin"):
            return "admin"
        elif has_role("user"):
            return "user"
        else:
            return "anonymous"
    
    def get_limits_for_role(self, role: str) -> Dict[str, int]:
        """Get rate limits for a specific role"""
        return self.role_limits.get(role, self.role_limits["anonymous"])
    
    def create_limit_string(self, role: str, operation_type: str = "standard") -> str:
        """Create Flask-Limiter compatible limit string for role"""
        limits = self.get_limits_for_role(role)
        
        if operation_type == "read":
            # More permissive for read operations
            return f"{limits['per_minute']} per minute; {limits['per_hour']} per hour"
        elif operation_type == "write":
            # More restrictive for write operations (admin only)
            if role == "admin":
                return f"{limits['per_minute']//2} per minute; {limits['per_hour']//2} per hour"
            else:
                return "0 per minute"  # Users cannot write
        elif operation_type == "dataops":
            # Most restrictive for DataOps operations (admin only)
            if role == "admin":
                return f"{limits['per_minute']//4} per minute; {limits['per_hour']//4} per hour"
            else:
                return "0 per minute"  # Only admins can access DataOps
        else:
            # Standard limits
            return f"{limits['per_minute']} per minute; {limits['per_hour']} per hour"


def role_based_rate_limit(operation_type: str = "standard"):
    """
    Decorator that applies role-based rate limiting
    
    Args:
        operation_type: Type of operation ('read', 'write', 'dataops', 'standard')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip rate limiting in test mode
            from flask import current_app
            if current_app.config.get("TESTING"):
                return f(*args, **kwargs)
            
            # Get rate limiter instance from app extensions
            limiter = getattr(current_app, 'limiter', None)
            if not limiter:
                logger.warning("Rate limiter not configured, allowing request")
                return f(*args, **kwargs)
            
            # Create role-based rate limiter
            role_limiter = RoleBasedRateLimiter(limiter)
            
            # Determine user role
            user_role = role_limiter.get_user_role()
            
            # Create limit string for this role and operation
            limit_string = role_limiter.create_limit_string(user_role, operation_type)
            
            # Apply the limit
            try:
                # Use Flask-Limiter's limit decorator dynamically
                limited_function = limiter.limit(limit_string)(f)
                result = limited_function(*args, **kwargs)
                
                logger.debug(f"Rate limit applied for {user_role}: {limit_string}")
                return result
                
            except Exception as e:
                if "rate limit exceeded" in str(e).lower():
                    logger.warning(f"Rate limit exceeded for {user_role} on {operation_type} operation")
                    return jsonify({
                        "error": "Rate limit exceeded",
                        "message": f"Too many {operation_type} requests. Please try again later.",
                        "user_role": user_role,
                        "limit": limit_string
                    }), 429
                else:
                    logger.error(f"Rate limiting error: {e}")
                    # If rate limiting fails, allow the request to proceed
                    return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def read_rate_limit(f):
    """Convenience decorator for read operations"""
    return role_based_rate_limit("read")(f)


def write_rate_limit(f):
    """Convenience decorator for write operations (admin only)"""
    return role_based_rate_limit("write")(f)


def dataops_rate_limit(f):
    """Convenience decorator for DataOps operations (admin only)"""
    return role_based_rate_limit("dataops")(f)


def auth_rate_limit(f):
    """Special rate limiting for authentication endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import current_app
        if current_app.config.get("TESTING"):
            return f(*args, **kwargs)
        
        # More restrictive limits for auth endpoints to prevent brute force
        limiter = getattr(current_app, 'limiter', None)
        if limiter:
            try:
                # 5 login attempts per minute, 20 per hour
                limited_function = limiter.limit("5 per minute; 20 per hour")(f)
                return limited_function(*args, **kwargs)
            except Exception as e:
                if "rate limit exceeded" in str(e).lower():
                    logger.warning(f"Authentication rate limit exceeded from {request.remote_addr}")
                    return jsonify({
                        "error": "Too many authentication attempts",
                        "message": "Please wait before trying again"
                    }), 429
                else:
                    logger.error(f"Auth rate limiting error: {e}")
        
        return f(*args, **kwargs)
    
    return decorated_function