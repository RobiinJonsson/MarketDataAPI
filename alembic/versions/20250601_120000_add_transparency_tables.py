"""Add transparency tables

Revision ID: 20250601_120000_add_transparency_tables
Revises: 20250530_parent_child
Create Date: 2025-06-01T12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20250601_120000_add_transparency_tables'
down_revision = '20250530_parent_child'
branch_labels = None
depends_on = None

def upgrade() -> None:
    from sqlalchemy import inspect
    
    # Get inspector to check for existing tables
    conn = op.get_bind()
    inspector = inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Create transparency_calculations base table if it doesn't exist
    if 'transparency_calculations' not in existing_tables:
        op.create_table(
            'transparency_calculations',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('tech_record_id', sa.String(), nullable=False),
            sa.Column('isin', sa.String(), nullable=False),
            sa.Column('calculation_type', sa.String(), nullable=False),
            sa.Column('from_date', sa.Date(), nullable=True),
            sa.Column('to_date', sa.Date(), nullable=True),
            sa.Column('liquidity', sa.Boolean(), nullable=True),
            sa.Column('total_transactions_executed', sa.Integer(), nullable=True),
            sa.Column('total_volume_executed', sa.Float(), nullable=True),
            sa.Column('statistics', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.CheckConstraint("calculation_type IN ('EQUITY', 'NON_EQUITY')", name='ck_calculation_type_values')
        )
        op.create_index('idx_transparency_isin', 'transparency_calculations', ['isin'])
        op.create_index('idx_transparency_tech_record', 'transparency_calculations', ['tech_record_id'])
        op.create_index('idx_transparency_type', 'transparency_calculations', ['calculation_type'])
    
    # Create equity_transparency table if it doesn't exist
    if 'equity_transparency' not in existing_tables:
        op.create_table(
            'equity_transparency',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('financial_instrument_classification', sa.String(), nullable=True),
            sa.Column('methodology', sa.String(), nullable=True),
            sa.Column('average_daily_turnover', sa.Float(), nullable=True),
            sa.Column('large_in_scale', sa.Float(), nullable=True),
            sa.Column('average_daily_number_of_transactions', sa.Float(), nullable=True),
            sa.Column('secondary_id', sa.String(), nullable=True),
            sa.Column('average_daily_transactions_secondary', sa.Float(), nullable=True),
            sa.Column('average_transaction_value', sa.Float(), nullable=True),
            sa.Column('standard_market_size', sa.Float(), nullable=True),
            sa.ForeignKeyConstraint(['id'], ['transparency_calculations.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create non_equity_transparency table if it doesn't exist
    if 'non_equity_transparency' not in existing_tables:
        op.create_table(
            'non_equity_transparency',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('criterion_name', sa.String(), nullable=True),
            sa.Column('criterion_value', sa.String(), nullable=True),
            sa.Column('financial_instrument_classification', sa.String(), nullable=True),
            sa.Column('pre_trade_large_in_scale_threshold', sa.Float(), nullable=True),
            sa.Column('post_trade_large_in_scale_threshold', sa.Float(), nullable=True),
            sa.Column('pre_trade_instrument_size_specific_threshold', sa.Float(), nullable=True),
            sa.Column('post_trade_instrument_size_specific_threshold', sa.Float(), nullable=True),
            sa.Column('criterion_name_secondary', sa.String(), nullable=True),
            sa.Column('criterion_value_secondary', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['id'], ['transparency_calculations.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create debt_transparency table if it doesn't exist
    if 'debt_transparency' not in existing_tables:
        op.create_table(
            'debt_transparency',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('bond_type', sa.String(), nullable=True),
            sa.Column('security_type', sa.String(), nullable=True),
            sa.Column('is_securitised_derivative', sa.Boolean(), nullable=True),
            sa.Column('is_corporate_bond', sa.Boolean(), nullable=True),
            sa.Column('is_liquid', sa.Boolean(), nullable=True),
            sa.ForeignKeyConstraint(['id'], ['non_equity_transparency.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create futures_transparency table if it doesn't exist
    if 'futures_transparency' not in existing_tables:
        op.create_table(
            'futures_transparency',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('criterion_name_3', sa.String(), nullable=True),
            sa.Column('criterion_value_3', sa.String(), nullable=True),
            sa.Column('criterion_name_4', sa.String(), nullable=True),
            sa.Column('criterion_value_4', sa.String(), nullable=True),
            sa.Column('criterion_name_5', sa.String(), nullable=True),
            sa.Column('criterion_value_5', sa.String(), nullable=True),
            sa.Column('criterion_name_6', sa.String(), nullable=True),
            sa.Column('criterion_value_6', sa.String(), nullable=True),
            sa.Column('criterion_name_7', sa.String(), nullable=True),
            sa.Column('criterion_value_7', sa.String(), nullable=True),
            sa.Column('pre_trade_large_in_scale_threshold_nb', sa.Float(), nullable=True),
            sa.Column('post_trade_large_in_scale_threshold_nb', sa.Float(), nullable=True),
            sa.Column('pre_trade_instrument_size_specific_threshold_nb', sa.Float(), nullable=True),
            sa.Column('post_trade_instrument_size_specific_threshold_nb', sa.Float(), nullable=True),
            sa.Column('is_stock_dividend_future', sa.Boolean(), nullable=True),
            sa.Column('underlying_isin', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['id'], ['non_equity_transparency.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade() -> None:
    # Drop tables in reverse order due to foreign key constraints
    op.drop_table('futures_transparency')
    op.drop_table('debt_transparency')
    op.drop_table('non_equity_transparency')
    op.drop_table('equity_transparency')
    
    # Drop indexes first, then the main table
    op.drop_index('idx_transparency_type')
    op.drop_index('idx_transparency_tech_record')
    op.drop_index('idx_transparency_isin')
    op.drop_table('transparency_calculations')
