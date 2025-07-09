"""
ESMA FITRS Data Download Example Script

Download and analyze FITRS (Financial Instruments Transparency System) data from ESMA.
This script allows you to specify dates and instrument types for downloading FITRS data.
"""

import os
import sys
# Fix the path to go up to project root and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from marketdata_api.services.esma_data_loader import EsmaDataLoader
from marketdata_api.services.esma_utils import Cfi
import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - modify these as needed
START_DATE = '2025-04-26'  # Start date for FITRS data
END_DATE = '2025-04-26'    # End date for FITRS data
CFI_CODE = 'D'             # CFI code: E=Equity, D=Debt, F=Future, etc.
EQUITY_INSTRUMENTS = False # True for equity instruments, False for non-equity
FILE_TYPE = 'Full'         # File type to download
UPDATE_DATA = False        # True to force download, False to use cached

def main():
    """Main function to download and process FITRS data"""
    logger.info("🚀 Starting FITRS data download...")
    logger.info(f"📅 Date range: {START_DATE} to {END_DATE}")
    logger.info(f"📊 CFI Code: {CFI_CODE}")
    logger.info(f"💼 Equity instruments: {EQUITY_INSTRUMENTS}")
    
    # Create FITRS data folder - now in downloads/fitrs/
    project_root = Path(__file__).parent.parent.parent  # Go up to project root
    fitrs_data_folder = project_root / 'downloads' / 'fitrs'
    fitrs_data_folder.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Data will be saved to: {fitrs_data_folder}")
    
    try:
        # Initialize EsmaDataLoader with date range
        edl = EsmaDataLoader(
            creation_date_from=START_DATE,
            creation_date_to=END_DATE,
            limit='10000'
        )
        
        logger.info("📋 Loading FITRS file list...")
        # Load FITRS file list
        file_list = edl.load_mifid_file_list(['fitrs'])
        
        if file_list.empty:
            logger.warning("❌ No FITRS files found for the specified date range")
            return
        
        logger.info(f"✅ Found {len(file_list)} FITRS files")
        
        # Filter for specific file type and instrument type
        fitrs_files = file_list[file_list['file_type'] == FILE_TYPE]
        
        if EQUITY_INSTRUMENTS:
            fitrs_files = fitrs_files[fitrs_files['instrument_type'] == "Equity Instruments"]
        else:
            fitrs_files = fitrs_files[fitrs_files['instrument_type'] == "Non-Equity Instruments"]
        
        # Filter by CFI code in filename
        fitrs_files = fitrs_files[fitrs_files['file_name'].str.contains(f'_{CFI_CODE}_', na=False)]
        
        logger.info(f"📊 Filtered to {len(fitrs_files)} files matching criteria")
        
        if fitrs_files.empty:
            logger.warning("❌ No files match the specified criteria")
            logger.info("Available files:")
            for idx, row in file_list.head(10).iterrows():
                logger.info(f"  - {row['file_name']} ({row.get('instrument_type', 'Unknown type')})")
            return
        
        # Download and process each file
        all_data = []
        for idx, file_info in fitrs_files.iterrows():
            file_url = file_info['download_link']
            file_name = file_info['file_name']
            
            logger.info(f"⬇️  Downloading: {file_name}")
            
            try:
                # Download and parse the file
                df = edl.download_file(file_url, update=UPDATE_DATA)
                
                if not df.empty:
                    logger.info(f"✅ Downloaded {len(df)} records from {file_name}")
                    
                    # Add metadata
                    df['source_file'] = file_name
                    df['download_date'] = pd.Timestamp.now()
                    
                    all_data.append(df)
                    
                    # Display sample data
                    logger.info("📋 Sample data columns:")
                    logger.info(f"   Columns: {list(df.columns)}")
                    logger.info(f"   Shape: {df.shape}")
                    
                    if len(df) > 0:
                        logger.info("📋 Sample record:")
                        sample_record = df.iloc[0]
                        for col, val in sample_record.items():
                            if pd.notna(val) and str(val).strip():
                                logger.info(f"   {col}: {val}")
                else:
                    logger.warning(f"⚠️  No data found in {file_name}")
                    
            except Exception as e:
                logger.error(f"❌ Error downloading {file_name}: {str(e)}")
                continue
        
        if all_data:
            # Combine all data
            combined_df = pd.concat(all_data, ignore_index=True)
            logger.info(f"🎉 Successfully downloaded {len(combined_df)} total records")
            
            # Save combined data
            output_file = fitrs_data_folder / f'{file_name}_fitrs_data.csv'
            combined_df.to_csv(output_file, index=False)
            logger.info(f"💾 Combined data saved to: {output_file}")
            
            # Display summary statistics
            logger.info("📊 Summary Statistics:")
            logger.info(f"   Total records: {len(combined_df)}")
            logger.info(f"   Total columns: {len(combined_df.columns)}")
            logger.info(f"   Source files: {combined_df['source_file'].nunique()}")
            
            # Show unique values for key columns if they exist
            key_columns = ['Id', 'FinInstrmGnlAttrbts_Id', 'TradgVnRltdAttrbts_MktIdrCd']
            for col in key_columns:
                if col in combined_df.columns:
                    unique_count = combined_df[col].nunique()
                    logger.info(f"   Unique {col}: {unique_count}")
        else:
            logger.warning("❌ No data was successfully downloaded")
            
    except Exception as e:
        logger.error(f"❌ Error in main process: {str(e)}")
        raise

def download_specific_date(date_str: str, cfi_code: str = 'E'):
    """Download FITRS data for a specific date"""
    logger.info(f"📅 Downloading FITRS data for {date_str} with CFI {cfi_code}")
    
    edl = EsmaDataLoader(
        creation_date_from=date_str,
        creation_date_to=date_str,
        limit='10000'
    )
    
    try:
        # Use the load_latest_files method with specific parameters
        df = edl.load_latest_files(
            file_type='Full',
            cfi=cfi_code,
            eqt=True,  # Set to False for non-equity
            update=True
        )
        
        if not df.empty:
            logger.info(f"✅ Downloaded {len(df)} records for {date_str}")
            
            # Save to FITRS folder - updated path
            project_root = Path(__file__).parent.parent.parent
            fitrs_data_folder = project_root / 'downloads' / 'fitrs'
            fitrs_data_folder.mkdir(parents=True, exist_ok=True)
            
            output_file = fitrs_data_folder / f'fitrs_{cfi_code}_{date_str}.csv'
            df.to_csv(output_file, index=False)
            logger.info(f"💾 Data saved to: {output_file}")
            
            return df
        else:
            logger.warning(f"⚠️  No data found for {date_str}")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"❌ Error downloading data for {date_str}: {str(e)}")
        return pd.DataFrame()

if __name__ == '__main__':
    # You can modify these parameters or uncomment the specific date download
    main()
    
    # Alternative: Download for a specific date
    # download_specific_date('2024-04-26', 'E')