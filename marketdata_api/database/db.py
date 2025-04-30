import sqlite3
import os
import sys
from typing import Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Dynamically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) #during development

#db_path = "C:\\Users\\robin\\Projects\\MarketDataAPI\\marketdata_api\\database\\marketdata.db"
file_path = "C:\\Users\\robin\\Projects\\MarketDataAPI\\downloads"

# Ensure the database is always created inside `marketdata_api/database/`
DB_PATH = os.path.join(os.path.dirname(__file__), "marketdata.db")

# Add SQLAlchemy setup
engine = create_engine(f'sqlite:///{DB_PATH}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add table mapping to indicate where each field should be stored
TABLE_MAPPING = {
    'instruments': [
        'FinInstrmGnlAttrbts_Id',
        'FinInstrmGnlAttrbts_FullNm',
        'FinInstrmGnlAttrbts_ShrtNm',
        'FinInstrmGnlAttrbts_ClssfctnTp',
        'FinInstrmGnlAttrbts_NtnlCcy',
        'FinInstrmGnlAttrbts_CmmdtyDerivInd',
        'Issr',
        'TradgVnRltdAttrbts_Id',
        'TradgVnRltdAttrbts_IssrReq',
        'TradgVnRltdAttrbts_FrstTradDt',
        'TechAttrbts_RlvntCmptntAuthrty',
        'TechAttrbts_RlvntTradgVn',
        'PblctnPrd_FrDt',
        'TradgVnRltdAttrbts_TermntnDt'
    ],
    'debts': [
        'DebtInstrmAttrbts_TtlIssdNmnlAmt',
        'DebtInstrmAttrbts_MtrtyDt',
        'DebtInstrmAttrbts_NmnlValPerUnit',
        'DebtInstrmAttrbts_IntrstRate_Fxd',
        'DebtInstrmAttrbts_DebtSnrty'
    ]
}

# field mapping for the database
# This mapping is used to rename the fields in the XML files to more user-friendly names
FIELD_MAPPING = {
    "FinInstrmGnlAttrbts_Id": "ISIN",
    "FinInstrmGnlAttrbts_FullNm": "FullName",
    "FinInstrmGnlAttrbts_ShrtNm": "ShortName",
    "FinInstrmGnlAttrbts_ClssfctnTp": "CFICode",
    "FinInstrmGnlAttrbts_NtnlCcy": "Currency",
    "FinInstrmGnlAttrbts_CmmdtyDerivInd": "ComdtyDerInd",
    "Issr": "IssuerLEI",
    "TradgVnRltdAttrbts_Id": "TradingVenueId",
    "TradgVnRltdAttrbts_IssrReq": "IssuerReq",
    "TradgVnRltdAttrbts_FrstTradDt": "FirstTradeDate",
    "DerivInstrmAttrbts_UndrlygInstrm": "UnderlyingInstrm",
    "TechAttrbts_RlvntCmptntAuthrty": "RlvntCmptntAuthrty",
    "TechAttrbts_RlvntTradgVn": "RelevantTradingVenue",
    "PblctnPrd_FrDt": "FromDate",
    "TradgVnRltdAttrbts_TermntnDt": "TerminationDate"
}

# Field mapping specifically for debt instruments
# Combines reusable fields from FIELD_MAPPING with debt-specific fields
DEBT_FIELD_MAPPING = {
    # Reused fields from FIELD_MAPPING
    "FinInstrmGnlAttrbts_Id": "ISIN",
    "FinInstrmGnlAttrbts_FullNm": "FullName",
    "FinInstrmGnlAttrbts_ShrtNm": "ShortName",
    "FinInstrmGnlAttrbts_ClssfctnTp": "CFICode",
    "FinInstrmGnlAttrbts_NtnlCcy": "Currency",
    "FinInstrmGnlAttrbts_CmmdtyDerivInd": "ComdtyDerInd",
    "Issr": "IssuerLEI",
    "TradgVnRltdAttrbts_Id": "TradingVenueId",
    "TradgVnRltdAttrbts_IssrReq": "IssuerReq",
    "TradgVnRltdAttrbts_FrstTradDt": "FirstTradeDate",
    "TechAttrbts_RlvntCmptntAuthrty": "RlvntCmptntAuthrty",
    "TechAttrbts_RlvntTradgVn": "RelevantTradingVenue",
    "PblctnPrd_FrDt": "FromDate",
    "TradgVnRltdAttrbts_TermntnDt": "TerminationDate",
    
    # New debt-specific fields
    "DebtInstrmAttrbts_TtlIssdNmnlAmt": "TotalIssuedNominalAmount",
    "DebtInstrmAttrbts_MtrtyDt": "MaturityDate",
    "DebtInstrmAttrbts_NmnlValPerUnit": "NominalValuePerUnit",
    "DebtInstrmAttrbts_IntrstRate_Fxd": "FixedInterestRate",
    "DebtInstrmAttrbts_DebtSnrty": "DebtSeniority"
}

def create_tables(cursor):
    # Base instrument reference data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instruments (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            symbol TEXT,
            isin TEXT,
            name TEXT,
            lei_id TEXT,
            additional_data JSON,
            last_updated TIMESTAMP,
            FOREIGN KEY (lei_id) REFERENCES legal_entities(lei),
            UNIQUE (isin),
            UNIQUE (symbol)
        )
    ''')
    
    # Legal entities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS legal_entities (
            lei TEXT PRIMARY KEY,
            legal_name TEXT,
            legal_jurisdiction TEXT,
            legal_form_id TEXT,
            registered_as TEXT,
            category TEXT,
            status TEXT,
            bic TEXT,
            mic TEXT,
            creation_date TIMESTAMP
        )
    ''')

    # Equity specific data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equities (
            instrument_id TEXT PRIMARY KEY,
            shares_outstanding REAL,
            market_cap REAL,
            exchange TEXT,
            sector TEXT,
            industry TEXT,
            FOREIGN KEY (instrument_id) REFERENCES instruments(id)
        )
    ''')

    # Debt specific data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS debts (
            instrument_id TEXT PRIMARY KEY,
            maturity_date DATE,
            coupon_rate REAL,
            face_value REAL,
            coupon_frequency TEXT,
            credit_rating TEXT,
            FOREIGN KEY (instrument_id) REFERENCES instruments(id)
        )
    ''')

    # Create indexes for common queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_instruments_type ON instruments(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_instruments_lei ON instruments(lei_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_equities_sector ON equities(sector)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_debts_maturity ON debts(maturity_date)')

