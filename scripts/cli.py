import sys
import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from lxml import etree

# Add the parent directory of 'marketdata_api' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketdata_api.services.firds import (
    process_all_xml_files_cli, 
    downloads_dir,
    get_firds_file_urls,
    download_files,
    test_get_attributes_for_isin,
    ns
)
from marketdata_api.database.db import (
    insert_into_db, 
    map_fields, 
    insert_lei_data,
    create_gleif_tables,
    FIELD_MAPPING, 
    DEBT_FIELD_MAPPING, 
    DB_PATH
)
from marketdata_api.services.gleif import fetch_lei_info, map_lei_record

def fetch_and_insert(isin, instrument_type="equity"):
    """
    Fetch data for the given ISIN and insert it into the appropriate table.
    
    Args:
        isin (str): The ISIN to fetch data for
        instrument_type (str): Type of instrument ('equity' or 'debt')
    """
    print(f"Fetching data for ISIN: {isin} (Type: {instrument_type})")
    result = process_all_xml_files_cli(downloads_dir, isin, instrument_type)

    if result:
        print(f"Data extracted for ISIN {isin}: {result}")
        # Use the appropriate field mapping based on instrument type
        field_mapping = FIELD_MAPPING if instrument_type == "equity" else DEBT_FIELD_MAPPING
        mapped_data = map_fields(result, field_mapping)
        insert_into_db(mapped_data, instrument_type)
    else:
        print(f"No data found for ISIN: {isin}")


def list_all_cli():
    """List all entries from all tables in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # List of tables to process
    tables = ['firds_e', 'firds_d', 'isin_figi_map']
    
    for table in tables:
        # Check if table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            print(f"Table {table} does not exist.")
            continue
            
        print(f"\n=== {table.upper()} ===")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get data
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        if rows:
            print_headers(columns)
            for row in rows:
                print(format_row(row))
        else:
            print(f"No data found in {table}.")

    conn.close()


def search_isin_cli(isin):
    """Search for an ISIN across all tables in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # List of tables to search
    tables = ['firds_e', 'firds_d', 'isin_figi_map']
    found = False
    
    for table in tables:
        # Check if table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            continue
            
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Search for ISIN
        cursor.execute(f"SELECT * FROM {table} WHERE ISIN = ?", (isin,))
        rows = cursor.fetchall()
        
        if rows:
            found = True
            print(f"\n=== Found in {table.upper()} ===")
            print_headers(columns)
            for row in rows:
                print(format_row(row))
    
    if not found:
        print(f"No results found for ISIN: {isin}")

    conn.close()

def download_firds_file(date: str, file_type: str = "debt"):
    """
    Download FIRDS files for a specific date and type.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        file_type (str): Type of file ('equity' or 'debt')
    """
    try:
        print(f"Downloading {file_type} files for date {date}...")
        urls = get_firds_file_urls(date)
        
        if file_type == "debt":
            download_files({"debt": urls["debt"]}, downloads_dir)
        else:
            download_files({"equity": urls["equity"]}, downloads_dir)
            
        print("Download complete!")
        
    except Exception as e:
        print(f"Error downloading files: {e}")
        
# testing function for FIRDS file key:value pairs. Currently debt only hardcoded.
def test_debt_instrument(downloads_dir: str, target_isin: str):
    """
    Test processing of debt instruments by downloading and analyzing a file.
    
    Args:
        downloads_dir (str): Directory to save files
        target_isin (str): ISIN to test with
    """
    try:
        # Use the correct date that we know has files
        date = "2025-03-15"  # Date with known debt files
        print(f"Downloading debt files for date {date}...")
        
        # Download debt files
        urls = get_firds_file_urls(date)
        if not urls.get("debt"):
            print("No debt files found for this date")
            return
            
        download_files({"debt": urls["debt"]}, downloads_dir)
        print("Download complete!")
        
        # Then run the test functions
        print("\nTesting debt instrument processing...")
        
        # Only process debt files
        for file_name in os.listdir(downloads_dir):
            if file_name.startswith("FULINS_D_") and file_name.endswith(".xml"):
                file_path = os.path.join(downloads_dir, file_name)
                try:
                    print(f"\nProcessing file: {file_name}")
                    print(f"Testing for ISIN: {target_isin}")
                    
                    # If we found the instrument, exit early
                    if test_get_attributes_for_isin(file_path, target_isin):
                        print(f"Found instrument in file: {file_name}")
                        return
                    
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")
        
        print(f"Instrument {target_isin} not found in any file")
        
    except Exception as e:
        print(f"Error in test: {e}")

