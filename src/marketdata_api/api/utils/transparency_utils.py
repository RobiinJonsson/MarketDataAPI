"""
Transparency API Response Utilities

This module provides utility functions for building rich CLI-style API responses
for transparency calculations, matching the comprehensive data formatting used in CLI commands.
"""

import logging
import math
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def _clean_metrics(metrics_dict):
    """Clean metrics dictionary, converting NaN and Inf values to None"""
    cleaned = {}
    for key, value in metrics_dict.items():
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            cleaned[key] = None
        else:
            cleaned[key] = value
    return cleaned


def build_transparency_response(calculation, include_rich_details=False):
    """
    Build a comprehensive transparency calculation response matching CLI formatting.
    
    Args:
        calculation: TransparencyCalculation model instance
        include_rich_details: Whether to include additional rich data sections
        
    Returns:
        dict: Comprehensive transparency calculation data
    """
    # Extract raw_data safely like CLI does
    raw_data = calculation.raw_data or {}
    
    # Calculate period like CLI
    period = "Unknown"
    if calculation.from_date and calculation.to_date:
        period = f"{calculation.from_date.strftime('%Y-%m-%d')} to {calculation.to_date.strftime('%Y-%m-%d')}"
    
    # Calculate liquidity status like CLI
    volume = calculation.total_volume_executed or 0
    transactions = calculation.total_transactions_executed or 0
    has_trading_activity = volume > 0 or transactions > 0
    
    if calculation.liquidity is True:
        liquidity_status = "✓ Liquid"
    elif calculation.liquidity is False:
        liquidity_status = "✗ Non-Liquid"
    elif has_trading_activity:
        liquidity_status = "🔄 Active"
    else:
        liquidity_status = "❓ Unknown"
    
    # Extract fields from raw_data like CLI with NaN cleaning
    instrument_class = raw_data.get("FinInstrmClssfctn", "N/A")
    methodology_raw = raw_data.get("Mthdlgy", "N/A")
    methodology = None if (isinstance(methodology_raw, float) and (math.isnan(methodology_raw) or math.isinf(methodology_raw))) else methodology_raw
    
    # Core response matching both CLI and API needs
    response = {
        "id": str(calculation.id) if calculation.id else None,
        "isin": calculation.isin,
        "file_type": calculation.file_type,
        "from_date": calculation.from_date.isoformat() if calculation.from_date else None,
        "to_date": calculation.to_date.isoformat() if calculation.to_date else None,
        "liquidity": calculation.liquidity,
        "transactions": calculation.total_transactions_executed,
        "volume": float(calculation.total_volume_executed) if calculation.total_volume_executed else 0.0,
        "methodology": methodology if methodology != "N/A" else None,
        "instrument_type": instrument_class if instrument_class != "N/A" else None,
    }
    
    # Add rich details if requested
    if include_rich_details:
        response.update({
            "transparency_analysis": {
                "period": period,
                "liquidity_status": liquidity_status,
                "has_trading_activity": has_trading_activity,
                "raw_metrics": _clean_metrics({
                    "avg_daily_turnover": raw_data.get("AvrgDalyTrnvr"),
                    "large_in_scale": raw_data.get("LrgInScale"),
                    "standard_market_size": raw_data.get("StdMktSz"),
                }) if raw_data else {}
            },
            "mifid_context": {
                "is_equity": calculation.file_type and calculation.file_type.startswith("FULECR"),
                "transparency_requirement": True,
            }
        })
    
    return response


