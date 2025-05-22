import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add the parent directory of 'marketdata_api' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketdata_api.services.instrument_service import InstrumentService
from marketdata_api.services.legal_entity_service import LegalEntityService
from marketdata_api.database.session import get_session
from marketdata_api.database.base import Base
from sqlalchemy import inspect
from marketdata_api.models.utils.cfi import CFI

def list_tables():
    """List all tables in the database with their columns."""
    with get_session() as session:
        inspector = inspect(session.bind)
        
        for table_name in inspector.get_table_names():
            print(f"\nTable: {table_name}")
            print("-" * (len(table_name) + 7))
            
            # Use a set to track unique column names
            seen_columns = set()
            columns = inspector.get_columns(table_name)
            
            for column in columns:
                col_name = column['name']
                if col_name not in seen_columns:
                    seen_columns.add(col_name)
                    nullable = "" if column.get('nullable', True) else "NOT NULL"
                    default = f"DEFAULT {column.get('default')}" if column.get('default') is not None else ""
                    print(f"  {col_name} ({column['type']}) {nullable} {default}".strip())
            
            # Show primary keys
            pk = inspector.get_pk_constraint(table_name)
            if pk['constrained_columns']:
                print(f"\n  Primary Key: {', '.join(pk['constrained_columns'])}")
            
            # Show foreign keys
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                print("\n  Foreign Keys:")
                for fk in fks:
                    print(f"    {', '.join(fk['constrained_columns'])} -> {fk['referred_table']}.{', '.join(fk['referred_columns'])}")

def print_instrument_detail(instrument):
    """Print detailed instrument information including relationships."""
    print("\n=== Instrument Details ===")
    # Print all non-empty fields from the instrument (excluding SQLAlchemy internals and relationships)
    exclude_fields = {'_sa_instance_state', 'legal_entity', 'figi_mapping', 'related_isins'}
    attrs = vars(instrument)
    for key, value in attrs.items():
        if key in exclude_fields:
            continue
        if value is not None and value != "" and value != [] and value != {}:
            print(f"{key}: {value}")

    # Print type-specific fields dynamically (fields defined on the subclass, not base)
    model_cls = type(instrument)
    base_cls = instrument.__class__.__bases__[0]
    # Get only subclass-specific columns (not inherited from Instrument)
    if hasattr(model_cls, '__table__') and hasattr(base_cls, '__table__'):
        base_cols = set(c.name for c in base_cls.__table__.columns)
        sub_cols = set(c.name for c in model_cls.__table__.columns)
        type_specific = sub_cols - base_cols
        if type_specific:
            print(f"\n=== {instrument.type.capitalize()} Specific Fields ===")
            for field in type_specific:
                value = getattr(instrument, field, None)
                if value not in (None, "", [], {}):
                    print(f"{field}: {value}")

    # Print relationships if present
    if getattr(instrument, 'figi_mapping', None):
        print("\n=== FIGI Data ===")
        figi = instrument.figi_mapping
        for key, value in vars(figi).items():
            if key != '_sa_instance_state' and value is not None:
                print(f"{key}: {value}")

    if getattr(instrument, 'legal_entity', None):
        print("\n=== Legal Entity Data ===")
        entity = instrument.legal_entity
        for key, value in vars(entity).items():
            if key != '_sa_instance_state' and value is not None:
                print(f"{key}: {value}")
        if getattr(entity, 'addresses', None):
            print("\nAddresses:")
            for addr in entity.addresses:
                for k, v in vars(addr).items():
                    if k != '_sa_instance_state' and v is not None:
                        print(f"  {k}: {v}")
        if getattr(entity, 'registration', None):
            print("\nRegistration Details:")
            reg = entity.registration
            for k, v in vars(reg).items():
                if k != '_sa_instance_state' and v is not None:
                    print(f"  {k}: {v}")

    # Print related ISINs if present
    if getattr(instrument, 'related_isins', None):
        print("\nRelated ISINs:")
        for rel in instrument.related_isins:
            for k, v in vars(rel).items():
                if k != '_sa_instance_state' and v is not None:
                    print(f"  {k}: {v}")

