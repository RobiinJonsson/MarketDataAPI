"""
MIC (Market Identification Code) Utilities

Pure utility functions for MIC data processing and business logic.
Extracted from routes/mic_routes.py for reusability across the application.
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...database.session import get_session
from ...models.sqlite.market_identification_code import (
    MarketCategoryCode,
    MarketIdentificationCode,
    MICStatus,
    MICType,
)
from ...services.utils.mic_data_loader import MICDataLoader, load_mic_data_from_csv


def get_mic_segments_data(session, mic_code: str):
    """
    Get all segment MICs for a given operating MIC.
    
    Args:
        session: SQLAlchemy session
        mic_code: Operating MIC code
        
    Returns:
        dict: Operating MIC and its segments, or error if not found
    """
    # Verify the operating MIC exists
    operating_mic = (
        session.query(MarketIdentificationCode)
        .filter_by(mic=mic_code.upper(), operation_type=MICType.OPRT)
        .first()
    )

    if not operating_mic:
        return {"error": f"Operating MIC not found: {mic_code}", "status_code": 404}

    segments = MarketIdentificationCode.get_segments_for_operating_mic(
        session, mic_code.upper()
    )

    return {
        "operating_mic": operating_mic.to_dict(),
        "segments": [segment.to_dict() for segment in segments],
    }


def get_countries_data(session):
    """
    Get all countries with MIC codes and counts.
    
    Args:
        session: SQLAlchemy session
        
    Returns:
        list: Country statistics with MIC counts
    """
    # Get basic country stats
    country_stats = (
        session.query(
            MarketIdentificationCode.iso_country_code,
            func.count(MarketIdentificationCode.mic).label("total_mics"),
        )
        .filter(MarketIdentificationCode.status == MICStatus.ACTIVE)
        .group_by(MarketIdentificationCode.iso_country_code)
        .order_by(func.count(MarketIdentificationCode.mic).desc())
        .all()
    )

    # Calculate operating and segment counts separately for each country
    results = []
    for country_code, total_mics in country_stats:
        operating_count = (
            session.query(MarketIdentificationCode)
            .filter(
                MarketIdentificationCode.iso_country_code == country_code,
                MarketIdentificationCode.status == MICStatus.ACTIVE,
                MarketIdentificationCode.operation_type == MICType.OPRT,
            )
            .count()
        )

        segment_count = (
            session.query(MarketIdentificationCode)
            .filter(
                MarketIdentificationCode.iso_country_code == country_code,
                MarketIdentificationCode.status == MICStatus.ACTIVE,
                MarketIdentificationCode.operation_type == MICType.SGMT,
            )
            .count()
        )

        results.append({
            "country_code": country_code,
            "total_mics": total_mics,
            "operating_mics": operating_count,
            "segment_mics": segment_count,
        })

    return results


def search_mics_data(session, **filters):
    """
    Search MICs with various filters.
    
    Args:
        session: SQLAlchemy session
        **filters: Search filters (market_name, legal_entity_name, etc.)
        
    Returns:
        dict: Search results with pagination metadata
    """
    query = session.query(MarketIdentificationCode)
    
    # Apply filters
    if 'market_name' in filters:
        search_term = f"%{filters['market_name']}%"
        query = query.filter(MarketIdentificationCode.market_name.ilike(search_term))
    
    if 'legal_entity_name' in filters:
        search_term = f"%{filters['legal_entity_name']}%"
        query = query.filter(MarketIdentificationCode.legal_entity_name.ilike(search_term))
    
    if 'mic_code' in filters:
        query = query.filter(MarketIdentificationCode.mic_code == filters['mic_code'].upper())
    
    if 'country' in filters:
        query = query.filter(MarketIdentificationCode.iso_country_code == filters['country'].upper())
    
    if 'status' in filters:
        query = query.filter(MarketIdentificationCode.status == filters['status'].upper())
    
    if 'mic_type' in filters:
        query = query.filter(MarketIdentificationCode.operation_type == filters['mic_type'].upper())
    
    # Get total count
    total_count = query.count()
    
    # Apply pagination
    page = filters.get('page', 1)
    per_page = min(filters.get('per_page', 50), 1000)  # Max 1000 results
    offset = (page - 1) * per_page
    
    results = query.offset(offset).limit(per_page).all()
    
    return {
        "results": [mic.to_dict() for mic in results],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total_count,
            "has_next": offset + per_page < total_count,
            "has_prev": page > 1,
        }
    }


def get_mic_statistics_data(session):
    """
    Get MIC registry statistics.
    
    Args:
        session: SQLAlchemy session
        
    Returns:
        dict: Statistical information about MIC registry
    """
    loader = MICDataLoader(session)
    stats = loader.get_load_statistics()
    validation_issues = loader.validate_mic_relationships()

    return {
        "statistics": stats,
        "validation_issues": validation_issues,
        "data_quality": {
            "total_issues": len(validation_issues),
            "data_integrity": "good" if len(validation_issues) == 0 else "issues_found",
        },
    }


def load_mic_data_logic(session: Session, source: str = "remote", 
                       csv_path: Optional[str] = None, 
                       data_version: Optional[str] = None) -> Dict[str, Any]:
    """
    Load MIC data from CSV file or remote source.
    
    Args:
        session: SQLAlchemy session
        source: "remote" or "local"
        csv_path: Path to CSV file (required if source is "local")
        data_version: Optional version identifier
        
    Returns:
        dict: Load result with success status and details
    """
    # Validate input
    if source == "local" and not csv_path:
        return {"success": False, "error": 'csv_path is required when source is "local"'}

    if source not in ["remote", "local"]:
        return {"success": False, "error": 'source must be either "remote" or "local"'}

    try:
        if source == "remote":
            result = load_mic_data_from_csv(session, csv_source=None, data_version=data_version)
        else:
            result = load_mic_data_from_csv(
                session, csv_source=csv_path, data_version=data_version
            )

        return result

    except Exception as e:
        return {"success": False, "error": str(e), "source": source}


def get_mic_enums(session):
    """
    Get available enum values for MIC fields.
    
    Returns:
        dict: Available enum values for each MIC field
    """
    return {
        "status_values": [status.value for status in MICStatus],
        "operation_types": [op_type.value for op_type in MICType],
        "market_categories": [category.value for category in MarketCategoryCode],
    }


def format_mic_list_response(mics: List, total_count: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """
    Format a standardized MIC list response.
    
    Args:
        mics: List of MIC model instances
        total_count: Total number of matching MICs
        page: Current page number
        per_page: Items per page
        
    Returns:
        dict: Formatted response with data and metadata
    """
    return {
        "status": "success",
        "data": [mic.to_dict() for mic in mics],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total_count,
            "has_next": (page * per_page) < total_count,
            "has_prev": page > 1,
        },
    }