def _extract_rich_transparency_metrics(calculation):
    """Extract rich transparency metrics and thresholds"""
    metrics_info = {
        "transparency_metrics": {},
        "thresholds": {},
        "calculated_values": {}
    }
    
    # Key transparency metrics
    metrics_info["transparency_metrics"] = {
        "average_daily_turnover": float(calculation.raw_data.get("AvrgDalyTrnvr")) if calculation.raw_data and calculation.raw_data.get("AvrgDalyTrnvr") else None,
        "large_in_scale_threshold": float(calculation.raw_data.get("LrgInScale")) if calculation.raw_data and calculation.raw_data.get("LrgInScale") else None,
        "standard_market_size": float(calculation.raw_data.get("StdMktSz")) if calculation.raw_data and calculation.raw_data.get("StdMktSz") else None,
        "average_transaction_size": float(calculation.total_volume_executed / calculation.total_transactions_executed) if calculation.total_volume_executed and calculation.total_transactions_executed else None,
    }
    
    # MiFID II thresholds and flags
    metrics_info["thresholds"] = {
        "lis_threshold": float(calculation.large_in_scale_threshold) if calculation.large_in_scale_threshold else None,
        "sms_value": float(calculation.raw_data.get("StdMktSz")) if calculation.raw_data and calculation.raw_data.get("StdMktSz") else None,
        "adt_value": float(calculation.raw_data.get("AvrgDalyTrnvr")) if calculation.raw_data and calculation.raw_data.get("AvrgDalyTrnvr") else None,
    }
    
    # Calculated transparency indicators
    volume_millions = float(calculation.total_volume_executed) / 1_000_000 if calculation.total_volume_executed else 0
    metrics_info["calculated_values"] = {
        "volume_millions": round(volume_millions, 2),
        "transaction_count": calculation.total_transactions_executed or 0,
        "methodology_code": calculation.raw_data.get("Mthdlgy") if calculation.raw_data else None,
        "period_days": _calculate_period_days(calculation),
    }
    
    return metrics_info


def _extract_rich_period_analysis(calculation):
    """Extract rich period and temporal analysis"""
    period_info = {
        "period_analysis": {},
        "temporal_context": {}
    }
    
    # Period formatting
    if calculation.from_date and calculation.to_date:
        period_info["period_analysis"] = {
            "start_date": calculation.from_date.isoformat(),
            "end_date": calculation.to_date.isoformat(),
            "period_formatted": f"{calculation.from_date.strftime('%Y-%m-%d')} to {calculation.to_date.strftime('%Y-%m-%d')}",
            "duration_days": _calculate_period_days(calculation),
        }
    
    # File type context
    file_type_descriptions = {
        "FULECR_E": "Full European Credit Instruments",
        "FULECR_N": "Full Non-European Credit Instruments", 
        "DVCECA": "Derivative Instruments",
        "FULRES": "Full Rescinded Instruments",
    }
    
    period_info["temporal_context"] = {
        "file_type_description": file_type_descriptions.get(calculation.file_type, f"File Type: {calculation.file_type}"),
        "data_source": "ESMA FITRS",
        "calculation_type": "MiFID II Transparency",
    }
    
    return period_info


def _extract_rich_liquidity_indicators(calculation):
    """Extract rich liquidity status and indicators"""
    liquidity_info = {
        "liquidity_analysis": {},
        "status_indicators": [],
        "display_status": ""
    }
    
    # Liquidity status analysis
    liquidity_status = "Unknown"
    liquidity_icon = "❓"
    
    if calculation.liquidity is not None:
        if calculation.liquidity:
            liquidity_status = "Liquid"
            liquidity_icon = "🔄"
        else:
            liquidity_status = "Illiquid"  
            liquidity_icon = "🔒"
    
    liquidity_info["liquidity_analysis"] = {
        "flag": calculation.liquidity,
        "status": liquidity_status,
        "description": f"{liquidity_icon} {liquidity_status}",
    }
    
    # Status indicators like CLI
    indicators = []
    
    # Liquidity indicator
    indicators.append(f"{liquidity_icon} {liquidity_status}")
    
    # Volume indicator
    if calculation.total_volume_executed:
        volume_m = calculation.total_volume_executed / 1_000_000
        if volume_m > 1000:
            indicators.append("📈 High Volume")
        elif volume_m > 100:
            indicators.append("📊 Medium Volume")
        else:
            indicators.append("📉 Low Volume")
    
    # Transaction count indicator
    if calculation.total_transactions_executed:
        if calculation.total_transactions_executed > 10000:
            indicators.append("🔥 High Activity")
        elif calculation.total_transactions_executed > 1000:
            indicators.append("⚡ Active")
        else:
            indicators.append("📝 Limited Activity")
    
    # Methodology indicator
    methodology = calculation.raw_data.get("Mthdlgy") if calculation.raw_data else None
    if methodology:
        indicators.append(f"🔧 {methodology}")
    
    liquidity_info["status_indicators"] = indicators
    liquidity_info["display_status"] = " • ".join(indicators)
    
    return liquidity_info


