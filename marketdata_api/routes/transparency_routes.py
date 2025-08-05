import logging
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload
from ..interfaces.factory.services_factory import ServicesFactory
from ..constants import (
    HTTPStatus, Pagination, API, ErrorMessages, SuccessMessages,
    ResponseFields, Endpoints, QueryParams, FormFields, DbFields
)
from typing import Dict, Any
from ..database.session import SessionLocal

# Setup logging
logging.basicConfig(level=logging.INFO)  # Standard logging level
logger = logging.getLogger(__name__)

# Create blueprint for transparency operations
transparency_bp = Blueprint("transparency", __name__, url_prefix=API.PREFIX)

@transparency_bp.route(Endpoints.TRANSPARENCY, methods=["GET"])
def list_transparency_calculations():
    """Get all transparency calculations with optional filtering"""
    try:
        # Query parameters for filtering
        calculation_type = request.args.get('calculation_type')
        instrument_type = request.args.get('instrument_type')
        isin = request.args.get('isin')
        limit = request.args.get(QueryParams.LIMIT, Pagination.DEFAULT_LIMIT, type=int)
        offset = request.args.get(QueryParams.OFFSET, Pagination.DEFAULT_OFFSET, type=int)
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        logger.info(f"GET /transparency with params: calculation_type={calculation_type}, instrument_type={instrument_type}, isin={isin}, page={page}, per_page={per_page}")
        
        # Get the correct TransparencyCalculation model from factory
        from ..database.factory.database_factory import DatabaseFactory
        db = DatabaseFactory.create_database()
        models = db.get_models()
        TransparencyCalculation = models.get('TransparencyCalculation')
        
        # Create a new session for this query
        session = SessionLocal()
        try:
            # Build query with eager loading - this approach consistently works
            query = session.query(TransparencyCalculation)
            
            # Add eager loading for related entities
            query = query.options(
                joinedload(TransparencyCalculation.equity_transparency),
                joinedload(TransparencyCalculation.non_equity_transparency),
                joinedload(TransparencyCalculation.debt_transparency),
                joinedload(TransparencyCalculation.futures_transparency)
            )
            
            # Apply filters
            if calculation_type:
                query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
                logger.info(f"Applied calculation_type filter: {calculation_type}")
            
            if isin:
                query = query.filter(TransparencyCalculation.isin == isin)
                logger.info(f"Applied isin filter: {isin}")
            
            # Get total count for pagination
            total_count = query.count()
            logger.info(f"Found {total_count} total transparency calculations matching filters")
            
            # Apply pagination
            if page and per_page:
                offset = (page - 1) * per_page
                query = query.offset(offset).limit(per_page)
            else:
                query = query.limit(limit).offset(offset)
            
            # Execute query
            calculations = query.all()
            logger.info(f"Retrieved {len(calculations)} transparency calculations after pagination")
            
            # Format calculations using the direct formatting approach that works
            result = []
            for calc in calculations:
                formatted_calc = direct_format_transparency(calc)
                if formatted_calc:
                    result.append(formatted_calc)
            
            logger.info(f"Formatted {len(result)} calculations for response")
            
            # Return the data in the expected format - same as get_transparency_by_isin
            return jsonify({
                ResponseFields.STATUS: f"{HTTPStatus.OK} OK",
                ResponseFields.DATA: result,
                ResponseFields.META: {
                    ResponseFields.PAGE: page,
                    ResponseFields.PER_PAGE: per_page,
                    ResponseFields.TOTAL: total_count
                }
            })
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error in list_transparency_calculations: {str(e)}")
        logger.exception(e)  # Log the full traceback
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error", 
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/<string:transparency_id>", methods=["GET"])
def get_transparency_calculation(transparency_id):
    """Get transparency calculation by ID"""
    try:
        service = ServicesFactory.get_transparency_service()
        session, calculation = service.get_transparency_by_id(transparency_id)
        
        if not calculation:
            session.close()
            return jsonify({ResponseFields.ERROR: "Transparency calculation not found"}), HTTPStatus.NOT_FOUND
        
        # Build comprehensive response
        result = {
            "id": calculation.id,
            "isin": calculation.isin,
            "calculation_type": calculation.calculation_type,
            "tech_record_id": calculation.tech_record_id,
            "from_date": calculation.from_date.isoformat() if calculation.from_date else None,
            "to_date": calculation.to_date.isoformat() if calculation.to_date else None,
            "liquidity": calculation.liquidity,
            "total_transactions_executed": calculation.total_transactions_executed,
            "total_volume_executed": calculation.total_volume_executed,
            "statistics": calculation.statistics,
            "created_at": calculation.created_at.isoformat() if calculation.created_at else None,
            "updated_at": calculation.updated_at.isoformat() if calculation.updated_at else None
        }
        
        # Add type-specific details
        if calculation.calculation_type == "EQUITY" and hasattr(calculation, 'equity_transparency'):
            et = calculation.equity_transparency
            result["equity_transparency"] = {
                "financial_instrument_classification": et.financial_instrument_classification,
                "methodology": et.methodology,
                "average_daily_turnover": et.average_daily_turnover,
                "large_in_scale": et.large_in_scale,
                "average_daily_number_of_transactions": et.average_daily_number_of_transactions,
                "secondary_id": et.secondary_id,
                "average_daily_transactions_secondary": et.average_daily_transactions_secondary,
                "average_transaction_value": et.average_transaction_value,
                "standard_market_size": et.standard_market_size
            }
        elif calculation.calculation_type == "NON_EQUITY":
            if hasattr(calculation, 'debt_transparency'):
                dt = calculation.debt_transparency
                result["debt_transparency"] = {
                    "description": dt.description,
                    "criterion_name": dt.criterion_name,
                    "criterion_value": dt.criterion_value,
                    "financial_instrument_classification": dt.financial_instrument_classification,
                    "bond_type": dt.bond_type,
                    "security_type": dt.security_type,
                    "is_securitised_derivative": dt.is_securitised_derivative,
                    "is_corporate_bond": dt.is_corporate_bond,
                    "is_liquid": dt.is_liquid,
                    "pre_trade_large_in_scale_threshold": dt.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": dt.post_trade_large_in_scale_threshold
                }
            elif hasattr(calculation, 'futures_transparency'):
                ft = calculation.futures_transparency
                result["futures_transparency"] = {
                    "description": ft.description,
                    "criterion_name": ft.criterion_name,
                    "criterion_value": ft.criterion_value,
                    "financial_instrument_classification": ft.financial_instrument_classification,
                    "underlying_isin": ft.underlying_isin,
                    "is_stock_dividend_future": ft.is_stock_dividend_future,
                    "pre_trade_large_in_scale_threshold": ft.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": ft.post_trade_large_in_scale_threshold,
                    "pre_trade_large_in_scale_threshold_nb": ft.pre_trade_large_in_scale_threshold_nb,
                    "post_trade_large_in_scale_threshold_nb": ft.post_trade_large_in_scale_threshold_nb
                }
            elif hasattr(calculation, 'non_equity_transparency'):
                net = calculation.non_equity_transparency
                result["non_equity_transparency"] = {
                    "description": net.description,
                    "criterion_name": net.criterion_name,
                    "criterion_value": net.criterion_value,
                    "financial_instrument_classification": net.financial_instrument_classification,
                    "criterion_name_secondary": net.criterion_name_secondary,
                    "criterion_value_secondary": net.criterion_value_secondary,
                    "pre_trade_large_in_scale_threshold": net.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": net.post_trade_large_in_scale_threshold
                }
        
        session.close()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_transparency_calculation: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(Endpoints.TRANSPARENCY, methods=["POST"])
