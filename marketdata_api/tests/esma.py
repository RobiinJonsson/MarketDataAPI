# Search and Download ESMA's data for data frame testing and analysis pre-model building
# EsmaDataLoader is a class that handles the downloading and processing of ESMA data files, using dates to filter the data.
# It is part of the marketdata_api module, which is a Python package for handling market data.
# The class is used to load data from ESMA's FIRDS (Financial Instruments Reference Data System) files,
# which are provided in a specific format (MIFID) and contain information about financial instruments.
# The FIRDS files are used to identify and classify financial instruments, and they are essential for compliance with MiFID II regulations.
# The EsmaDataLoader class provides methods to download, parse, and process these files.
# It also processes FITRS (Financial Instruments Transparency System) files, which contain information about the transparency of financial instruments.
# The class is designed to be flexible and can handle different types of files and data formats.
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from marketdata_api.services.esma_data_loader import EsmaDataLoader
from marketdata_api.services.esma_utils import Cfi
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup arguments
cfi = "E"  # Replace with your desired CFI code
isin = "SE0020845014"  # Replace with specific ISIN if needed

# instantiate edl
edl = EsmaDataLoader('2025-04-26', '2025-04-26')

# If ISIN is provided, look for specific instrument
if isin:
    logger.info(f"\nSearching for ISIN: {isin}")
    list_files = edl.load_mifid_file_list(['firds'])
    
    # If CFI is provided, only search relevant files
    if cfi:
        list_files = list_files[list_files['download_link'].str.contains(f'FULINS_{cfi}', na=False)]
    
    for idx, file_info in list_files.iterrows():
        try:
            df = edl.download_file(file_info['download_link'], update=False)
            if 'Id' in df.columns and isin in df['Id'].values:
                logger.info(f"\nFound ISIN {isin} in file: {file_info['download_link']}")
                isin_data = df[df['Id'] == isin].iloc[0]
                for column, value in isin_data.items():
                    if pd.notna(value):  # Only print non-null values
                        logger.info(f"{column}: {value}")
                break
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            continue
    else:
        logger.warning(f"ISIN {isin} not found in any files")

# Process specific CFI code if no ISIN is provided
elif cfi:
    logger.info(f"\nProcessing CFI code: {cfi}")
    
    # Load available FIRDS files for this CFI
    list_files = edl.load_mifid_file_list(['firds'])
    fulins_files = list_files[list_files['download_link'].str.contains(f'FULINS_{cfi}', na=False)]
    
    if fulins_files.empty:
        logger.warning(f"No FULINS files found for CFI {cfi}")
    else:
        # Process each FULINS file
        for idx, file_info in fulins_files.iterrows():
            link = file_info['download_link']
            logger.info(f"\nProcessing file: {link}")
            
            try:
                # Download and parse file
                df = edl.download_file(link, update=False)
                
                # Print DataFrame info directly
                logger.info("\nDataFrame Information:")
                print(df.info())
                
                # Print information about the DataFrame
                logger.info(f"File columns: {df.columns.tolist()}")
                logger.info(f"DataFrame shape: {df.shape}")
                
                # Display first 5 ISINs in a transposed table format
                logger.info("\nFirst 5 ISINs data (transposed):")
                transposed_df = df.head().transpose()
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                logger.info("\n" + transposed_df.to_string())
                
                # Print column stats
                logger.info("\nColumn Statistics:")
                column_stats = pd.DataFrame({
                    'Non-Null Count': df.count(),
                    'Data Type': df.dtypes
                })
                print(column_stats)
                
                # Reshape ISIN columns into a normalized structure
                isin_columns = [col for col in df.columns if col.startswith('ISIN_')]
                
                # Create a list of related ISINs with their counts
                related_isins = pd.DataFrame()
                for col in isin_columns:
                    temp_df = df[col].dropna()
                    if not temp_df.empty:
                        temp_df = pd.DataFrame({
                            'primary_id': df.index[df[col].notna()],
                            'related_isin': temp_df,
                            'isin_sequence': col.replace('ISIN_', '')
                        })
                        related_isins = pd.concat([related_isins, temp_df])

                # Show statistics of related ISINs
                logger.info("\nRelated ISINs Statistics:")
                isin_stats = related_isins.groupby('isin_sequence').size().sort_values(ascending=False)
                print(isin_stats.head(10))  # Show top 10 most common positions
                
                # Optional: Filter out rare relationships (e.g., keep only ISINs that appear more than once)
                filtered_isins = related_isins[related_isins.groupby('related_isin')['related_isin'].transform('size') > 1]
                
                logger.info(f"\nTotal unique ISINs before filtering: {len(related_isins)}")
                logger.info(f"Total unique ISINs after filtering rare occurrences: {len(filtered_isins)}")
                
                # Reset display options
                pd.reset_option('display.max_rows')
                pd.reset_option('display.max_columns')
                pd.reset_option('display.width')
                
            except Exception as e:
                logger.error(f"Error processing file {link}: {str(e)}")
                continue