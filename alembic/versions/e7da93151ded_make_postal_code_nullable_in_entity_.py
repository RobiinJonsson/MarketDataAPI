"""make_postal_code_nullable_in_entity_addresses

Revision ID: e7da93151ded
Revises: 75f145b14939
Create Date: 2025-10-05 16:33:13.962833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7da93151ded'
down_revision = '75f145b14939'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite doesn't support ALTER COLUMN, so we need to recreate the table
    # First, create a new table with nullable postal_code
    op.create_table('entity_addresses_new',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('lei', sa.String(20), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('address_lines', sa.String(500)),
        sa.Column('country', sa.String(5)),
        sa.Column('city', sa.String(100)),
        sa.Column('region', sa.String(100)),
        sa.Column('postal_code', sa.String(20), nullable=True),  # Now nullable
        sa.ForeignKeyConstraint(['lei'], ['legal_entities.lei'], ondelete='CASCADE'),
    )
    
    # Copy data from old table to new table
    op.execute('INSERT INTO entity_addresses_new SELECT * FROM entity_addresses')
    
    # Drop old table and rename new one
    op.drop_table('entity_addresses')
    op.rename_table('entity_addresses_new', 'entity_addresses')


def downgrade():
    # Reverse the change by recreating table with NOT NULL postal_code
    op.create_table('entity_addresses_new',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('lei', sa.String(20), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('address_lines', sa.String(500)),
        sa.Column('country', sa.String(5)),
        sa.Column('city', sa.String(100)),
        sa.Column('region', sa.String(100)),
        sa.Column('postal_code', sa.String(20), nullable=False),  # Back to NOT NULL
        sa.ForeignKeyConstraint(['lei'], ['legal_entities.lei'], ondelete='CASCADE'),
    )
    
    # Copy only records with non-null postal codes (data may be lost)
    op.execute('INSERT INTO entity_addresses_new SELECT * FROM entity_addresses WHERE postal_code IS NOT NULL')
    
    # Drop old table and rename new one
    op.drop_table('entity_addresses')
    op.rename_table('entity_addresses_new', 'entity_addresses')
