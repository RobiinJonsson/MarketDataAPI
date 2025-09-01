#!/usr/bin/env python3
"""
FIRDS File Analysis Script

Analyzes all FIRDS CSV files to understand column structures and data patterns
for expanding the ESMA instrument model to support all instrument types.

FIRDS = Financial Instruments Reference Data System
Contains reference data for instruments (C,D,E,F,H,I,J,S,R,O types)

This script will:
1. Read all FIRDS CSV files in downloads/firds/
2. Extract column names and first 5 rows from each file
3. Identify patterns and differences between instrument types
4. Generate a comprehensive markdown report for model design decisions
"""

import os
import csv
import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter
import json
from typing import Dict, List, Any, Optional
import re


class FirdsAnalyzer:
    """Analyzes FIRDS files to understand instrument reference data structure and patterns."""
    
    def __init__(self, firds_directory: str):
        self.firds_directory = Path(firds_directory)
        self.analysis_results = {}
        self.column_patterns = defaultdict(set)
        self.data_type_patterns = defaultdict(dict)
        self.instrument_types = set()  # Changed from transparency_types
        
    def analyze_all_files(self) -> Dict[str, Any]:
        """Analyze all FIRDS CSV files in the directory."""
        
        if not self.firds_directory.exists():
            raise FileNotFoundError(f"FIRDS directory not found: {self.firds_directory}")
        
        csv_files = list(self.firds_directory.glob("*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in: {self.firds_directory}")
        
        print(f"Found {len(csv_files)} FIRDS CSV files to analyze...")
        
        for csv_file in sorted(csv_files):
            print(f"Analyzing: {csv_file.name}")
            try:
                self._analyze_single_file(csv_file)
            except Exception as e:
                print(f"Error analyzing {csv_file.name}: {e}")
                self.analysis_results[csv_file.name] = {
                    'error': str(e),
                    'instrument_type': self._extract_instrument_type(csv_file.name)
                }
        
        # Generate summary patterns
        self._analyze_patterns()
        
        return self.analysis_results
    
    def _analyze_single_file(self, csv_file: Path) -> None:
        """Analyze a single FIRDS CSV file."""
        
        instrument_type = self._extract_instrument_type(csv_file.name)
        self.instrument_types.add(instrument_type)
        
        # Read file with pandas for better handling of various CSV formats
        try:
            # Try reading with different encodings and separators
            df = None
            for encoding in ['utf-8', 'iso-8859-1', 'cp1252']:
                for sep in [',', ';', '\t']:
                    try:
                        df = pd.read_csv(csv_file, encoding=encoding, sep=sep, low_memory=False)
                        if len(df.columns) > 1:  # Found proper separator
                            break
                    except:
                        continue
                if df is not None and len(df.columns) > 1:
                    break
            
            if df is None or len(df.columns) <= 1:
                raise ValueError("Could not parse CSV with any encoding/separator combination")
            
        except Exception as e:
            raise Exception(f"Failed to read CSV: {e}")
        
        # Store analysis results
        file_analysis = {
            'file_name': csv_file.name,
            'instrument_type': instrument_type,  # Changed from transparency_type
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'sample_data': [],
            'data_types': {},
            'null_counts': {},
            'unique_counts': {},
            'sample_values': {}
        }
        
        # Get first 5 rows for inspection
        sample_rows = df.head(5)
        for idx, row in sample_rows.iterrows():
            sample_row = {}
            for col in df.columns:
                value = row[col]
                # Convert pandas types to JSON-serializable types
                if pd.isna(value):
                    sample_row[col] = None
                elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                    sample_row[col] = str(value)
                elif isinstance(value, (pd.Int64Dtype, pd.Float64Dtype)):
                    sample_row[col] = value.item() if not pd.isna(value) else None
                else:
                    sample_row[col] = str(value) if value is not None else None
            file_analysis['sample_data'].append(sample_row)
        
        # Analyze data types and patterns
        for col in df.columns:
            # Track column names across instrument types
            self.column_patterns[instrument_type].add(col)
            
            # Basic data type analysis
            dtype_str = str(df[col].dtype)
            file_analysis['data_types'][col] = dtype_str
            
            # Null count analysis
            null_count = df[col].isnull().sum()
            file_analysis['null_counts'][col] = int(null_count)
            
            # Unique value count (for small datasets)
            if len(df) < 10000:  # Only for smaller files to avoid memory issues
                unique_count = df[col].nunique()
                file_analysis['unique_counts'][col] = int(unique_count)
                
                # Sample unique values for categorical-looking columns
                if unique_count < 50 and unique_count > 1:
                    sample_vals = df[col].dropna().unique()[:10]
                    file_analysis['sample_values'][col] = [str(val) for val in sample_vals]
            
            # Track data type patterns across files
            if instrument_type not in self.data_type_patterns:
                self.data_type_patterns[instrument_type] = {}
            self.data_type_patterns[instrument_type][col] = dtype_str
        
        self.analysis_results[csv_file.name] = file_analysis
    
    def _extract_instrument_type(self, filename: str) -> str:
        """Extract instrument type from filename (C, D, E, F, etc.)."""
        match = re.search(r'FULINS_([A-Z])_', filename)
        return match.group(1) if match else 'UNKNOWN'
    
    def _analyze_patterns(self) -> None:
        """Analyze patterns across all files."""
        
        # Find common columns across all instrument types
        all_columns = set()
        for cols in self.column_patterns.values():
            all_columns.update(cols)
        
        common_columns = set(all_columns)
        for cols in self.column_patterns.values():
            common_columns = common_columns.intersection(cols)
        
        # Find type-specific columns
        type_specific_columns = {}
        for instrument_type, cols in self.column_patterns.items():
            type_specific = cols - common_columns
            if type_specific:
                type_specific_columns[instrument_type] = list(type_specific)
        
        # Store pattern analysis
        self.analysis_results['_PATTERN_ANALYSIS'] = {
            'instrument_types_found': sorted(list(self.instrument_types)),
            'total_unique_columns': len(all_columns),
            'common_columns': sorted(list(common_columns)),
            'common_column_count': len(common_columns),
            'type_specific_columns': type_specific_columns,
            'column_patterns_by_type': {k: sorted(list(v)) for k, v in self.column_patterns.items()}
        }


def generate_markdown_report(analysis_results: Dict[str, Any], output_file: str) -> None:
    """Generate a comprehensive markdown report from analysis results."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# FIRDS Files Analysis Report\n\n")
        f.write("**Financial Instruments Reference Data System (FIRDS) Analysis**\n\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("This report analyzes FIRDS CSV files containing instrument reference data for different instrument types (C, D, E, F, H, I, J, S, R, O).\n\n")
        
        # Executive Summary
        if '_PATTERN_ANALYSIS' in analysis_results:
            patterns = analysis_results['_PATTERN_ANALYSIS']
            
            f.write("## Executive Summary\n\n")
            f.write(f"- **Instrument Types Found**: {', '.join(patterns['instrument_types_found'])}\n")
            f.write(f"- **Total Files Analyzed**: {len([k for k in analysis_results.keys() if not k.startswith('_')])}\n")
            f.write(f"- **Total Unique Columns**: {patterns['total_unique_columns']}\n")
            f.write(f"- **Common Columns Across All Types**: {patterns['common_column_count']}\n\n")
        
        # File-by-File Analysis
        f.write("## File-by-File Analysis\n\n")
        
        for filename, analysis in analysis_results.items():
            if filename.startswith('_'):  # Skip pattern analysis
                continue
                
            if 'error' in analysis:
                f.write(f"### ❌ {filename} (ERROR)\n\n")
                f.write(f"**Error**: {analysis['error']}\n")
                f.write(f"**Instrument Type**: {analysis.get('instrument_type', 'UNKNOWN')}\n\n")
                continue
            
            f.write(f"### 📊 {filename}\n\n")
            f.write(f"- **Instrument Type**: {analysis['instrument_type']}\n")
            f.write(f"- **Total Rows**: {analysis['total_rows']:,}\n")
            f.write(f"- **Total Columns**: {analysis['total_columns']}\n\n")
            
            # Columns Table
            f.write("#### Column Structure\n\n")
            f.write("| Column Name | Data Type | Null Count | Unique Count | Sample Values |\n")
            f.write("|-------------|-----------|------------|--------------|---------------|\n")
            
            for col in analysis['columns']:
                data_type = analysis['data_types'].get(col, 'unknown')
                null_count = analysis['null_counts'].get(col, 0)
                unique_count = analysis['unique_counts'].get(col, 'N/A')
                sample_values = analysis['sample_values'].get(col, [])
                
                # Truncate long sample values
                sample_str = ', '.join(sample_values[:5])
                if len(sample_str) > 50:
                    sample_str = sample_str[:47] + "..."
                
                f.write(f"| {col} | {data_type} | {null_count:,} | {unique_count} | {sample_str} |\n")
            
            # Sample Data
            f.write(f"\n#### First 5 Rows Sample\n\n")
            
            if analysis['sample_data']:
                f.write("```json\n")
                for i, row in enumerate(analysis['sample_data'][:5], 1):
                    f.write(f"// Row {i}\n")
                    f.write(json.dumps(row, indent=2, ensure_ascii=False))
                    f.write("\n\n")
                f.write("```\n\n")
            
            f.write("---\n\n")
        
        # Pattern Analysis
        if '_PATTERN_ANALYSIS' in analysis_results:
            patterns = analysis_results['_PATTERN_ANALYSIS']
            
            f.write("## Pattern Analysis\n\n")
            
            # Common Columns
            f.write("### Common Columns (Present in All Types)\n\n")
            if patterns['common_columns']:
                for col in patterns['common_columns']:
                    f.write(f"- `{col}`\n")
            else:
                f.write("*No columns are common across all instrument types.*\n")
            f.write("\n")
            
            # Type-Specific Columns
            f.write("### Type-Specific Columns\n\n")
            for instrument_type in sorted(patterns['instrument_types_found']):
                f.write(f"#### Type {instrument_type} Specific Columns\n\n")
                
                type_columns = patterns['type_specific_columns'].get(instrument_type, [])
                if type_columns:
                    for col in sorted(type_columns):
                        f.write(f"- `{col}`\n")
                else:
                    f.write("*No type-specific columns (all columns are shared with other types).*\n")
                f.write("\n")
            
            # Complete Column Listing by Type
            f.write("### Complete Column Listing by Type\n\n")
            for instrument_type in sorted(patterns['instrument_types_found']):
                columns = patterns['column_patterns_by_type'].get(instrument_type, [])
                f.write(f"#### Type {instrument_type} - All {len(columns)} Columns\n\n")
                f.write("```\n")
                for col in columns:
                    f.write(f"{col}\n")
                f.write("```\n\n")
        
        # Model Design Recommendations
        f.write("## Model Design Recommendations\n\n")
        f.write("### Current Instrument Model Analysis\n\n")
        f.write("The current `Instrument` model uses a unified approach with:\n\n")
        f.write("- **Core identification fields**: `id`, `isin`, `instrument_type`\n")
        f.write("- **Essential common fields**: `full_name`, `short_name`, `currency`, `cfi_code`, `lei_id`\n")
        f.write("- **JSON document storage**: `firds_data`, `processed_attributes`\n")
        f.write("- **Type-specific formatting**: Methods for equity, debt, future attributes\n\n")
        
        f.write("### Recommended Changes Based on Analysis\n\n")
        f.write("Based on the FIRDS reference data analysis above, consider:\n\n")
        f.write("1. **Expand instrument_type values** to handle all FIRDS instrument types (C, D, E, F, H, I, J, S, R, O)\n")
        f.write("2. **Review common columns** - these should be promoted to dedicated database columns for better performance\n")
        f.write("3. **Update type-specific formatters** - add methods for each instrument type found in FIRDS\n")
        f.write("4. **Consider data type mappings** - ensure proper handling of dates, numbers, text fields, etc.\n")
        f.write("5. **Update service layer** - modify FIRDS parsing logic to handle all instrument types\n")
        f.write("6. **Map FIRDS types to business logic** - determine how each FIRDS type maps to internal instrument categories\n\n")
        
        f.write("### Next Steps\n\n")
        f.write("1. Review this analysis report\n")
        f.write("2. Identify which columns should become dedicated database fields vs JSON storage\n")
        f.write("3. Plan the mapping from FIRDS instrument types to internal instrument_type values\n")
        f.write("4. Update the instrument model, service layer, and routes accordingly\n")
        f.write("5. Test data ingestion for all FIRDS instrument types\n\n")


def main():
    """Main execution function."""
    
    # Configuration
    firds_dir = r"c:\Users\robin\Projects\MarketDataAPI\downloads\firds"
    output_file = r"c:\Users\robin\Projects\MarketDataAPI\docs\firds_analysis_report.md"
    
    try:
        print("🔍 Starting FIRDS File Analysis...")
        print(f"📂 Analyzing files in: {firds_dir}")
        print(f"📝 Report will be saved to: {output_file}")
        print()
        
        # Create analyzer and run analysis
        analyzer = FirdsAnalyzer(firds_dir)
        results = analyzer.analyze_all_files()
        
        print()
        print("📊 Generating markdown report...")
        
        # Generate report
        generate_markdown_report(results, output_file)
        
        print(f"✅ Analysis complete! Report saved to: {output_file}")
        print()
        print("📋 Summary:")
        if '_PATTERN_ANALYSIS' in results:
            patterns = results['_PATTERN_ANALYSIS']
            print(f"   - Instrument types found: {', '.join(patterns['instrument_types_found'])}")
            print(f"   - Total files analyzed: {len([k for k in results.keys() if not k.startswith('_')])}")
            print(f"   - Total unique columns: {patterns['total_unique_columns']}")
            print(f"   - Common columns: {patterns['common_column_count']}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
