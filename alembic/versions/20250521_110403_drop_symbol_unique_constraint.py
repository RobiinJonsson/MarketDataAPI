"""drop symbol unique constraint

Revision ID: 20250521_110403_drop_symbol_unique_constraint
Revises: 20250521_081253_add_full_fulins_coverage_fields_to_instrument_models
Create Date: 2025-05-21T11:04:03.021698

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250521_110403_drop_symbol_unique_constraint'
down_revision = '20250521_081253_add_full_fulins_coverage_fields_to_instrument_models'
branch_labels = None
depends_on = None

def upgrade():
    # Try to drop any unique constraint on 'symbol', regardless of its name.
    # For SQLite, unique constraints on columns are often implemented as unique indexes.
    # We'll drop any unique index on 'symbol' if it exists.
    conn = op.get_bind()
    insp = sa.inspect(conn)
    indexes = insp.get_indexes('instruments')
    for idx in indexes:
        if idx.get('unique', False) and idx.get('column_names') == ['symbol']:
            op.drop_index(idx['name'], table_name='instruments')
            break
    # If you know the constraint is not an index but a table constraint, you can also try:
    # with op.batch_alter_table('instruments') as batch_op:
    #     batch_op.drop_constraint('<constraint_name>', type_='unique')

def downgrade():
    # Re-add unique constraint on 'symbol'
    with op.batch_alter_table('instruments') as batch_op:
        batch_op.create_unique_constraint('uq_instruments_symbol', ['symbol'])