def create_transparency_calculation():
    """Create transparency calculations from FITRS data for a given ISIN"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        # Get required parameters
        isin = data.get('isin')
        instrument_type = data.get('instrument_type')
        
        if not isin:
            return jsonify({ResponseFields.ERROR: "ISIN is required"}), HTTPStatus.BAD_REQUEST
        
        if not instrument_type:
            return jsonify({ResponseFields.ERROR: "instrument_type is required"}), HTTPStatus.BAD_REQUEST
        
        logger.info(f"Creating transparency calculations for ISIN={isin}, instrument_type={instrument_type}")
        
        # 1. Check if instrument exists, if not create it
        from ..interfaces.factory.services_factory import ServicesFactory
        instrument_service = ServicesFactory.get_instrument_service()
        
        # First check if instrument exists
        session, instrument = instrument_service.get_instrument(isin)
        if session:
            session.close()
        
        if not instrument:
            logger.info(f"Instrument {isin} not found, creating from FITRS data")
            # Create instrument using FITRS data
            instrument = instrument_service.get_or_create_instrument(
                isin=isin,
                instrument_type=instrument_type,
                create_from_fitrs=True
            )
            
            if not instrument:
                return jsonify({
                    ResponseFields.ERROR: f"Failed to create instrument {isin} from FITRS data"
                }), HTTPStatus.BAD_REQUEST
        
        # 2. Derive calculation_type from instrument_type
        calculation_type = "EQUITY" if instrument_type.lower() == "equity" else "NON_EQUITY"
        logger.info(f"Derived calculation_type={calculation_type} from instrument_type={instrument_type}")
        
        # 3. Use TransparencyService to get transparency data from FITRS
        service = ServicesFactory.get_transparency_service()
        
        # Get or create transparency calculations - remove the unsupported fetch_from_fitrs parameter
        created_calculations = service.get_or_create_transparency_calculation(
            isin=isin,
            calculation_type=calculation_type,
            ensure_instrument=True
        )
        
        # Ensure we have a list
        if not isinstance(created_calculations, list):
            created_calculations = [created_calculations] if created_calculations else []
        
        # Filter out None values
        created_calculations = [calc for calc in created_calculations if calc is not None]
        
        if not created_calculations:
            return jsonify({
                ResponseFields.ERROR: f"No transparency data found for ISIN {isin}"
            }), HTTPStatus.NOT_FOUND
        
        # 4. Format response with created calculations
        result = []
        for calc in created_calculations:
            formatted_calc = direct_format_transparency(calc)
            if formatted_calc:
                result.append(formatted_calc)
        
        logger.info(f"Successfully created {len(result)} transparency calculations for ISIN {isin}")
        
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.CREATED} Created",
            ResponseFields.MESSAGE: f"Successfully created {len(result)} transparency calculations",
            ResponseFields.DATA: result,
            ResponseFields.META: {
                "isin": isin,
                "instrument_type": instrument_type,
                "calculation_type": calculation_type,
                "total_created": len(result)
            }
        }), HTTPStatus.CREATED
        
    except Exception as e:
        logger.error(f"Error in create_transparency_calculation: {str(e)}")
        logger.exception(e)
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error",
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/<string:transparency_id>", methods=["PUT"])
def update_transparency_calculation(transparency_id):
    """Update an existing transparency calculation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        service = ServicesFactory.get_transparency_service()
        calculation = service.update_transparency_calculation(transparency_id, data)
        
        if not calculation:
            return jsonify({ResponseFields.ERROR: "Transparency calculation not found"}), HTTPStatus.NOT_FOUND
        
        return jsonify({
            ResponseFields.MESSAGE: "Transparency calculation updated successfully",
            "id": calculation.id,
            "isin": calculation.isin,
            "calculation_type": calculation.calculation_type
        })
        
    except Exception as e:
        logger.error(f"Error in update_transparency_calculation: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/<string:transparency_id>", methods=["DELETE"])
