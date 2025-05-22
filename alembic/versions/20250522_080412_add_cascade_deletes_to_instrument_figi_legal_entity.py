"""Add cascade deletes to instrument/figi/legal_entity

Revision ID: 20250522_080412_add_cascade_deletes_to_instrument_figi_legal_entity
Revises: 20250521_110403_drop_symbol_unique_constraint
Create Date: 2025-05-22T08:04:12.914852

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20250522_080412_add_cascade_deletes_to_instrument_figi_legal_entity'
down_revision = '20250521_110403_drop_symbol_unique_constraint'  # Set this to your last migration ID
branch_labels = None
depends_on = None

def upgrade() -> None:
    with op.batch_alter_table('figi_mappings', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_figi_mappings_isin_instruments',
            'instruments',
            ['isin'],
            ['isin'],
            ondelete='CASCADE'
        )

    with op.batch_alter_table('instruments', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_instruments_lei_id_legal_entities',
            'legal_entities',
            ['lei_id'],
            ['lei'],
            ondelete='CASCADE'
        )

    with op.batch_alter_table('related_isins', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_related_isins_primary_instrument_id_instruments',
            'instruments',
            ['primary_instrument_id'],
            ['id'],
            ondelete='CASCADE'
        )

    with op.batch_alter_table('entity_addresses', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_entity_addresses_lei_legal_entities',
            'legal_entities',
            ['lei'],
            ['lei'],
            ondelete='CASCADE'
        )

    with op.batch_alter_table('entity_registrations', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_entity_registrations_lei_legal_entities',
            'legal_entities',
            ['lei'],
            ['lei'],
            ondelete='CASCADE'
        )

    for table in ['equities', 'debts', 'futures']:
        with op.batch_alter_table(table, recreate='always') as batch_op:
            batch_op.create_foreign_key(
                f'fk_{table}_id_instruments',
                'instruments',
                ['id'],
                ['id'],
                ondelete='CASCADE'
            )

def downgrade() -> None:
    with op.batch_alter_table('figi_mappings', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_figi_mappings_isin_instruments',
            'instruments',
            ['isin'],
            ['isin']
        )

    with op.batch_alter_table('instruments', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_instruments_lei_id_legal_entities',
            'legal_entities',
            ['lei_id'],
            ['lei']
        )

    with op.batch_alter_table('related_isins', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_related_isins_primary_instrument_id_instruments',
            'instruments',
            ['primary_instrument_id'],
            ['id']
        )

    with op.batch_alter_table('entity_addresses', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_entity_addresses_lei_legal_entities',
            'legal_entities',
            ['lei'],
            ['lei']
        )

    with op.batch_alter_table('entity_registrations', recreate='always') as batch_op:
        batch_op.create_foreign_key(
            'fk_entity_registrations_lei_legal_entities',
            'legal_entities',
            ['lei'],
            ['lei']
        )

    for table in ['equities', 'debts', 'futures']:
        with op.batch_alter_table(table, recreate='always') as batch_op:
            batch_op.create_foreign_key(
                f'fk_{table}_id_instruments',
                'instruments',
                ['id'],
                ['id']
            )
