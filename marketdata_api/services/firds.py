import requests
import xml.etree.ElementTree as ET
import os
import zipfile
from lxml import etree
import sqlite3 as sql
import sys
from typing import Dict, Any
# Dynamically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) #during development

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Define the namespaces used in the XML files
# These namespaces are used to parse the XML files correctly
ns = {
    'BizData': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'AppHdr': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.01',
    'Document': 'urn:iso:std:iso:20022:tech:xsd:auth.017.001.02'
}
    
# This should be set to the directory where you want to save the downloaded files
downloads_dir = "C:\\Users\\robin\\Projects\\MarketDataAPI\\downloads"
# List of possible elements as helper variable
possible_elements = [
    "AddtlSubPdct", "AdmssnApprvlDtByIssr", "AppHdr", "AsstClssSpcfcAttrbts", "BasePdct", 
    "BizData", "BizMsgIdr", "Bskt", "ClssfctnTp", "Cmmdty", "CmmdtyDerivInd", "CreDt", 
    "DerivInstrmAttrbts", "Document", "Dt", "FinInstrmGnlAttrbts", "FinInstrmRptgRefDataRpt", 
    "Fr", "FrDt", "FrstTradDt", "FullNm", "Hdr", "ISIN", "Id", "Indx", "Issr", "IssrReq", 
    "Metl", "MsgDefIdr", "Nm", "Nrgy", "NtlCmptntAuthrty", "NtnlCcy", "Oil", "OrgId", "Othr", 
    "PblctnPrd", "Pdct", "Prcs", "PricMltplr", "Pyld", "RefData", "RefRate", "ReqForAdmssnDt", 
    "RlvntCmptntAuthrty", "RlvntTradgVn", "RptHdr", "RptgNtty", "RptgPrd", "ShrtNm", "Sngl", 
    "SubPdct", "TechAttrbts", "TermntnDt", "To", "TradgVnRltdAttrbts", "UndrlygInstrm"
]

