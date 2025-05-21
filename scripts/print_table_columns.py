import sqlite3

db_path = "c:/Users/robin/Projects/MarketDataAPI/marketdata_api/database/marketdata.db"  # Update this path if needed

tables = ["equities", "debts", "futures"]

conn = sqlite3.connect(db_path)
cur = conn.cursor()

for table in tables:
    print(f"\nColumns in table '{table}':")
    cur.execute(f"PRAGMA table_info({table})")
    for row in cur.fetchall():
        print(f"  {row[1]}")
conn.close()
