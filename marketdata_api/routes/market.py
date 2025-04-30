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
from ..services.instrument_service import InstrumentService
from ..models.instrument import Instrument, Equity, Debt

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
    """Fetch and insert data using SQLAlchemy models"""
    try:
        data = request.get_json()
        identifier = data.get('identifier')
        instrument_type = data.get('instrument_type', 'equity')
        
        if not identifier:
            return jsonify({'error': 'Missing identifier'}), 400

        service = InstrumentService()
        instrument = service.create_instrument(data, instrument_type)
        
        return jsonify({
            'message': f'Data successfully stored as {instrument_type}',
            'instrument_id': instrument.id,
            'instrument_type': instrument_type
        })
    except Exception as e:
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

@market_bp.route('/api/instruments', methods=['GET'])
def list_instruments():
    """List all instruments using SQLAlchemy"""
    try:
        service = InstrumentService()
        with get_session() as session:
            instruments = session.query(Instrument).all()
            return jsonify([{
                'id': i.id,
                'type': i.type,
                'isin': i.isin,
                'name': i.full_name,
                'symbol': i.symbol,
                'last_updated': i.last_updated.isoformat() if i.last_updated else None
            } for i in instruments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/api/instruments/<identifier>', methods=['GET'])
def get_instrument(identifier):
    """Get instrument by ID, ISIN, or symbol using SQLAlchemy"""
    try:
        service = InstrumentService()
        instrument = service.get_instrument(identifier)
        if not instrument:
            return jsonify({'error': 'Instrument not found'}), 404
            
        return jsonify({
            'id': instrument.id,
            'type': instrument.type,
            'isin': instrument.isin,
            'name': instrument.full_name,
            'symbol': instrument.symbol,
            'figi': instrument.figi,
            'additional_data': instrument.additional_data,
            'last_updated': instrument.last_updated.isoformat() if instrument.last_updated else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/api/test/instrument', methods=['POST'])
def test_instrument_creation():
    """Test route for instrument creation"""
    try:
        data = request.get_json()
        service = InstrumentService()
        instrument = service.create_instrument(data, data.get('type', 'equity'))
        
        return jsonify({
            'message': 'Test successful',
            'instrument_id': instrument.id,
            'type': instrument.type,
            'isin': instrument.isin
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500