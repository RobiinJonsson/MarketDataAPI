"""Add MIC (Market Identification Code) support

Revision ID: add_mic_support
Revises: add_firds_common_fields
Create Date: 2025-09-07 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_mic_support'
down_revision = 'add_firds_common_fields'
branch_labels = None
depends_on = None


def upgrade():
    """Add MIC table and update TradingVenue with MIC foreign key."""
    
    # Create MIC table
    op.create_table('market_identification_codes',
        sa.Column('mic', sa.String(length=4), nullable=False),
        sa.Column('operating_mic', sa.String(length=4), nullable=False),
        sa.Column('operation_type', sa.Enum('OPRT', 'SGMT', name='mictype'), nullable=False),
        sa.Column('market_name', sa.String(length=500), nullable=False),
        sa.Column('legal_entity_name', sa.String(length=500), nullable=True),
        sa.Column('lei', sa.String(length=20), nullable=True),
        sa.Column('market_category_code', sa.Enum('APPA', 'ATSS', 'CASP', 'DCMS', 'IDQS', 'MLTF', 'NSPD', 'OTFS', 'OTHR', 'RMOS', 'RMKT', 'SEFS', 'SINT', 'TRFS', name='marketcategorycode'), nullable=True),
        sa.Column('acronym', sa.String(length=50), nullable=True),
        sa.Column('iso_country_code', sa.String(length=2), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('ACTIVE', 'EXPIRED', 'SUSPENDED', 'UPDATED', name='micstatus'), nullable=False),
        sa.Column('creation_date', sa.DateTime(), nullable=True),
        sa.Column('last_update_date', sa.DateTime(), nullable=True),
        sa.Column('last_validation_date', sa.DateTime(), nullable=True),
        sa.Column('expiry_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('data_source_version', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('mic')
    )
    
    # Create indexes for MIC table
    op.create_index('idx_mic_operating_mic', 'market_identification_codes', ['operating_mic'], unique=False)
    op.create_index('idx_mic_country', 'market_identification_codes', ['iso_country_code'], unique=False)
    op.create_index('idx_mic_status', 'market_identification_codes', ['status'], unique=False)
    op.create_index('idx_mic_category', 'market_identification_codes', ['market_category_code'], unique=False)
    op.create_index('idx_mic_lei', 'market_identification_codes', ['lei'], unique=False)
    op.create_index('idx_mic_name_search', 'market_identification_codes', ['market_name'], unique=False)
    op.create_index('idx_mic_entity_search', 'market_identification_codes', ['legal_entity_name'], unique=False)
    
    # Add MIC foreign key to trading_venues table
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mic_code', sa.String(length=4), nullable=True))
        batch_op.create_foreign_key('fk_trading_venues_mic_code', 'market_identification_codes', ['mic_code'], ['mic'], ondelete='SET NULL')
        batch_op.create_index('idx_trading_venues_unified_mic_code', ['mic_code'], unique=False)


def downgrade():
    """Remove MIC support."""
    
    # Remove MIC foreign key and column from trading_venues
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        batch_op.drop_index('idx_trading_venues_unified_mic_code')
        batch_op.drop_constraint('fk_trading_venues_mic_code', type_='foreignkey')
        batch_op.drop_column('mic_code')
    
    # Drop MIC table indexes
    op.drop_index('idx_mic_entity_search', table_name='market_identification_codes')
    op.drop_index('idx_mic_name_search', table_name='market_identification_codes')
    op.drop_index('idx_mic_lei', table_name='market_identification_codes')
    op.drop_index('idx_mic_category', table_name='market_identification_codes')
    op.drop_index('idx_mic_status', table_name='market_identification_codes')
    op.drop_index('idx_mic_country', table_name='market_identification_codes')
    op.drop_index('idx_mic_operating_mic', table_name='market_identification_codes')
    
    # Drop MIC table
    op.drop_table('market_identification_codes')
