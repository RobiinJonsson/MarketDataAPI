"""add entity addresses table

Revision ID: 20250517_121500_add_entity_addresses_table
Revises: 20250517_120000_add_last_updated_to_figi
Create Date: 2025-05-17T12:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250517_121500_add_entity_addresses_table'
down_revision = '20250517_120000_add_last_updated_to_figi'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('entity_addresses',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lei', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('address_lines', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('postal_code', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['lei'], ['legal_entities.lei'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_entity_addresses_lei', 'entity_addresses', ['lei'])

def downgrade() -> None:
    op.drop_index('idx_entity_addresses_lei')
    op.drop_table('entity_addresses')