"""Add parent-child relationships for legal entities

Revision ID: 20250530_parent_child
Revises: 20250522_080412_add_cascade_deletes_to_instrument_figi_legal_entity
Create Date: 2025-05-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250530_parent_child'
down_revision: Union[str, None] = '20250522_080412_add_cascade_deletes_to_instrument_figi_legal_entity'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from sqlalchemy import inspect
    from sqlalchemy.sql import text
    
    # Get inspector to check for existing tables
    conn = op.get_bind()
    inspector = inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Create entity_relationships table if it doesn't exist
    if 'entity_relationships' not in existing_tables:
        op.create_table(
            'entity_relationships',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('parent_lei', sa.String(), nullable=False),
            sa.Column('child_lei', sa.String(), nullable=False),
            sa.Column('relationship_type', sa.String(), nullable=False),
            sa.Column('relationship_status', sa.String(), nullable=False),
            sa.Column('relationship_period_start', sa.DateTime(), nullable=False),
            sa.Column('relationship_period_end', sa.DateTime(), nullable=True),
            sa.Column('percentage_of_ownership', sa.Integer(), nullable=True),
            sa.Column('qualification_method', sa.String(), nullable=True),
            sa.Column('last_updated', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['child_lei'], ['legal_entities.lei'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['parent_lei'], ['legal_entities.lei'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.CheckConstraint("relationship_type IN ('DIRECT', 'ULTIMATE')", name='ck_relationship_type_values')
        )
        op.create_index('idx_parent_child', 'entity_relationships', 
                        ['parent_lei', 'child_lei', 'relationship_type'], unique=True)
    
    # Create entity_relationship_exceptions table if it doesn't exist
    if 'entity_relationship_exceptions' not in existing_tables:
        op.create_table(
            'entity_relationship_exceptions',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('lei', sa.String(), nullable=False),
            sa.Column('exception_type', sa.String(), nullable=False),
            sa.Column('exception_reason', sa.String(), nullable=False),
            sa.Column('exception_category', sa.String(), nullable=False),
            sa.Column('provided_parent_lei', sa.String(), nullable=True),
            sa.Column('provided_parent_name', sa.String(), nullable=True),
            sa.Column('last_updated', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['lei'], ['legal_entities.lei'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.CheckConstraint("exception_type IN ('DIRECT_PARENT', 'ULTIMATE_PARENT')", name='ck_exception_type_values')
        )
        op.create_index('idx_lei_exception_type', 'entity_relationship_exceptions', 
                        ['lei', 'exception_type'], unique=True)


def downgrade() -> None:
    from sqlalchemy import inspect
    
    # Get inspector to check for existing tables
    conn = op.get_bind()
    inspector = inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Only drop tables if they exist
    if 'entity_relationship_exceptions' in existing_tables:
        op.drop_index('idx_lei_exception_type', table_name='entity_relationship_exceptions')
        op.drop_table('entity_relationship_exceptions')
    
    if 'entity_relationships' in existing_tables:
        op.drop_index('idx_parent_child', table_name='entity_relationships')
        op.drop_table('entity_relationships')
