import logging
from flask import Blueprint, jsonify, request
from ..services.transparency_service import TransparencyService
from ..constants import (
    HTTPStatus, Pagination, API, ErrorMessages, SuccessMessages,
    ResponseFields, Endpoints, QueryParams, FormFields, DbFields
)
from typing import Dict, Any

# Setup logging
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
        
        service = TransparencyService()
        
        if isin:
            # Get by specific ISIN
            session, calculations = service.get_transparency_by_isin(isin)
            session.close()
        elif instrument_type:
            # Get by instrument type
            session, calculations = service.get_transparency_by_instrument_type(instrument_type, limit)
            session.close()
        else:
            # Get all (limited implementation for now)
            from ..database.session import SessionLocal
            from ..models.transparency import TransparencyCalculation
            
            session = SessionLocal()
            try:
                query = session.query(TransparencyCalculation)
                
                if calculation_type:
                    query = query.filter(TransparencyCalculation.calculation_type == calculation_type)
                
                total_count = query.count()
                calculations = query.limit(limit).offset(offset).all()
            finally:
                session.close()
        
        result = []
        for calc in calculations:
            calc_data = {
                "id": calc.id,
                "isin": calc.isin,
                "calculation_type": calc.calculation_type,
                "tech_record_id": calc.tech_record_id,
                "from_date": calc.from_date.isoformat() if calc.from_date else None,
                "to_date": calc.to_date.isoformat() if calc.to_date else None,
                "liquidity": calc.liquidity,
                "total_transactions_executed": calc.total_transactions_executed,
                "total_volume_executed": calc.total_volume_executed,
                "created_at": calc.created_at.isoformat() if calc.created_at else None
            }
            
            # Add type-specific data
            if calc.calculation_type == "EQUITY" and hasattr(calc, 'equity_transparency'):
                calc_data["equity_details"] = {
                    "financial_instrument_classification": calc.equity_transparency.financial_instrument_classification,
                    "methodology": calc.equity_transparency.methodology,
                    "average_daily_turnover": calc.equity_transparency.average_daily_turnover,
                    "large_in_scale": calc.equity_transparency.large_in_scale,
                    "standard_market_size": calc.equity_transparency.standard_market_size
                }
            elif calc.calculation_type == "NON_EQUITY":
                if hasattr(calc, 'debt_transparency'):
                    calc_data["debt_details"] = {
                        "description": calc.debt_transparency.description,
                        "bond_type": calc.debt_transparency.bond_type,
                        "is_liquid": calc.debt_transparency.is_liquid,
                        "pre_trade_large_in_scale_threshold": calc.debt_transparency.pre_trade_large_in_scale_threshold,
                        "post_trade_large_in_scale_threshold": calc.debt_transparency.post_trade_large_in_scale_threshold
                    }
                elif hasattr(calc, 'futures_transparency'):
                    calc_data["futures_details"] = {
                        "description": calc.futures_transparency.description,
                        "underlying_isin": calc.futures_transparency.underlying_isin,
                        "is_stock_dividend_future": calc.futures_transparency.is_stock_dividend_future,
                        "pre_trade_large_in_scale_threshold": calc.futures_transparency.pre_trade_large_in_scale_threshold,
                        "post_trade_large_in_scale_threshold": calc.futures_transparency.post_trade_large_in_scale_threshold
                    }
                elif hasattr(calc, 'non_equity_transparency'):
                    calc_data["non_equity_details"] = {
                        "description": calc.non_equity_transparency.description,
                        "criterion_name": calc.non_equity_transparency.criterion_name,
                        "criterion_value": calc.non_equity_transparency.criterion_value,
                        "financial_instrument_classification": calc.non_equity_transparency.financial_instrument_classification
                    }
            
            result.append(calc_data)
        
        return jsonify({
            ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
            ResponseFields.DATA: result,
            ResponseFields.META: {
                ResponseFields.PAGE: page,
                ResponseFields.PER_PAGE: per_page,
                ResponseFields.TOTAL: len(result)
            }
        })
            
    except Exception as e:
        logger.error(f"Error in list_transparency_calculations: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/<string:transparency_id>", methods=["GET"])
