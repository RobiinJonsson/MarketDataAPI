# Search and Download ESMA's data

from esma_data_loader import EsmaDataLoader
import pandas as pd

# instantiate edl
edl = EsmaDataLoader('2025-04-26', '2025-04-26')  # Use past date for testing

# load available mifid file list
list_files = edl.load_mifid_file_list(['firds'])
print("\nAvailable columns:", list_files.columns.tolist())

# get preferred link 
link = list_files.iloc[0].download_link
print(f"\nDownload link: {link}")

# download data
df = edl.download_file(link, True)

# Preview DataFrame
print("\nDataFrame Info:")
print(df.info())

print("\nSample Data (first 5 rows):")
pd.set_option('display.max_columns', None)
print(df.head())

print("\nUnique columns:", df.columns.tolist())
print("\nShape:", df.shape)

# If you want to look for specific ISINs
if 'Id' in df.columns:  # ISIN is typically in 'Id' column
    print("\nSample ISINs:", df['Id'].head().tolist())