def _extract_calculation_summary(calculation):
    """Extract calculation counts and summary information"""
    summary_info = {
        "calculation_counts": {
            "total_transactions": calculation.total_transactions_executed or 0,
            "volume_millions": round(float(calculation.total_volume_executed) / 1_000_000, 2) if calculation.total_volume_executed else 0.0,
            "period_days": _calculate_period_days(calculation),
        },
        "calculation_summary": ""
    }
    
    # Create summary
    summary_parts = []
    
    if calculation.total_transactions_executed:
        summary_parts.append(f"{calculation.total_transactions_executed:,} transactions")
        
    if calculation.total_volume_executed:
        volume_m = calculation.total_volume_executed / 1_000_000
        summary_parts.append(f"{volume_m:.1f}M volume")
    
    period_days = _calculate_period_days(calculation)
    if period_days:
        summary_parts.append(f"{period_days} days")
        
    methodology = calculation.raw_data.get("Mthdlgy") if calculation.raw_data else None
    if methodology:
        summary_parts.append(f"{methodology} method")
    
    summary_info["calculation_summary"] = " • ".join(summary_parts) if summary_parts else "Basic calculation data"
    
    return summary_info


def _calculate_period_days(calculation):
    """Calculate the number of days in the calculation period"""
    if calculation.from_date and calculation.to_date:
        delta = calculation.to_date - calculation.from_date
        return delta.days + 1  # Include both start and end dates
    return None


def format_transparency_list_response(calculations, total_count, page, per_page):
    """
    Format a list of transparency calculations for API response.
    
    Args:
        calculations: List of TransparencyCalculation model instances
        total_count: Total number of calculations matching the query
        page: Current page number
        per_page: Items per page
        
    Returns:
        dict: Formatted response with data and metadata
    """
    return {
        "status": "success",
        "data": [build_transparency_response(calc, include_rich_details=True) for calc in calculations],
        "meta": {
            "page": page,
            "per_page": per_page, 
            "total": total_count,
            "has_next": page * per_page < total_count,
            "has_prev": page > 1,
        }
    }


def format_transparency_analysis_response(isin, calculations, analysis_data=None):
    """
    Format a comprehensive transparency analysis response for a specific ISIN.
    
    Args:
        isin: The ISIN being analyzed
        calculations: List of TransparencyCalculation instances for this ISIN
        analysis_data: Optional additional analysis data
        
    Returns:
        dict: Comprehensive analysis response matching CLI format
    """
    if not calculations:
        return {
            "status": "success",
            "data": [],
            "meta": {"total": 0, "isin": isin, "message": "No transparency calculations found"}
        }
    
    # Build individual calculation responses
    calculation_responses = []
    for calc in calculations:
        try:
            calc_response = build_transparency_response(calc, include_rich_details=True)
            calculation_responses.append(calc_response)
        except Exception as e:
            # Skip failed calculations but log the error
            continue
    
    # Calculate summary metrics
    total_volume = sum(calc.total_volume_executed for calc in calculations if calc.total_volume_executed)
    total_transactions = sum(calc.total_transactions_executed for calc in calculations if calc.total_transactions_executed)
    
    # Get date range
    start_dates = [calc.from_date for calc in calculations if calc.from_date]
    end_dates = [calc.to_date for calc in calculations if calc.to_date]
    
    data_period = "Unknown"
    if start_dates and end_dates:
        data_period = f"{min(start_dates).strftime('%Y-%m-%d')} to {max(end_dates).strftime('%Y-%m-%d')}"
    
    return {
        "status": "success", 
        "data": calculation_responses,
        "meta": {
            "total": len(calculation_responses),
            "isin": isin,
            "summary": {
                "total_volume": float(total_volume) if total_volume else 0,
                "total_transactions": total_transactions,
                "data_period": data_period,
                "calculations_count": len(calculations)
            }
        }
    }