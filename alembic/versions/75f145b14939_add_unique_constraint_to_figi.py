"""add_unique_constraint_to_figi

Revision ID: 75f145b14939
Revises: c17e3d6fbbc1
Create Date: 2025-09-20 14:41:06.909456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75f145b14939'
down_revision = 'c17e3d6fbbc1'
branch_labels = None
depends_on = None


def upgrade():
    """Add unique constraint to FIGI field to prevent duplicate FIGIs across all instruments."""
    # For SQLite, we need to recreate the table with the unique constraint
    
    # Create new table with unique constraint on figi
    op.create_table('figi_mappings_new',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('isin', sa.String(length=12), nullable=False),
        sa.Column('figi', sa.String(length=12), unique=True, nullable=True),  # Added unique=True
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
    
    # Copy data, removing any potential duplicates by keeping only the first occurrence of each FIGI
    # SQLite doesn't support DISTINCT ON, so we use a different approach
    op.execute("""
        INSERT INTO figi_mappings_new (id, isin, figi, composite_figi, share_class_figi, 
                                       ticker, security_type, market_sector, security_description, last_updated)
        SELECT id, isin, figi, composite_figi, share_class_figi, 
               ticker, security_type, market_sector, security_description, last_updated
        FROM figi_mappings f1
        WHERE figi IS NOT NULL 
        AND NOT EXISTS (
            SELECT 1 FROM figi_mappings f2 
            WHERE f2.figi = f1.figi 
            AND f2.last_updated > f1.last_updated
        )
    """)
    
    # Also copy records with NULL FIGIs (they don't violate uniqueness)
    op.execute("""
        INSERT INTO figi_mappings_new (id, isin, figi, composite_figi, share_class_figi, 
                                       ticker, security_type, market_sector, security_description, last_updated)
        SELECT id, isin, figi, composite_figi, share_class_figi, 
               ticker, security_type, market_sector, security_description, last_updated
        FROM figi_mappings
        WHERE figi IS NULL
    """)
    
    # Drop old table and rename new table
    op.drop_table('figi_mappings')
    op.rename_table('figi_mappings_new', 'figi_mappings')


def downgrade():
    """Remove unique constraint from FIGI field."""
    # Create table without unique constraint
    op.create_table('figi_mappings_old',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('isin', sa.String(length=12), nullable=False),
        sa.Column('figi', sa.String(length=12), nullable=True),  # Removed unique=True
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
    
    # Copy all data back
    op.execute("""
        INSERT INTO figi_mappings_old (id, isin, figi, composite_figi, share_class_figi, 
                                       ticker, security_type, market_sector, security_description, last_updated)
        SELECT id, isin, figi, composite_figi, share_class_figi, 
               ticker, security_type, market_sector, security_description, last_updated
        FROM figi_mappings
    """)
    
    # Drop new table and rename old table back
    op.drop_table('figi_mappings')
    op.rename_table('figi_mappings_old', 'figi_mappings')
