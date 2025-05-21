import hashlib
import functools
import os
import re
import requests
import tempfile
import zipfile
import warnings
import pandas as pd
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from dataclasses import dataclass
from requests.models import Response
from enum import Enum
import logging
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
        'BizData': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
        'AppHdr': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.01',
        'Document': 'urn:iso:std:iso:20022:tech:xsd:auth.017.001.02'
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
        
        logger = Utils.set_logger('EsmaDataUtils')
        logger.warning("Previously saved data used:\n{}\nSet update=True to get the most up-to-date data".format(file))

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _create_folder(folder: str = "data"):

        """
        Create a folder in the user's home directory to store data.

        Args:
            folder (str): The name of the folder to create. Default is "data".

        Returns:
            Path: The path to the created folder.

        Example:
            >>> folder_path = Utils._create_folder("my_data")
            >>> print(folder_path)
            "/home/user/esma_data_py/my_data"
        """

        main_folder = esmaConfig.file_path

        if not main_folder.exists():
            main_folder.mkdir(parents=True)

        return main_folder

    def save_df(obj=pd.DataFrame, print_cached_data=True, folder="data"):

        """
        Decorator to save and retrieve DataFrames to/from cache as pickled files. If a file already exists and `update` is False,
        the cached version will be used.

        Args:
            obj (pd.DataFrame): Default object that will be returned if no new data is fetched.
            print_cached_data (bool): Whether to print a warning when cached data is used. Defaults to True.
            folder (str): The folder where the data is stored. Defaults to "data".

        Returns:
            function: A decorated function that will save and load data as necessary.
        
        Example:
            >>> @Utils.save_df()
            >>> def fetch_data():
            >>>     return pd.DataFrame({'col': [1, 2, 3]})
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                logger = Utils.set_logger('EsmaDataUtils')
                data_folder = Utils._create_folder(folder=folder)

                non_update_save_args = [str(value) for key, value in kwargs.items() if key not in ["update"]]
                string_file_arg = non_update_save_args + [func.__name__] + [str(arg) for arg in args]

                file_name = os.path.join(data_folder, Utils._hash("".join(string_file_arg)) + ".csv")

                update = kwargs.get("update", False)
                
                if not os.path.exists(file_name) or update:
                    df = func(*args, **kwargs)
                    try:
                        df.to_pickle(file_name)
                        logger.info(f"Data saved: {file_name}")
                    except Exception as e:
                        warnings.warn(f"Error saving file: {file_name}\n{str(e)}")
                        logger.error(f"Error, file not saved: {file_name}\n{df}")
                        logger.error(f"Type of df: {type(df)}")

                    df = obj(df)

                else:
                    try:
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

        file_name_raw = url.split('/')[len(url.split('/')) - 1]
        file_name = file_name_raw.split(".")[0]
        return file_name

    @staticmethod
    def clean_inner_tags(root: ET):
        """Clean XML inner tags by stripping namespaces and adjusting the tag names."""
        parent_elem = None
        pattern_tag = r"\{[^}]*\}(\S+)"

        for elem in root.iter():
            if (clean_tag := re.search(pattern_tag, elem.tag).group(1)) in ['Amt', 'Nb']:
                elem.tag = '_'.join([parent_elem.tag, clean_tag])
            else:
                elem.tag = clean_tag

            parent_elem = elem

    @staticmethod
    def process_tags(child: ET) -> dict:
        """Process XML tags and map values into a dictionary."""
        mini_tags = defaultdict(list)
        list_additional_vals = [deque(range(2,101)) for _ in range(15)]
        mini_tags_list_map = defaultdict(int)

        for i in child.iter():
            if str(i.text).strip() != '':
                if i.tag not in mini_tags:
                    mini_tags[i.tag].append(i.text)
                else:
                    if i.tag not in mini_tags_list_map:
                        mini_tags_list_map[i.tag] = len(mini_tags_list_map)

                    key_list_map = mini_tags_list_map[i.tag]
                    key = '_'.join([i.tag, str(list_additional_vals[key_list_map].popleft())])
                    mini_tags[key].append(i.text)

        return mini_tags

    @staticmethod
    def process_tags_firds(child: ET) -> dict:
        """Process XML tags by building complete paths for all fields."""
        mini_tags = defaultdict(list)
        
        def process_element(elem, current_path=[]):
            """Recursively process elements and build path."""
            # Special case for ISIN ID field - always map to Id for consistency
            if elem.tag == 'Id' and current_path and current_path[-1] == 'FinInstrmGnlAttrbts':
                if str(elem.text).strip():
                    mini_tags['Id'].append(elem.text)
                return
                
            path = current_path + [elem.tag]
            
            # Store any non-empty value with its full path
            if str(elem.text).strip() and str(elem.text).strip().lower() != 'nan':
                column_name = '_'.join(path)
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

        xml = BeautifulSoup(request.text, 'xml')
        list_of_dicts = []

        for doc in xml.find_all('doc'):
            record_dict = {}

            for element in doc.find_all():
                name = element.get('name')  
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

        logger = Utils.set_logger('EsmaDataUtils')
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
        if root.find('.//Document:RefData', Utils.NAMESPACES) is not None:
            logger.info("Detected FIRDS format")
            Utils.clean_inner_tags_firds(root)
            logger.info("Cleaned inner tags for FIRDS")
            root_list = list(root.iter('RefData'))
            if not root_list:
                logger.warning("No RefData found in FIRDS XML")
                return pd.DataFrame()
            logger.info(f"Found {len(root_list)} records to process")
            list_dicts = []
            for child in tqdm(root_list, desc='Parsing file ... ', position=0, leave=True):
                list_dicts.append(Utils.process_tags_firds(child))
            df = pd.DataFrame.from_records(list_dicts)
            
            # Clean the DataFrame:
            # 1. Convert lists to scalar values
            df = df.map(lambda x: x[0] if isinstance(x, list) else x)
            
            # 2. Drop columns with all null values (includes np.nan, None, and empty strings)
            df = df.replace(r'^\s*$', pd.NA, regex=True)  # Convert empty strings to NA
            df = df.dropna(axis=1, how='all')  # Drop columns where all values are NA
            
            # 3. Drop intermediate node columns (those with count = 0)
            null_counts = df.isnull().sum()
            empty_columns = null_counts[null_counts == len(df)].index
            df = df.drop(columns=empty_columns)
            
            # 4. Clean up RefData prefix from column names
            df.columns = df.columns.str.replace('^RefData_', '', regex=True)
            
            logger.info(f"Final DataFrame shape after cleaning: {df.shape}")
            if df.empty:
                logger.warning("The DataFrame is empty after processing FIRDS XML.")
                return pd.DataFrame()
            return df

        # Continue with existing FITRS/DVCAP processing
        Utils.clean_inner_tags(root)
        logger.info("Cleaned inner tags")

        root_list = list(root.iter('NonEqtyTrnsprncyData'))
        if not root_list:
            root_list = list(root.iter('EqtyTrnsprncyData'))
        if not root_list:
            root_list = list(root.iter('VolCapRslt'))
        
        logger.info(f"Found {len(root_list)} records to process")

        list_dicts = []
        for child in tqdm(root_list, desc='Parsing file ... ', position=0, leave=True):
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
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
            'FinInstrmGnlAttrbts': True,
            'DerivInstrmAttrbts': True,
            'TradgVnRltdAttrbts': True,
            'TechAttrbts': True,
            'PblctnPrd': True
        }
        current_parent = None

        for elem in root.iter():
            # Clean namespace
            if (clean_tag := re.search(pattern_tag, elem.tag)):
                clean_tag = clean_tag.group(1)
                # Handle parent sections
                if clean_tag in parent_sections:
                    current_parent = clean_tag
                    # Remove numbered duplicates
                    if '_' in clean_tag:
                        base_tag = clean_tag.split('_')[0]
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
    FITRS = 'fitrs'
    FIRDS = 'firds'
    DVCAP = 'dvcap'


class Cfi(Enum):
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    H = 'H'
    I = 'I'
    J = 'J'
    O = 'O'
    R = 'R'
    S = 'S'


@dataclass
class QueryUrl:

    ssr: str = ('https://registers.esma.europa.eu/solr/esma_registers_mifid_shsexs/select?'
                'q=({{!parent%20which=%27type_s:parent%27}})&wt=json&indent=true&rows=150000&fq=(shs_countryCode:{country})')
    mifid: str = ('https://registers.esma.europa.eu/solr/esma_registers_{db}_files/select?q=*'
                  '&fq={date_column}:%5B{creation_date_from}T00:00:00Z+TO+{creation_date_to}T23:59:59Z%5D&wt=xml&indent=true&start=0&rows={limit}')
    fca_firds: str =  ('https://api.data.fca.org.uk/fca_data_firds_files?q=((file_type:FULINS)'
                       '%20AND%20(publication_date:[{creation_date_from}%20TO%20{creation_date_to}]))&from=0&size={limit}')