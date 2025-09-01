"""Add FIRDS common fields to instruments

Revision ID: add_firds_common_fields
Revises: 7f8e2d9c1a4b
Create Date: 2025-09-01 20:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_firds_common_fields'
down_revision = '7f8e2d9c1a4b'
branch_labels = None
depends_on = None


def upgrade():
    """Add FIRDS common fields to instruments and trading_venues tables."""
    
    # Add new columns to instruments table
    with op.batch_alter_table('instruments', schema=None) as batch_op:
        # Add commodity derivative indicator
        batch_op.add_column(sa.Column('commodity_derivative_indicator', sa.Boolean(), nullable=True))
        
        # Add publication and regulatory fields
        batch_op.add_column(sa.Column('publication_from_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('competent_authority', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('relevant_trading_venue', sa.String(length=100), nullable=True))
        
        # Add new indexes for performance
        batch_op.create_index('idx_instruments_unified_cfi', ['cfi_code'], unique=False)
        batch_op.create_index('idx_instruments_unified_currency', ['currency'], unique=False)
        batch_op.create_index('idx_instruments_unified_competent_auth', ['competent_authority'], unique=False)
    
    # Update trading_venues table to align with FIRDS structure
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        # Change issuer_requested from String to Boolean to match FIRDS data
        # First add the new column
        batch_op.add_column(sa.Column('issuer_requested_bool', sa.Boolean(), nullable=True))
        
    # Migrate existing data: convert string 'True'/'False' to boolean
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE trading_venues 
        SET issuer_requested_bool = CASE 
            WHEN issuer_requested = 'True' OR issuer_requested = 'true' OR issuer_requested = '1' THEN 1
            WHEN issuer_requested = 'False' OR issuer_requested = 'false' OR issuer_requested = '0' THEN 0
            ELSE NULL
        END
    """))
    
    # Drop old column and rename new one
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        batch_op.drop_column('issuer_requested')
        
    # Rename the new column to the original name
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        batch_op.alter_column('issuer_requested_bool', new_column_name='issuer_requested')


def downgrade():
    """Remove FIRDS common fields from instruments and trading_venues tables."""
    
    # Revert instruments table changes
    with op.batch_alter_table('instruments', schema=None) as batch_op:
        # Drop new indexes
        batch_op.drop_index('idx_instruments_unified_competent_auth')
        batch_op.drop_index('idx_instruments_unified_currency')
        batch_op.drop_index('idx_instruments_unified_cfi')
        
        # Drop new columns
        batch_op.drop_column('relevant_trading_venue')
        batch_op.drop_column('competent_authority')
        batch_op.drop_column('publication_from_date')
        batch_op.drop_column('commodity_derivative_indicator')
    
    # Revert trading_venues table changes
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        # Add back the string column
        batch_op.add_column(sa.Column('issuer_requested_str', sa.String(length=100), nullable=True))
    
    # Convert boolean back to string
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE trading_venues 
        SET issuer_requested_str = CASE 
            WHEN issuer_requested = 1 THEN 'True'
            WHEN issuer_requested = 0 THEN 'False'
            ELSE NULL
        END
    """))
    
    # Drop boolean column and rename string column
    with op.batch_alter_table('trading_venues', schema=None) as batch_op:
        batch_op.drop_column('issuer_requested')
        batch_op.alter_column('issuer_requested_str', new_column_name='issuer_requested')