def delete_transparency_calculation(transparency_id):
    """Delete a transparency calculation"""
    try:
        service = ServicesFactory.get_transparency_service()
        result = service.delete_transparency_calculation(transparency_id)
        
        if not result:
            return jsonify({ResponseFields.ERROR: "Transparency calculation not found"}), HTTPStatus.NOT_FOUND
        
        return jsonify({
            ResponseFields.MESSAGE: "Transparency calculation deleted successfully",
            "id": transparency_id
        })
        
    except Exception as e:
        logger.error(f"Error in delete_transparency_calculation: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/isin/<string:isin>", methods=["GET"])
def get_transparency_by_isin(isin):
    """Get transparency calculations for a specific ISIN"""
    try:
        calculation_type = request.args.get(QueryParams.CALCULATION_TYPE)
        ensure_instrument = request.args.get('ensure_instrument', 'false').lower() == 'true'
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        logger.info(f"GET transparency for ISIN={isin}, calculation_type={calculation_type}, ensure_instrument={ensure_instrument}")
        
        # Get the correct TransparencyCalculation model from factory
        from ..database.factory.database_factory import DatabaseFactory
        db = DatabaseFactory.create_database()
        models = db.get_models()
        TransparencyCalculation = models.get('TransparencyCalculation')
        
        # Direct database query approach that we know works from direct_test.py
        session = SessionLocal()
        
        try:
            # Query for existing calculations
            query = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.isin == isin
            )
            
            if calculation_type:
                query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
            
            # Add eager loading for related entities
            query = query.options(
                joinedload(TransparencyCalculation.equity_transparency),
                joinedload(TransparencyCalculation.non_equity_transparency),
                joinedload(TransparencyCalculation.debt_transparency),
                joinedload(TransparencyCalculation.futures_transparency)
            )
            
            calculations = query.all()
            logger.info(f"Found {len(calculations)} transparency calculations for ISIN {isin}")
            
            # If no existing calculations and ensure_instrument is true, create them
            if not calculations and ensure_instrument:
                session.close()
                session = None
                
                service = ServicesFactory.get_transparency_service()
                logger.info(f"No calculations found, creating new ones with ensure_instrument=True")
                
                created_calcs = service.get_or_create_transparency_calculation(
                    isin=isin,
                    calculation_type=calculation_type or 'EQUITY',
                    ensure_instrument=True
                )
                
                # Ensure we have a list
                if not isinstance(created_calcs, list):
                    created_calcs = [created_calcs] if created_calcs else []
                    
                logger.info(f"Created {len(created_calcs)} new calculations")
                
                if created_calcs:
                    # Open a new session to query the newly created calculations
                    session = SessionLocal()
                    # Get the correct TransparencyCalculation model from factory
                    from ..database.factory.database_factory import DatabaseFactory
                    db = DatabaseFactory.create_database()
                    models = db.get_models()
                    TransparencyCalculation = models.get('TransparencyCalculation')
                    
                    ids = [calc.id for calc in created_calcs if calc and hasattr(calc, 'id')]
                    
                    if ids:
                        query = session.query(TransparencyCalculation).filter(
                            TransparencyCalculation.id.in_(ids)
                        ).options(
                            joinedload(TransparencyCalculation.equity_transparency),
                            joinedload(TransparencyCalculation.non_equity_transparency),
                            joinedload(TransparencyCalculation.debt_transparency),
                            joinedload(TransparencyCalculation.futures_transparency)
                        )
                        
                        calculations = query.all()
                        logger.info(f"Retrieved {len(calculations)} newly created calculations")
                    else:
                        calculations = []
            
            # Format calculations using the direct formatting approach that works
            result = []
            for calc in calculations:
                if calc:
                    formatted_calc = direct_format_transparency(calc)
                    if formatted_calc:
                        result.append(formatted_calc)
                        logger.debug(f"Successfully formatted calculation: {calc.id}")
                    else:
                        logger.warning(f"Failed to format calculation: {calc.id}")
            
            logger.info(f"Formatted {len(result)} calculations for response")
            
            # If no results found and ensure_instrument is true, return a minimal response
            if not result and ensure_instrument:
                logger.warning(f"No valid calculations found for {isin}, returning minimal response")
                calculation_type = calculation_type or "EQUITY"
                
                minimal_response = {
                    "id": None,
                    "isin": isin,
                    "calculation_type": calculation_type,
                    "tech_record_id": None,
                    "from_date": None,
                    "to_date": None,
                    "liquidity": None,
                    "total_transactions_executed": None,
                    "total_volume_executed": None,
                    "created_at": None,
                    "updated_at": None,
                }
                
                # Add minimal details based on calculation_type
                if calculation_type == "EQUITY":
                    minimal_response["details"] = {
                        "financial_instrument_classification": None,
                        "methodology": None,
                        "average_daily_turnover": None,
                        "large_in_scale": None,
                        "average_daily_number_of_transactions": None,
                        "average_transaction_value": None,
                        "standard_market_size": None,
                        "type": "equity"
                    }
                else:
                    minimal_response["details"] = {
                        "description": None,
                        "criterion_name": None,
                        "criterion_value": None,
                        "pre_trade_large_in_scale_threshold": None,
                        "post_trade_large_in_scale_threshold": None,
                        "type": "non_equity"
                    }
                    
                result = [minimal_response]
            elif not result:
                # No results and ensure_instrument is false - return 404
                return jsonify({
                    ResponseFields.STATUS: f"{HTTPStatus.NOT_FOUND} Not Found",
                    ResponseFields.ERROR: f"No transparency calculations found for ISIN {isin}",
                    ResponseFields.META: {
                        ResponseFields.PAGE: page,
                        ResponseFields.PER_PAGE: per_page,
                        ResponseFields.TOTAL: 0
                    }
                }), HTTPStatus.NOT_FOUND
            
            # Return the data with the expected structure
            return jsonify({
                ResponseFields.STATUS: f"{HTTPStatus.OK} OK",
                ResponseFields.DATA: result,
                ResponseFields.META: {
                    ResponseFields.PAGE: page,
                    ResponseFields.PER_PAGE: per_page,
                    ResponseFields.TOTAL: len(result)
                }
            })
            
        finally:
            if session:
                session.close()
            
    except Exception as e:
        logger.error(f"Error in get_transparency_by_isin: {str(e)}")
        logger.exception(e)  # Log the full traceback
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error",
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