def instrument_operations():
    """Handle instrument CRUD operations."""
    service = InstrumentService()
    
    if len(sys.argv) < 3:
        print("Usage: python scripts/cli.py instrument <command> [args]")
        print("Commands:")
        print("  get <id/isin>                     - Get basic instrument info")
        print("  create-ext <type> <isin>          - Create instrument from external source")
        print("  create-int <type> <data>          - Create instrument from provided data")
        print("  update <id> <data>                - Update existing instrument")
        print("  delete <id/isin>                  - Delete instrument")
        print("  enrich <id>                       - Enrich with FIGI and LEI data")
        print("  list                              - List all instruments")
        print("  detail <isin>                     - Show detailed instrument info")
        return

    command = sys.argv[2]
    
    try:
        if command == "get" and len(sys.argv) == 4:
            session, instrument = service.get_instrument(sys.argv[3])
            if instrument:
                print(f"Found instrument: {instrument.__dict__}")
            else:
                print("Instrument not found")
            session.close()
            
        elif command == "create-ext" and len(sys.argv) == 5:
            # Create from external source (FIRDS)
            instrument_type = sys.argv[3]
            isin = sys.argv[4]
            instrument = service.get_or_create_instrument(isin, instrument_type)
            if instrument:
                print(f"Created/Retrieved instrument from external source: {instrument.__dict__}")
            else:
                print(f"Failed to create/retrieve instrument: {isin}")
            
        elif command == "create-int" and len(sys.argv) >= 4:
            # Create directly with provided data
            instrument_type = sys.argv[3]
            data = eval(" ".join(sys.argv[4:]))  # Be careful with eval in production!
            instrument = service.create_instrument(data, instrument_type)
            print(f"Created instrument directly: {instrument.__dict__}")
            
        elif command == "update" and len(sys.argv) >= 4:
            identifier = sys.argv[3]
            data = eval(" ".join(sys.argv[4:]))  # Be careful with eval in production!
            instrument = service.update_instrument(identifier, data)
            if instrument:
                print(f"Updated instrument: {instrument.__dict__}")
            else:
                print("Instrument not found")
                
        elif command == "delete" and len(sys.argv) == 4:
            identifier = sys.argv[3]
            if service.delete_instrument(identifier):
                print(f"Successfully deleted instrument: {identifier}")
            else:
                print(f"Instrument not found: {identifier}")
                
        elif command == "enrich" and len(sys.argv) == 4:
            session, instrument = service.get_instrument(sys.argv[3])
            if instrument:
                print(f"Enriching {instrument.isin}...")
                print("- Current state:")
                print(f"  FIGI: {'Present' if instrument.figi_mapping else 'Missing'}")
                print(f"  Legal Entity: {'Present' if instrument.legal_entity else 'Missing'}")
                
                session, enriched = service.enrich_instrument(instrument)
                
                print("\n- After enrichment:")
                print(f"  FIGI: {'Present' if enriched.figi_mapping else 'Missing'}")
                print(f"  Legal Entity: {'Present' if enriched.legal_entity else 'Missing'}")
                
                if enriched.legal_entity:
                    print(f"\nLinked Legal Entity:")
                    print(f"  Name: {enriched.legal_entity.name}")
                    print(f"  LEI: {enriched.legal_entity.lei}")
            else:
                print("Instrument not found")
            session.close()
            
        elif command == "list":
            from marketdata_api.models.instrument import Instrument
            with get_session() as session:
                instruments = session.query(Instrument).all()
                for inst in instruments:
                    print(f"{inst.id}: {inst.isin} - {inst.type}")
                    
        elif command == "detail" and len(sys.argv) == 4:
            session, instrument = service.get_instrument(sys.argv[3])
            if instrument:
                print_instrument_detail(instrument)
            else:
                print("Instrument not found")
            session.close()
            
    except Exception as e:
        print(f"Error: {str(e)}")

