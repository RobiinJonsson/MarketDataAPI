#!/usr/bin/env python3
"""
Database Schema Analysis Tool

This script provides detailed analysis of your database schema,
useful for monitoring, debugging, and understanding your data structure.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 Database Schema Analysis")
print("=" * 40)

try:
    from marketdata_api.database.base import engine
    from marketdata_api.database.schema_detector import schema_analyzer
    from marketdata_api.config import DATABASE_TYPE, AZURE_SQL_SERVER, AZURE_SQL_DATABASE
    from sqlalchemy import text
    
    print(f"Database: {DATABASE_TYPE}")
    if DATABASE_TYPE.lower() == "azure_sql":
        print(f"Server: {AZURE_SQL_SERVER}")
        print(f"Database: {AZURE_SQL_DATABASE}")
    
    # Run schema analysis
    schema_info = schema_analyzer.analyze_schema()
    
    if 'error' in schema_info:
        print(f"\n❌ Analysis failed: {schema_info['error']}")
        sys.exit(1)
    
    print(f"\n📊 Schema Overview:")
    print(f"  Tables: {schema_info['table_count']}")
    print(f"  Migration Level: {schema_info.get('migration_level', 'Not tracked')}")
    print(f"  Fully Migrated: {'✅' if schema_info.get('is_fully_migrated') else '❌'}")
    
    print(f"\n🔧 Features:")
    features = {
        'Transparency Calculations': schema_info.get('has_transparency', False),
        'Entity Relationships': schema_info.get('has_entity_relationships', False),
        'Related ISINs': schema_info.get('has_related_isins', False),
        'FIGI Mappings': schema_info.get('has_figi_mappings', False)
    }
    
    for feature, available in features.items():
        status = "✅" if available else "❌"
        print(f"  {status} {feature}")
    
    # Detailed table analysis
    print(f"\n� Table Details:")
    print("-" * 60)
    
    key_tables = ['instruments', 'equities', 'debts', 'legal_entities', 
                  'transparency_calculations', 'entity_relationships']
    
    for table in sorted(schema_info['tables']):
        table_info = schema_analyzer.get_table_info(table)
        
        if 'error' in table_info:
            print(f"  ⚠️  {table}: {table_info['error']}")
            continue
        
        icon = "🔑" if table in key_tables else "📄"
        print(f"  {icon} {table}")
        print(f"     Columns: {table_info['column_count']}")
        print(f"     Records: {table_info['row_count']}")
        
        # Show first few columns for key tables
        if table in key_tables and table_info['column_count'] > 0:
            columns = table_info['columns'][:5]  # First 5 columns
            print(f"     Key columns: {', '.join(columns)}")
            if table_info['column_count'] > 5:
                print(f"     ... and {table_info['column_count'] - 5} more")
        print()
    
    print("=" * 40)
    print("✅ Schema analysis completed!")
    
except Exception as e:
    print(f"\n❌ Analysis failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
