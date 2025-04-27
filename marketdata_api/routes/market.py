import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import Blueprint, jsonify, request, render_template
from marketdata_api.services.openfigi import search_openfigi, batch_search_openfigi
from marketdata_api.services.firds import get_firds_file_names
from marketdata_api.database.db import insert_into_db, map_fields, FIELD_MAPPING, DEBT_FIELD_MAPPING, insert_figi_data, get_figi_data, insert_lei_data
from marketdata_api.services.firds import process_all_xml_files_cli, downloads_dir
from scripts.frontend import search_isin_frontend, list_all_entries_frontend
from marketdata_api.database.db import get_db_connection
from marketdata_api.services.gleif import fetch_lei_info, map_lei_record

# Create a Blueprint for the market routes
market_bp = Blueprint("market", __name__)

# Route for the home page
@market_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Route to get market data for a specific ticker
@market_bp.route("/marketdata/<ticker>", methods=["GET"])
def get_market_data(ticker):
    data = search_openfigi(ticker)
    return jsonify(data)


    data = request.json
    query = data.get("query")

    # Debugging output
    print(f"Received search query: {query}")

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    result = search_openfigi(query)
    return jsonify(result)

# Route to handle batch search
@market_bp.route("/batch_search", methods=["POST"])
def batch_search():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    isin_list = file.read().decode("utf-8").splitlines()
    
    if not isin_list:
        return jsonify({"error": "File is empty"}), 400

    result = batch_search_openfigi(isin_list)
    return jsonify(result)

# Route to handle FIRDS file lookup
@market_bp.route('/firds', methods=['GET', 'POST'])
def firds_lookup():
    date = request.form.get('date')
    file_prefix = request.form.get('file_prefix')
    file_names = get_firds_file_names(date, file_prefix)

     # Print the file names to check if they are fetched correctly
    print(f"File names: {file_names}")

    # Check if the request is an AJAX request by checking the 'X-Requested-With' header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        response = jsonify(file_names=file_names)
        print(f"Returning JSON: {response.data}")  # Log the actual JSON response
        return response
    # If it's not an AJAX request, render the page with file names
    return render_template('index.html', file_names=file_names)

# Route to handle database operations list all db entries
@market_bp.route('/api/list', methods=['GET'])
def list_db_entries():
    """List all entries in the database with their FIGI data."""
    print("Starting list_db_entries")  # Debug
    entries = list_all_entries_frontend()
    print(f"List results: {entries}")  # Debug
    if entries:
        return jsonify(entries)
    else:
        return jsonify({"message": "No data found in database"}), 200

