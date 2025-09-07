"""
Enhanced Transparency Routes

Routes for managing transparency calculations using the unified architecture.
Updated with full FITRS file type support and enhanced filtering capabilities.
"""

import logging
from flask import Blueprint, jsonify, request
from ..services.sqlite.transparency_service import TransparencyService
from ..models.sqlite.transparency import TransparencyCalculation, TransparencyThreshold
from ..models.utils.cfi_instrument_manager import (
    validate_instrument_type, 
    validate_cfi_code, 
    get_valid_instrument_types,
    normalize_instrument_type_from_cfi
)
from ..constants import (
    HTTPStatus, Pagination, API, ErrorMessages, SuccessMessages,
    ResponseFields, Endpoints, QueryParams, FormFields, DbFields
)
from typing import Dict, Any
from ..database.session import SessionLocal
from sqlalchemy import and_, or_

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint for transparency operations
transparency_bp = Blueprint("transparency", __name__, url_prefix=API.PREFIX)


def format_unified_transparency(calc: TransparencyCalculation) -> Dict[str, Any]:
    """
    Format a unified transparency calculation for API response.
    
    Uses the new unified model structure with JSON storage.
    """
    try:
        if not calc:
            return None

        # Basic data with direct attribute access
        result = {
            "id": calc.id,
            "isin": calc.isin,
            "file_type": calc.file_type,
            "tech_record_id": calc.tech_record_id,
            "from_date": calc.from_date.isoformat() if calc.from_date else None,
            "to_date": calc.to_date.isoformat() if calc.to_date else None,
            "liquidity": calc.liquidity,
            "total_transactions_executed": calc.total_transactions_executed,
            "total_volume_executed": calc.total_volume_executed,
            "source_file": calc.source_file,
            "created_at": calc.created_at.isoformat() if calc.created_at else None,
            "updated_at": calc.updated_at.isoformat() if calc.updated_at else None,
            "raw_data": calc.raw_data if calc.raw_data else {}
        }
        
        # Add enhanced derived information with new model properties
        result["is_equity"] = calc.is_equity
        result["is_non_equity"] = calc.is_non_equity
        result["instrument_category"] = calc.instrument_category  # C, D, E, F, H, I, J, O, R
        result["is_debt_instrument"] = calc.is_debt_instrument
        result["is_derivatives_or_complex"] = calc.is_derivatives_or_complex
        result["instrument_classification"] = calc.instrument_classification
        result["description"] = calc.description
        
        # Add enhanced data availability information using new model methods
        try:
            transaction_data = calc.get_transaction_data()
            result["transaction_data"] = transaction_data
            result["has_transaction_data"] = transaction_data.get("has_transaction_data", False)
        except Exception as e:
            logger.warning(f"Error getting transaction data for {calc.id}: {e}")
            result["transaction_data"] = {"has_transaction_data": False}
            result["has_transaction_data"] = False
        
        try:
            threshold_data = calc.get_threshold_data()
            result["threshold_data"] = threshold_data
            result["has_threshold_data"] = threshold_data.get("has_threshold_data", False)
        except Exception as e:
            logger.warning(f"Error getting threshold data for {calc.id}: {e}")
            result["threshold_data"] = {"has_threshold_data": False}
            result["has_threshold_data"] = False
        
        # Add criteria pairs for non-equity instruments
        if calc.is_non_equity:
            try:
                criteria_pairs = calc.get_criteria_pairs()
                result["criteria_pairs"] = criteria_pairs
            except Exception as e:
                logger.warning(f"Error getting criteria pairs for {calc.id}: {e}")
                result["criteria_pairs"] = []
        
        # Add threshold information (load if available)
        try:
            if hasattr(calc, 'thresholds') and calc.thresholds:
                thresholds = []
                for threshold in calc.thresholds:
                    threshold_data = {
                        "id": threshold.id,
                        "threshold_type": threshold.threshold_type,
                        "amount_value": threshold.amount_value,
                        "number_value": threshold.number_value,
                        "raw_data": threshold.raw_data if threshold.raw_data else {}
                    }
                    thresholds.append(threshold_data)
                result["thresholds"] = thresholds
            else:
                result["thresholds"] = []
        except Exception as e:
            logger.warning(f"Error getting thresholds for {calc.id}: {e}")
            result["thresholds"] = []
        
        return result
        
    except Exception as e:
        calc_id = getattr(calc, 'id', 'unknown') if calc else 'None'
        logger.error(f"Error formatting calculation {calc_id}: {str(e)}")
        logger.exception(e)
        return None


