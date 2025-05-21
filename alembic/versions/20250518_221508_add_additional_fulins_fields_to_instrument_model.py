"""Add additional fulins fields to instrument model

Revision ID: 20250518_221508_add_additional_fulins_fields_to_instrument_model
Revises: 20250517_122000_add_entity_registrations_table
Create Date: 2025-05-18T22:15:08.553403

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20250518_221508_add_additional_fulins_fields_to_instrument_model'
down_revision = '20250517_122000_add_entity_registrations_table'  # Set this to your last migration ID
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Your migration code here
    pass

def downgrade() -> None:
    # Your rollback code here
    pass
def upgrade() -> None:
    # Add technical_from_date to instruments table
    op.add_column('instruments', sa.Column('technical_from_date', sa.DateTime(), nullable=True))

    # Add floating rate fields to debts table
    op.add_column('debts', sa.Column('floating_rate_reference', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('floating_rate_term_unit', sa.String(), nullable=True))
    op.add_column('debts', sa.Column('floating_rate_term_value', sa.Float(), nullable=True))
    op.add_column('debts', sa.Column('floating_rate_basis_points_spread', sa.Float(), nullable=True))

    # Add commodity and index fields to futures table
    op.add_column('futures', sa.Column('final_price_type', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('transaction_type', sa.String(), nullable=True))
    op.add_column('futures', sa.Column('underlying_index_name', sa.String(), nullable=True))

def downgrade() -> None:
    # Remove futures fields
    op.drop_column('futures', 'underlying_index_name')
    op.drop_column('futures', 'transaction_type')
    op.drop_column('futures', 'final_price_type')

    # Remove debts fields
    op.drop_column('debts', 'floating_rate_basis_points_spread')
    op.drop_column('debts', 'floating_rate_term_value')
    op.drop_column('debts', 'floating_rate_term_unit')
    op.drop_column('debts', 'floating_rate_reference')

    # Remove instruments fields
    op.drop_column('instruments', 'technical_from_date')