def get_transparency_calculation(transparency_id):
    """Get transparency calculation by ID"""
    try:
        service = TransparencyService()
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
    """Create a new transparency calculation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        calculation_type = data.get('calculation_type', 'NON_EQUITY')
        
        service = TransparencyService()
        calculation = service.create_transparency_calculation(data, calculation_type)
        
        return jsonify({
            ResponseFields.MESSAGE: "Transparency calculation created successfully",
            "id": calculation.id,
            "isin": calculation.isin,
            "calculation_type": calculation.calculation_type
        }), HTTPStatus.CREATED
        
    except Exception as e:
        logger.error(f"Error in create_transparency_calculation: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/<string:transparency_id>", methods=["PUT"])
def update_transparency_calculation(transparency_id):
    """Update an existing transparency calculation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        service = TransparencyService()
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
        service = TransparencyService()
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
        
        service = TransparencyService()
        
        if ensure_instrument:
            # Use the get_or_create method when ensure_instrument is true
            calculations = service.get_or_create_transparency_calculation(
                isin=isin,
                calculation_type=calculation_type or 'EQUITY',  # Default to EQUITY if not specified
                ensure_instrument=True
            )
            # Convert to the expected format
            result = []
            for calc in calculations:
                result.append(_format_transparency_calculation(calc))
        else:
            # Use the direct database query method
            session, calculations = service.get_transparency_by_isin(isin, calculation_type)
            try:
                result = []
                for calc in calculations:
                    result.append(_format_transparency_calculation(calc))
            finally:
                session.close()
        
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.OK} OK",
            ResponseFields.DATA: result,
            ResponseFields.META: {
                ResponseFields.PAGE: page,
                ResponseFields.PER_PAGE: per_page,
                ResponseFields.TOTAL: len(result)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in get_transparency_by_isin: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

def _format_transparency_calculation(calc):
    """Format a transparency calculation for API response"""
    # Base calculation data
    base_data = {
        "id": calc.id,
        "isin": calc.isin,
        "calculation_type": calc.calculation_type,
        "tech_record_id": calc.tech_record_id,
        "from_date": calc.from_date.isoformat() if calc.from_date else None,
        "to_date": calc.to_date.isoformat() if calc.to_date else None,
        "liquidity": calc.liquidity,
        "total_transactions_executed": calc.total_transactions_executed,
        "total_volume_executed": calc.total_volume_executed,
        "created_at": calc.created_at.isoformat() if hasattr(calc, 'created_at') and calc.created_at else None,
        "updated_at": calc.updated_at.isoformat() if hasattr(calc, 'updated_at') and calc.updated_at else None
    }
    
    # Initialize all detail sections as null
    equity_details = {
        "financial_instrument_classification": None,
        "methodology": None,
        "average_daily_turnover": None,
        "large_in_scale": None,
        "average_daily_number_of_transactions": None,
        "average_transaction_value": None,
        "standard_market_size": None
    }
    
    debt_details = {
        "description": None,
        "bond_type": None,
        "is_liquid": None,
        "pre_trade_large_in_scale_threshold": None,
        "post_trade_large_in_scale_threshold": None,
        "criterion_name": None,
        "criterion_value": None
    }
    
    futures_details = {
        "description": None,
        "underlying_isin": None,
        "is_stock_dividend_future": None,
        "pre_trade_large_in_scale_threshold": None,
        "post_trade_large_in_scale_threshold": None,
        "criterion_name": None,
        "criterion_value": None
    }
    
    # Populate specific details based on calculation type and available relationships
    if calc.calculation_type == "EQUITY":
        if hasattr(calc, 'equity_transparency') and calc.equity_transparency:
            equity = calc.equity_transparency
            equity_details.update({
                "financial_instrument_classification": equity.financial_instrument_classification,
                "methodology": equity.methodology,
                "average_daily_turnover": equity.average_daily_turnover,
                "large_in_scale": equity.large_in_scale,
                "average_daily_number_of_transactions": equity.average_daily_number_of_transactions,
                "average_transaction_value": equity.average_transaction_value,
                "standard_market_size": equity.standard_market_size
            })
    else:  # NON_EQUITY
        # Check for debt transparency
        if hasattr(calc, 'debt_transparency') and calc.debt_transparency:
            debt = calc.debt_transparency
            debt_details.update({
                "description": debt.description,
                "bond_type": debt.bond_type,
                "is_liquid": debt.is_liquid,
                "pre_trade_large_in_scale_threshold": debt.pre_trade_large_in_scale_threshold,
                "post_trade_large_in_scale_threshold": debt.post_trade_large_in_scale_threshold,
                "criterion_name": debt.criterion_name,
                "criterion_value": debt.criterion_value
            })
        
        # Check for futures transparency
        if hasattr(calc, 'futures_transparency') and calc.futures_transparency:
            futures = calc.futures_transparency
            futures_details.update({
                "description": futures.description,
                "underlying_isin": futures.underlying_isin,
                "is_stock_dividend_future": futures.is_stock_dividend_future,
                "pre_trade_large_in_scale_threshold": futures.pre_trade_large_in_scale_threshold,
                "post_trade_large_in_scale_threshold": futures.post_trade_large_in_scale_threshold,
                "criterion_name": futures.criterion_name,
                "criterion_value": futures.criterion_value
            })
        
        # Check for generic non-equity transparency
        if hasattr(calc, 'non_equity_transparency') and calc.non_equity_transparency:
            non_equity = calc.non_equity_transparency
            # For non-equity, we'll populate the debt_details structure as fallback
            if not debt_details["description"]:  # Only if debt details weren't already populated
                debt_details.update({
                    "description": non_equity.description,
                    "criterion_name": non_equity.criterion_name,
                    "criterion_value": non_equity.criterion_value,
                    "pre_trade_large_in_scale_threshold": non_equity.pre_trade_large_in_scale_threshold,
                    "post_trade_large_in_scale_threshold": non_equity.post_trade_large_in_scale_threshold
                })
    
    # Combine all data
    base_data.update({
        "equity_details": equity_details,
        "debt_details": debt_details,
        "futures_details": futures_details
    })
    
    return base_data