def create_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    conn.close()

def map_fields(data, field_mapping):
    # Create a new dictionary with only the mapped fields
    mapped_data = {}
    
    for raw_tag, mapped_field in field_mapping.items():
        if raw_tag in data:
            mapped_data[mapped_field] = data[raw_tag]
    
    return mapped_data

def create_db_table(db_name):
    """
    Create SQLite tables for storing the extracted XML elements and OpenFIGI data,
    only if the tables don't already exist.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        create_tables(cursor)
        conn.commit()
        print("Tables created successfully")
        
        # Verify tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Existing tables:", [table[0] for table in tables])
        
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        raise
    finally:
        conn.close()

def insert_into_db(mapped_data, instrument_type="equity"):
    """
    Insert data into the appropriate FIRDS table based on instrument type.
    
    Args:
        mapped_data (dict): Dictionary containing the mapped data to insert
        instrument_type (str): Type of instrument ('equity' or 'debt')
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Determine which table to use
    table_name = "firds_e" if instrument_type == "equity" else "firds_d"
    
    # Get the appropriate field mapping
    field_mapping = FIELD_MAPPING if instrument_type == "equity" else DEBT_FIELD_MAPPING
    
    # Create the insert query based on the field mapping
    columns = list(field_mapping.values())
    placeholders = ','.join(['?' for _ in columns])
    insert_query = f"""INSERT INTO {table_name} (
        {', '.join(columns)}
    ) VALUES ({placeholders})"""

    # Extract values from the mapped_data dictionary in the correct order
    values = []
    for column in columns:
        value = mapped_data.get(column)
        # Convert boolean strings to actual booleans
        if column in ['ComdtyDerInd', 'IssuerReq']:
            value = value.lower() == 'true' if value else False
        values.append(value)
    
    try:
        cursor.execute(insert_query, tuple(values))
        conn.commit()
        print(f"Successfully inserted data into {table_name}")
    except sqlite3.Error as e:
        print(f"Error inserting data into {table_name}: {e}")
        raise
    finally:
        conn.close()

