"""Add remaining FULINS fields to instrument models

Revision ID: 20250518_222535_add_remaining_fulins_fields_to_instrument_models
Revises: 220250518_221508_add_additional_fulins_fields_to_instrument_model
Create Date: 2025-05-18T22:25:35.225043

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite, postgresql

# revision identifiers, used by Alembic.
revision = '20250518_222535_add_remaining_fulins_fields_to_instrument_models'
down_revision = '20250518_221508_add_additional_fulins_fields_to_instrument_model'  # Set this to your last migration ID
branch_labels = None
depends_on = None

# Choose JSON implementation based on dialect
JSON = postgresql.JSON().with_variant(sqlite.JSON(), 'sqlite')

def upgrade() -> None:
    # Add new fields to equities table
    op.add_column('equities', sa.Column('basket_isin', sa.String(), nullable=True))
    op.add_column('equities', sa.Column('basket_lei', sa.String(), nullable=True))
    op.add_column('equities', sa.Column('underlying_index_isin', sa.String(), nullable=True))
    
    # Add new fields to debts table
    op.add_column('debts', sa.Column('interest_rate_floating_reference_index', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('interest_rate_floating_reference_isin', sa.String(), nullable=True))
    
    # Add new fields to futures table
    op.add_column('futures', sa.Column('agricultural_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('natural_gas_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('electricity_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('renewable_energy_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('paper_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('environmental_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('freight_attributes', JSON, nullable=True))
    op.add_column('futures', sa.Column('fx_type', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('other_notional_currency', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('interest_rate_reference', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('interest_rate_term_unit', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('interest_rate_term_value', sa.Float(), nullable=True))
    op.add_column('futures', sa.Column('index_reference_rate', sa.String(), nullable=True))

def downgrade() -> None:
    # Remove fields from futures table
    op.drop_column('futures', 'index_reference_rate')
    op.drop_column('futures', 'interest_rate_term_value')
    op.drop_column('futures', 'interest_rate_term_unit')
    op.drop_column('futures', 'interest_rate_reference')
    op.drop_column('futures', 'other_notional_currency')
    op.drop_column('futures', 'fx_type')
    op.drop_column('futures', 'freight_attributes')
    op.drop_column('futures', 'environmental_attributes')
    op.drop_column('futures', 'paper_attributes')
    op.drop_column('futures', 'renewable_energy_attributes')
    op.drop_column('futures', 'electricity_attributes')
    op.drop_column('futures', 'natural_gas_attributes')
    op.drop_column('futures', 'agricultural_attributes')
    
    # Remove fields from debts table
    op.drop_column('debts', 'interest_rate_floating_reference_isin')
    op.drop_column('debts', 'interest_rate_floating_reference_index')
    
    # Remove fields from equities table
    op.drop_column('equities', 'underlying_index_isin')
    op.drop_column('equities', 'basket_lei')
    op.drop_column('equities', 'basket_isin')