import sys
import os
from datetime import datetime
import re

MIGRATION_TEMPLATE = '''"""{}

Revision ID: {}
Revises: {}
Create Date: {}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '{}'
down_revision = '{}'  # Set this to your last migration ID
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Your migration code here
    pass

def downgrade() -> None:
    # Your rollback code here
    pass
'''

def create_migration(description):
    # Convert description to snake_case for filename
    filename = re.sub(r'[^a-z0-9]+', '_', description.lower()).strip('_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    revision = f'{timestamp}_{filename}'
    
    # Get the latest revision
    migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'alembic', 'versions')
    latest_revision = None
    if os.path.exists(migrations_dir):
        files = os.listdir(migrations_dir)
        if files:
            files.sort(reverse=True)
            latest_revision = files[0].split('_')[0]
    
    # Create migration content
    content = MIGRATION_TEMPLATE.format(
        description,
        revision,
        latest_revision or '<previous_revision_id>',
        datetime.now().isoformat(),
        revision,
        latest_revision or '<previous_revision_id>'
    )
    
    # Create migrations directory if it doesn't exist
    os.makedirs(migrations_dir, exist_ok=True)
    
    # Write migration file
    filepath = os.path.join(migrations_dir, f'{revision}.py')
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f'Created migration file: {filepath}')
    print('Remember to add your upgrade/downgrade code!')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python create_migration.py "Description of migration"')
        sys.exit(1)
    
    create_migration(sys.argv[1])
