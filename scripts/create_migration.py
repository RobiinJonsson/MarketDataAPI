"""
Database migration creation script for MarketDataAPI

This script creates new Alembic migration files with proper templates and naming.
"""

import sys
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for Windows compatibility
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def safe_print(message):
    """Print message with encoding safety for Windows terminals."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

def create_migration(description):
    """Create a new migration file with proper naming and template"""
    
    migrations_dir = project_root / 'migrations' / 'versions'
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate revision ID and timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    revision = f"{timestamp}_{description.lower().replace(' ', '_')}"
    
    # Create migration content template
    content = f'''"""
{description}

Revision ID: {revision}
Revises: 
Create Date: {datetime.now().isoformat()}

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '{revision}'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Upgrade database schema"""
    # Add your upgrade code here
    pass

def downgrade():
    """Downgrade database schema"""
    # Add your downgrade code here
    pass
'''
    
    # Write migration file
    filepath = migrations_dir / f'{revision}.py'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    safe_print(f'Created migration file: {filepath}')
    safe_print('Remember to add your upgrade/downgrade code!')
    
    return filepath

def main():
    """Main migration creation workflow"""
    if len(sys.argv) < 2:
        safe_print("Usage: python create_migration.py 'Migration description'")
        safe_print("Example: python create_migration.py 'Add transparency tables'")
        return False
    
    description = sys.argv[1]
    try:
        filepath = create_migration(description)
        safe_print(f"Migration created successfully: {filepath}")
        return True
    except Exception as e:
        safe_print(f"Error creating migration: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
