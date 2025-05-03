# Search and Download ESMA's data

from ..services.esma_data_loader import EsmaDataLoader
from ..services.esma_utils import Cfi
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# instantiate edl
edl = EsmaDataLoader('2025-04-26', '2025-04-26')

# Process each CFI code
for cfi in Cfi:
    logger.info(f"\nProcessing CFI code: {cfi.value}")
    
    # Load available FIRDS files for this CFI
    list_files = edl.load_mifid_file_list(['firds'])
    fulins_files = list_files[list_files['download_link'].str.contains('FULINS', na=False)]
    
    if fulins_files.empty:
        logger.warning(f"No FULINS files found for CFI {cfi.value}")
        continue
    
    # Process each FULINS file
    for idx, file_info in fulins_files.iterrows():
        link = file_info['download_link']
        logger.info(f"\nProcessing file: {link}")
        
        try:
            # Download and parse file
            df = edl.download_file(link, update=True)
            
            # Print information about the DataFrame
            logger.info(f"File columns: {df.columns.tolist()}")
            logger.info(f"DataFrame shape: {df.shape}")
            
            # Print sample ISINs if available
            if 'Id' in df.columns:
                logger.info(f"First 5 ISINs: {df['Id'].head().tolist()}")
            
        except Exception as e:
            logger.error(f"Error processing file {link}: {str(e)}")
            continue