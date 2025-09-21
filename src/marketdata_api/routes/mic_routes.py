"""
Market Identification Code (MIC) API routes.

Provides REST API endpoints for querying ISO 10383 Market Identification Codes
and their relationships with trading venues.
"""

from typing import Any, Dict, List

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from ..database.session import get_session
from ..models.sqlite.market_identification_code import (
    MarketCategoryCode,
    MarketIdentificationCode,
    MICStatus,
    MICType,
)
from ..services.mic_data_loader import (
    OFFICIAL_MIC_CSV_URL,
    MICDataLoader,
    load_mic_data_from_csv,
    remote_mic_service,
)

mic_bp = Blueprint("mic", __name__, url_prefix="/api/v1/mic")


@mic_bp.route("/", methods=["GET"])
def list_mics():
    """
    List Market Identification Codes with optional filtering.

    Query parameters:
    - country: Filter by ISO country code
    - status: Filter by status (ACTIVE, EXPIRED, SUSPENDED)
    - type: Filter by operation type (OPRT, SGMT)
    - category: Filter by market category code
    - search: Search in market name or legal entity name
    - limit: Number of results to return (default 100, max 1000)
    - offset: Number of results to skip (default 0)
    """
    with get_session() as session:
        query = session.query(MarketIdentificationCode)

        # Apply filters
        country = request.args.get("country")
        if country:
            query = query.filter(MarketIdentificationCode.iso_country_code == country.upper())

        status = request.args.get("status")
        if status:
            try:
                status_enum = MICStatus(status.upper())
                query = query.filter(MarketIdentificationCode.status == status_enum)
            except ValueError:
                return jsonify({"error": f"Invalid status: {status}"}), 400

        operation_type = request.args.get("type")
        if operation_type:
            try:
                type_enum = MICType(operation_type.upper())
                query = query.filter(MarketIdentificationCode.operation_type == type_enum)
            except ValueError:
                return jsonify({"error": f"Invalid operation type: {operation_type}"}), 400

        category = request.args.get("category")
        if category:
            try:
                category_enum = MarketCategoryCode(category.upper())
                query = query.filter(MarketIdentificationCode.market_category_code == category_enum)
            except ValueError:
                return jsonify({"error": f"Invalid market category: {category}"}), 400

        search = request.args.get("search")
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (MarketIdentificationCode.market_name.ilike(search_pattern))
                | (MarketIdentificationCode.legal_entity_name.ilike(search_pattern))
            )

        # Pagination
        limit = min(int(request.args.get("limit", 100)), 1000)
        offset = int(request.args.get("offset", 0))

        total_count = query.count()
        mics = query.offset(offset).limit(limit).all()

        # Determine response format
        summary = request.args.get("summary", "false").lower() == "true"

        return jsonify(
            {
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
                "mics": [mic.to_summary_dict() if summary else mic.to_dict() for mic in mics],
            }
        )


@mic_bp.route("/<mic_code>", methods=["GET"])
def get_mic(mic_code: str):
    """Get detailed information for a specific MIC code."""
    with get_session() as session:
        mic = session.query(MarketIdentificationCode).filter_by(mic=mic_code.upper()).first()

        if not mic:
            return jsonify({"error": f"MIC not found: {mic_code}"}), 404

        # Optionally include related trading venues
        include_venues = request.args.get("include_venues", "false").lower() == "true"

        result = mic.to_dict()

        if include_venues:
            # Get trading venues that use this MIC
            from ..models.sqlite.instrument import TradingVenue

            venues = session.query(TradingVenue).filter_by(mic_code=mic_code.upper()).all()
            result["trading_venues"] = [
                {
                    "id": venue.id,
                    "venue_id": venue.venue_id,
                    "isin": venue.isin,
                    "first_trade_date": (
                        venue.first_trade_date.isoformat() if venue.first_trade_date else None
                    ),
                }
                for venue in venues
            ]

        return jsonify(result)


