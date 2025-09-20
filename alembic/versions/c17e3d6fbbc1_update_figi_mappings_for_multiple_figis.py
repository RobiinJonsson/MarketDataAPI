"""update_figi_mappings_for_multiple_figis

Revision ID: c17e3d6fbbc1
Revises: 8bb128ae650d
Create Date: 2025-09-20 14:21:16.961087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17e3d6fbbc1'
down_revision = '8bb128ae650d'
branch_labels = None
depends_on = None


def upgrade():
    """Remove unique constraint on ISIN to allow multiple FIGIs per ISIN."""
    # Drop the existing unique constraint on ISIN column
    # SQLite doesn't support dropping constraints directly, so we need to recreate the table
    
    # Create a new table with the same structure but without unique constraint on ISIN
    op.create_table('figi_mappings_new',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('isin', sa.String(length=12), nullable=False),  # Removed unique=True
        sa.Column('figi', sa.String(length=12), nullable=True),
        sa.Column('composite_figi', sa.String(length=12), nullable=True),
        sa.Column('share_class_figi', sa.String(length=12), nullable=True),
        sa.Column('ticker', sa.String(length=20), nullable=True),
        sa.Column('security_type', sa.String(length=50), nullable=True),
        sa.Column('market_sector', sa.String(length=50), nullable=True),
        sa.Column('security_description', sa.String(length=255), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['isin'], ['instruments.isin'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data from old table to new table
    op.execute("""
        INSERT INTO figi_mappings_new (id, isin, figi, composite_figi, share_class_figi, 
                                       ticker, security_type, market_sector, security_description, last_updated)
        SELECT id, isin, figi, composite_figi, share_class_figi, 
               ticker, security_type, market_sector, security_description, last_updated
        FROM figi_mappings
    """)
    
    # Drop old table and rename new table
    op.drop_table('figi_mappings')
    op.rename_table('figi_mappings_new', 'figi_mappings')


def downgrade():
    """Restore unique constraint on ISIN (will fail if multiple FIGIs per ISIN exist)."""
    # Create table with unique constraint restored
    op.create_table('figi_mappings_old',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('isin', sa.String(length=12), nullable=False, unique=True),  # Restored unique=True
        sa.Column('figi', sa.String(length=12), nullable=True),
        sa.Column('composite_figi', sa.String(length=12), nullable=True),
        sa.Column('share_class_figi', sa.String(length=12), nullable=True),
        sa.Column('ticker', sa.String(length=20), nullable=True),
        sa.Column('security_type', sa.String(length=50), nullable=True),
        sa.Column('market_sector', sa.String(length=50), nullable=True),
        sa.Column('security_description', sa.String(length=255), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['isin'], ['instruments.isin'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data (this will fail if multiple FIGIs per ISIN exist)
    op.execute("""
        INSERT INTO figi_mappings_old (id, isin, figi, composite_figi, share_class_figi, 
                                       ticker, security_type, market_sector, security_description, last_updated)
        SELECT id, isin, figi, composite_figi, share_class_figi, 
               ticker, security_type, market_sector, security_description, last_updated
        FROM figi_mappings
        GROUP BY isin  -- This will keep only one FIGI per ISIN
    """)
    
    # Drop new table and rename old table back
    op.drop_table('figi_mappings')
    op.rename_table('figi_mappings_old', 'figi_mappings')
