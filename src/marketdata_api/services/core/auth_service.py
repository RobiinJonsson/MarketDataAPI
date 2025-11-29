"""Authentication Service - Database-agnostic authentication management"""

import jwt
from datetime import datetime, timedelta, UTC
from typing import Dict, Any, List, Optional, Union
import logging
from flask import current_app
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ...database.session import SessionLocal
from ...config import DatabaseConfig

logger = logging.getLogger(__name__)


class AuthService:
    """Database-agnostic authentication service"""
    
    def __init__(self):
        """Initialize authentication service with database-specific models"""
        self._user_model = None
        self._role_model = None
        self._permission_model = None
        self._create_default_roles_func = None
        self._load_models()
    
    def _load_models(self):
        """Load authentication models - only available for SQL Server (production)"""
        db_type = DatabaseConfig.get_database_type()
        
        if db_type == "sqlite":
            # SQLite is for development only - no authentication needed
            logger.info("SQLite mode: Authentication disabled for development environment")
            self._user_model = None
            self._role_model = None
            self._permission_model = None
            self._create_default_roles_func = None
        else:
            # SQL Server or other production databases
            from ...models.sqlserver.auth import User, Role, Permission, create_default_roles
            self._user_model = User
            self._role_model = Role
            self._permission_model = Permission
            self._create_default_roles_func = create_default_roles
            logger.info("SQL Server mode: Authentication enabled for production environment")
    
    def _get_jwt_secret(self) -> str:
        """Get JWT secret key from configuration"""
        return current_app.config.get('JWT_SECRET_KEY', 'dev-secret-change-in-production')
    
    def _get_jwt_algorithm(self) -> str:
        """Get JWT algorithm from configuration"""
        return current_app.config.get('JWT_ALGORITHM', 'HS256')
    
    def _get_token_expiry_hours(self, token_type: str = 'access') -> int:
        """Get token expiry time in hours"""
        if token_type == 'refresh':
            return current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 24 * 7)  # 7 days
        return current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 1)  # 1 hour
    
    def is_authentication_enabled(self) -> bool:
        """Check if authentication is enabled (only for SQL Server/production)"""
        return self._user_model is not None
    
    def _check_auth_enabled(self):
        """Raise error if authentication is not enabled"""
        if not self.is_authentication_enabled():
            raise ValueError("Authentication is only available in production (SQL Server) mode")
    
    def generate_token(self, user_dict: Dict[str, Any], token_type: str = 'access') -> str:
        """Generate JWT token for user"""
        try:
            expiry_hours = self._get_token_expiry_hours(token_type)
            expiry_time = datetime.now(UTC) + timedelta(hours=expiry_hours)
            
            payload = {
                'user_id': user_dict['id'],
                'username': user_dict['username'],
                'email': user_dict['email'],
                'roles': user_dict['roles'],
                'permissions': user_dict['permissions'],
                'token_type': token_type,
                'exp': expiry_time,
                'iat': datetime.now(UTC),
                'sub': user_dict['id']
            }
            
            token = jwt.encode(
                payload,
                self._get_jwt_secret(),
                algorithm=self._get_jwt_algorithm()
            )
            
            logger.info(f"Generated {token_type} token for user: {user_dict['username']}")
            return token
            
        except Exception as e:
            logger.error(f"Error generating {token_type} token for user {user_dict.get('username', 'unknown')}: {e}")
            raise ValueError(f"Token generation failed: {str(e)}")
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                self._get_jwt_secret(),
                algorithms=[self._get_jwt_algorithm()]
            )
            
            # Check if token has expired
            exp_timestamp = payload.get('exp')
            if exp_timestamp and datetime.fromtimestamp(exp_timestamp, UTC) < datetime.now(UTC):
                raise jwt.ExpiredSignatureError("Token has expired")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token verification failed: Token has expired")
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token verification failed: {e}")
            raise ValueError("Invalid token")
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {e}")
            raise ValueError("Token verification failed")
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username/password"""
        self._check_auth_enabled()
        try:
            with SessionLocal() as session:
                # Find user by username or email
                user = session.query(self._user_model).filter(
                    (self._user_model.username == username) |
                    (self._user_model.email == username)
                ).first()
                
                if not user:
                    logger.warning(f"Authentication failed: User not found: {username}")
                    return None
                
                if not user.is_active:
                    logger.warning(f"Authentication failed: User inactive: {username}")
                    return None
                
                if not user.check_password(password):
                    logger.warning(f"Authentication failed: Invalid password for user: {username}")
                    return None
                
                # Update last login
                user.update_last_login()
                session.commit()
                
                logger.info(f"User authenticated successfully: {username}")
                return user.to_dict()
                
        except Exception as e:
            logger.error(f"Error during user authentication for {username}: {e}")
            return None
    
    def create_user(self, username: str, email: str, password: str, roles: List[str] = None) -> Dict[str, Any]:
        """Create a new user with specified roles"""
        self._check_auth_enabled()
        try:
            with SessionLocal() as session:
                # Check if user already exists
                existing_user = session.query(self._user_model).filter(
                    (self._user_model.username == username) |
                    (self._user_model.email == email)
                ).first()
                
                if existing_user:
                    raise ValueError("Username or email already exists")
                
                # Create new user
                user = self._user_model(username=username, email=email, password=password)
                session.add(user)
                session.flush()  # Get user ID
                
                # Assign roles
                if roles:
                    for role_name in roles:
                        role = session.query(self._role_model).filter(
                            self._role_model.name == role_name
                        ).first()
                        if role:
                            user.roles.append(role)
                        else:
                            logger.warning(f"Role not found: {role_name}")
                else:
                    # Assign default 'user' role if no roles specified
                    default_role = session.query(self._role_model).filter(
                        self._role_model.name == "user"
                    ).first()
                    if default_role:
                        user.roles.append(default_role)
                
                session.commit()
                logger.info(f"Created user: {username} with roles: {roles or ['user']}")
                return user.to_dict()
                
        except IntegrityError as e:
            logger.error(f"Database integrity error creating user {username}: {e}")
            raise ValueError("Username or email already exists")
        except Exception as e:
            logger.error(f"Error creating user {username}: {e}")
            raise ValueError(f"User creation failed: {str(e)}")
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        self._check_auth_enabled()
        try:
            with SessionLocal() as session:
                user = session.query(self._user_model).filter(
                    self._user_model.id == user_id
                ).first()
                
                return user.to_dict() if user else None
                
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            with SessionLocal() as session:
                user = session.query(self._user_model).filter(
                    self._user_model.username == username
                ).first()
                
                return user.to_dict() if user else None
                
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {e}")
            return None
    
    def update_user_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Update user password"""
        try:
            with SessionLocal() as session:
                user = session.query(self._user_model).filter(
                    self._user_model.id == user_id
                ).first()
                
                if not user:
                    logger.warning(f"Password update failed: User not found: {user_id}")
                    return False
                
                if not user.check_password(old_password):
                    logger.warning(f"Password update failed: Invalid old password for user: {user_id}")
                    return False
                
                user.set_password(new_password)
                session.commit()
                
                logger.info(f"Password updated for user: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating password for user {user_id}: {e}")
            return False
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account"""
        try:
            with SessionLocal() as session:
                user = session.query(self._user_model).filter(
                    self._user_model.id == user_id
                ).first()
                
                if not user:
                    logger.warning(f"Deactivation failed: User not found: {user_id}")
                    return False
                
                user.is_active = False
                session.commit()
                
                logger.info(f"Deactivated user: {user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            return False
    
    def list_users(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List all users with pagination"""
        try:
            with SessionLocal() as session:
                query = session.query(self._user_model)
                total_count = query.count()
                
                # Add ORDER BY for SQL Server compatibility when using offset/limit
                users = query.order_by(self._user_model.created_at.desc()).offset(offset).limit(limit).all()
                user_dicts = [user.to_dict() for user in users]
                
                return {
                    "users": user_dicts,
                    "total": total_count,
                    "limit": limit,
                    "offset": offset
                }
                
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return {"users": [], "total": 0, "limit": limit, "offset": offset}
    
    def create_default_roles(self) -> bool:
        """Create default roles if they don't exist"""
        self._check_auth_enabled()
        try:
            with SessionLocal() as session:
                # Check if roles already exist
                existing_roles = session.query(self._role_model).count()
                if existing_roles > 0:
                    logger.info("Default roles already exist")
                    return True
                
                # Create default roles
                roles = self._create_default_roles_func()
                for role in roles:
                    session.add(role)
                
                session.commit()
                logger.info("Created default roles successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating default roles: {e}")
            return False
    
    def get_roles(self) -> List[Dict[str, Any]]:
        """Get all available roles"""
        try:
            with SessionLocal() as session:
                roles = session.query(self._role_model).all()
                return [role.to_dict() for role in roles]
                
        except Exception as e:
            logger.error(f"Error getting roles: {e}")
            return []
    
    def assign_role_to_user(self, user_id: str, role_name: str) -> bool:
        """Assign role to user"""
        try:
            with SessionLocal() as session:
                user = session.query(self._user_model).filter(
                    self._user_model.id == user_id
                ).first()
                
                if not user:
                    logger.warning(f"Role assignment failed: User not found: {user_id}")
                    return False
                
                role = session.query(self._role_model).filter(
                    self._role_model.name == role_name
                ).first()
                
                if not role:
                    logger.warning(f"Role assignment failed: Role not found: {role_name}")
                    return False
                
                if role not in user.roles:
                    user.roles.append(role)
                    session.commit()
                    logger.info(f"Assigned role {role_name} to user {user_id}")
                
                return True
                
        except Exception as e:
            logger.error(f"Error assigning role {role_name} to user {user_id}: {e}")
            return False
    
    def remove_role_from_user(self, user_id: str, role_name: str) -> bool:
        """Remove role from user"""
        try:
            with SessionLocal() as session:
                user = session.query(self._user_model).filter(
                    self._user_model.id == user_id
                ).first()
                
                if not user:
                    logger.warning(f"Role removal failed: User not found: {user_id}")
                    return False
                
                role = session.query(self._role_model).filter(
                    self._role_model.name == role_name
                ).first()
                
                if not role:
                    logger.warning(f"Role removal failed: Role not found: {role_name}")
                    return False
                
                if role in user.roles:
                    user.roles.remove(role)
                    session.commit()
                    logger.info(f"Removed role {role_name} from user {user_id}")
                
                return True
                
        except Exception as e:
            logger.error(f"Error removing role {role_name} from user {user_id}: {e}")
            return False


# Global authentication service instance
auth_service = AuthService()