def entity_operations():
    """Handle legal entity CRUD operations."""
    service = LegalEntityService()
    
    if len(sys.argv) < 3:
        print("Usage: python scripts/cli.py entity <command> [args]")
        print("Commands: get <lei>, create <lei>, update <lei>, delete <lei>, list")
        return

    command = sys.argv[2]
    
    try:
        if command == "get" and len(sys.argv) == 4:
            session, entity = service.get_entity(sys.argv[3])
            if entity:
                print(f"Found entity: {entity.__dict__}")
            else:
                print("Entity not found")
            session.close()
            
        elif command in ["create", "update"] and len(sys.argv) == 4:
            session, entity = service.create_or_update_entity(sys.argv[3])
            if entity:
                print(f"{'Created' if command == 'create' else 'Updated'} entity: {entity.__dict__}")
            else:
                print("Failed to create/update entity")
            session.close()
            
        elif command == "delete" and len(sys.argv) == 4:
            success = service.delete_entity(sys.argv[3])
            print(f"{'Successfully deleted' if success else 'Failed to delete'} entity")
            
        elif command == "list":
            session, entities = service.get_all_entities()
            for entity in entities:
                print(f"{entity.lei}: {entity.name}")
            session.close()
            
    except Exception as e:
        print(f"Error: {str(e)}")

def batch_operations():
    """Handle batch operations for instruments."""
    service = InstrumentService()
    
    if len(sys.argv) < 3:
        print("Usage: python scripts/cli.py batch <command> [args]")
        print("Commands: create, enrich, batch-source, batch-enrich")
        print("Example: python scripts/cli.py batch create docs/isin_test.txt equity")
        print("Example: python scripts/cli.py batch batch-source equity SE")
        print("Example: python scripts/cli.py batch batch-enrich")
        return

    command = sys.argv[2]
    
    try:
        if command == "create":
            file_path = sys.argv[3]
            instrument_type = sys.argv[4] if len(sys.argv) > 4 else "equity"
            
            with open(file_path, 'r') as f:
                identifiers = [line.strip() for line in f if line.strip()]
                
            print(f"Processing {len(identifiers)} instruments...")
            success = failed = 0
                
            for isin in identifiers:
                try:
                    instrument = service.get_or_create_instrument(isin, instrument_type)
                    if instrument:
                        print(f"✓ Processed {isin}")
                        success += 1
                    else:
                        print(f"✗ Failed to process {isin}")
                        failed += 1
                except Exception as e:
                    print(f"✗ Error processing {isin}: {str(e)}")
                    failed += 1
            
            print(f"\nProcessing complete: {success} successful, {failed} failed")
        
        elif command == "enrich":
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
            print(f"Batch enriching all instruments in the database (limit={limit})...")
            count = service.batch_enrich_instrument(limit=limit)
            print(f"Batch enrichment complete: {count} instruments enriched.")
        
        elif command == "batch-source":
            # Usage: python scripts/cli.py batch batch-source <instrument_type> [isin_prefix] [mic_code] [limit]
            instrument_type = sys.argv[3] if len(sys.argv) > 3 else "equity"
            isin_prefix = sys.argv[4] if len(sys.argv) > 4 else None
            mic_code = sys.argv[5] if len(sys.argv) > 5 else None
            limit = int(sys.argv[6]) if len(sys.argv) > 6 else None

            print(f"Batch sourcing instruments from FIRDS: type={instrument_type}, isin_prefix={isin_prefix}, mic_code={mic_code}, limit={limit}")
            instruments = service.batch_source_instrument(
                instrument_type=instrument_type,
                isin_prefix=isin_prefix,
                mic_code=mic_code,
                limit=limit
            )
            print(f"Batch source complete: {len(instruments)} instruments created.")

        elif command == "batch-enrich":
            # Usage: python scripts/cli.py batch batch-enrich [limit]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
            print(f"Batch enriching all instruments in the database (limit={limit})...")
            count = service.batch_enrich_instrument(limit=limit)
            print(f"Batch enrichment complete: {count} instruments enriched.")

    except Exception as e:
        print(f"Error in batch operation: {str(e)}")

def filter_instruments():
    """Filter and list instruments based on criteria."""
    from marketdata_api.models.instrument import Instrument
    
    if len(sys.argv) < 4:
        print("Usage: python scripts/cli.py filter <field> <value>")
        print("Fields: type, currency, trading_venue")
        return
        
    field = sys.argv[2]
    value = sys.argv[3]
    
    with get_session() as session:
        query = session.query(Instrument)
        if hasattr(Instrument, field):
            query = query.filter(getattr(Instrument, field) == value)
        instruments = query.all()
        
        for inst in instruments:
            print(f"{inst.isin}: {inst.full_name} ({inst.type})")