def get_firds_file_urls(date: str, start: int = 0, rows: int = 100, force_refresh: bool = False):
    """
    Fetches FIRDS file URLs for a given date from the ESMA FIRDS machine-to-machine interface.
    Supports both equity (FULINS_E_*) and debt (FULINS_D_*) files.
    Implements caching to avoid unnecessary downloads.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        start (int): Start index for pagination
        rows (int): Number of records to fetch
        force_refresh (bool): If True, ignores cache and fetches fresh data
        
    Returns:
        dict: Dictionary with 'equity' and 'debt' keys containing lists of URLs
    """
    base_url = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
    query_params = {
        "q": "*",
        "fq": f"publication_date:[{date}T00:00:00Z TO {date}T23:59:59Z]",
        "wt": "xml",
        "indent": "true",
        "start": start,
        "rows": rows,
    }
    
    print(f"Querying ESMA API with params: {query_params}")  # Debug print
    
    # Check if we already have files for this date
    if not force_refresh:
        equity_files = [f for f in os.listdir(downloads_dir) if f.startswith("FULINS_E_") and date in f]
        debt_files = [f for f in os.listdir(downloads_dir) if f.startswith("FULINS_D_") and date in f]
        
        if equity_files and debt_files:
            print(f"Using cached files for date {date}")
            return {
                "equity": [os.path.join(downloads_dir, f) for f in equity_files],
                "debt": [os.path.join(downloads_dir, f) for f in debt_files]
            }
    
    response = requests.get(base_url, params=query_params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    # Parse XML response
    root = ET.fromstring(response.text)
    urls = [elem.text for elem in root.findall(".//str[@name='download_link']")]
    
    print(f"Found URLs: {urls}")  # Debug print
    
    # Filter URLs by type
    filtered_urls = {
        "equity": [url for url in urls if "FULINS_E_" in url],
        "debt": [url for url in urls if "FULINS_D_" in url]
    }
    
    print(f"Filtered URLs: {filtered_urls}")  # Debug print
    
    return filtered_urls

def download_files(urls: dict, downloads_dir: str, force_refresh: bool = False):
    """
    Downloads and unzips files from the given URLs with error handling.
    Handles both equity and debt instrument files.
    
    Args:
        urls (dict): Dictionary with 'equity' and 'debt' keys containing lists of URLs
        downloads_dir (str): Directory to save files
        force_refresh (bool): If True, re-downloads existing files
    """
    # Ensure the directory exists
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Get existing files
    existing_files = {os.path.splitext(f)[0] for f in os.listdir(downloads_dir)}
    
    for file_type, type_urls in urls.items():
        print(f"Processing {file_type} files...")
        for url in type_urls:
            file_name = url.split("/")[-1]
            file_base_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(downloads_dir, file_name)
            
            # Skip if file exists and we're not forcing refresh
            if file_base_name in existing_files and not force_refresh:
                print(f"Skipped: {file_name} already exists in '{downloads_dir}'")
                continue
            
            try:
                # Download the file
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded: {file_name}")
                
                # Unzip if it's a zip file
                if zipfile.is_zipfile(file_path):
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(downloads_dir)
                        print(f"Unzipped: {file_name}")
                        
                        # Remove the zip file after extraction
                        os.remove(file_path)
                        print(f"Deleted zipped file: {file_name}")
                    except zipfile.BadZipFile:
                        print(f"Error: {file_name} is not a valid zip file.")
                        os.remove(file_path)
                        
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

def get_firds_file_names(date: str, file_prefix: str, start: int = 0, rows: int = 100):
    """
    Fetches FIRDS file names for a given date and file prefix from the ESMA FIRDS machine-to-machine interface.
    :param date: Date in YYYY-MM-DD format.
    :param file_prefix: Prefix of the file to filter.
    :param start: Start index for pagination.
    :param rows: Number of records to fetch.
    :return: List of file names.
    """
    base_url = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
    query_params = {
        "q": "*",
        "fq": f"publication_date:[{date}T00:00:00Z TO {date}T23:59:59Z]",
        "wt": "xml",
        "indent": "true",
        "start": start,
        "rows": rows,
    }
    
    response = requests.get(base_url, params=query_params)
    if response.status_code != 200:
        return [f"Error: Failed to fetch data ({response.status_code})"]
    
    # Parse XML response
    root = ET.fromstring(response.text)
    file_names = [elem.text for elem in root.findall(".//str[@name='file_name']")]
    
    # Filter file names based on prefix
    filtered_files = [name for name in file_names if name.startswith(file_prefix)]
    print("Filtered Files:")
    for file in filtered_files:
        print(file)
    
    return filtered_files

# Function to process all XML files in the given directory, executing the main logic of extracting data
# looking for a specific ISIN and inserting it into the database
def process_all_xml_files(downloads_dir, target_isin):
    """
    Cycles through all XML files in the input directory, processes each,
    and prints ISIN/LEI pairs for each security described in the XML files.
    :param downloads_dir: Directory containing the XML files.
    """
    # Ensure the directory exists
    if not os.path.exists(downloads_dir):
        print(f"Directory '{downloads_dir}' does not exist.")
        return

    # Iterate through all files in the directory
    for file_name in os.listdir(downloads_dir):
        # Check if the file is an XML file
        if file_name.endswith(".xml"):
            file_path = os.path.join(downloads_dir, file_name)
            try:
                print(f"Processing file: {file_name}")
                #print_xml_root(file_path)
                #get_attributes_for_isin(file_path, "NL00150001S5") # Gives back all attributes, but in multple levels
                #test_get_attributes_for_isin(file_path, target_isin)
                #get_all_attributes_for_isin(file_path, "NL00150001S5") # gives all back in one list 1 to 1
                column_map = extract_attributes_for_isin(file_path, target_isin)
                if column_map:  # Only insert if column_map has data
                    
                    # Map the columns to match the DB schema
                    mapped_data = map_fields(column_map, FIELD_MAPPING)
                    print(f"Mapped data: {mapped_data}")
                    
                    # Insert into DB with the mapped data
                    insert_into_db(mapped_data)  
                else:
                    print(f"No data found for {file_path}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# Function to process all XML files in the given directory for CLI
def process_all_xml_files_cli(downloads_dir, target_isin, instrument_type="equity"):
    """
    Cycles through all XML files in the input directory, processes each,
    and prints ISIN/LEI pairs for each security described in the XML files.
    
    Args:
        downloads_dir (str): Directory containing the XML files
        target_isin (str): The ISIN to search for
        instrument_type (str): Type of instrument ('equity' or 'debt')
    """
    # Ensure the directory exists
    if not os.path.exists(downloads_dir):
        print(f"Directory '{downloads_dir}' does not exist.")
        return None

    # Determine the file prefix based on instrument type
    file_prefix = "FULINS_E_" if instrument_type == "equity" else "FULINS_D_"
    
    # Iterate through all files in the directory
    for file_name in os.listdir(downloads_dir):
        # Check if the file is an XML file and matches the instrument type
        if file_name.endswith(".xml") and file_name.startswith(file_prefix):
            file_path = os.path.join(downloads_dir, file_name)
            try:
                print(f"Looking in file: {file_name}")
                column_map = extract_attributes_for_isin(file_path, target_isin)
                if column_map and column_map.get('ISIN') == target_isin:
                    print(f"Matched ISIN: {target_isin}")
                    return column_map
                else:
                    print(f"No match for: {target_isin} in {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Only reached if no match was found in any file
    print(f"No data found for ISIN: {target_isin}")
    return None

# Function to print the root of the XML file and extract ISIN/LEI pairs, will not be used later
def print_xml_root(file_path: str):
    """
    Processes a single XML file, extracts ISIN/LEI pairs, and prints them.
    Limits the number of prints to 10 iterations.
    :param file_path: Path to the XML file.
    """
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
        
        # Extract and print the desired information
        ref_data_elements = root.xpath('//Document:RefData', namespaces=ns)
        
        # Limit prints to 10 iterations
        for i, ref_data in enumerate(ref_data_elements):
            if i >= 10:
                break  # Stop after 10 iterations
            isin = ref_data.xpath('Document:FinInstrmGnlAttrbts/Document:Id', namespaces=ns)[0].text
            lei = ref_data.xpath('Document:Issr', namespaces=ns)[0].text
            name = ref_data.xpath('Document:FinInstrmGnlAttrbts/Document:FullNm', namespaces=ns)[0].text
            print(isin, lei, name)

    except etree.XMLSyntaxError as e:
        print(f"Invalid XML in {file_path}: {e}")

# Function to print all tag names in the XML file, will not be used later
def get_attributes_for_isin(file_path, target_isin):
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Find the <RefData> block that contains the given ISIN
    ref_data_elements = root.xpath('//Document:RefData', namespaces=ns)

    for ref_data in ref_data_elements:
        isin_element = ref_data.xpath('Document:FinInstrmGnlAttrbts/Document:Id', namespaces=ns)

        if isin_element and isin_element[0].text == target_isin:
            print(f"\n--- Attributes for ISIN {target_isin} ---")

            # Iterate over all children of <RefData> and print their values
            for child in ref_data:
                tag_name = child.tag.split("}")[-1]  # Remove namespace
                
                # If the child has sub-elements, iterate over them
                sub_elements = list(child)
                if sub_elements:
                    print(f"\n{tag_name}:")  # Print the section name
                    for sub_element in sub_elements:
                        sub_tag = sub_element.tag.split("}")[-1]
                        sub_text = sub_element.text.strip() if sub_element.text else "None"
                        print(f"  {sub_tag}: {sub_text}")

                # If the child **has no sub-elements**, print its own text (e.g., `Issr`)
                else:
                    child_text = child.text.strip() if child.text else "None"
                    print(f"\n{tag_name}: {child_text}")  # Print the single value
            break


    tree = etree.parse(file_path)
    root = tree.getroot()
    
    unique_elements = set()  # Use a set to store unique element names

    for element in root.iter():
        tag_name = element.tag.split("}")[-1]  # Remove namespace
        unique_elements.add(tag_name)

    print("\n--- Unique Elements in XML ---")
    for tag in sorted(unique_elements):  # Sort for better readability
        print(tag)

# Function to print all tag names in the XML file, might be used later
def get_all_attributes_for_isin(file_path, target_isin):
    """
    Extract all attributes for the given ISIN from an XML file and print them in list 1to1.
    :param file_path: Path to the XML file.
    """
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Find the <RefData> block that contains the given ISIN
    ref_data_elements = root.xpath('//Document:RefData', namespaces=ns)
    
    all_columns = set()  # To track all unique column names (tags)

    for ref_data in ref_data_elements:
        isin_element = ref_data.xpath('Document:FinInstrmGnlAttrbts/Document:Id', namespaces=ns)

        if isin_element and isin_element[0].text == target_isin:
            print(f"\n--- Attributes for ISIN {target_isin} ---")
            
            column_values = {"isin": target_isin}  # Start with ISIN as the first column
            
            # Iterate over all possible elements and extract their data
            for possible_element in possible_elements:
                elements = ref_data.xpath(f'.//Document:{possible_element}', namespaces=ns)

                if elements:
                    for element in elements:
                        tag_name = element.tag.split("}")[-1]  # Remove namespace

                        # Skip if the parent tag is 'Id'
                        if tag_name == "Id":
                            continue
                        
                        # If the element has sub-elements, iterate over them
                        sub_elements = list(element)
                        if sub_elements:
                            for sub_element in sub_elements:
                                sub_tag = sub_element.tag.split("}")[-1]
                                sub_text = sub_element.text.strip() if sub_element.text else "None"
                                print(f"{tag_name}_{sub_tag}: {sub_text}")
                                
                                # Create the column name for sub-element
                                column_name = f"{tag_name}_{sub_tag}"
                                all_columns.add(column_name)
                                column_values[column_name] = sub_text
                        else:
                            # If no sub-elements, store the element's value
                            element_text = element.text.strip() if element.text else "None"
                            print(f"{tag_name}: {element_text}")
                            all_columns.add(tag_name)
                            column_values[tag_name] = element_text


    """
    Extract attributes for the given ISIN and return unique column names and values.
    """
    tree = etree.parse(file_path)
    root = tree.getroot()

    all_columns = set()  # To track all unique column names (tags)
    column_values = set()  # To track all unique values

    # Find all <RefData> blocks
    ref_data_elements = root.xpath('//Document:RefData', namespaces=ns)

    if not ref_data_elements:
        print("No <RefData> elements found. Check the XML structure.")
        return all_columns, column_values

    isin_found = False  # Flag to check if ISIN is found

    for ref_data in ref_data_elements:
        isin_element = ref_data.xpath('Document:FinInstrmGnlAttrbts/Document:Id', namespaces=ns)

        if isin_element and isin_element[0].text == target_isin:
            isin_found = True
            column_values.add(target_isin)  # Store ISIN as a value

            # Iterate over all child elements within <RefData>
            for element in ref_data.iter():
                tag_name = element.tag.split("}")[-1]  # Remove namespace

                # Skip "Id"
                if tag_name == "Id":
                    continue

                sub_elements = list(element)
                if sub_elements:
                    for sub_element in sub_elements:
                        sub_tag = sub_element.tag.split("}")[-1]
                        sub_text = sub_element.text.strip() if sub_element.text else "None"

                        column_name = f"{tag_name}_{sub_tag}"
                        all_columns.add(column_name)
                        column_values.add(sub_text)
                else:
                    element_text = element.text.strip() if element.text else "None"
                    all_columns.add(tag_name)
                    column_values.add(element_text)

    if not isin_found:
        print(f"ISIN {target_isin} not found in XML.")

    return all_columns, column_values

# Prints the extracted columns and values for a specific ISIN from the XML file using the function `extract_attributes_for_isin`
# This function is used for testing purposes and to determine the database table structure
# and the values to be inserted into the database
def test_get_attributes_for_isin(file_path, target_isin):
    """
    Test function to print the extracted columns and values.
    Returns True if the instrument was found, False otherwise.
    """
    result = extract_attributes_for_isin(file_path, target_isin)
    
    if result:  # If we found the instrument
        for column, value in result.items():
            print(f"{column}: {value}")
        return True
    return False

# Function to extract attributes for a specific ISIN from an XML file
def extract_attributes_for_isin(file_path, target_isin):
    """
    Extract attributes for the given ISIN from an XML file.

    :param file_path: Path to the XML file.
    :param target_isin: The ISIN to search for.
    :return: A dictionary mapping column names to values.
    """
    tree = etree.parse(file_path)
    root = tree.getroot()

    column_map = {}

    # Find all <RefData> blocks
    ref_data_elements = root.xpath('//Document:RefData', namespaces=ns)

    if not ref_data_elements:
        print(f"No <RefData> elements found in {file_path}.")
        return column_map

    isin_found = False

    for ref_data in ref_data_elements:
        isin_element = ref_data.xpath('Document:FinInstrmGnlAttrbts/Document:Id', namespaces=ns)

        if isin_element and isin_element[0].text == target_isin:
            isin_found = True
            column_map["ISIN"] = target_isin

            for element in ref_data.iter():
                tag_name = element.tag.split("}")[-1]  # Remove namespace

                if tag_name == "Id":
                    continue

                sub_elements = list(element)
                if sub_elements:
                    for sub_element in sub_elements:
                        sub_tag = sub_element.tag.split("}")[-1]
                        sub_text = sub_element.text.strip() if sub_element.text else "None"

                        column_name = f"{tag_name}_{sub_tag}"
                        column_map[column_name] = sub_text
                else:
                    element_text = element.text.strip() if element.text else "None"
                    column_map[tag_name] = element_text

    if not isin_found:
        print(f"ISIN {target_isin} not found in {file_path}.")

    return column_map

#Only used for testing purposes
def test_process_all_xml_files(downloads_dir, target_isin="NL00150001S5"):
    """
    Cycles through all XML files in the input directory, processes each,
    and prints ISIN/LEI pairs for each security described in the XML files.
    :param downloads_dir: Directory containing the XML files.
    """
    # Ensure the directory exists
    if not os.path.exists(downloads_dir):
        print(f"Directory '{downloads_dir}' does not exist.")
        return

    # Iterate through all files in the directory
    for file_name in os.listdir(downloads_dir):
        # Check if the file is an XML file
        if file_name.endswith(".xml"):
            file_path = os.path.join(downloads_dir, file_name)
            try:
                print(f"Processing file: {file_name}")
                #print_xml_root(file_path)
                #get_attributes_for_isin(file_path, "NL00150001S5") # Gives back all attributes, but in multple levels
                test_get_attributes_for_isin(file_path, target_isin) # Gives back all attributes, printed as ditcionary
                #get_all_attributes_for_isin(file_path, "NL00150001S5") # gives all back in one list 1 to 1
                #result = get_attributes_for_isin_to_db(file_path, target_isin)
                #print_all_tag_names(file_path)

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
   
# Example Usage for downloading an unzipping files to directory
#date = "2025-03-15"#datetime.today().strftime('%Y-%m-%d')  # Use today's date or specify manually
#download_urls = get_firds_file_urls(date)
#download_files(download_urls)

# Process all XML files in the directory
#downloads_dir = "../../downloads"
#process_all_xml_files(downloads_dir, target_isin="NL00150001S5")  # Specify the target ISIN
#test_process_all_xml_files(downloads_dir)
# Example for getting attributes for a specific ISIN


    