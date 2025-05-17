"""add last_updated to figi

Revision ID: 20250517_120000_add_last_updated_to_figi
Revises: 20250517_114500_add_supporting_tables
Create Date: 2025-05-17T12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250517_120000_add_last_updated_to_figi'
down_revision = '20250517_114500_add_supporting_tables'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Only add last_updated column since id is already there
    op.add_column('figi_mappings', sa.Column('last_updated', sa.DateTime(), nullable=True))

def downgrade() -> None:
    with op.batch_alter_table('figi_mappings') as batch_op:
        batch_op.drop_column('last_updated')
