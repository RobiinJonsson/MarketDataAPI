"""add supporting tables

Revision ID: 20250517_114500_add_supporting_tables
Revises: 20250517_initial_schema
Create Date: 2025-05-17T11:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20250517_114500_add_supporting_tables'
down_revision = '20250517_initial_schema'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create legal_entities table
    op.create_table('legal_entities',
        sa.Column('lei', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('legal_form', sa.String(), nullable=True),
        sa.Column('jurisdiction', sa.String(), nullable=True),
        sa.Column('registered_as', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('bic', sa.String(), nullable=True),
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('next_renewal_date', sa.DateTime(), nullable=True),
        sa.Column('registration_status', sa.String(), nullable=True),
        sa.Column('managing_lou', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('lei')
    )
    
    # Create figi_mappings table
    op.create_table('figi_mappings',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('isin', sa.String(), nullable=False),
        sa.Column('figi', sa.String(), nullable=True),
        sa.Column('composite_figi', sa.String(), nullable=True),
        sa.Column('share_class_figi', sa.String(), nullable=True),
        sa.Column('ticker', sa.String(), nullable=True),
        sa.Column('security_type', sa.String(), nullable=True),
        sa.Column('market_sector', sa.String(), nullable=True),
        sa.Column('security_description', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['isin'], ['instruments.isin'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create related_isins table
    op.create_table('related_isins',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('primary_instrument_id', sa.String(), nullable=False),
        sa.Column('related_isin', sa.String(), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('relationship_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['primary_instrument_id'], ['instruments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes
    op.create_index('idx_related_isins_primary_instrument', 'related_isins', ['primary_instrument_id'])
    op.create_index('idx_related_isins_isin', 'related_isins', ['related_isin'])
    op.create_index('idx_related_isins_type', 'related_isins', ['relationship_type'])

def downgrade() -> None:
    op.drop_table('related_isins')
    op.drop_table('figi_mappings')
    op.drop_table('legal_entities')