@transparency_bp.route(Endpoints.TRANSPARENCY, methods=["GET"])
def list_transparency_calculations():
    """
    Get all transparency calculations with enhanced filtering options.
    
    Query Parameters:
    - file_type: Specific FITRS file type (e.g., FULNCR_D, FULECR_E)
    - instrument_category: Instrument category (C, D, E, F, H, I, J, O, R)  
    - is_equity: Filter by equity instruments (true/false)
    - is_debt: Filter by debt instruments (true/false)
    - has_transaction_data: Filter by records with transaction data (true/false)
    - has_threshold_data: Filter by records with threshold data (true/false)
    - isin: Filter by specific ISIN
    """
    try:
        # Enhanced query parameters for filtering
        file_type = request.args.get('file_type')
        instrument_category = request.args.get('instrument_category')  # C, D, E, F, H, I, J, O, R
        is_equity = request.args.get('is_equity')  # true/false
        is_debt = request.args.get('is_debt')  # true/false
        has_transaction_data = request.args.get('has_transaction_data')  # true/false
        has_threshold_data = request.args.get('has_threshold_data')  # true/false
        isin = request.args.get('isin')
        
        # Pagination parameters
        limit = request.args.get(QueryParams.LIMIT, Pagination.DEFAULT_LIMIT, type=int)
        offset = request.args.get(QueryParams.OFFSET, Pagination.DEFAULT_OFFSET, type=int)
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        logger.info(f"GET /transparency with enhanced params: file_type={file_type}, category={instrument_category}, is_equity={is_equity}, is_debt={is_debt}, isin={isin}")
        
        # Create a new session for this query
        session = SessionLocal()
        try:
            # Build query
            query = session.query(TransparencyCalculation)
            
            # Apply specific file type filter
            if file_type:
                query = query.filter(TransparencyCalculation.file_type == file_type)
                logger.info(f"Applied file_type filter: {file_type}")
            
            # Apply instrument category filter (C, D, E, F, H, I, J, O, R)
            if instrument_category:
                # Filter by file types that end with the specified category
                category_pattern = f'%_{instrument_category.upper()}'
                query = query.filter(TransparencyCalculation.file_type.like(category_pattern))
                logger.info(f"Applied instrument_category filter: {instrument_category}")
            
            # Apply equity/non-equity filters
            if is_equity and is_equity.lower() == 'true':
                query = query.filter(TransparencyCalculation.file_type.like('FULECR_%'))
                logger.info("Applied is_equity=true filter")
            elif is_equity and is_equity.lower() == 'false':
                query = query.filter(TransparencyCalculation.file_type.like('FULNCR_%'))
                logger.info("Applied is_equity=false filter")
            
            # Apply debt instrument filter
            if is_debt and is_debt.lower() == 'true':
                query = query.filter(TransparencyCalculation.file_type == 'FULNCR_D')
                logger.info("Applied is_debt=true filter")
            elif is_debt and is_debt.lower() == 'false':
                query = query.filter(TransparencyCalculation.file_type != 'FULNCR_D')
                logger.info("Applied is_debt=false filter")
            
            # Apply data availability filters
            if has_transaction_data and has_transaction_data.lower() == 'true':
                query = query.filter(
                    or_(
                        TransparencyCalculation.total_transactions_executed.isnot(None),
                        TransparencyCalculation.total_volume_executed.isnot(None)
                    )
                )
                logger.info("Applied has_transaction_data=true filter")
            elif has_transaction_data and has_transaction_data.lower() == 'false':
                query = query.filter(
                    and_(
                        TransparencyCalculation.total_transactions_executed.is_(None),
                        TransparencyCalculation.total_volume_executed.is_(None)
                    )
                )
                logger.info("Applied has_transaction_data=false filter")
            
            # Apply ISIN filter
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
            
            # Format calculations using the enhanced unified format
            result = []
            for calc in calculations:
                formatted_calc = format_unified_transparency(calc)
                if formatted_calc:
                    result.append(formatted_calc)
            
            logger.info(f"Formatted {len(result)} calculations for response")
            
            # Return the data in the expected format
            return jsonify({
                ResponseFields.STATUS: f"{HTTPStatus.OK} OK",
                ResponseFields.DATA: result,
                ResponseFields.META: {
                    ResponseFields.PAGE: page,
                    ResponseFields.PER_PAGE: per_page,
                    ResponseFields.TOTAL: total_count
                }
            })
        except Exception as service_error:
            logger.error(f"Service error in transparency calculations: {str(service_error)}")
            raise service_error
            
    except Exception as e:
        logger.error(f"Error in list_transparency_calculations: {str(e)}")
        logger.exception(e)
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error", 
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/<string:transparency_id>", methods=["GET"])
def get_transparency_calculation(transparency_id):
    """Get transparency calculation by ID"""
    try:
        session = SessionLocal()
        try:
            calculation = session.query(TransparencyCalculation).filter(
                TransparencyCalculation.id == transparency_id
            ).first()
            
            if not calculation:
                return jsonify({ResponseFields.ERROR: "Transparency calculation not found"}), HTTPStatus.NOT_FOUND
            
            # Format the calculation
            result = format_unified_transparency(calculation)
            if not result:
                return jsonify({ResponseFields.ERROR: "Error formatting transparency calculation"}), HTTPStatus.INTERNAL_SERVER_ERROR
            
            return jsonify(result)
            
        finally:
            session.close()
        
    except Exception as e:
        logger.error(f"Error in get_transparency_calculation: {str(e)}")
        return jsonify({ResponseFields.ERROR: str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@transparency_bp.route(Endpoints.TRANSPARENCY, methods=["POST"])
def create_transparency_calculation():
    """Create transparency calculation from FITRS data for an existing ISIN"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        # Extract required fields
        isin = data.get('isin')
        instrument_type = data.get('instrument_type')
        cfi_code = data.get('cfi_code')
        
        if not isin:
            return jsonify({ResponseFields.ERROR: "ISIN is required"}), HTTPStatus.BAD_REQUEST
        
        # Validate instrument type if provided
        if instrument_type and not validate_instrument_type(instrument_type):
            valid_types = get_valid_instrument_types()
            return jsonify({
                ResponseFields.ERROR: f"Invalid instrument type '{instrument_type}'. Must be one of: {', '.join(valid_types)}"
            }), HTTPStatus.BAD_REQUEST
        
        # Validate CFI code if provided and ensure consistency
        if cfi_code:
            is_valid, error_msg = validate_cfi_code(cfi_code)
            if not is_valid:
                return jsonify({ResponseFields.ERROR: f"Invalid CFI code: {error_msg}"}), HTTPStatus.BAD_REQUEST
                
            # If both CFI code and instrument type are provided, ensure consistency
            if instrument_type:
                normalized_type = normalize_instrument_type_from_cfi(cfi_code)
                if normalized_type != instrument_type:
                    return jsonify({
                        ResponseFields.ERROR: f"CFI code '{cfi_code}' indicates type '{normalized_type}' but '{instrument_type}' was specified"
                    }), HTTPStatus.BAD_REQUEST
            else:
                # If only CFI code provided, derive the instrument type
                instrument_type = normalize_instrument_type_from_cfi(cfi_code)
        
        # Use the unified transparency service
        service = TransparencyService()
        
        # Check if this is raw FITRS data or if we need to create from ISIN lookup
        if 'TechRcrdId' in data:
            # This is raw FITRS data - create directly
            source_filename = data.get('source_filename')
            calculation = service.create_transparency_calculation(
                data=data,
                source_filename=source_filename
            )
            calculations = [calculation] if calculation else []
        else:
            # This is an ISIN lookup request - search FITRS files
            calculations = service.create_transparency(
                isin=isin,
                instrument_type=instrument_type
            )
        
        if not calculations:
            return jsonify({
                ResponseFields.ERROR: "Failed to create transparency calculation"
            }), HTTPStatus.BAD_REQUEST
        
        # Format the response
        if len(calculations) == 1:
            result = format_unified_transparency(calculations[0])
        else:
            result = [format_unified_transparency(calc) for calc in calculations]
            
        if not result:
            return jsonify({ResponseFields.ERROR: "Error formatting created transparency calculation"}), HTTPStatus.INTERNAL_SERVER_ERROR
        
        logger.info(f"Successfully created {len(calculations)} transparency calculation(s) for {isin}")
        
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.CREATED} Created",
            ResponseFields.MESSAGE: f"Successfully created {len(calculations)} transparency calculation(s)",
            ResponseFields.DATA: result
        }), HTTPStatus.CREATED
        
    except Exception as e:
        logger.error(f"Error in create_transparency_calculation: {str(e)}")
        logger.exception(e)
        if "does not exist in the database" in str(e):
            return jsonify({
                ResponseFields.STATUS: f"{HTTPStatus.NOT_FOUND} Not Found",
                ResponseFields.ERROR: str(e)
            }), HTTPStatus.NOT_FOUND
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error",
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


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
        # Query parameters
        file_type = request.args.get('file_type')
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        logger.info(f"GET transparency for ISIN={isin}, file_type={file_type}")
        
        # Use the unified transparency service
        service = TransparencyService()
        calculations = service.get_transparency_by_isin(isin)
        
        if not calculations:
            return jsonify({
                ResponseFields.STATUS: f"{HTTPStatus.NOT_FOUND} Not Found",
                ResponseFields.ERROR: f"No transparency calculations found for ISIN {isin}",
                ResponseFields.META: {
                    ResponseFields.PAGE: page,
                    ResponseFields.PER_PAGE: per_page,
                    ResponseFields.TOTAL: 0
                }
            }), HTTPStatus.NOT_FOUND
        
        # Apply file_type filter if specified
        if file_type:
            calculations = [calc for calc in calculations if calc.file_type == file_type]
        
        # Format calculations using the new unified format
        result = []
        for calc in calculations:
            formatted_calc = format_unified_transparency(calc)
            if formatted_calc:
                result.append(formatted_calc)
        
        logger.info(f"Formatted {len(result)} calculations for response")
        
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
            
    except Exception as e:
        logger.error(f"Error in get_transparency_by_isin: {str(e)}")
        logger.exception(e)
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error",
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/process-fitrs", methods=["POST"])
def process_fitrs_file():
    """Process an entire FITRS file and create transparency calculations"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        source_filename = data.get('source_filename')
        file_data = data.get('file_data')  # Should be a list of records
        
        if not source_filename or not file_data:
            return jsonify({
                ResponseFields.ERROR: "Both source_filename and file_data are required"
            }), HTTPStatus.BAD_REQUEST
        
        # Use the unified transparency service
        service = TransparencyService()
        
        # Process the file data
        import pandas as pd
        df = pd.DataFrame(file_data)
        
        results = service.process_fitrs_file(df, source_filename)
        
        # Format results
        formatted_results = []
        for calc in results:
            formatted_calc = format_unified_transparency(calc)
            if formatted_calc:
                formatted_results.append(formatted_calc)
        
        logger.info(f"Successfully processed {len(formatted_results)} transparency calculations from {source_filename}")
        
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.CREATED} Created",
            ResponseFields.MESSAGE: f"Successfully processed {len(formatted_results)} transparency calculations",
            ResponseFields.DATA: formatted_results,
            ResponseFields.META: {
                "source_filename": source_filename,
                "total_processed": len(formatted_results)
            }
        }), HTTPStatus.CREATED
        
    except Exception as e:
        logger.error(f"Error in process_fitrs_file: {str(e)}")
        logger.exception(e)
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error",
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


