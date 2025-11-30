"""Authentication API endpoints"""

import logging
from flask import request, jsonify, current_app
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError

from ...services.core.auth_service import auth_service
from ...auth.decorators import require_auth, admin_required, get_current_user
from ...auth.rate_limiting import auth_rate_limit, read_rate_limit
from ...constants import HTTPStatus

logger = logging.getLogger(__name__)

# Create authentication namespace
auth_ns = Namespace('auth', description='Authentication operations')

# API Models for Swagger documentation
auth_models = {
    'LoginRequest': auth_ns.model('LoginRequest', {
        'username': fields.String(required=True, description='Username or email', example='admin'),
        'password': fields.String(required=True, description='Password', example='password123')
    }),
    
    'RegisterRequest': auth_ns.model('RegisterRequest', {
        'username': fields.String(required=True, description='Unique username', example='newuser'),
        'email': fields.String(required=True, description='Email address', example='user@example.com'),
        'password': fields.String(required=True, description='Password (min 8 characters)', example='password123'),
        'roles': fields.List(fields.String(), required=False, description='User roles', example=['user'])
    }),
    
    'AuthResponse': auth_ns.model('AuthResponse', {
        'access_token': fields.String(required=True, description='JWT access token'),
        'refresh_token': fields.String(required=True, description='JWT refresh token'),
        'token_type': fields.String(required=True, description='Token type', example='Bearer'),
        'expires_in': fields.Integer(required=True, description='Token expiry in seconds'),
        'user': fields.Raw(required=True, description='User information')
    }),
    
    'RefreshRequest': auth_ns.model('RefreshRequest', {
        'refresh_token': fields.String(required=True, description='Valid refresh token')
    }),
    
    'PasswordChangeRequest': auth_ns.model('PasswordChangeRequest', {
        'old_password': fields.String(required=True, description='Current password'),
        'new_password': fields.String(required=True, description='New password (min 8 characters)')
    }),
    
    'UserResponse': auth_ns.model('UserResponse', {
        'id': fields.String(description='User ID'),
        'username': fields.String(description='Username'),
        'email': fields.String(description='Email address'),
        'is_active': fields.Boolean(description='Account active status'),
        'roles': fields.List(fields.String(), description='User roles'),
        'permissions': fields.List(fields.String(), description='User permissions'),
        'last_login': fields.String(description='Last login timestamp'),
        'created_at': fields.String(description='Account creation timestamp')
    }),
    
    'ErrorResponse': auth_ns.model('ErrorResponse', {
        'error': fields.String(required=True, description='Error type'),
        'message': fields.String(required=True, description='Error message'),
        'details': fields.Raw(required=False, description='Additional error details')
    })
}

# Add models to namespace
for model_name, model in auth_models.items():
    auth_ns.models[model_name] = model