def fetch_all_data(db_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query to select all rows from your table
    cursor.execute("SELECT * FROM firds_e")

    # Fetch column names
    columns = [description[0] for description in cursor.description]

    # Print the column names (header)
    print(f"{' | '.join(columns)}")

    # Print a separator line for clarity
    print('-' * (len(' | '.join(columns))))

    # Fetch all rows and print them
    rows = cursor.fetchall()
    for row in rows:
        print(f"{' | '.join(str(cell) for cell in row)}")

    # Close the connection
    conn.close()
    
def check_table_columns(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(firds_e);")  # Get table structure
    columns = cursor.fetchall()  # Fetch all column details

    print("\nTable 'firds_e' Columns:")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")  # col[1] = column name, col[2] = data type

    conn.close()
    
def insert_figi_data(figi_data):
    """
    Insert or update FIGI data for an ISIN.
    
    Args:
        figi_data (dict): Dictionary containing FIGI data with the following keys:
            - ISIN: The ISIN identifier
            - FIGI: The FIGI identifier
            - CompositeFIGI: The composite FIGI
            - ShareClassFIGI: The share class FIGI
            - Ticker: The instrument's ticker symbol
            - SecurityType: The security type
            - MarketSector: The market sector
            - SecurityDescription: Additional security description
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if isin_figi_map table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='isin_figi_map'")
        if not cursor.fetchone():
            print("Creating isin_figi_map table...")
            cursor.execute(CREATE_OPENFIGI_TABLE)
            conn.commit()

        # Check if FIGI data already exists for this ISIN
        cursor.execute("SELECT ISIN FROM isin_figi_map WHERE ISIN = ?", (figi_data['ISIN'],))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update existing record
            update_query = """UPDATE isin_figi_map 
                             SET FIGI = ?, CompositeFIGI = ?, ShareClassFIGI = ?, 
                                 Ticker = ?, SecurityType = ?, MarketSector = ?, 
                                 SecurityDescription = ?, LastUpdated = CURRENT_TIMESTAMP
                             WHERE ISIN = ?"""
            values = (
                figi_data.get('FIGI'),
                figi_data.get('CompositeFIGI'),
                figi_data.get('ShareClassFIGI'),
                figi_data.get('Ticker'),
                figi_data.get('SecurityType'),
                figi_data.get('MarketSector'),
                figi_data.get('SecurityDescription'),
                figi_data['ISIN']
            )
            cursor.execute(update_query, values)
        else:
            # Insert new record
            insert_query = """INSERT INTO isin_figi_map 
                             (ISIN, FIGI, CompositeFIGI, ShareClassFIGI, Ticker,
                              SecurityType, MarketSector, SecurityDescription)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            values = (
                figi_data['ISIN'],
                figi_data.get('FIGI'),
                figi_data.get('CompositeFIGI'),
                figi_data.get('ShareClassFIGI'),
                figi_data.get('Ticker'),
                figi_data.get('SecurityType'),
                figi_data.get('MarketSector'),
                figi_data.get('SecurityDescription')
            )
            cursor.execute(insert_query, values)

        conn.commit()
        print(f"FIGI data for ISIN {figi_data['ISIN']} successfully stored")
        
    except Exception as e:
        print(f"Error storing FIGI data: {str(e)}")
        raise
    finally:
        conn.close()

def get_figi_data(isin):
    """
    Retrieve FIGI data for a given ISIN.
    
    Args:
        isin (str): The ISIN identifier
        
    Returns:
        dict: Dictionary containing FIGI data if found, None otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM isin_figi_map WHERE ISIN = ?", (isin,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))
    return None

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database and create tables for GLEIF data
def create_gleif_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS gleif_lei_records (
        lei TEXT PRIMARY KEY,
        legalName TEXT,
        legalJurisdiction TEXT,
        legalFormId TEXT,
        registeredAs TEXT,
        category TEXT,
        subCategory TEXT,
        status TEXT,
        bic TEXT,
        mic TEXT,
        ocid TEXT,
        qcc TEXT,
        conformityFlag TEXT,
        spglobal TEXT,
        associatedEntityLei TEXT,
        associatedEntityName TEXT,
        successorEntityLei TEXT,
        successorEntityName TEXT,
        creationDate TEXT
    );

    CREATE TABLE IF NOT EXISTS gleif_addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lei TEXT,
        type TEXT CHECK(type IN ('legal', 'headquarters')),
        language TEXT,
        addressLines TEXT,
        city TEXT,
        region TEXT,
        country TEXT,
        postalCode TEXT,
        FOREIGN KEY (lei) REFERENCES gleif_lei_records(lei)
    );

    CREATE TABLE IF NOT EXISTS gleif_registration (
        lei TEXT PRIMARY KEY,
        initialRegistrationDate TEXT,
        lastUpdateDate TEXT,
        status TEXT,
        nextRenewalDate TEXT,
        managingLou TEXT,
        corroborationLevel TEXT,
        validatedAt TEXT,
        validatedAs TEXT,
        FOREIGN KEY (lei) REFERENCES gleif_lei_records(lei)
    );

    CREATE TABLE IF NOT EXISTS gleif_meta_info (
        lei TEXT PRIMARY KEY,
        publishDate TEXT,
        FOREIGN KEY (lei) REFERENCES gleif_lei_records(lei)
    );
    """)

    conn.commit()
# Function to insert LEI data into the database from GLEIF
def insert_lei_data(data: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert into gleif_lei_records
    cursor.execute("""
        INSERT OR REPLACE INTO gleif_lei_records (
            lei, legalName, legalJurisdiction, legalFormId, registeredAs,
            category, subCategory, status, bic, mic, ocid, qcc, conformityFlag,
            spglobal, associatedEntityLei, associatedEntityName,
            successorEntityLei, successorEntityName, creationDate
        ) VALUES (
            :lei, :legalName, :legalJurisdiction, :legalFormId, :registeredAs,
            :category, :subCategory, :status, :bic, :mic, :ocid, :qcc, :conformityFlag,
            :spglobal, :associatedEntityLei, :associatedEntityName,
            :successorEntityLei, :successorEntityName, :creationDate
        )
    """, data["leiRecord"])

    # Insert addresses
    for address in data["addresses"]:
        cursor.execute("""
            INSERT INTO gleif_addresses (
                lei, type, language, addressLines, city, region, country, postalCode
            ) VALUES (
                :lei, :type, :language, :addressLines, :city, :region, :country, :postalCode
            )
        """, address)

    # Insert registration
    cursor.execute("""
        INSERT OR REPLACE INTO gleif_registration (
            lei, initialRegistrationDate, lastUpdateDate, status,
            nextRenewalDate, managingLou, corroborationLevel,
            validatedAt, validatedAs
        ) VALUES (
            :lei, :initialRegistrationDate, :lastUpdateDate, :status,
            :nextRenewalDate, :managingLou, :corroborationLevel,
            :validatedAt, :validatedAs
        )
    """, data["registration"])

    # Insert meta info
    cursor.execute("""
        INSERT OR REPLACE INTO gleif_meta_info (
            lei, publishDate
        ) VALUES (
            :lei, :publishDate
        )
    """, data["metaInfo"])

    conn.commit()