def direct_format_transparency(calc):
    """
    Format transparency calculation directly, using the approach proven to work in direct_test.py.
    This function directly accesses attributes without complex logic.
    """
    try:
        if not calc:
            return None

        # Basic data with direct attribute access
        result = {
            "id": calc.id,
            "isin": calc.isin,
            "calculation_type": calc.calculation_type,
            "tech_record_id": calc.tech_record_id,
            "liquidity": calc.liquidity,
            "total_transactions_executed": calc.total_transactions_executed,
            "total_volume_executed": calc.total_volume_executed,
            "from_date": calc.from_date.isoformat() if calc.from_date else None,
            "to_date": calc.to_date.isoformat() if calc.to_date else None,
            "created_at": calc.created_at.isoformat() if calc.created_at else None,
            "updated_at": calc.updated_at.isoformat() if calc.updated_at else None
        }
        
        # Include only the relevant details based on calculation_type - matching get_transparency_by_isin format
        if calc.calculation_type == "EQUITY" and hasattr(calc, 'equity_transparency') and calc.equity_transparency:
            et = calc.equity_transparency
            result["details"] = {
                "financial_instrument_classification": et.financial_instrument_classification,
                "methodology": et.methodology,
                "average_daily_turnover": et.average_daily_turnover,
                "large_in_scale": et.large_in_scale,
                "average_daily_number_of_transactions": et.average_daily_number_of_transactions,
                "average_transaction_value": et.average_transaction_value,
                "standard_market_size": et.standard_market_size,
                "type": "equity"
            }
        elif calc.calculation_type == "NON_EQUITY":
            # For NON_EQUITY, check which specific type applies
            if hasattr(calc, 'debt_transparency') and calc.debt_transparency:
                dt = calc.debt_transparency
                result["details"] = {
                    "description": dt.description,
                    "bond_type": dt.bond_type,
                    "is_liquid": dt.is_liquid,
                    "pre_trade_large_in_scale_threshold": dt.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": dt.post_trade_large_in_scale_threshold,
                    "criterion_name": dt.criterion_name,
                    "criterion_value": dt.criterion_value,
                    "type": "debt"
                }
            elif hasattr(calc, 'futures_transparency') and calc.futures_transparency:
                ft = calc.futures_transparency
                result["details"] = {
                    "description": ft.description,
                    "underlying_isin": ft.underlying_isin,
                    "is_stock_dividend_future": ft.is_stock_dividend_future,
                    "pre_trade_large_in_scale_threshold": ft.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": ft.post_trade_large_in_scale_threshold,
                    "criterion_name": ft.criterion_name,
                    "criterion_value": ft.criterion_value,
                    "type": "futures"
                }
            elif hasattr(calc, 'non_equity_transparency') and calc.non_equity_transparency:
                net = calc.non_equity_transparency
                result["details"] = {
                    "description": net.description,
                    "criterion_name": net.criterion_name,
                    "criterion_value": net.criterion_value,
                    "pre_trade_large_in_scale_threshold": net.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": net.post_trade_large_in_scale_threshold,
                    "type": "non_equity"
                }
            else:
                # No specific type found, add empty details
                result["details"] = {
                    "type": "unknown"
                }
        else:
            # Default case - add minimal details structure
            result["details"] = {
                "type": "unknown"
            }
        
        return result
        
    except Exception as e:
        calc_id = getattr(calc, 'id', 'unknown') if calc else 'None'
        logger.error(f"Error formatting calculation {calc_id}: {str(e)}")
        logger.exception(e)
        return None

# Keep existing formatting functions for compatibility but make them delegate to direct_format_transparency
format_transparency_calculation_simple = direct_format_transparency
_format_transparency_calculation_detailed = direct_format_transparency
_format_transparency_calculation = direct_format_transparency