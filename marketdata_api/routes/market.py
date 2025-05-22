import os
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import Blueprint, jsonify, request, render_template
from marketdata_api.services.openfigi import search_openfigi, batch_search_openfigi
from marketdata_api.services.firds import get_firds_file_names
from marketdata_api.services.gleif import fetch_lei_info
from marketdata_api.database.session import get_session
from ..services.instrument_service import InstrumentService
from ..models.instrument import Instrument, Equity, Debt, Future
from sqlalchemy.exc import SQLAlchemyError
from marketdata_api.models.utils.cfi import CFI

# Setup logging
logger = logging.getLogger(__name__)

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
                "commodity_derivative": instrument.commodity_derivative,
                "first_trade_date": instrument.first_trade_date.isoformat() if instrument.first_trade_date else None,
                "termination_date": instrument.termination_date.isoformat() if getattr(instrument, "termination_date", None) else None,
                "basket_isin": getattr(instrument, "basket_isin", None),
                "basket_lei": getattr(instrument, "basket_lei", None),
                "underlying_index_isin": getattr(instrument, "underlying_index_isin", None),
                "underlying_single_isin": getattr(instrument, "underlying_single_isin", None),
                "basket_isin": getattr(instrument, "basket_isin", None),
                "underlying_index_isin": getattr(instrument, "underlying_index_isin", None),
                "underlying_single_index_name": getattr(instrument, "underlying_single_index_name", None)
            }
        }

        # Add contract data fields for futures
        if instrument.type == "future":
            result["instrument"].update({
                "expiration_date": getattr(instrument, "expiration_date", None),
                "price_multiplier": getattr(instrument, "price_multiplier", None),
                "delivery_type": getattr(instrument, "delivery_type", None)
            })

        # Add debt-specific fields
        if instrument.type == "debt":
            result["instrument"].update({
                "maturity_date": instrument.maturity_date.isoformat() if instrument.maturity_date else None,
                "total_issued_nominal": instrument.total_issued_nominal,
                "nominal_value_per_unit": instrument.nominal_value_per_unit,
                "debt_seniority": instrument.debt_seniority,
                "floating_rate_term_unit": instrument.floating_rate_term_unit,
                "floating_rate_term_value": instrument.floating_rate_term_value,
                "floating_rate_basis_points_spread": instrument.floating_rate_basis_points_spread,
                "interest_rate_floating_reference_index": instrument.interest_rate_floating_reference_index
            })

        # Add CFI decoded output if available
        cfi_code = instrument.cfi_code
        if cfi_code and len(cfi_code) == 6:
            try:
                cfi = CFI(cfi_code)
                result["instrument"]["cfi_decoded"] = cfi.describe()
            except Exception as e:
                result["instrument"]["cfi_decoded"] = {"error": str(e)}

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
                "status": instrument.legal_entity.status,
                "creation_date": instrument.legal_entity.creation_date.isoformat() if instrument.legal_entity.creation_date else None
            }

        # Add Derivatives section: ISINs and symbols of futures where this ISIN is underlying
        if instrument.type == "equity":
            future_rows = session.query(Future.isin, Future.symbol).filter(
                (Future.underlying_single_isin == isin) |
                (Future.basket_isin == isin) |
                (Future.underlying_index_isin == isin)
            ).all()
            result["derivatives"] = [
                {"isin": f[0], "symbol": f[1]} for f in future_rows if f[0]
            ]

        # Add underlying instrument symbol for futures
        if instrument.type == "future":
            underlying_isin = (
                getattr(instrument, "underlying_single_isin", None)
                or getattr(instrument, "basket_isin", None)
                or getattr(instrument, "underlying_index_isin", None)
            )
            underlying_full_name = None
            if underlying_isin:
                underlying_inst = session.query(Instrument).filter_by(isin=underlying_isin).first()
                if underlying_inst:
                    underlying_full_name = underlying_inst.full_name
            result["underlying_instrument"] = {"full_name": underlying_full_name}

        session.close()
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle database operations fetch and insert from frontend
@market_bp.route('/api/fetch', methods=['POST'])
def fetch_and_insert_frontend():
    """Fetch and insert data using SQLAlchemy models."""
    try:
        data = request.get_json()
        identifier = data.get('Id')
        instrument_type = data.get('Category')
        
        if not identifier:
            return jsonify({'error': 'Missing identifier'}), 400
        if not instrument_type:
            return jsonify({'error': 'Missing instrument category'}), 400

        service = InstrumentService()
        with get_session() as session:
            # Get or create the instrument with specified type
            instrument = service.get_or_create_instrument(identifier, instrument_type)
            if not instrument:
                logger.warning(f"Unable to fetch or create instrument: {identifier}")
                return jsonify({'error': 'Unable to fetch or create instrument'}), 404

            # Enrich the instrument
            session, enriched = service.enrich_instrument(instrument)
            
            # Build response with enrichment status
            response_data = {
                'message': f'Successfully processed instrument',
                'instrument_id': enriched.id,
                'instrument_type': enriched.type,
                'isin': enriched.isin,
                'figi': enriched.figi_mapping.figi if enriched.figi_mapping else None,
                'lei': enriched.legal_entity.lei if enriched.legal_entity else None
            }
            
            logger.info(f"Successfully processed {instrument_type} instrument {identifier}")
            return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in fetch_and_insert: {str(e)}")
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