def export_data():
    """Export data to CSV/JSON format."""
    import json
    import csv
    from marketdata_api.models.instrument import Instrument
    
    if len(sys.argv) < 4:
        print("Usage: python scripts/cli.py export <format> <table>")
        print("Formats: csv, json")
        return
        
    export_format = sys.argv[2]
    table = sys.argv[3]
    
    with get_session() as session:
        if table == 'instruments':
            data = session.query(Instrument).all()
            if export_format == 'json':
                result = [{'id': i.id, 'isin': i.isin, 'type': i.type, 
                          'full_name': i.full_name} for i in data]
                with open('instruments.json', 'w') as f:
                    json.dump(result, f, indent=2)
            else:  # csv
                with open('instruments.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['id', 'isin', 'type', 'full_name'])
                    writer.writeheader()
                    for item in data:
                        writer.writerow({'id': item.id, 'isin': item.isin, 
                                       'type': item.type, 'full_name': item.full_name})

def decode_cfi():
    """Decode CFI code and display human-readable description."""
    if len(sys.argv) < 3:
        print("Usage: python scripts/cli.py cfi <code>")
        print("Example: python scripts/cli.py cfi ESVUFR")
        return

    try:
        cfi_code = sys.argv[2].upper()
        cfi = CFI(cfi_code)
        result = cfi.describe()
        
        print("\n=== CFI Code Analysis ===")
        print(f"Code: {result['cfi_code']}")
        print(f"Category: {result['category']} - {result['category_description']}")
        print(f"Group: {result['group']} - {result['group_description']}")
        
        if isinstance(result['attributes'], dict):
            print("\nAttributes:")
            for key, value in result['attributes'].items():
                print(f"  {key}: {value}")
        else:
            print(f"\nAttributes: {result['attributes']}")
            
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error decoding CFI code: {str(e)}")

def print_usage():
    print("""
Market Data API CLI Tool
=======================

Basic Commands:
    tables                              - List all database tables with schema
    instrument <command>                - Instrument operations
    entity <command>                    - Legal entity operations
    batch <command> <file>             - Batch process instruments
    batch batch-source <type> [prefix] [mic] [limit] - Batch source from FIRDS (e.g. equity SE)
    batch batch-enrich [limit]          - Batch enrich all instruments in DB
    filter <field> <value>             - Filter instruments by field
    export <format> <table>            - Export data to CSV/JSON
    cfi <code>                         - Decode CFI code

Instrument Commands:
    get <id/isin>                      - Get basic instrument info
    create-ext <type> <isin>           - Create instrument from external source (FIRDS)
    create-int <type> <data>           - Create instrument from provided data
    update <id> <data>                 - Update existing instrument
    delete <id/isin>                   - Delete instrument by ID or ISIN
    enrich <id>                        - Enrich with FIGI and LEI data
    list                               - List all instruments

Entity Commands:
    get <lei>                          - Get legal entity info
    create <lei>                       - Create new entity from GLEIF API
    update <lei>                       - Update entity from GLEIF API
    delete <lei>                       - Delete legal entity
    list                               - List all legal entities

Batch Operations:
    batch create <file> [type]         - Create instruments from file (default: equity)
    batch enrich <file>                - Enrich instruments from file with FIGI/LEI
    batch batch-source <type> [prefix] [mic] [limit] - Source from FIRDS by ISIN prefix/MIC
    batch batch-enrich [limit]          - Enrich all instruments in DB

Export Commands:
    export json instruments            - Export instruments to JSON
    export csv instruments             - Export instruments to CSV

Examples:
    python scripts/cli.py instrument detail DE000A1EWWW0
    python scripts/cli.py batch create futures.txt future
    python scripts/cli.py entity create 549300PPETP6IPXYTE40
    python scripts/cli.py filter type equity
    python scripts/cli.py cfi ESVUFR
    python scripts/cli.py batch batch-source equity SE
    python scripts/cli.py batch batch-enrich
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    
    if command == "tables":
        list_tables()
    elif command == "instrument":
        instrument_operations()
    elif command == "entity":
        entity_operations()
    elif command == "batch":
        batch_operations()
    elif command == "filter":
        filter_instruments()
    elif command == "export":
        export_data()
    elif command == "cfi":
        decode_cfi()
    else:
        print("Invalid command")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