@auth_ns.route('/login')
class LoginResource(Resource):
    """User authentication endpoint"""
    
    @auth_ns.expect(auth_models['LoginRequest'])
    @auth_ns.response(200, 'Login successful', auth_models['AuthResponse'])
    @auth_ns.response(401, 'Authentication failed', auth_models['ErrorResponse'])
    @auth_ns.response(400, 'Invalid request data', auth_models['ErrorResponse'])
    # @auth_rate_limit  # Temporarily disabled for debugging
    def post(self):
        """
        Authenticate user and return JWT tokens
        """
        try:
            data = request.get_json()
            if not data:
                return {
                    'error': 'Invalid request',
                    'message': 'Request body must contain JSON data'
                }, HTTPStatus.BAD_REQUEST
            
            username = data.get('username')
            password = data.get('password')
            
            # Validate required fields
            if not username or not password:
                print("LOGIN DEBUG: Missing username or password")
                return {
                    'error': 'Missing credentials',
                    'message': 'Username and password are required'
                }, HTTPStatus.BAD_REQUEST
            
            # Authenticate user
            user_data = auth_service.authenticate_user(username, password)
            if not user_data:
                return {
                    'error': 'Authentication failed',
                    'message': 'Invalid username or password'
                }, HTTPStatus.UNAUTHORIZED
            
            # Generate tokens
            access_token = auth_service.generate_token(user_data, 'access')
            refresh_token = auth_service.generate_token(user_data, 'refresh')
            
            logger.info(f"User logged in successfully: {username}")
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour
                'user': {
                    'id': user_data['id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'roles': user_data['roles'],
                    'permissions': user_data['permissions']
                }
            }, HTTPStatus.OK
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            return {
                'error': 'Login failed',
                'message': 'An unexpected error occurred during login'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/register')
class RegisterResource(Resource):
    """User registration endpoint"""
    
    @auth_ns.expect(auth_models['RegisterRequest'])
    @auth_ns.response(201, 'User created successfully', auth_models['UserResponse'])
    @auth_ns.response(400, 'Invalid request data', auth_models['ErrorResponse'])
    @auth_ns.response(409, 'User already exists', auth_models['ErrorResponse'])
    @admin_required
    def post(self):
        """
        Register a new user (Admin only)
        """
        try:
            data = request.get_json()
            if not data:
                return {
                    'error': 'Invalid request',
                    'message': 'Request body must contain JSON data'
                }, HTTPStatus.BAD_REQUEST
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            roles = data.get('roles', ['user'])
            
            # Validate required fields
            if not username or not email or not password:
                return {
                    'error': 'Missing fields',
                    'message': 'Username, email, and password are required'
                }, HTTPStatus.BAD_REQUEST
            
            # Validate password length
            if len(password) < 8:
                return {
                    'error': 'Invalid password',
                    'message': 'Password must be at least 8 characters long'
                }, HTTPStatus.BAD_REQUEST
            
            # Validate email format (basic check)
            if '@' not in email or '.' not in email:
                return {
                    'error': 'Invalid email',
                    'message': 'Please provide a valid email address'
                }, HTTPStatus.BAD_REQUEST
            
            # Create user
            user_data = auth_service.create_user(username, email, password, roles)
            
            logger.info(f"User registered successfully: {username} by {get_current_user()['username']}")
            
            return user_data, HTTPStatus.CREATED
            
        except ValueError as e:
            logger.warning(f"User registration failed: {e}")
            return {
                'error': 'Registration failed',
                'message': str(e)
            }, HTTPStatus.CONFLICT
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return {
                'error': 'Registration failed',
                'message': 'An unexpected error occurred during registration'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/refresh')
class RefreshTokenResource(Resource):
    """Token refresh endpoint"""
    
    @auth_ns.expect(auth_models['RefreshRequest'])
    @auth_ns.response(200, 'Token refreshed successfully', auth_models['AuthResponse'])
    @auth_ns.response(401, 'Invalid refresh token', auth_models['ErrorResponse'])
    def post(self):
        """
        Refresh access token using refresh token
        """
        try:
            data = request.get_json()
            if not data:
                return {
                    'error': 'Invalid request',
                    'message': 'Request body must contain JSON data'
                }, HTTPStatus.BAD_REQUEST
            
            refresh_token = data.get('refresh_token')
            if not refresh_token:
                return {
                    'error': 'Missing token',
                    'message': 'Refresh token is required'
                }, HTTPStatus.BAD_REQUEST
            
            # Verify refresh token
            payload = auth_service.verify_token(refresh_token)
            if payload.get('token_type') != 'refresh':
                return {
                    'error': 'Invalid token',
                    'message': 'Token must be a refresh token'
                }, HTTPStatus.UNAUTHORIZED
            
            # Get user data
            user_data = auth_service.get_user_by_id(payload['user_id'])
            if not user_data:
                return {
                    'error': 'User not found',
                    'message': 'User associated with token no longer exists'
                }, HTTPStatus.UNAUTHORIZED
            
            # Generate new tokens
            new_access_token = auth_service.generate_token(user_data, 'access')
            new_refresh_token = auth_service.generate_token(user_data, 'refresh')
            
            logger.info(f"Token refreshed for user: {user_data['username']}")
            
            return {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token,
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour
                'user': {
                    'id': user_data['id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'roles': user_data['roles'],
                    'permissions': user_data['permissions']
                }
            }, HTTPStatus.OK
            
        except ValueError as e:
            logger.warning(f"Token refresh failed: {e}")
            return {
                'error': 'Token refresh failed',
                'message': str(e)
            }, HTTPStatus.UNAUTHORIZED
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return {
                'error': 'Token refresh failed',
                'message': 'An unexpected error occurred during token refresh'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/me')
class CurrentUserResource(Resource):
    """Current user information endpoint"""
    
    @auth_ns.response(200, 'User information retrieved', auth_models['UserResponse'])
    @auth_ns.response(401, 'Authentication required', auth_models['ErrorResponse'])
    @require_auth
    @read_rate_limit
    def get(self):
        """
        Get current user information
        """
        try:
            current_user = get_current_user()
            user_data = auth_service.get_user_by_id(current_user['id'])
            
            if not user_data:
                return {
                    'error': 'User not found',
                    'message': 'Current user data could not be retrieved'
                }, HTTPStatus.NOT_FOUND
            
            return user_data, HTTPStatus.OK
            
        except Exception as e:
            logger.error(f"Get current user error: {e}")
            return {
                'error': 'User retrieval failed',
                'message': 'An unexpected error occurred'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/change-password')
class ChangePasswordResource(Resource):
    """Password change endpoint"""
    
    @auth_ns.expect(auth_models['PasswordChangeRequest'])
    @auth_ns.response(200, 'Password changed successfully')
    @auth_ns.response(400, 'Invalid request data', auth_models['ErrorResponse'])
    @auth_ns.response(401, 'Authentication required', auth_models['ErrorResponse'])
    @require_auth
    def post(self):
        """
        Change user password
        """
        try:
            data = request.get_json()
            if not data:
                return {
                    'error': 'Invalid request',
                    'message': 'Request body must contain JSON data'
                }, HTTPStatus.BAD_REQUEST
            
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            
            if not old_password or not new_password:
                return {
                    'error': 'Missing passwords',
                    'message': 'Both old and new passwords are required'
                }, HTTPStatus.BAD_REQUEST
            
            if len(new_password) < 8:
                return {
                    'error': 'Invalid password',
                    'message': 'New password must be at least 8 characters long'
                }, HTTPStatus.BAD_REQUEST
            
            current_user = get_current_user()
            success = auth_service.update_user_password(
                current_user['id'], 
                old_password, 
                new_password
            )
            
            if not success:
                return {
                    'error': 'Password change failed',
                    'message': 'Invalid old password or user not found'
                }, HTTPStatus.BAD_REQUEST
            
            logger.info(f"Password changed for user: {current_user['username']}")
            
            return {
                'message': 'Password changed successfully'
            }, HTTPStatus.OK
            
        except Exception as e:
            logger.error(f"Password change error: {e}")
            return {
                'error': 'Password change failed',
                'message': 'An unexpected error occurred'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/users')
class UsersResource(Resource):
    """User management endpoint (Admin only)"""
    
    @auth_ns.response(200, 'Users retrieved successfully')
    @auth_ns.response(401, 'Authentication required', auth_models['ErrorResponse'])
    @auth_ns.response(403, 'Admin access required', auth_models['ErrorResponse'])
    @admin_required
    def get(self):
        """
        List all users (Admin only)
        """
        try:
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            
            result = auth_service.list_users(limit=limit, offset=offset)
            
            return result, HTTPStatus.OK
            
        except Exception as e:
            logger.error(f"List users error: {e}")
            return {
                'error': 'User listing failed',
                'message': 'An unexpected error occurred'
            }, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_ns.route('/roles')
class RolesResource(Resource):
    """Roles information endpoint"""
    
    @auth_ns.response(200, 'Roles retrieved successfully')
    @auth_ns.response(401, 'Authentication required', auth_models['ErrorResponse'])
    @require_auth
    def get(self):
        """
        Get available roles
        """
        try:
            roles = auth_service.get_roles()
            
            return {
                'roles': roles
            }, HTTPStatus.OK
            
        except Exception as e:
            logger.error(f"Get roles error: {e}")
            return {
                'error': 'Roles retrieval failed',
                'message': 'An unexpected error occurred'
            }, HTTPStatus.INTERNAL_SERVER_ERROR