@mic_bp.route("/<mic_code>/segments", methods=["GET"])
def get_mic_segments(mic_code: str):
    """Get all segment MICs for a given operating MIC."""
    with get_session() as session:
        # Verify the operating MIC exists
        operating_mic = (
            session.query(MarketIdentificationCode)
            .filter_by(mic=mic_code.upper(), operation_type=MICType.OPRT)
            .first()
        )

        if not operating_mic:
            return jsonify({"error": f"Operating MIC not found: {mic_code}"}), 404

        segments = MarketIdentificationCode.get_segments_for_operating_mic(
            session, mic_code.upper()
        )

        return jsonify(
            {
                "operating_mic": operating_mic.to_dict(),
                "segments": [segment.to_dict() for segment in segments],
            }
        )


@mic_bp.route("/countries", methods=["GET"])
def list_countries():
    """List all countries with MIC codes and counts."""
    with get_session() as session:
        # Get countries with active MICs using simpler approach
        from sqlalchemy import func

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

            results.append(
                {
                    "country_code": country_code,
                    "total_mics": int(total_mics),
                    "operating_mics": int(operating_count),
                    "segment_mics": int(segment_count),
                }
            )

        return jsonify({"countries": results})


@mic_bp.route("/search", methods=["GET"])
def search_mics():
    """
    Advanced search for MIC codes.

    Query parameters:
    - q: Search query (searches name, entity, acronym)
    - country: Country filter
    - active_only: Only return active MICs (default: true)
    """
    query_text = request.args.get("q", "").strip()
    if not query_text:
        return jsonify({"error": 'Search query parameter "q" is required'}), 400

    with get_session() as session:
        search_pattern = f"%{query_text}%"

        query = session.query(MarketIdentificationCode).filter(
            (MarketIdentificationCode.market_name.ilike(search_pattern))
            | (MarketIdentificationCode.legal_entity_name.ilike(search_pattern))
            | (MarketIdentificationCode.acronym.ilike(search_pattern))
            | (MarketIdentificationCode.mic.ilike(search_pattern))
        )

        # Filter by country if specified
        country = request.args.get("country")
        if country:
            query = query.filter(MarketIdentificationCode.iso_country_code == country.upper())

        # Filter by active status by default
        active_only = request.args.get("active_only", "true").lower() != "false"
        if active_only:
            query = query.filter(MarketIdentificationCode.status == MICStatus.ACTIVE)

        results = query.limit(50).all()  # Limit search results

        return jsonify(
            {
                "query": query_text,
                "count": len(results),
                "results": [mic.to_summary_dict() for mic in results],
            }
        )


@mic_bp.route("/statistics", methods=["GET"])
def get_statistics():
    """Get MIC registry statistics."""
    with get_session() as session:
        loader = MICDataLoader(session)
        stats = loader.get_load_statistics()
        validation_issues = loader.validate_mic_relationships()

        return jsonify(
            {
                "statistics": stats,
                "validation_issues": validation_issues,
                "data_quality": {
                    "total_issues": len(validation_issues),
                    "data_integrity": "good" if len(validation_issues) == 0 else "issues_found",
                },
            }
        )


@mic_bp.route("/load-data", methods=["POST"])
def load_mic_data():
    """
    Load MIC data from CSV file or remote source.

    Request body (optional):
    {
        "source": "remote" | "local",
        "csv_path": "/path/to/file.csv",  // only for local source
        "data_version": "optional_version_identifier"
    }

    If no body provided, loads from official ISO 20022 remote source.
    """
    data = request.get_json() if request.is_json else {}

    source = data.get("source", "remote")
    csv_path = data.get("csv_path")
    data_version = data.get("data_version")

    # Validate input
    if source == "local" and not csv_path:
        return jsonify({"error": 'csv_path is required when source is "local"'}), 400

    if source not in ["remote", "local"]:
        return jsonify({"error": 'source must be either "remote" or "local"'}), 400

    with get_session() as session:
        try:
            if source == "remote":
                result = load_mic_data_from_csv(session, csv_source=None, data_version=data_version)
            else:
                result = load_mic_data_from_csv(
                    session, csv_source=csv_path, data_version=data_version
                )

            if result["success"]:
                return jsonify(result), 200
            else:
                return jsonify(result), 500

        except Exception as e:
            return jsonify({"success": False, "error": str(e), "source": source}), 500