@transparency_bp.route(f"{Endpoints.TRANSPARENCY}/stats", methods=["GET"])
def get_transparency_statistics():
    """
    Get comprehensive transparency statistics by file type and instrument category.
    Useful for understanding data distribution across the expanded FITRS file types.
    """
    try:
        logger.info("GET /transparency/stats")
        
        session = SessionLocal()
        try:
            from sqlalchemy import func
            
            # Get file type distribution
            file_type_stats = session.query(
                TransparencyCalculation.file_type,
                func.count(TransparencyCalculation.id).label('count')
            ).group_by(TransparencyCalculation.file_type).all()
            
            # Get data availability statistics
            transaction_data_stats = session.query(
                func.count(TransparencyCalculation.id).label('total'),
                func.count(TransparencyCalculation.total_transactions_executed).label('with_transactions'),
                func.count(TransparencyCalculation.total_volume_executed).label('with_volume')
            ).first()
            
            # Get equity vs non-equity distribution
            equity_stats = session.query(
                func.sum(func.case([(TransparencyCalculation.file_type.like('FULECR_%'), 1)], else_=0)).label('equity_count'),
                func.sum(func.case([(TransparencyCalculation.file_type.like('FULNCR_%'), 1)], else_=0)).label('non_equity_count')
            ).first()
            
            # Get instrument category breakdown
            category_stats = {}
            for file_type, count in file_type_stats:
                category = file_type.split('_')[1] if '_' in file_type else 'Unknown'
                if category not in category_stats:
                    category_stats[category] = {'total': 0, 'file_types': {}}
                category_stats[category]['total'] += count
                category_stats[category]['file_types'][file_type] = count
            
            # Calculate data availability percentages
            total_records = transaction_data_stats.total if transaction_data_stats else 0
            transaction_fill_rate = (transaction_data_stats.with_transactions / total_records * 100) if total_records > 0 else 0
            volume_fill_rate = (transaction_data_stats.with_volume / total_records * 100) if total_records > 0 else 0
            
            result = {
                "summary": {
                    "total_records": total_records,
                    "equity_records": equity_stats.equity_count if equity_stats else 0,
                    "non_equity_records": equity_stats.non_equity_count if equity_stats else 0,
                    "transaction_data_fill_rate": round(transaction_fill_rate, 1),
                    "volume_data_fill_rate": round(volume_fill_rate, 1)
                },
                "file_type_distribution": {
                    ft: count for ft, count in file_type_stats
                },
                "instrument_categories": category_stats,
                "data_availability": {
                    "total_records": total_records,
                    "records_with_transactions": transaction_data_stats.with_transactions if transaction_data_stats else 0,
                    "records_with_volume": transaction_data_stats.with_volume if transaction_data_stats else 0,
                    "transaction_fill_rate_percent": round(transaction_fill_rate, 1),
                    "volume_fill_rate_percent": round(volume_fill_rate, 1)
                }
            }
            
            return jsonify({
                ResponseFields.STATUS: f"{HTTPStatus.OK} OK",
                ResponseFields.DATA: result
            }), HTTPStatus.OK
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error in get_transparency_statistics: {str(e)}")
        logger.exception(e)
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.INTERNAL_SERVER_ERROR} Internal Server Error",
            ResponseFields.ERROR: str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR
