import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import Blueprint, jsonify, request, render_template
from marketdata_api.services.openfigi import search_openfigi, batch_search_openfigi
from marketdata_api.services.firds import get_firds_file_names
from marketdata_api.services.gleif import fetch_lei_info
from ..services.instrument_service import InstrumentService
from ..models.instrument import Instrument, Equity, Debt
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for the market routes
market_bp = Blueprint("market", __name__)

# Error handler for database errors
@market_bp.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    return jsonify({"error": "A database error occurred"}), 500

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


# Route to handle database operations search db entry by ISIN
@market_bp.route('/api/search/<string:isin>', methods=['GET'])
def search_db_entry(isin):
    """Handle search requests from the frontend."""
    try:
        service = InstrumentService()
        session, instrument = service.get_instrument(isin)
        
        if not instrument:
            return jsonify({"message": f"No data found for ISIN: {isin}"}), 404
            
        result = {
            "instrument": {
                "id": instrument.id,
                "type": instrument.type,
                "isin": instrument.isin,
                "full_name": instrument.full_name,
                "short_name": instrument.short_name,
                "symbol": instrument.symbol,
                "cfi_code": instrument.cfi_code,
                "currency": instrument.currency,
                "trading_venue": instrument.trading_venue,
                "relevant_authority": instrument.relevant_authority,
                "relevant_venue": instrument.relevant_venue,
                "commodity_derivative": instrument.commodity_derivative
            }
        }
        
        if instrument.figi_mapping:
            result["figi"] = {
                "figi": instrument.figi_mapping.figi,
                "composite_figi": instrument.figi_mapping.composite_figi,
                "share_class_figi": instrument.figi_mapping.share_class_figi,
                "security_type": instrument.figi_mapping.security_type,
                "market_sector": instrument.figi_mapping.market_sector
            }
            
        if instrument.legal_entity:
            result["lei"] = {
                "lei": instrument.legal_entity.lei,
                "name": instrument.legal_entity.name,
                "jurisdiction": instrument.legal_entity.jurisdiction,
                "legal_form": instrument.legal_entity.legal_form,
                "status": instrument.legal_entity.status
            }
            
        session.close()
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle database operations fetch and insert from frontend
@market_bp.route('/api/fetch', methods=['POST'])
def fetch_and_insert_frontend():
    """Fetch and insert data using SQLAlchemy models"""
    try:
        data = request.get_json()
        identifier = data.get('Id')
        instrument_type = data.get('type', 'equity')
        
        if not identifier:
            return jsonify({'error': 'Missing identifier'}), 400

        service = InstrumentService()
        instrument = service.get_or_create_instrument(identifier, instrument_type)
        
        if not instrument:
            return jsonify({'error': 'Unable to fetch or create instrument'}), 404
            
        # Enrich the instrument with FIGI and LEI data
        session, enriched = service.enrich_instrument(instrument)
        if session:
            session.close()

        return jsonify({
            'message': f'Successfully fetched/created and enriched {instrument_type} instrument',
            'instrument_id': enriched.id,
            'instrument_type': enriched.type,
            'isin': enriched.isin,
            'figi': enriched.figi_mapping.figi if enriched.figi_mapping else None,
            'lei': enriched.legal_entity.lei if enriched.legal_entity else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@market_bp.route("/api/gleif", methods=["POST"])
def get_lei_info():
    data = request.get_json()
    lei_code = data.get("lei")
    
    if not lei_code:
        return jsonify({"error": "LEI code is required"}), 400
    
    result = fetch_lei_info(lei_code)
    return jsonify(result)


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