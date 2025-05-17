"""add entity registrations table

Revision ID: 20250517_122000_add_entity_registrations_table
Revises: 20250517_121500_add_entity_addresses_table
Create Date: 2025-05-17T12:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250517_122000_add_entity_registrations_table'
down_revision = '20250517_121500_add_entity_addresses_table'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('entity_registrations',
        sa.Column('lei', sa.String(), nullable=False),
        sa.Column('initial_date', sa.DateTime(), nullable=True),
        sa.Column('last_update', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('next_renewal', sa.DateTime(), nullable=True),
        sa.Column('managing_lou', sa.String(), nullable=True),
        sa.Column('validation_sources', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['lei'], ['legal_entities.lei'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('lei')
    )
    op.create_index('idx_entity_registrations_lei', 'entity_registrations', ['lei'])

def downgrade() -> None:
    op.drop_index('idx_entity_registrations_lei')
    op.drop_table('entity_registrations')
