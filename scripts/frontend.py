import sqlite3
from typing import List, Dict, Any
from marketdata_api.database.db import DB_PATH, FIELD_MAPPING

def search_isin_frontend(isin):
    """
    Search for an ISIN and gather all related data from all tables.
    
    Args:
        isin (str): ISIN to search for
    
    Returns:
        Dict: Dictionary containing results from all tables if found, None otherwise
    """
    conn = None
    try:
        print(f"Starting search for ISIN: {isin}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        results = {}
        
        # Search in firds_e table
        cursor.execute("SELECT * FROM firds_e WHERE ISIN = ?", (isin,))
        row_e = cursor.fetchone()
        if row_e:
            cursor.execute("PRAGMA table_info(firds_e)")
            columns_e = [col[1] for col in cursor.fetchall()]
            results['equity'] = dict(zip(columns_e, row_e))
            print(f"Found equity data: {results['equity']}")  # Debug log
            # Store LEI for later lookup
            lei = results['equity'].get('IssuerLEI')

        # Search in firds_d table
        cursor.execute("SELECT * FROM firds_d WHERE ISIN = ?", (isin,))
        row_d = cursor.fetchone()
        if row_d:
            cursor.execute("PRAGMA table_info(firds_d)")
            columns_d = [col[1] for col in cursor.fetchall()]
            results['debt'] = dict(zip(columns_d, row_d))
            print(f"Found debt data: {results['debt']}")  # Debug log
            if 'lei' not in locals():
                lei = results['debt'].get('IssuerLEI')

        # Search in isin_figi_map table
        cursor.execute("SELECT * FROM isin_figi_map WHERE ISIN = ?", (isin,))
        row_figi = cursor.fetchone()
        if row_figi:
            cursor.execute("PRAGMA table_info(isin_figi_map)")
            columns_figi = [col[1] for col in cursor.fetchall()]
            results['figi'] = dict(zip(columns_figi, row_figi))
            print(f"Found FIGI data: {results['figi']}")  # Debug log

        # If we have an LEI, look up the data in gleif_lei_records
        if 'lei' in locals() and lei:
            cursor.execute("SELECT * FROM gleif_lei_records WHERE lei = ?", (lei,))
            row_lei = cursor.fetchone()
            if row_lei:
                cursor.execute("PRAGMA table_info(gleif_lei_records)")
                columns_lei = [col[1] for col in cursor.fetchall()]
                results['lei'] = dict(zip(columns_lei, row_lei))
                print(f"Found LEI data: {results['lei']}")  # Debug log

        if not results:
            print(f"No data found for ISIN: {isin}")
            return None

        print(f"Final results: {results}")  # Debug log
        return results

    except Exception as e:
        print(f"Error in search_isin_frontend: {str(e)}")
        raise  # Re-raise the exception to handle it in the route
    finally:
        if conn:
            conn.close()

def preview_table_data_frontend(table_name: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Preview data from a table for frontend use.
    
    Args:
        table_name (str): Name of the table
        limit (int): Number of rows to preview
    
    Returns:
        List[Dict]: List of rows with column names as keys
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))
        
        return result
    
    finally:
        conn.close()

def list_all_entries_frontend():
    """
    List latest entries from both firds_e and firds_d tables (10 each) for frontend use.
    
    Returns:
        Dict: Dictionary containing results from both tables
    """
    try:
        print("Starting list_all_entries_frontend")  # Debug
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        results = {}
        
        # Get data from firds_e table
        cursor.execute("PRAGMA table_info(firds_e)")
        columns_e = [col[1] for col in cursor.fetchall()]
        cursor.execute("SELECT * FROM firds_e ORDER BY ROWID DESC LIMIT 10")
        rows_e = cursor.fetchall()
        if rows_e:
            results['equity'] = [dict(zip(columns_e, row)) for row in rows_e]

        # Get data from firds_d table
        cursor.execute("PRAGMA table_info(firds_d)")
        columns_d = [col[1] for col in cursor.fetchall()]
        cursor.execute("SELECT * FROM firds_d ORDER BY ROWID DESC LIMIT 10")
        rows_d = cursor.fetchall()
        if rows_d:
            results['debt'] = [dict(zip(columns_d, row)) for row in rows_d]

        # Get FIGI mappings for all ISINs we found
        if results.get('equity') or results.get('debt'):
            all_isins = []
            if results.get('equity'):
                all_isins.extend(row['ISIN'] for row in results['equity'])
            if results.get('debt'):
                all_isins.extend(row['ISIN'] for row in results['debt'])

            # Get FIGI data for these ISINs
            cursor.execute("PRAGMA table_info(isin_figi_map)")
            columns_figi = [col[1] for col in cursor.fetchall()]
            placeholders = ','.join('?' * len(all_isins))
            cursor.execute(f"SELECT * FROM isin_figi_map WHERE ISIN IN ({placeholders})", all_isins)
            rows_figi = cursor.fetchall()
            if rows_figi:
                results['figi'] = [dict(zip(columns_figi, row)) for row in rows_figi]

        return results if results else None

    except Exception as e:
        print(f"Error in list_all_entries_frontend: {str(e)}")  # Debug
        return None
    finally:
        conn.close()
