"""
Unified Transparency Routes

Routes for managing transparency calculations using the new unified architecture.
Replaces the complex polymorphic inheritance approach with simplified JSON-based storage.
"""

import logging
from flask import Blueprint, jsonify, request
from ..services.sqlite.transparency_service import TransparencyService
from ..models.sqlite.transparency import TransparencyCalculation, TransparencyThreshold
from ..constants import (
    HTTPStatus, Pagination, API, ErrorMessages, SuccessMessages,
    ResponseFields, Endpoints, QueryParams, FormFields, DbFields
)
from typing import Dict, Any
from ..database.session import SessionLocal

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
        
        # Add derived information
        result["is_equity"] = calc.is_equity
        result["is_non_equity"] = calc.is_non_equity
        result["instrument_classification"] = calc.instrument_classification
        result["description"] = calc.description
        
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
    """Get all transparency calculations with optional filtering"""
    try:
        # Query parameters for filtering
        file_type = request.args.get('file_type')
        isin = request.args.get('isin')
        limit = request.args.get(QueryParams.LIMIT, Pagination.DEFAULT_LIMIT, type=int)
        offset = request.args.get(QueryParams.OFFSET, Pagination.DEFAULT_OFFSET, type=int)
        page = request.args.get(QueryParams.PAGE, Pagination.DEFAULT_PAGE, type=int)
        per_page = min(request.args.get(QueryParams.PER_PAGE, Pagination.DEFAULT_PER_PAGE, type=int), Pagination.MAX_PER_PAGE)
        
        logger.info(f"GET /transparency with params: file_type={file_type}, isin={isin}, page={page}, per_page={per_page}")
        
        # Create a new session for this query
        session = SessionLocal()
        try:
            # Build query
            query = session.query(TransparencyCalculation)
            
            # Apply filters
            if file_type:
                query = query.filter(TransparencyCalculation.file_type == file_type)
                logger.info(f"Applied file_type filter: {file_type}")
            
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
            
            # Format calculations using the new unified format
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
        finally:
            session.close()
            
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
    """Create transparency calculation from FITRS data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({ResponseFields.ERROR: "No data provided"}), HTTPStatus.BAD_REQUEST
        
        # Use the unified transparency service
        service = TransparencyService()
        
        # Check if this is raw FITRS data or if we need to create from source filename
        source_filename = data.get('source_filename')
        if source_filename:
            # Create from FITRS data with source filename
            calculation = service.create_transparency_calculation(
                data=data,
                source_filename=source_filename
            )
        else:
            # Create from raw data
            calculation = service.create_transparency_calculation(
                data=data
            )
        
        if not calculation:
            return jsonify({
                ResponseFields.ERROR: "Failed to create transparency calculation"
            }), HTTPStatus.BAD_REQUEST
        
        # Format the response
        result = format_unified_transparency(calculation)
        if not result:
            return jsonify({ResponseFields.ERROR: "Error formatting created transparency calculation"}), HTTPStatus.INTERNAL_SERVER_ERROR
        
        logger.info(f"Successfully created transparency calculation {calculation.id}")
        
        return jsonify({
            ResponseFields.STATUS: f"{HTTPStatus.CREATED} Created",
            ResponseFields.MESSAGE: "Successfully created transparency calculation",
            ResponseFields.DATA: result
        }), HTTPStatus.CREATED
        
    except Exception as e:
        logger.error(f"Error in create_transparency_calculation: {str(e)}")
        logger.exception(e)
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