def process_all_lei_records():
    """Process LEI records for all ISINs in FIRDS tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("[+] Fetching all unique LEIs from FIRDS tables...")
        
        # Get unique IssuerLEI values from both tables
        cursor.execute("""
            SELECT DISTINCT IssuerLEI FROM (
                SELECT IssuerLEI FROM firds_e WHERE IssuerLEI IS NOT NULL
                UNION
                SELECT IssuerLEI FROM firds_d WHERE IssuerLEI IS NOT NULL
            )
        """)
        
        lei_codes = [row[0] for row in cursor.fetchall()]
        total = len(lei_codes)
        
        print(f"[+] Found {total} unique LEI codes")
        
        for index, lei in enumerate(lei_codes, 1):
            try:
                print(f"[{index}/{total}] Processing LEI: {lei}")
                
                # Fetch and process LEI data
                response = fetch_lei_info(lei)
                if 'error' not in response:
                    lei_data = map_lei_record(response)
                    insert_lei_data(lei_data)
                    print(f"[✓] Successfully processed LEI: {lei}")
                else:
                    print(f"[!] Error fetching data for LEI: {lei}")
                
            except Exception as e:
                print(f"[!] Error processing LEI {lei}: {str(e)}")
                continue
        
        print(f"\n[✓] Completed processing {total} LEI records")
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")
    finally:
        conn.close()

def print_usage():
    print("""
Usage:
    python scripts/cli.py fetch <ISIN> [instrument_type]       or: python scripts/cli.py f <ISIN> [instrument_type]
    python scripts/cli.py search <ISIN>                        or: python scripts/cli.py s <ISIN>
    python scripts/cli.py list                                 or: python scripts/cli.py l
    python scripts/cli.py delete <ISIN> [table]                or: python scripts/cli.py d <ISIN> [table]
    python scripts/cli.py rename <table> <old_name> <new_name> or: python scripts/cli.py r <table> <old_name> <new_name>
    python scripts/cli.py tables                               or: python scripts/cli.py t
    python scripts/cli.py schema <table>                       or: python scripts/cli.py sc <table>
    python scripts/cli.py preview <table> [limit]              or: python scripts/cli.py p <table> [limit]
    python scripts/cli.py modify <table> <column> <new_type>   or: python scripts/cli.py m <table> <column> <new_type>
    python scripts/cli.py copy <src_table> <new_table> [data]  or: python scripts/cli.py cp <src_table> <new_table> [data]
    python scripts/cli.py backup                               or: python scripts/cli.py b
    python scripts/cli.py cfi <code>                           or: python scripts/cli.py c <code>
    python scripts/cli.py analyze_cfi                          or: python scripts/cli.py ac
    python scripts/cli.py download <date> [type]               or: python scripts/cli.py dl <date> [type]
    python scripts/cli.py test_debt <ISIN>                     or: python scripts/cli.py td <ISIN>
    python scripts/cli.py gleif <LEI>        - Import LEI record from GLEIF API
    python scripts/cli.py gleif-print <LEI> - Print LEI record from GLEIF API
    python scripts/cli.py process-lei                         - Process LEI records for all ISINs in database
          
Commands:
    fetch     Fetch data for the given ISIN from XML and insert into the database
              For equity instruments: python scripts/cli.py fetch <ISIN> or python scripts/cli.py fetch <ISIN> equity
              For debt instruments: python scripts/cli.py fetch <ISIN> debt
    search    Search for an ISIN across all tables (firds_e, firds_d, isin_figi_map)
    list      List all rows from all tables (firds_e, firds_d, isin_figi_map)
    delete    Delete a row by ISIN from the specified table (default: firds_e)
    rename    Rename a column in the specified table
    tables    List all tables and their columns in the database
    schema    Show detailed schema for a table
    preview   Preview data from a table (default 5 rows)
    modify    Modify a column's data type
    copy      Copy table structure and optionally data
    backup    Create a timestamped backup of the database
    cfi       Classify a CFI code
    analyze_cfi Analyze CFI codes in the database
    download  Download FIRDS files for a specific date and type (default: debt)
    test_debt Test processing of debt instruments with a specific ISIN
    gleif     Import LEI record from GLEIF API
    gleif-print Print LEI record from GLEIF API
    process-lei Process LEI records for all ISINs in database

