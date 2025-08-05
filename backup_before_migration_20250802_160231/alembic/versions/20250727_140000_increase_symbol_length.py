"""increase symbol column length

Revision ID: 20250727_140000_increase_symbol_length
Revises: 20250601_120000_add_transparency_tables
Create Date: 2025-07-27 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250727_140000_increase_symbol_length'
down_revision = '20250601_120000_add_transparency_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Increase symbol column length from 20 to 50 characters"""
    # Use raw SQL for SQL Server compatibility
    op.execute("ALTER TABLE instruments ALTER COLUMN symbol NVARCHAR(50)")


def downgrade():
    """Decrease symbol column length back to 20 characters"""
    # Use raw SQL for SQL Server compatibility  
    op.execute("ALTER TABLE instruments ALTER COLUMN symbol NVARCHAR(20)")
