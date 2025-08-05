#!/usr/bin/env python3

import pandas as pd
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath('.'))

def get_sample_isins():
    """Get sample ISINs from each file type for testing"""
    firds_path = "downloads/firds/"
    
    files = {
        'equity': 'FULINS_E_20250712_01of02_firds_data.csv',
        'corporate': 'FULINS_C_20250712_01of01_firds_data.csv'
    }
    
    samples = {}
    
    for file_type, filename in files.items():
        try:
            print(f"\nAnalyzing {file_type} file: {filename}")
            df = pd.read_csv(f"{firds_path}{filename}", dtype=str)
            print(f"  Shape: {df.shape}")
            
            # Get European ISINs (country codes)
            eu_countries = ['DE', 'FR', 'NL', 'IT', 'ES', 'BE', 'AT', 'IE', 'PT', 'FI', 'GR', 'SE', 'DK', 'NO']
            eu_isins = df[df['Id'].str.startswith(tuple(eu_countries), na=False)]
            
            print(f"  European ISINs: {len(eu_isins)}")
            
            if len(eu_isins) > 0:
                # Get first few samples
                for i in range(min(3, len(eu_isins))):
                    sample = eu_isins.iloc[i]
                    isin = sample['Id']
                    name = sample.get('FinInstrmGnlAttrbts_FullNm', 'Unknown')
                    cfi_type = sample.get('FinInstrmGnlAttrbts_ClssfctnTp', 'Unknown')
                    
                    print(f"    Sample {i+1}: {isin} - {name[:50]}... (CFI: {cfi_type})")
                    
                    if i == 0:  # Store first sample for testing
                        samples[file_type] = {
                            'isin': isin,
                            'name': name,
                            'cfi_type': cfi_type
                        }
            
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    return samples

if __name__ == "__main__":
    print("Getting sample ISINs for testing...")
    samples = get_sample_isins()
    
    print(f"\n=== TEST SAMPLES ===")
    for file_type, data in samples.items():
        print(f"{file_type.upper()}:")
        print(f"  ISIN: {data['isin']}")
        print(f"  Name: {data['name']}")
        print(f"  CFI: {data['cfi_type']}")
        print()
