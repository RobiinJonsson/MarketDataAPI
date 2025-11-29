"""Authentication models for SQL Server backend"""

import bcrypt
from datetime import datetime, UTC, timedelta
from typing import Dict, Any, List, Optional
import uuid

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from .base_model import SqlServerBaseModel


# Association table for user-role many-to-many relationship
user_roles = Table(
    'user_roles',
    SqlServerBaseModel.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('role_id', String(36), ForeignKey('roles.id'), primary_key=True)
)


class User(SqlServerBaseModel):
    """User model for authentication (SQL Server)"""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    def __init__(self, username: str, email: str, password: str):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password: str) -> None:
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)
    
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self.has_role("admin")
    
    def can_access_dataops(self) -> bool:
        """Check if user can access DataOps endpoints"""
        return self.is_admin()
    
    def can_modify_data(self) -> bool:
        """Check if user can perform POST/PUT/DELETE operations"""
        return self.is_admin()
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = datetime.now(UTC)
    
    def get_permissions(self) -> List[str]:
        """Get all permissions for user based on roles"""
        permissions = set()
        for role in self.roles:
            permissions.update(role.get_permissions())
        return list(permissions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary for API responses"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "roles": [role.name for role in self.roles],
            "permissions": self.get_permissions(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Role(SqlServerBaseModel):
    """Role model for role-based access control (SQL Server)"""
    
    __tablename__ = "roles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)  # String instead of enum for SQL Server
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", back_populates="role", cascade="all, delete-orphan")
    
    def __init__(self, name: str, display_name: str, description: str = None):
        """Initialize role"""
        self.name = name
        self.display_name = display_name
        self.description = description
    
    def get_permissions(self) -> List[str]:
        """Get all permission names for this role"""
        return [permission.name for permission in self.permissions]
    
    def add_permission(self, permission_name: str, description: str = None) -> 'Permission':
        """Add permission to role"""
        permission = Permission(
            role_id=self.id,
            name=permission_name,
            description=description
        )
        self.permissions.append(permission)
        return permission
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert role to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "permissions": self.get_permissions(),
            "user_count": len(self.users),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<Role(name='{self.name}', display_name='{self.display_name}')>"


class Permission(SqlServerBaseModel):
    """Permission model for granular access control (SQL Server)"""
    
    __tablename__ = "permissions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role_id = Column(String(36), ForeignKey('roles.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")
    
    def __init__(self, role_id: str, name: str, description: str = None):
        """Initialize permission"""
        self.role_id = role_id
        self.name = name
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert permission to dictionary for API responses"""
        return {
            "id": self.id,
            "role_id": self.role_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<Permission(name='{self.name}', role='{self.role.name if self.role else 'Unknown'}')>"


# Define default permissions for each role
DEFAULT_PERMISSIONS = {
    "user": [
        "instruments:read",
        "legal_entities:read", 
        "transparency:read",
        "venues:read",
        "mic_codes:read",
        "relationships:read",
        "frontend:access"
    ],
    "admin": [
        "instruments:read",
        "instruments:write", 
        "instruments:delete",
        "legal_entities:read",
        "legal_entities:write",
        "legal_entities:delete",
        "transparency:read",
        "transparency:write",
        "transparency:delete",
        "venues:read",
        "venues:write",
        "venues:delete",
        "mic_codes:read",
        "mic_codes:write",
        "relationships:read",
        "relationships:write",
        "relationships:delete",
        "dataops:access",
        "admin:access",
        "frontend:access",
        "users:manage",
        "system:manage"
    ]
}


def create_default_roles() -> List[Role]:
    """Create default roles with their permissions"""
    roles = []
    
    # Create User role
    user_role = Role(
        name="user",
        display_name="User",
        description="Read-only access to API and frontend. Cannot access DataOps."
    )
    for permission in DEFAULT_PERMISSIONS["user"]:
        user_role.add_permission(permission)
    roles.append(user_role)
    
    # Create Admin role
    admin_role = Role(
        name="admin",
        display_name="Administrator", 
        description="Full access to all features including DataOps and user management."
    )
    for permission in DEFAULT_PERMISSIONS["admin"]:
        admin_role.add_permission(permission)
    roles.append(admin_role)
    
    return roles