# Route to handle database operations search db entry by ISIN
@market_bp.route('/api/search/<string:isin>', methods=['GET'])
def search_db_entry(isin):
    """Handle search requests from the frontend."""
    try:
        print(f"Received search request for ISIN: {isin}")
        
        # Validate ISIN format
        if not isin or len(isin) != 12:
            return jsonify({"message": "Invalid ISIN format"}), 400
            
        # Search using the updated frontend function
        try:
            entry = search_isin_frontend(isin)
            print(f"Search result: {entry}")  # Debug log
            
            if not entry:
                return jsonify({"message": f"No data found for ISIN: {isin}"}), 404
                
            # Return the complete dataset
            return jsonify(entry), 200
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            return jsonify({"error": "Database error occurred"}), 500
        
    except Exception as e:
        print(f"Route error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# Route to handle database operations fetch and insert from frontend
@market_bp.route('/api/fetch', methods=['POST'])
def fetch_and_insert_frontend():
    """Fetch data from FI and insert into database."""
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        identifier_type = data.get('identifier_type')
        
        print(f"Received fetch request for identifier: {identifier}, type: {identifier_type}")  # Debug
        
        if not identifier or not identifier_type:
            return jsonify({'error': 'Missing identifier or identifier_type'}), 400

        # First check if the ISIN exists in either table
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check in both tables and get TradingVenueID
        cursor.execute("""
            SELECT 'equity' as type, TradingVenueID FROM firds_e WHERE ISIN = ? 
            UNION 
            SELECT 'debt' as type, TradingVenueID FROM firds_d WHERE ISIN = ?
        """, (identifier, identifier))
        existing_record = cursor.fetchone()
        conn.close()

        if existing_record:
            instrument_type = existing_record[0]
            trading_venue_id = existing_record[1]
            print(f"ISIN {identifier} exists in {instrument_type} table with MIC: {trading_venue_id}")  # Debug
            
            # Get IssuerLEI for existing record
            conn = get_db_connection()
            cursor = conn.cursor()
            table = "firds_e" if instrument_type == "equity" else "firds_d"
            cursor.execute(f"SELECT IssuerLEI FROM {table} WHERE ISIN = ?", (identifier,))
            lei_record = cursor.fetchone()
            conn.close()

            if lei_record and lei_record[0]:
                try:
                    lei_response = fetch_lei_info(lei_record[0])
                    if 'error' not in lei_response:
                        lei_data = map_lei_record(lei_response)
                        insert_lei_data(lei_data)
                except Exception as lei_error:
                    print(f"Error processing LEI data: {str(lei_error)}")
            
            # Check if FIGI data already exists
            existing_figi = get_figi_data(identifier)
            print(f"Existing FIGI data: {existing_figi}")  # Debug
            
            if not existing_figi:
                print(f"No FIGI data found for ISIN {identifier}, fetching from OpenFIGI...")  # Debug
                # Fetch FIGI data from OpenFIGI using TradingVenueID
                # If TradingVenueID is None, we can still search by ISIN only
                if instrument_type == "equity":
                    figi_data = search_openfigi(identifier, trading_venue_id)
                    print(f"OpenFIGI response: {figi_data}")  # Debug
                else:
                    figi_data = search_openfigi(identifier)
                    print(f"OpenFIGI response: {figi_data}")

                if figi_data and len(figi_data) > 0:
                    figi_result = figi_data[0]
                    # Prepare FIGI data for database
                    figi_db_data = {
                        'ISIN': identifier,
                        'FIGI': figi_result.get('figi'),
                        'CompositeFIGI': figi_result.get('compositeFIGI'),
                        'ShareClassFIGI': figi_result.get('shareClassFIGI'),
                        'Ticker': figi_result.get('ticker'),
                        'SecurityType': figi_result.get('securityType'),
                        'MarketSector': figi_result.get('marketSector'),
                        'SecurityDescription': figi_result.get('securityDescription')
                    }
                    print(f"Prepared FIGI data for DB: {figi_db_data}")  # Debug
                    # Insert FIGI data
                    insert_figi_data(figi_db_data)
                    return jsonify({
                        'message': f'Added FIGI data for existing ISIN {identifier}',
                        'figi_data': figi_data[0],
                        'instrument_type': instrument_type
                    })
                else:
                    return jsonify({
                        'message': f'ISIN {identifier} exists but no FIGI data found',
                        'status': 'exists_no_figi',
                        'instrument_type': instrument_type
                    })
            else:
                return jsonify({
                    'message': f'ISIN {identifier} exists with FIGI data',
                    'status': 'exists_with_figi',
                    'figi_data': existing_figi,
                    'instrument_type': instrument_type
                })
            
        # Try to find the ISIN in equity files first
        result = process_all_xml_files_cli(downloads_dir, identifier, instrument_type="equity")
        if result:
            mapped_data = map_fields(result, FIELD_MAPPING)
            insert_into_db(mapped_data, "equity")
            
            # Process LEI data if available
            if mapped_data.get('IssuerLEI'):
                try:
                    lei_response = fetch_lei_info(mapped_data['IssuerLEI'])
                    if 'error' not in lei_response:
                        lei_data = map_lei_record(lei_response)
                        insert_lei_data(lei_data)
                except Exception as lei_error:
                    print(f"Error processing LEI data: {str(lei_error)}")
                    # Continue execution even if LEI processing fails
            
            # Get TradingVenueID for the newly inserted record
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TradingVenueID FROM firds_e WHERE ISIN = ?", (identifier,))
            venue_record = cursor.fetchone()
            conn.close()
            
            trading_venue_id = venue_record[0] if venue_record else None
            
            # Fetch FIGI data using both ISIN and TradingVenueID (MIC)
            figi_data = search_openfigi(identifier, trading_venue_id)
            if figi_data and len(figi_data) > 0:
                figi_result = figi_data[0]
                figi_db_data = {
                    'ISIN': identifier,
                    'FIGI': figi_result.get('figi'),
                    'CompositeFIGI': figi_result.get('compositeFIGI'),
                    'ShareClassFIGI': figi_result.get('shareClassFIGI'),
                    'Ticker': figi_result.get('ticker'),
                    'SecurityType': figi_result.get('securityType'),
                    'MarketSector': figi_result.get('marketSector'),
                    'SecurityDescription': figi_result.get('securityDescription')
                }
                insert_figi_data(figi_db_data)
                return jsonify({
                    'message': 'Data successfully fetched and stored as equity with FIGI data',
                    'fi_data': mapped_data,
                    'figi_data': figi_data[0],
                    'instrument_type': 'equity'
                })
            return jsonify({
                'message': 'Data successfully fetched and stored as equity (no FIGI data found)',
                'fi_data': mapped_data,
                'instrument_type': 'equity'
            })
            
        # If not found in equity files, try debt files
        result = process_all_xml_files_cli(downloads_dir, identifier, instrument_type="debt")
        if result:
            mapped_data = map_fields(result, DEBT_FIELD_MAPPING)
            insert_into_db(mapped_data, "debt")
            
            # Process LEI data if available
            if mapped_data.get('IssuerLEI'):
                try:
                    lei_response = fetch_lei_info(mapped_data['IssuerLEI'])
                    if 'error' not in lei_response:
                        lei_data = map_lei_record(lei_response)
                        insert_lei_data(lei_data)
                except Exception as lei_error:
                    print(f"Error processing LEI data: {str(lei_error)}")
                    # Continue execution even if LEI processing fails
            
            # Get TradingVenueID for the newly inserted record
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TradingVenueID FROM firds_d WHERE ISIN = ?", (identifier,))
            venue_record = cursor.fetchone()
            conn.close()
            
            trading_venue_id = venue_record[0] if venue_record else None
            
            # Fetch FIGI data using only ISIN
            figi_data = search_openfigi(identifier)
            if figi_data and len(figi_data) > 0:
                figi_result = figi_data[0]
                figi_db_data = {
                    'ISIN': identifier,
                    'FIGI': figi_result.get('figi'),
                    'CompositeFIGI': figi_result.get('compositeFIGI'),
                    'ShareClassFIGI': figi_result.get('shareClassFIGI'),
                    'Ticker': figi_result.get('ticker'),
                    'SecurityType': figi_result.get('securityType'),
                    'MarketSector': figi_result.get('marketSector'),
                    'SecurityDescription': figi_result.get('securityDescription')
                }
                insert_figi_data(figi_db_data)
                return jsonify({
                    'message': 'Data successfully fetched and stored as debt with FIGI data',
                    'fi_data': mapped_data,
                    'figi_data': figi_data[0],
                    'instrument_type': 'debt'
                })
            return jsonify({
                'message': 'Data successfully fetched and stored as debt (no FIGI data found)',
                'fi_data': mapped_data,
                'instrument_type': 'debt'
            })
            
        return jsonify({'error': 'No data found for the given identifier'}), 404
        
    except Exception as e:
        print(f"Error in fetch_and_insert_frontend: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 500

@market_bp.route('/api/figi/<string:figi>', methods=['GET'])
def get_isin_by_figi(figi):
    """Look up ISIN by FIGI in the isin_figi_map table."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if isin_figi_map table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='isin_figi_map'")
        if not cursor.fetchone():
            return jsonify({"error": "isin_figi_map table does not exist"}), 404
            
        # Look up ISIN by FIGI
        cursor.execute("SELECT ISIN FROM isin_figi_map WHERE FIGI = ?", (figi,))
        result = cursor.fetchone()
        
        if result:
            return jsonify({"ISIN": result[0]})
        else:
            return jsonify({"error": f"No ISIN found for FIGI: {figi}"}), 404
            
    except Exception as e:
        print(f"Error in get_isin_by_figi: {str(e)}")  # Debug
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@market_bp.route("/api/gleif", methods=["POST"])
def get_lei_info():
    data = request.get_json()
    lei_code = data.get("lei")
    
    if not lei_code:
        return jsonify({"error": "LEI code is required"}), 400
    
    result = fetch_lei_info(lei_code)
    return jsonify(result)