Examples:
    python scripts/cli.py fetch SE0000242455
    python scripts/cli.py fetch SE0000242455 equity
    python scripts/cli.py fetch SE0000242455 debt
    python scripts/cli.py s SE0000242455
    python scripts/cli.py l
    python scripts/cli.py delete NL00150001S5
    python scripts/cli.py d NL00150001S5 isin_figi_map
    python scripts/cli.py gleif 5493001KJTIIGC8Y1R12 - Import LEI record from GLEIF API
    python scripts/cli.py gleif-print 5493001KJTIIGC8Y1R12 - Print LEI record from GLEIF API
    python scripts/cli.py process-lei      - Process all LEI records
""")

def print_headers(columns):
    print(" | ".join(columns))
    print("-" * 150)

def format_row(row):
    return " | ".join(str(col) if col is not None else "" for col in row)

def rename_column(old_name, new_name):
    """
    Rename a column in the firds_e table.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # First, check if the old column exists
        cursor.execute(f"PRAGMA table_info(firds_e)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if old_name not in column_names:
            print(f"Error: Column '{old_name}' does not exist in the table.")
            return False

        # Create a new table with the desired schema
        column_definitions = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            if col_name == old_name:
                column_definitions.append(f'"{new_name}" {col_type}')
            else:
                column_definitions.append(f'"{col_name}" {col_type}')

        # Create new table and copy data
        cursor.execute(f"""
            CREATE TABLE firds_e_new (
                {', '.join(column_definitions)}
            )
        """)

        # Copy the data
        old_cols = [old_name if col == old_name else col for col in column_names]
        cursor.execute(f"""
            INSERT INTO firds_e_new 
            SELECT {', '.join(old_cols)} 
            FROM firds_e
        """)

        # Drop the old table and rename the new one
        cursor.execute("DROP TABLE firds_e")
        cursor.execute("ALTER TABLE firds_e_new RENAME TO firds_e")

        conn.commit()
        print(f"Successfully renamed column '{old_name}' to '{new_name}'")
        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def backup_database():
    """
    Create a backup of the database with timestamp.
    
    Returns:
        str: Path to the backup file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{DB_PATH}_backup_{timestamp}"
    
    try:
        with sqlite3.connect(DB_PATH) as src, sqlite3.connect(backup_path) as dst:
            src.backup(dst)
        print(f"Database backup created: {backup_path}")
        return backup_path
    except sqlite3.Error as e:
        print(f"Backup failed: {e}")
        return None

def get_table_schema(table_name: str) -> List[Dict[str, Any]]:
    """
    Get detailed schema information for a table.
    
    Args:
        table_name (str): Name of the table
    
    Returns:
        List[Dict]: List of column definitions with detailed information
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get index info
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        
        # Get foreign key info
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        
        schema_info = []
        for col in columns:
            col_info = {
                "name": col[1],
                "type": col[2],
                "not_null": bool(col[3]),
                "default_value": col[4],
                "is_primary_key": bool(col[5]),
                "indexes": [],
                "foreign_keys": []
            }
            
            # Add index information
            for idx in indexes:
                cursor.execute(f"PRAGMA index_info({idx[1]})")
                index_columns = cursor.fetchall()
                if any(index_col[2] == col[1] for index_col in index_columns):
                    col_info["indexes"].append({
                        "name": idx[1],
                        "unique": bool(idx[2])
                    })
            
            # Add foreign key information
            for fk in foreign_keys:
                if fk[3] == col[1]:
                    col_info["foreign_keys"].append({
                        "table": fk[2],
                        "column": fk[4],
                        "on_update": fk[5],
                        "on_delete": fk[6]
                    })
            
            schema_info.append(col_info)
        
        return schema_info
    
    finally:
        conn.close()

def preview_table_data(table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Preview data from a table.
    
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

def modify_column_type(table_name: str, column_name: str, new_type: str) -> bool:
    """
    Modify the data type of a column.
    
    Args:
        table_name (str): Name of the table
        column_name (str): Name of the column to modify
        new_type (str): New SQL data type
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create backup before modifying
        backup_path = backup_database()
        if not backup_path:
            return False
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get current table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Verify column exists
        if not any(col[1] == column_name for col in columns):
            print(f"Error: Column '{column_name}' does not exist in table '{table_name}'")
            return False
        
        # Create new table with modified schema
        column_defs = []
        for col in columns:
            name = col[1]
            type_ = new_type if name == column_name else col[2]
            not_null = "NOT NULL" if col[3] else ""
            pk = "PRIMARY KEY" if col[5] else ""
            column_defs.append(f'"{name}" {type_} {not_null} {pk}'.strip())
        
        # Create new table and copy data
        cursor.execute(f"""
            CREATE TABLE {table_name}_new (
                {', '.join(column_defs)}
            )
        """)
        
        cursor.execute(f"""
            INSERT INTO {table_name}_new 
            SELECT * FROM {table_name}
        """)
        
        # Replace old table
        cursor.execute(f"DROP TABLE {table_name}")
        cursor.execute(f"ALTER TABLE {table_name}_new RENAME TO {table_name}")
        
        conn.commit()
        print(f"Successfully modified column '{column_name}' to type '{new_type}'")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if backup_path:
            print(f"You can restore from backup: {backup_path}")
        return False
    finally:
        conn.close()

def copy_table(source_table: str, target_table: str, with_data: bool = True) -> bool:
    """
    Copy a table structure and optionally its data.
    
    Args:
        source_table (str): Name of the source table
        target_table (str): Name of the new table
        with_data (bool): Whether to copy the data as well
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if source table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (source_table,))
        if not cursor.fetchone():
            print(f"Error: Source table '{source_table}' does not exist")
            return False
            
        # Check if target table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (target_table,))
        if cursor.fetchone():
            print(f"Error: Target table '{target_table}' already exists")
            return False
        
        # Create new table with same schema
        cursor.execute(f"""
            CREATE TABLE {target_table} AS 
            SELECT * FROM {source_table} 
            {'' if with_data else 'WHERE 1=0'}
        """)
        
        # Copy indexes
        cursor.execute(f"PRAGMA index_list({source_table})")
        indexes = cursor.fetchall()
        
        for idx in indexes:
            cursor.execute(f"PRAGMA index_info({idx[1]})")
            index_columns = cursor.fetchall()
            column_names = [f'"{col[2]}"' for col in index_columns]
            
            cursor.execute(f"""
                CREATE {'UNIQUE ' if idx[2] else ''}INDEX 
                {target_table}_{idx[1]} ON {target_table}
                ({', '.join(column_names)})
            """)
        
        conn.commit()
        print(f"Successfully copied table '{source_table}' to '{target_table}'")
        print(f"Copied {'with' if with_data else 'without'} data")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def list_tables():
    """
    List all tables and their columns in the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            print("-" * (len(table_name) + 7))
            
            # Get columns for this table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
        
    finally:
        conn.close()

def classify_cfi(cfi_code: str) -> Dict[str, str]:
    """
    Classify a CFI code according to ISO 10962 standard.
    
    Args:
        cfi_code (str): 6-character CFI code (e.g., 'ESVUFR')
    
    Returns:
        Dict[str, str]: Dictionary with classification details
    """
    if len(cfi_code) != 6:
        return {"error": "CFI code must be 6 characters long"}
    
    # CFI code classification mapping
    category_map = {
        'E': 'Equities',
        'D': 'Debt',
        'R': 'Rights',
        'O': 'Options',
        'F': 'Futures',
        'C': 'Commodities',
        'M': 'Miscellaneous'
    }
    
    group_map = {
        'S': 'Shares',
        'B': 'Bonds',
        'P': 'Preferred',
        'W': 'Warrants',
        'C': 'Convertible',
        'N': 'Non-convertible',
        'T': 'Transferable',
        'U': 'Non-transferable'
    }
    
    attribute_map = {
        'V': 'Voting',
        'N': 'Non-voting',
        'P': 'Preference',
        'C': 'Common',
        'B': 'Bearer',
        'R': 'Registered'
    }
    
    type_map = {
        'R': 'Registered',
        'B': 'Bearer',
        'N': 'Non-voting',
        'V': 'Voting'
    }
    
    form_map = {
        'C': 'Certificate',
        'D': 'Dematerialized',
        'B': 'Bearer',
        'R': 'Registered'
    }
    
    additional_map = {
        'P': 'Preferred',
        'C': 'Common',
        'B': 'Bearer',
        'R': 'Registered',
        'F': 'Free',
        'N': 'Non-voting'
    }
    
    try:
        return {
            "Category": category_map.get(cfi_code[0], "Unknown"),
            "Group": group_map.get(cfi_code[1], "Unknown"),
            "Attribute": attribute_map.get(cfi_code[2], "Unknown"),
            "Type": type_map.get(cfi_code[3], "Unknown"),
            "Form": form_map.get(cfi_code[4], "Unknown"),
            "Additional": additional_map.get(cfi_code[5], "Unknown")
        }
    except Exception as e:
        return {"error": f"Error classifying CFI code: {str(e)}"}

def analyze_cfi_codes(table_name: str = "firds_e", cfi_column: str = "CFICode") -> Dict[str, Any]:
    """
    Analyze CFI codes in a table and provide statistics.
    
    Args:
        table_name (str): Name of the table
        cfi_column (str): Name of the CFI code column
    
    Returns:
        Dict[str, Any]: Statistics about CFI codes in the table
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get unique CFI codes and their counts
        cursor.execute(f"""
            SELECT {cfi_column}, COUNT(*) as count 
            FROM {table_name} 
            WHERE {cfi_column} IS NOT NULL 
            GROUP BY {cfi_column}
        """)
        results = cursor.fetchall()
        
        # Analyze each CFI code
        analysis = {
            "total_codes": len(results),
            "codes": {}
        }
        
        for cfi_code, count in results:
            if cfi_code:
                analysis["codes"][cfi_code] = {
                    "count": count,
                    "classification": classify_cfi(cfi_code)
                }
        
        return analysis
    
    finally:
        conn.close()

def delete_by_isin(isin: str, table: str = "firds_e") -> bool:
    """
    Delete a row from the specified table using ISIN as the key.
    Handles both string values and NULL/None values.
    
    Args:
        isin (str): The ISIN to delete (can be 'N/A', 'None', or actual ISIN)
        table (str): The table to delete from (default: "firds_e")
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Debug: List all ISINs in the table
        cursor.execute(f"SELECT ISIN FROM {table}")
        all_isins = cursor.fetchall()
        print(f"All ISINs in table {table}: {all_isins}")
        
        # Handle NULL/None values
        if isin.upper() in ['N/A', 'NONE']:
            # Delete rows where ISIN is NULL
            cursor.execute(f"DELETE FROM {table} WHERE ISIN IS NULL")
            print("Deleting rows with NULL ISIN values")
        else:
            # Delete rows with matching ISIN
            cursor.execute(f"DELETE FROM {table} WHERE ISIN = '{isin}'")
            print(f"Deleting rows with ISIN = '{isin}'")
        
        # If deleting from firds_e, also delete from isin_figi_map if it exists
        if table == "firds_e":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='isin_figi_map'")
            if cursor.fetchone():
                if isin.upper() in ['N/A', 'NONE']:
                    cursor.execute("DELETE FROM isin_figi_map WHERE ISIN IS NULL")
                else:
                    cursor.execute(f"DELETE FROM isin_figi_map WHERE ISIN = '{isin}'")
        
        # Get the number of rows affected
        rows_affected = cursor.rowcount
        conn.commit()
        
        if rows_affected > 0:
            print(f"Successfully deleted {rows_affected} rows from table {table}")
            return True
        else:
            print(f"No rows found to delete in table {table}")
            return False
        
    except sqlite3.Error as e:
        print(f"Error deleting ISIN {isin}: {str(e)}")
        return False
    finally:
        conn.close()

def run_gleif_cli(lei: str):
    conn = sqlite3.connect(DB_PATH)
    try:
        print(f"[+] Creating tables if not present...")
        create_gleif_tables()

        print(f"[+] Fetching LEI record for: {lei}")
        response = fetch_lei_info(lei)

        print(f"[+] Mapping GLEIF data to internal structure...")
        parsed = map_lei_record(response)

        print(f"[+] Inserting data into database...")
        insert_lei_data(parsed)

        print(f"[✓] Success! Inserted data for LEI: {lei}")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()

def print_gleif_record(lei: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        print(f"\n🔍 Fetching data for LEI: {lei}")

        cur.execute("SELECT * FROM gleif_lei_records WHERE lei = ?", (lei,))
        lei_record = cur.fetchone()

        if not lei_record:
            print("⚠️ No record found.")
            return

        print("\n📄 LEI Record:")
        for key in lei_record.keys():
            print(f"  {key}: {lei_record[key]}")

        print("\n🏢 Addresses:")
        cur.execute("SELECT * FROM gleif_addresses WHERE lei = ?", (lei,))
        addresses = cur.fetchall()
        for addr in addresses:
            print(f"  - Type: {addr['type']}")
            print(f"    Address: {addr['addressLines']}, {addr['city']}, {addr['region']} {addr['postalCode']} ({addr['country']})")

        print("\n🗂 Registration:")
        cur.execute("SELECT * FROM gleif_registration WHERE lei = ?", (lei,))
        reg = cur.fetchone()
        if reg:
            for key in reg.keys():
                print(f"  {key}: {reg[key]}")

        print("\n🕒 Meta Info:")
        cur.execute("SELECT * FROM gleif_meta_info WHERE lei = ?", (lei,))
        meta = cur.fetchone()
        if meta:
            for key in meta.keys():
                print(f"  {key}: {meta[key]}")

    except Exception as e:
        print(f"[!] Error while querying: {e}")
    finally:
        conn.close()

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    
    if command in ['fetch', 'f']:
        if len(sys.argv) < 3:
            print("Usage: python scripts/cli.py fetch <ISIN> [instrument_type]")
            return
        isin = sys.argv[2]
        instrument_type = sys.argv[3] if len(sys.argv) > 3 else "equity"
        if instrument_type not in ["equity", "debt"]:
            print("Error: instrument_type must be either 'equity' or 'debt'")
            return
        fetch_and_insert(isin, instrument_type)
        
    elif command in ['search', 's']:
        if len(sys.argv) != 3:
            print("Usage: python scripts/cli.py search <ISIN>")
            return
        search_isin_cli(sys.argv[2])
        
    elif command in ['list', 'l']:
        list_all_cli()
        
    elif command in ['delete', 'd']:
        if len(sys.argv) < 3:
            print("Usage: python scripts/cli.py delete <ISIN> [table]")
            return
        isin = sys.argv[2]
        table = sys.argv[3] if len(sys.argv) > 3 else "firds_e"
        delete_by_isin(isin, table)
        
    elif command in ['tables', 't']:
        list_tables()
        
    elif command in ['rename', 'r'] and len(sys.argv) == 5:
        table_name = sys.argv[2]
        old_name = sys.argv[3]
        new_name = sys.argv[4]
        if not rename_column(table_name, old_name, new_name):
            sys.exit(1)
        
    elif command in ['schema', 'sc'] and len(sys.argv) == 3:
        schema = get_table_schema(sys.argv[2])
        print(json.dumps(schema, indent=2))
        
    elif command in ['preview', 'p']:
        table_name = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        data = preview_table_data(table_name, limit)
        print(json.dumps(data, indent=2))
        
    elif command in ['modify', 'm'] and len(sys.argv) == 5:
        if not modify_column_type(sys.argv[2], sys.argv[3], sys.argv[4]):
            sys.exit(1)
        
    elif command in ['copy', 'cp']:
        source = sys.argv[2]
        target = sys.argv[3]
        with_data = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else True
        if not copy_table(source, target, with_data):
            sys.exit(1)
        
    elif command in ['backup', 'b']:
        if not backup_database():
            sys.exit(1)
        
    elif command in ['cfi', 'c'] and len(sys.argv) == 3:
        result = classify_cfi(sys.argv[2])
        print(json.dumps(result, indent=2))
        
    elif command in ['analyze_cfi', 'ac']:
        result = analyze_cfi_codes()
        print(json.dumps(result, indent=2))
        
    elif command in ['download', 'dl']:
        if len(sys.argv) < 3:
            print("Usage: python scripts/cli.py download <date> [type]")
            return
        date = sys.argv[2]
        file_type = sys.argv[3] if len(sys.argv) > 3 else "debt"
        download_firds_file(date, file_type)
        
    elif command in ['test_debt', 'td']:
        if len(sys.argv) != 3:
            print("Usage: python scripts/cli.py test_debt <ISIN>")
            return
        test_debt_instrument(downloads_dir, sys.argv[2])
    
    elif command in ['gleif', 'lei'] and len(sys.argv) == 3:
        if len(sys.argv) != 3:
            print("Usage: python scripts/cli.py gleif <LEI>")
            return
        lei = sys.argv[2]
        run_gleif_cli(lei)
    
    elif command == 'gleif-print' and len(sys.argv) == 3:
        if len(sys.argv) != 3:
            print("Usage: python scripts/cli.py gleif-print <LEI>")
            return
        lei = sys.argv[2]
        print_gleif_record(lei)
    
    elif command == 'process-lei':
        process_all_lei_records()
        
    else:
        print("Invalid command or wrong number of arguments.")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
