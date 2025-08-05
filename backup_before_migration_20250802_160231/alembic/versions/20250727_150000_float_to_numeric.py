"""convert float to numeric for sql server compatibility

Revision ID: 20250727_150000_float_to_numeric
Revises: 20250727_140000_increase_symbol_length
Create Date: 2025-07-27 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250727_150000_float_to_numeric'
down_revision: Union[str, None] = '20250727_140000_increase_symbol_length'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convert Float columns to Numeric in equities table
    op.execute("ALTER TABLE equities ALTER COLUMN price_multiplier NUMERIC(18,6)")
    op.execute("ALTER TABLE equities ALTER COLUMN shares_outstanding NUMERIC(18,2)")
    op.execute("ALTER TABLE equities ALTER COLUMN market_cap NUMERIC(20,2)")
    
    # Convert Float columns to Numeric in debts table
    op.execute("ALTER TABLE debts ALTER COLUMN total_issued_nominal NUMERIC(20,2)")
    op.execute("ALTER TABLE debts ALTER COLUMN nominal_value_per_unit NUMERIC(18,6)")
    op.execute("ALTER TABLE debts ALTER COLUMN fixed_interest_rate NUMERIC(8,4)")
    op.execute("ALTER TABLE debts ALTER COLUMN floating_rate_term_value NUMERIC(10,4)")
    op.execute("ALTER TABLE debts ALTER COLUMN floating_rate_basis_points_spread NUMERIC(10,4)")


def downgrade() -> None:
    # Convert back to Float (though this might lose precision)
    op.execute("ALTER TABLE equities ALTER COLUMN price_multiplier FLOAT")
    op.execute("ALTER TABLE equities ALTER COLUMN shares_outstanding FLOAT")
    op.execute("ALTER TABLE equities ALTER COLUMN market_cap FLOAT")
    
    op.execute("ALTER TABLE debts ALTER COLUMN total_issued_nominal FLOAT")
    op.execute("ALTER TABLE debts ALTER COLUMN nominal_value_per_unit FLOAT")
    op.execute("ALTER TABLE debts ALTER COLUMN fixed_interest_rate FLOAT")
    op.execute("ALTER TABLE debts ALTER COLUMN floating_rate_term_value FLOAT")
    op.execute("ALTER TABLE debts ALTER COLUMN floating_rate_basis_points_spread FLOAT")
