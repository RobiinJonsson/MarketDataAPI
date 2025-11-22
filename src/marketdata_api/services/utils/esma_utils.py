import functools
import hashlib
import logging
import os
import re
import tempfile
import warnings
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.models import Response
from tqdm import tqdm

from marketdata_api.config import esmaConfig


class Utils:
    """
    Utility class providing various helper methods for data processing, file handling,
    logging, and caching. It includes functions for hashing strings, managing directories,
    logging, parsing XML responses, and caching DataFrames.

    This class is designed to work in symbiosis with EsmaDataLoader and  to simplify common tasks such as working with files,
    handling data caching, and performing logging for operations related to data retrieval.

    """

    # Add namespaces as class constant at the top of class
    NAMESPACES = {
        "BizData": "urn:iso:std:iso:20022:tech:xsd:head.003.001.01",
        "AppHdr": "urn:iso:std:iso:20022:tech:xsd:head.001.001.01",
        "Document": "urn:iso:std:iso:20022:tech:xsd:auth.017.001.02",
    }

    @staticmethod
    def _hash(string: str) -> str:
        """
        Generate an MD5 hash from a string.

        Args:
            string (str): The input string to hash.

        Returns:
            str: The MD5 hash of the input string.

        Example:
            >>> Utils._hash("my_string")
            'e99a18c428cb38d5f260853678922e03'
        """

        h = hashlib.new("md5")
        h.update(string.encode("utf-8"))
        return h.hexdigest()

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _warning_cached_data(file: str):
        """
        Warn about previously saved data being used and notify that an update can be triggered.

        Args:
            file (str): The file being used from the cache.

        Example:
            >>> Utils._warning_cached_data("file_path.csv")
            "Previously saved data used: file_path.csv"
        """
        """Warn about previously saved data being used."""

        logger = Utils.set_logger("EsmaDataUtils")
        logger.warning(
            "Previously saved data used:\n{}\nSet update=True to get the most up-to-date data".format(
                file
            )
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _create_folder(folder: str = "data"):
        """
        Create a folder structure for storing ESMA data files.
        Now properly organized by file type.
        """
        downloads_folder = esmaConfig.downloads_path

        if not downloads_folder.exists():
            downloads_folder.mkdir(parents=True)

        # Create FIRDS subdirectory for FIRDS files
        firds_folder = downloads_folder / "firds"
        if not firds_folder.exists():
            firds_folder.mkdir(parents=True)

        # Create FITRS subdirectory for transparency data
        fitrs_folder = downloads_folder / "fitrs"
        if not fitrs_folder.exists():
            fitrs_folder.mkdir(parents=True)

        return downloads_folder

    def save_df(obj=pd.DataFrame, print_cached_data=True, folder="data"):
        """
        Enhanced decorator to save and retrieve DataFrames with improved file organization.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                logger = Utils.set_logger("EsmaDataUtils")

                # Determine file type and target directory based on URL and content
                url = kwargs.get("url") or (args[0] if args else "")
                url_str = str(url).lower()

                # More comprehensive URL pattern matching
                is_fitrs = (
                    "fitrs" in url_str
                    or "transparency" in url_str
                    or "fulncr" in url_str  # Non-equity transparency
                    or "fulecr" in url_str  # Equity transparency
                )
                is_firds = (
                    "firds" in url_str
                    or "fulins" in url_str  # Full instrument reference data
                    or "delvins" in url_str  # Delta instrument reference data
                )
                # DVCAP (volume cap) files also go to FIRDS folder
                is_dvcap = "dvcap" in url_str or "dvcres" in url_str

                base_folder = Utils._create_folder(folder)

                if is_fitrs:
                    data_folder = base_folder / "fitrs"
                elif is_firds or is_dvcap:
                    data_folder = base_folder / "firds"
                else:
                    # Default to firds folder for other ESMA data
                    data_folder = base_folder / "firds"

                non_update_save_args = [
                    str(value) for key, value in kwargs.items() if key not in ["update"]
                ]
                string_file_arg = (
                    non_update_save_args + [func.__name__] + [str(arg) for arg in args]
                )

                # Create meaningful filename based on URL if available
                if url and ("download" in func.__name__.lower() or url.startswith("http")):
                    # Extract meaningful filename from URL
                    original_filename = Utils.extract_file_name_from_url(url)
                    if is_fitrs:
                        file_name = os.path.join(data_folder, f"{original_filename}_fitrs_data.csv")
                    elif is_firds or is_dvcap:
                        file_name = os.path.join(data_folder, f"{original_filename}_firds_data.csv")
                    else:
                        file_name = os.path.join(data_folder, f"{original_filename}_data.csv")
                else:
                    # Use hash-based filename for other functions
                    file_name = os.path.join(
                        data_folder, Utils._hash("".join(string_file_arg)) + ".csv"
                    )

                update = kwargs.get("update", False)

                if not os.path.exists(file_name) or update:
                    df = func(*args, **kwargs)
                    try:
                        # Save as CSV instead of pickle since file has .csv extension
                        if file_name.endswith(".csv"):
                            df.to_csv(file_name, index=False, encoding="utf-8")
                        else:
                            df.to_pickle(file_name)
                        logger.info(f"Data saved: {file_name}")

                    except Exception as e:
                        warnings.warn(f"Error saving file: {file_name}\n{str(e)}")
                        logger.error(f"Error, file not saved: {file_name}\n{df}")
                        logger.error(f"Type of df: {type(df)}")

                    df = obj(df)

                else:
                    try:
                        # Load file based on extension
                        if file_name.endswith(".csv"):
                            df = pd.read_csv(file_name, encoding="utf-8")
                        else:
                            df = pd.read_pickle(file_name)

                        if "Unnamed: 0" in df.columns:
                            del df["Unnamed: 0"]
                    except Exception as e:
                        warnings.warn(f"Error loading file: {file_name}\n{str(e)}")
                        os.remove(file_name)
                        kwargs["update"] = True
                        logger.error("Unable to load data, function retriggered")
                        df = func(*args, **kwargs)
                        df = obj(df)
                    else:
                        if print_cached_data:
                            Utils._warning_cached_data(file_name)
                        df = obj(df)

                return df

            return wrapper

        return decorator

    @staticmethod
    def extract_file_name_from_url(url: str) -> str:
        """
        Extract the file name from a URL.

        Args:
            url (str): The URL from which to extract the file name.

        Returns:
            str: The extracted file name without extension.

        Example:
            >>> Utils.extract_file_name_from_url("http://example.com/file.zip")
            'file'
        """

        file_name_raw = url.split("/")[len(url.split("/")) - 1]
        file_name = file_name_raw.split(".")[0]
        return file_name

    @staticmethod
    def clean_inner_tags(root: ET):
        """Clean XML inner tags by stripping namespaces and adjusting the tag names."""
        parent_elem = None
        pattern_tag = r"\{[^}]*\}(\S+)"

        for elem in root.iter():
            if (clean_tag := re.search(pattern_tag, elem.tag).group(1)) in ["Amt", "Nb"]:
                elem.tag = "_".join([parent_elem.tag, clean_tag])
            else:
                elem.tag = clean_tag

            parent_elem = elem

    @staticmethod
    def process_tags(child: ET) -> dict:
        """Process XML tags and map values into a dictionary."""
        mini_tags = defaultdict(list)
        list_additional_vals = [deque(range(2, 101)) for _ in range(15)]
        mini_tags_list_map = defaultdict(int)

        for i in child.iter():
            if str(i.text).strip() != "":
                if i.tag not in mini_tags:
                    mini_tags[i.tag].append(i.text)
                else:
                    if i.tag not in mini_tags_list_map:
                        mini_tags_list_map[i.tag] = len(mini_tags_list_map)

                    key_list_map = mini_tags_list_map[i.tag]
                    key = "_".join([i.tag, str(list_additional_vals[key_list_map].popleft())])
                    mini_tags[key].append(i.text)

        return mini_tags

    @staticmethod
    def process_tags_firds(child: ET) -> dict:
        """Process XML tags by building complete paths for all fields."""
        mini_tags = defaultdict(list)

        def process_element(elem, current_path=[]):
            """Recursively process elements and build path."""
            # Special case for ISIN ID field - always map to Id for consistency
            if elem.tag == "Id" and current_path and current_path[-1] == "FinInstrmGnlAttrbts":
                if str(elem.text).strip():
                    mini_tags["Id"].append(elem.text)
                return

            path = current_path + [elem.tag]

            # Store any non-empty value with its full path
            if str(elem.text).strip() and str(elem.text).strip().lower() != "nan":
                column_name = "_".join(path)
                mini_tags[column_name].append(elem.text)

            # Process children
            for child_elem in elem:
                process_element(child_elem, path)

        # Start processing from root
        process_element(child)

        return mini_tags

    @staticmethod
    def parse_request_to_df(request: Response) -> pd.DataFrame:
        """
        Parse an XML response to a DataFrame.

        Args:
            request (Response): The HTTP response containing XML data.

        Returns:
            pd.DataFrame: The parsed DataFrame containing the XML data.

        Example:
            >>> df = Utils.parse_request_to_df(response)
        """

        xml = BeautifulSoup(request.text, "xml")
        list_of_dicts = []

        for doc in xml.find_all("doc"):
            record_dict = {}

            for element in doc.find_all():
                name = element.get("name")
                if name:
                    record_dict[name] = element.text

            list_of_dicts.append(record_dict)

        data = pd.DataFrame.from_records(list_of_dicts)

        return data

    @staticmethod
    @save_df()
    def download_and_parse_file(url: str, update: bool = False) -> pd.DataFrame:
        """
        Download a file from a URL, extract its contents, and parse it into a DataFrame.

        Args:
            url (str): The URL to download the file from.
            update (bool): Whether to force an update of the cached data. Defaults to False.

        Returns:
            pd.DataFrame: The parsed DataFrame.

        Example:
            >>> df = Utils.download_and_parse_file("http://example.com/file.zip")
        """

        logger = Utils.set_logger("EsmaDataUtils")
        logger.info(f"Downloading from URL: {url}")

        file_name = Utils.extract_file_name_from_url(url)
        logger.info(f"Extracted file name: {file_name}")

        r = requests.get(url)
        logger.info(f"Download status code: {r.status_code}")

        with tempfile.TemporaryDirectory() as temp_dir:
            dataDir = str(temp_dir) + "/" + file_name
            logger.info(f"Created temporary directory: {dataDir}")

            if not os.path.exists(dataDir):
                os.mkdir(dataDir)
            logger.info(f"Created data directory: {dataDir}")

            file_dwn = dataDir + "/" + "file_" + file_name
            logger.info(f"Saving downloaded file to: {file_dwn}")

            try:
                with open(file_dwn, mode="wb") as file:
                    file.write(r.content)
                    logger.info(f"File written successfully, size: {len(r.content)} bytes")

                with zipfile.ZipFile(file_dwn, "r") as zip_ref:
                    logger.info(f"Zip contents: {zip_ref.namelist()}")
                    zip_ref.extractall(dataDir)
                    logger.info("Zip extracted successfully")

                xml_files = [f for f in os.listdir(dataDir) if ".xml" in f]
                logger.info(f"Found XML files: {xml_files}")
                file_xml = dataDir + "/" + xml_files[0]

                root = ET.parse(file_xml).getroot()
                logger.info(f"XML root tag: {root.tag}")

            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                raise

        # First check for FIRDS format
        if root.find(".//Document:RefData", Utils.NAMESPACES) is not None:
            logger.info("Detected FIRDS format")
            Utils.clean_inner_tags_firds(root)
            logger.info("Cleaned inner tags for FIRDS")
            root_list = list(root.iter("RefData"))
            if not root_list:
                logger.warning("No RefData found in FIRDS XML")
                return pd.DataFrame()
            logger.info(f"Found {len(root_list)} records to process")
            list_dicts = []
            for child in tqdm(root_list, desc="Parsing file ... ", position=0, leave=True):
                list_dicts.append(Utils.process_tags_firds(child))
            df = pd.DataFrame.from_records(list_dicts)

            # Clean the DataFrame:
            # 1. Convert lists to scalar values
            df = df.map(lambda x: x[0] if isinstance(x, list) else x)

            # 2. Drop columns with all null values (includes np.nan, None, and empty strings)
            df = df.replace(r"^\s*$", pd.NA, regex=True)  # Convert empty strings to NA
            df = df.dropna(axis=1, how="all")  # Drop columns where all values are NA

            # 3. Drop intermediate node columns (those with count = 0)
            null_counts = df.isnull().sum()
            empty_columns = null_counts[null_counts == len(df)].index
            df = df.drop(columns=empty_columns)

            # 4. Clean up RefData prefix from column names
            df.columns = df.columns.str.replace("^RefData_", "", regex=True)

            logger.info(f"Final DataFrame shape after cleaning: {df.shape}")
            if df.empty:
                logger.warning("The DataFrame is empty after processing FIRDS XML.")
                return pd.DataFrame()
            return df

        # Continue with existing FITRS/DVCAP processing
        Utils.clean_inner_tags(root)
        logger.info("Cleaned inner tags")

        root_list = list(root.iter("NonEqtyTrnsprncyData"))
        if not root_list:
            root_list = list(root.iter("EqtyTrnsprncyData"))
        if not root_list:
            root_list = list(root.iter("VolCapRslt"))

        logger.info(f"Found {len(root_list)} records to process")

        list_dicts = []
        for child in tqdm(root_list, desc="Parsing file ... ", position=0, leave=True):
            list_dicts.append(Utils.process_tags(child))

        df = pd.DataFrame.from_records(list_dicts)
        delivery_df = df.map(lambda x: x[0] if isinstance(x, list) else x)
        logger.info(f"Final DataFrame shape: {delivery_df.shape}")
        return delivery_df

    @staticmethod
    def set_logger(name: str):
        """Set up a logger for the specified name."""
        logger = logging.getLogger(name)

        # Only configure if the logger doesn't already have handlers
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            logger.propagate = False

        return logger

    @staticmethod
    def clean_inner_tags_firds(root: ET):
        """Clean XML inner tags specifically for FIRDS format."""
        pattern_tag = r"\{[^}]*\}(\S+)"

        # Track parents and their children
        parent_sections = {
            "FinInstrmGnlAttrbts": True,
            "DerivInstrmAttrbts": True,
            "TradgVnRltdAttrbts": True,
            "TechAttrbts": True,
            "PblctnPrd": True,
        }
        current_parent = None

        for elem in root.iter():
            # Clean namespace
            if clean_tag := re.search(pattern_tag, elem.tag):
                clean_tag = clean_tag.group(1)
                # Handle parent sections
                if clean_tag in parent_sections:
                    current_parent = clean_tag
                    # Remove numbered duplicates
                    if "_" in clean_tag:
                        base_tag = clean_tag.split("_")[0]
                        if base_tag in parent_sections:
                            clean_tag = base_tag
                    elem.tag = clean_tag
                else:
                    # Add parent prefix for child elements
                    if current_parent:
                        elem.tag = f"{current_parent}_{clean_tag}"
                    else:
                        elem.tag = clean_tag

            # Reset parent when exiting section
            if elem.tag in parent_sections:
                current_parent = None


class Dataset(Enum):
    FITRS = "fitrs"
    FIRDS = "firds"
    DVCAP = "dvcap"


class Cfi(Enum):
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    H = "H"
    I = "I"
    J = "J"
    O = "O"
    R = "R"
    S = "S"


@dataclass
class QueryUrl:

    ssr: str = (
        "https://registers.esma.europa.eu/solr/esma_registers_mifid_shsexs/select?"
        "q=({{!parent%20which=%27type_s:parent%27}})&wt=json&indent=true&rows=150000&fq=(shs_countryCode:{country})"
    )
    mifid: str = (
        "https://registers.esma.europa.eu/solr/esma_registers_{db}_files/select?q=*"
        "&fq={date_column}:%5B{creation_date_from}T00:00:00Z+TO+{creation_date_to}T23:59:59Z%5D&wt=xml&indent=true&start=0&rows={limit}"
    )
    fca_firds: str = (
        "https://api.data.fca.org.uk/fca_data_firds_files?q=((file_type:FULINS)"
        "%20AND%20(publication_date:[{creation_date_from}%20TO%20{creation_date_to}]))&from=0&size={limit}"
    )


class BatchDataExtractor:
    """
    High-performance batch data extraction utility for ESMA FIRDS/FITRS files.
    
    Creates consolidated in-memory DataFrames per asset type to eliminate redundant file I/O
    operations during batch processing. Optimized for bulk operations on large datasets.
    """
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self._consolidated_cache = {}  # Cache for consolidated DataFrames
    
    @staticmethod
    def get_firds_consolidated_dataframe(
        asset_type: str, 
        data_directory: str = None,
        logger: logging.Logger = None
    ) -> pd.DataFrame:
        """
        Create a consolidated DataFrame for all FIRDS files of a specific asset type.
        
        This function reads all FIRDS CSV files matching the asset type pattern,
        combines them into a single DataFrame, and returns it for batch processing.
        
        Args:
            asset_type: CFI first character (C, D, E, F, H, I, J, O, R, S)
            data_directory: Path to FIRDS data directory (defaults to config path)
            logger: Logger instance for progress tracking
            
        Returns:
            pd.DataFrame: Consolidated DataFrame containing all records for the asset type
            
        Example:
            # Get all equity (E) instruments in one DataFrame
            equity_df = BatchDataExtractor.get_firds_consolidated_dataframe('E')
            target_isins = ['GB00B1YW4409', 'US0378331005']
            matches = equity_df[equity_df['ISIN'].isin(target_isins)]
        """
        if logger is None:
            logger = logging.getLogger(__name__)
            
        if data_directory is None:
            from ...config import Config
            data_directory = os.path.join(Config.ROOT_PATH, "data", "downloads", "firds")
        
        if not os.path.exists(data_directory):
            logger.warning(f"FIRDS directory not found: {data_directory}")
            return pd.DataFrame()
        
        # Get all FIRDS files for this asset type
        # FIRDS format: FULINS_{letter}_{date}_{part}_firds_data.csv
        pattern = rf"FULINS_{asset_type.upper()}_\d{{8}}_\d+of\d+_firds_data\.csv"
        
        matching_files = []
        for filename in os.listdir(data_directory):
            if re.match(pattern, filename):
                matching_files.append(filename)
        
        if not matching_files:
            logger.info(f"No FIRDS files found for asset type {asset_type}")
            return pd.DataFrame()
        
        logger.info(f"🔄 Consolidating {len(matching_files)} FIRDS files for asset type {asset_type}")
        
        consolidated_dfs = []
        for filename in sorted(matching_files):
            filepath = os.path.join(data_directory, filename)
            try:
                df = pd.read_csv(filepath, dtype=str, low_memory=False)
                if not df.empty:
                    df['source_file'] = filename  # Track source for debugging
                    consolidated_dfs.append(df)
                    logger.debug(f"   📁 Loaded {len(df)} records from {filename}")
            except Exception as e:
                logger.warning(f"Failed to read FIRDS file {filename}: {str(e)}")
                continue
        
        if not consolidated_dfs:
            logger.warning(f"No valid FIRDS data found for asset type {asset_type}")
            return pd.DataFrame()
        
        # Combine all DataFrames
        consolidated_df = pd.concat(consolidated_dfs, ignore_index=True)
        
        # Remove duplicates based on ISIN (keep most recent)
        if 'ISIN' in consolidated_df.columns:
            initial_count = len(consolidated_df)
            consolidated_df = consolidated_df.drop_duplicates(subset=['ISIN'], keep='last')
            final_count = len(consolidated_df)
            if initial_count != final_count:
                logger.info(f"   🔧 Removed {initial_count - final_count} duplicate ISINs")
        
        logger.info(f"✅ Consolidated FIRDS data: {len(consolidated_df)} unique records for asset type {asset_type}")
        return consolidated_df
    
    @staticmethod
    def get_fitrs_consolidated_dataframe(
        asset_type: str, 
        data_directory: str = None,
        logger: logging.Logger = None
    ) -> pd.DataFrame:
        """
        Create a consolidated DataFrame for all FITRS files of a specific asset type.
        
        This function reads all FITRS CSV files matching the asset type pattern,
        combines them into a single DataFrame for efficient batch transparency processing.
        
        Args:
            asset_type: CFI first character (C, D, E, F, H, I, J, O, R, S)
            data_directory: Path to FITRS data directory (defaults to config path)
            logger: Logger instance for progress tracking
            
        Returns:
            pd.DataFrame: Consolidated DataFrame containing all transparency records
            
        Example:
            # Get all debt (D) transparency data in one DataFrame
            debt_df = BatchDataExtractor.get_fitrs_consolidated_dataframe('D')
            target_isins = ['XS1234567890', 'US912828XY12']
            matches = debt_df[debt_df['ISIN'].isin(target_isins)]
        """
        if logger is None:
            logger = logging.getLogger(__name__)
            
        if data_directory is None:
            from ...config import Config
            data_directory = os.path.join(Config.ROOT_PATH, "data", "downloads", "fitrs")
        
        if not os.path.exists(data_directory):
            logger.warning(f"FITRS directory not found: {data_directory}")
            return pd.DataFrame()
        
        # Get all FITRS files for this asset type
        # FITRS format: FUL{ECR|NCR}_{date}_{letter}_{part}_fitrs_data.csv
        pattern = rf"FUL(ECR|NCR)_\d{{8}}_{asset_type.upper()}_\d+of\d+_fitrs_data\.csv"
        
        matching_files = []
        for filename in os.listdir(data_directory):
            if re.match(pattern, filename):
                matching_files.append(filename)
        
        if not matching_files:
            logger.info(f"No FITRS files found for asset type {asset_type}")
            return pd.DataFrame()
        
        logger.info(f"🔄 Consolidating {len(matching_files)} FITRS files for asset type {asset_type}")
        
        consolidated_dfs = []
        for filename in sorted(matching_files):
            filepath = os.path.join(data_directory, filename)
            try:
                df = pd.read_csv(filepath, dtype=str, low_memory=False)
                if not df.empty:
                    df['source_file'] = filename  # Track source for debugging
                    consolidated_dfs.append(df)
                    logger.debug(f"   📁 Loaded {len(df)} records from {filename}")
            except Exception as e:
                logger.warning(f"Failed to read FITRS file {filename}: {str(e)}")
                continue
        
        if not consolidated_dfs:
            logger.warning(f"No valid FITRS data found for asset type {asset_type}")
            return pd.DataFrame()
        
        # Combine all DataFrames
        consolidated_df = pd.concat(consolidated_dfs, ignore_index=True)
        
        logger.info(f"✅ Consolidated FITRS data: {len(consolidated_df)} records for asset type {asset_type}")
        return consolidated_df
    
    @staticmethod
    def batch_extract_firds_data(
        isin_list: list,
        asset_type_mapping: dict = None,
        data_directory: str = None,
        logger: logging.Logger = None
    ) -> dict:
        """
        Extract FIRDS data for multiple ISINs in an optimized batch operation.
        
        Groups ISINs by asset type, creates consolidated DataFrames per type,
        and extracts all matching records in a single pass per asset type.
        
        Args:
            isin_list: List of ISINs to extract data for
            asset_type_mapping: Optional mapping of ISIN -> asset_type to avoid lookups
            data_directory: Path to FIRDS data directory
            logger: Logger instance
            
        Returns:
            dict: {
                'results': {isin: [matching_records]},
                'statistics': {asset_type: count},
                'total_found': int,
                'total_searched': int
            }
        """
        if logger is None:
            logger = logging.getLogger(__name__)
            
        results = {}
        statistics = {}
        total_found = 0
        
        logger.info(f"🚀 Starting batch FIRDS extraction for {len(isin_list)} ISINs")
        
        # Group ISINs by asset type if mapping provided, otherwise try all types
        if asset_type_mapping:
            isin_groups = {}
            for isin in isin_list:
                asset_type = asset_type_mapping.get(isin, 'E')  # Default to equity
                if asset_type not in isin_groups:
                    isin_groups[asset_type] = []
                isin_groups[asset_type].append(isin)
        else:
            # Try all common asset types if no mapping provided
            asset_types_to_try = ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'O', 'R', 'S']
            isin_groups = {asset_type: isin_list for asset_type in asset_types_to_try}
        
        # Process each asset type group
        for asset_type, group_isins in isin_groups.items():
            if not group_isins:
                continue
                
            logger.info(f"🔍 Processing asset type {asset_type} ({len(group_isins)} ISINs)")
            
            # Get consolidated DataFrame for this asset type
            consolidated_df = BatchDataExtractor.get_firds_consolidated_dataframe(
                asset_type, data_directory, logger
            )
            
            if consolidated_df.empty:
                statistics[asset_type] = 0
                continue
            
            # Extract matching records
            matches = consolidated_df[consolidated_df['ISIN'].isin(group_isins)]
            found_count = len(matches)
            
            if found_count > 0:
                # Group matches by ISIN
                for isin in matches['ISIN'].unique():
                    isin_matches = matches[matches['ISIN'] == isin]
                    if isin not in results:
                        results[isin] = []
                    results[isin].extend(isin_matches.to_dict('records'))
                
                total_found += found_count
                logger.info(f"   ✅ Found {found_count} records for asset type {asset_type}")
            
            statistics[asset_type] = found_count
        
        logger.info(f"🎉 Batch FIRDS extraction completed: {total_found} records found for {len(results)} ISINs")
        
        return {
            'results': results,
            'statistics': statistics,
            'total_found': total_found,
            'total_searched': len(isin_list)
        }
    
    @staticmethod
    def batch_extract_fitrs_data(
        isin_list: list,
        asset_type_mapping: dict = None,
        data_directory: str = None,
        logger: logging.Logger = None
    ) -> dict:
        """
        Extract FITRS transparency data for multiple ISINs in an optimized batch operation.
        
        Groups ISINs by asset type, creates consolidated DataFrames per type,
        and extracts all matching transparency records in a single pass per asset type.
        
        Args:
            isin_list: List of ISINs to extract transparency data for
            asset_type_mapping: Optional mapping of ISIN -> asset_type to avoid lookups
            data_directory: Path to FITRS data directory
            logger: Logger instance
            
        Returns:
            dict: {
                'results': {isin: [matching_transparency_records]},
                'statistics': {asset_type: count},
                'total_found': int,
                'total_searched': int
            }
        """
        if logger is None:
            logger = logging.getLogger(__name__)
            
        results = {}
        statistics = {}
        total_found = 0
        
        logger.info(f"🚀 Starting batch FITRS extraction for {len(isin_list)} ISINs")
        
        # Group ISINs by asset type if mapping provided, otherwise try all types
        if asset_type_mapping:
            isin_groups = {}
            for isin in isin_list:
                asset_type = asset_type_mapping.get(isin, 'E')  # Default to equity
                if asset_type not in isin_groups:
                    isin_groups[asset_type] = []
                isin_groups[asset_type].append(isin)
        else:
            # Try all common asset types if no mapping provided
            asset_types_to_try = ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'O', 'R', 'S']
            isin_groups = {asset_type: isin_list for asset_type in asset_types_to_try}
        
        # Process each asset type group
        for asset_type, group_isins in isin_groups.items():
            if not group_isins:
                continue
                
            logger.info(f"🔍 Processing asset type {asset_type} ({len(group_isins)} ISINs)")
            
            # Get consolidated DataFrame for this asset type
            consolidated_df = BatchDataExtractor.get_fitrs_consolidated_dataframe(
                asset_type, data_directory, logger
            )
            
            if consolidated_df.empty:
                statistics[asset_type] = 0
                continue
            
            # Search in both ISIN and Id columns (FULECR uses 'Id')
            matches = pd.DataFrame()
            
            if 'ISIN' in consolidated_df.columns:
                isin_matches = consolidated_df[consolidated_df['ISIN'].isin(group_isins)]
                matches = pd.concat([matches, isin_matches], ignore_index=True)
            
            if 'Id' in consolidated_df.columns:
                id_matches = consolidated_df[consolidated_df['Id'].isin(group_isins)]
                matches = pd.concat([matches, id_matches], ignore_index=True)
            
            # Remove duplicates
            matches = matches.drop_duplicates()
            found_count = len(matches)
            
            if found_count > 0:
                # Group matches by ISIN (handle both ISIN and Id columns)
                for _, row in matches.iterrows():
                    isin = row.get('ISIN') or row.get('Id')
                    if isin and isin in group_isins:
                        if isin not in results:
                            results[isin] = []
                        results[isin].append(row.to_dict())
                
                total_found += found_count
                logger.info(f"   ✅ Found {found_count} transparency records for asset type {asset_type}")
            
            statistics[asset_type] = found_count
        
        logger.info(f"🎉 Batch FITRS extraction completed: {total_found} records found for {len(results)} ISINs")
        
        return {
            'results': results,
            'statistics': statistics,
            'total_found': total_found,
            'total_searched': len(isin_list)
        }
