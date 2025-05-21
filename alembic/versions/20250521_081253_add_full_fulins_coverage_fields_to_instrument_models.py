"""Add full FULINS coverage fields to instrument models

Revision ID: 20250521_081253_add_full_fulins_coverage_fields_to_instrument_models
Revises: <previous_revision_id>
Create Date: 2025-05-21T08:12:53.439389

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20250521_081253_add_full_fulins_coverage_fields_to_instrument_models'
down_revision = '20250518_222535_add_remaining_fulins_fields_to_instrument_models'  # Set this to your last migration ID
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Equity: Only add missing columns
    op.add_column('equities', sa.Column('underlying_single_isin', sa.String(), nullable=True))
    op.add_column('equities', sa.Column('underlying_single_index_name', sa.String(), nullable=True))
    op.add_column('equities', sa.Column('additional_metal_product', sa.String(), nullable=True))

    # Debt: Only add missing columns
    op.add_column('debts', sa.Column('underlying_single_isin', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('basket_isin', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('underlying_index_isin', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('underlying_single_index_name', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('underlying_single_lei', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('additional_metal_product', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('oil_type', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('sub_product', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('additional_sub_product', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('metal_type', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('precious_metal', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('other_commodity_base_product', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('underlying_index_name_term_unit', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('underlying_index_name_term_value', sa.String(), nullable=True))

    # Future: Only add missing columns
    op.add_column('futures', sa.Column('underlying_single_isin', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('basket_isin', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('underlying_index_isin', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('underlying_single_index_name', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('underlying_single_lei', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('basket_lei', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('additional_metal_product', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('oil_type', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('sub_product', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('additional_sub_product', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('metal_type', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('precious_metal', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('multi_commodity_base_product', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('other_c10_nondeliverable_base_product', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('other_c10_nondeliverable_sub_product', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('underlying_index_name_term_unit', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('underlying_index_name_term_value', sa.String(), nullable=True))

def downgrade() -> None:
    # Future
    op.drop_column('futures', 'underlying_index_name_term_value')
    op.drop_column('futures', 'underlying_index_name_term_unit')
    op.drop_column('futures', 'other_c10_nondeliverable_sub_product')
    op.drop_column('futures', 'other_c10_nondeliverable_base_product')
    op.drop_column('futures', 'multi_commodity_base_product')
    op.drop_column('futures', 'precious_metal')
    op.drop_column('futures', 'metal_type')
    op.drop_column('futures', 'additional_sub_product')
    op.drop_column('futures', 'sub_product')
    op.drop_column('futures', 'oil_type')
    op.drop_column('futures', 'additional_metal_product')
    op.drop_column('futures', 'basket_lei')
    op.drop_column('futures', 'underlying_single_lei')
    op.drop_column('futures', 'underlying_single_index_name')
    op.drop_column('futures', 'underlying_index_isin')
    op.drop_column('futures', 'basket_isin')
    op.drop_column('futures', 'underlying_single_isin')

    # Debt
    op.drop_column('debts', 'underlying_index_name_term_value')
    op.drop_column('debts', 'underlying_index_name_term_unit')
    op.drop_column('debts', 'other_commodity_base_product')
    op.drop_column('debts', 'precious_metal')
    op.drop_column('debts', 'metal_type')
    op.drop_column('debts', 'additional_sub_product')
    op.drop_column('debts', 'sub_product')
    op.drop_column('debts', 'oil_type')
    op.drop_column('debts', 'additional_metal_product')
    op.drop_column('debts', 'underlying_single_lei')
    op.drop_column('debts', 'underlying_single_index_name')
    op.drop_column('debts', 'underlying_index_isin')
    op.drop_column('debts', 'basket_isin')
    op.drop_column('debts', 'underlying_single_isin')

    # Equity
    op.drop_column('equities', 'additional_metal_product')
    op.drop_column('equities', 'underlying_single_index_name')
    op.drop_column('equities', 'underlying_single_isin')