@mic_bp.route("/enums", methods=["GET"])
def get_enums():
    """Get available enum values for MIC fields."""
    return jsonify(
        {
            "status_options": [status.value for status in MICStatus],
            "operation_types": [op_type.value for op_type in MICType],
            "market_categories": [category.value for category in MarketCategoryCode],
        }
    )


@mic_bp.route("/remote/lookup/<mic_code>", methods=["GET"])
def remote_lookup_mic(mic_code: str):
    """
    Look up a MIC code directly from the official ISO registry (no database required).

    This endpoint fetches data directly from the ISO 20022 website,
    useful for real-time validation without local database dependency.
    """
    try:
        mic_info = remote_mic_service.lookup_mic(mic_code.upper())

        if mic_info is None:
            return jsonify({"error": f"MIC code {mic_code.upper()} not found in ISO registry"}), 404

        return jsonify(
            {
                "mic_code": mic_code.upper(),
                "source": "iso_registry_remote",
                "url": OFFICIAL_MIC_CSV_URL,
                "data": mic_info,
            }
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to lookup MIC from remote source: {str(e)}"}), 500


@mic_bp.route("/remote/search", methods=["GET"])
def remote_search_mics():
    """
    Search MICs directly from the official ISO registry (no database required).

    Query parameters:
    - q: Search query (required)
    - limit: Number of results (default 20, max 100)
    """
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": 'Search query parameter "q" is required'}), 400

    limit = min(int(request.args.get("limit", 20)), 100)

    try:
        results = remote_mic_service.search_mics(query, limit)

        return jsonify(
            {
                "query": query,
                "source": "iso_registry_remote",
                "url": OFFICIAL_MIC_CSV_URL,
                "count": len(results),
                "results": results,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Failed to search MICs from remote source: {str(e)}"}), 500


@mic_bp.route("/remote/country/<country_code>", methods=["GET"])
def remote_get_country_mics(country_code: str):
    """
    Get all MICs for a country directly from the official ISO registry.

    Args:
        country_code: ISO 3166 country code (e.g., 'US', 'GB', 'DE')
    """
    try:
        results = remote_mic_service.get_country_mics(country_code.upper())

        return jsonify(
            {
                "country_code": country_code.upper(),
                "source": "iso_registry_remote",
                "url": OFFICIAL_MIC_CSV_URL,
                "count": len(results),
                "mics": results,
            }
        )

    except Exception as e:
        return jsonify({"error": f"Failed to get country MICs from remote source: {str(e)}"}), 500


@mic_bp.route("/remote/validate/<mic_code>", methods=["GET"])
def remote_validate_mic(mic_code: str):
    """
    Validate a MIC code directly from the official ISO registry.

    Returns validation result with detailed information about the MIC's status.
    """
    try:
        validation_result = remote_mic_service.validate_mic(mic_code.upper())

        return jsonify(
            {
                "mic_code": mic_code.upper(),
                "source": "iso_registry_remote",
                "url": OFFICIAL_MIC_CSV_URL,
                **validation_result,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "mic_code": mic_code.upper(),
                    "valid": False,
                    "error": f"Failed to validate MIC: {str(e)}",
                }
            ),
            500,
        )


@mic_bp.route("/remote/cache/clear", methods=["POST"])
def clear_remote_cache():
    """Clear the remote MIC data cache to force fresh data on next request."""
    try:
        remote_mic_service.clear_cache()
        return jsonify({"success": True, "message": "Remote MIC cache cleared successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Error handlers
@mic_bp.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@mic_bp.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
