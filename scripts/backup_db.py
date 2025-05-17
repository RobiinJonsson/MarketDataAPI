import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketdata_api.database.session import get_session
import json
from datetime import datetime

def backup_data():
    with get_session() as session:
        # Query all instruments
        result = session.execute("SELECT * FROM instruments")
        data = [dict(row) for row in result]
        
        # Save to backup file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'db_backup_{timestamp}.json', 'w') as f:
            json.dump(data, f, default=str)

if __name__ == "__main__":
    backup_data()
