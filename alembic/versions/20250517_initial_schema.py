"""initial schema

Revision ID: 20250517_initial_schema
Revises: 
Create Date: 2025-05-17T11:36:53.080996

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20250517_initial_schema'
down_revision = None  # Set to None for initial migration
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create instruments table first (base table)
    op.create_table('instruments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('isin', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('short_name', sa.String(), nullable=True),
        sa.Column('symbol', sa.String(), nullable=True),
        sa.Column('figi', sa.String(), nullable=True),
        sa.Column('cfi_code', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('commodity_derivative', sa.Boolean(), nullable=True),
        sa.Column('trading_venue', sa.String(), nullable=True),
        sa.Column('issuer_req', sa.String(), nullable=True),
        sa.Column('first_trade_date', sa.DateTime(), nullable=True),
        sa.Column('termination_date', sa.DateTime(), nullable=True),
        sa.Column('relevant_authority', sa.String(), nullable=True),
        sa.Column('relevant_venue', sa.String(), nullable=True),
        sa.Column('from_date', sa.DateTime(), nullable=True),
        sa.Column('lei_id', sa.String(), nullable=True),
        sa.Column('additional_data', sqlite.JSON().with_variant(sa.Text(), 'sqlite'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isin'),
        sa.UniqueConstraint('symbol')
    )

    # Create equities table
    op.create_table('equities',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('admission_approval_date', sa.Date(), nullable=True),
        sa.Column('admission_request_date', sa.Date(), nullable=True),
        sa.Column('price_multiplier', sa.Float(), nullable=True),
        sa.Column('asset_class', sa.String(), nullable=True),
        sa.Column('commodity_product', sa.String(), nullable=True),
        sa.Column('energy_type', sa.String(), nullable=True),
        sa.Column('oil_type', sa.String(), nullable=True),
        sa.Column('base_product', sa.String(), nullable=True),
        sa.Column('sub_product', sa.String(), nullable=True),
        sa.Column('additional_sub_product', sa.String(), nullable=True),
        sa.Column('metal_type', sa.String(), nullable=True),
        sa.Column('precious_metal', sa.String(), nullable=True),
        sa.Column('shares_outstanding', sa.Float(), nullable=True),
        sa.Column('market_cap', sa.Float(), nullable=True),
        sa.Column('exchange', sa.String(), nullable=True),
        sa.Column('sector', sa.String(), nullable=True),
        sa.Column('industry', sa.String(), nullable=True),
        sa.Column('underlying_isins', sqlite.JSON().with_variant(sa.Text(), 'sqlite'), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['instruments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create debts table
    op.create_table('debts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('total_issued_nominal', sa.Float(), nullable=True),
        sa.Column('maturity_date', sa.Date(), nullable=True),
        sa.Column('nominal_value_per_unit', sa.Float(), nullable=True),
        sa.Column('fixed_interest_rate', sa.Float(), nullable=True),
        sa.Column('debt_seniority', sa.String(), nullable=True),
        sa.Column('coupon_frequency', sa.String(), nullable=True),
        sa.Column('credit_rating', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['instruments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create futures table
    op.create_table('futures',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('admission_approval_date', sa.Date(), nullable=True),
        sa.Column('admission_request_date', sa.Date(), nullable=True),
        sa.Column('expiration_date', sa.Date(), nullable=True),
        sa.Column('final_settlement_date', sa.Date(), nullable=True),
        sa.Column('delivery_type', sa.String(), nullable=True),
        sa.Column('settlement_method', sa.String(), nullable=True),
        sa.Column('contract_size', sa.Float(), nullable=True),
        sa.Column('contract_unit', sa.String(), nullable=True),
        sa.Column('price_multiplier', sa.Float(), nullable=True),
        sa.Column('settlement_currency', sa.String(), nullable=True),
        sa.Column('contract_details', sqlite.JSON().with_variant(sa.Text(), 'sqlite'), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['instruments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('futures')
    op.drop_table('debts')
    op.drop_table('equities')
    op.drop_table('instruments')
