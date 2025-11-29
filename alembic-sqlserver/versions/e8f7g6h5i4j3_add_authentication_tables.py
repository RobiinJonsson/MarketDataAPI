"""Add authentication tables for production use

Revision ID: e8f7g6h5i4j3
Revises: 0b0e19e0468e
Create Date: 2025-11-29 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8f7g6h5i4j3'
down_revision: Union[str, None] = '0b0e19e0468e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create authentication tables for production SQL Server"""
    
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('display_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('username', sa.String(80), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('last_login', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )
    
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('role_id', sa.String(36), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )
    
    # Create user_roles association table
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', sa.String(36), sa.ForeignKey('roles.id'), primary_key=True)
    )
    
    # Create indexes for better performance
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_email', 'users', ['email'])


def downgrade() -> None:
    """Remove authentication tables"""
    
    # Drop indexes
    op.drop_index('ix_users_email', 'users')
    op.drop_index('ix_users_username', 'users')
    
    # Drop tables in reverse order
    op.drop_table('user_roles')
    op.drop_table('permissions')
    op.drop_table('users')
    op.drop_table('roles')