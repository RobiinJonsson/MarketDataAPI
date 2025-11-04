"""
Venue Swagger Models

This module contains all Swagger model definitions for trading venue endpoints,
including venue listing, search, statistics, and instrument relationships.
"""

from flask_restx import fields


def create_venue_models(api, common_models):
    """
    Create venue-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common model definitions

    Returns:
        dict: Dictionary of venue model definitions
    """

    # Basic venue summary model
    venue_summary = api.model(
        "VenueSummary",
        {
            "mic_code": fields.String(
                required=True, description="4-character Market Identification Code", example="XNYS"
            ),
            "operating_mic": fields.String(
                description="Operating MIC for segment MICs", example="XNYS"
            ),
            "market_name": fields.String(
                required=True,
                description="Official market name",
                example="NEW YORK STOCK EXCHANGE, INC.",
            ),
            "legal_entity_name": fields.String(description="Legal entity operating the market"),
            "country_code": fields.String(
                description="ISO country code", example="US"
            ),
            "city": fields.String(description="Market city", example="NEW YORK"),
            "status": fields.String(
                description="Market status",
                enum=["ACTIVE", "EXPIRED", "SUSPENDED", "UPDATED"],
                example="ACTIVE"
            ),
            "operation_type": fields.String(
                description="Operating/Segment indicator", 
                enum=["OPRT", "SGMT"],
                example="OPRT"
            ),
            "market_category": fields.String(
                description="Market category code",
                enum=["APPA", "ATSS", "CASP", "DCMS", "IDQS", "MLTF", "NSPD", "OTFS", "OTHR", "RMOS", "RMKT", "SEFS", "SINT", "TRFS"]
            ),
            "website": fields.String(description="Market website URL"),
            "instrument_count": fields.Integer(description="Number of instruments traded", example=1500),
            "last_update_date": fields.DateTime(description="Last update date"),
        },
    )

    # Detailed venue model
    venue_detail = api.model(
        "VenueDetail",
        {
            "mic_code": fields.String(
                required=True, description="4-character Market Identification Code", example="XNYS"
            ),
            "operating_mic": fields.String(
                description="Operating MIC for segment MICs", example="XNYS"
            ),
            "market_name": fields.String(
                required=True,
                description="Official market name",
                example="NEW YORK STOCK EXCHANGE, INC.",
            ),
            "legal_entity_name": fields.String(description="Legal entity operating the market"),
            "acronym": fields.String(description="Market acronym", example="NYSE"),
            "lei": fields.String(
                description="Legal Entity Identifier", example="549300DTUYXVMJXZNY12"
            ),
            "country_code": fields.String(
                description="ISO country code", example="US"
            ),
            "city": fields.String(description="Market city", example="NEW YORK"),
            "status": fields.String(
                description="Market status",
                enum=["ACTIVE", "EXPIRED", "SUSPENDED", "UPDATED"],
                example="ACTIVE"
            ),
            "operation_type": fields.String(
                description="Operating/Segment indicator", 
                enum=["OPRT", "SGMT"],
                example="OPRT"
            ),
            "market_category": fields.String(
                description="Market category code",
                enum=["APPA", "ATSS", "CASP", "DCMS", "IDQS", "MLTF", "NSPD", "OTFS", "OTHR", "RMOS", "RMKT", "SEFS", "SINT", "TRFS"]
            ),
            "website": fields.String(description="Market website URL"),
            "comments": fields.String(description="Additional comments"),
            "instrument_count": fields.Integer(description="Number of instruments traded", example=1500),
            "creation_date": fields.DateTime(description="MIC creation date"),
            "last_update_date": fields.DateTime(description="Last update date"),
            "last_validation_date": fields.DateTime(description="Last validation date"),
            "expiry_date": fields.DateTime(description="MIC expiry date if applicable"),
            "data_source_version": fields.String(description="Data source version"),
        },
    )

    # Segment MIC model
    segment_mic = api.model(
        "SegmentMIC",
        {
            "mic_code": fields.String(required=True, description="Segment MIC code"),
            "market_name": fields.String(description="Segment market name"),
            "status": fields.String(description="Segment status"),
        },
    )

    # Venue with segments (for operating MICs)
    venue_with_segments = api.inherit(
        "VenueWithSegments",
        venue_detail,
        {
            "segment_mics": fields.List(
                fields.Nested(segment_mic), description="Segment MICs under this operating MIC"
            ),
        },
    )

    # Instrument in venue context
    venue_instrument = api.model(
        "VenueInstrument",
        {
            "isin": fields.String(required=True, description="Instrument ISIN", example="US0378331005"),
            "venue_id": fields.String(description="Venue-specific instrument ID"),
            "instrument_name": fields.String(description="Instrument name"),
            "cfi_code": fields.String(description="CFI classification code"),
            "instrument_type": fields.String(description="Instrument type"),
            "issuer_name": fields.String(description="Issuer name"),
            "first_trade_date": fields.DateTime(description="First trading date"),
            "termination_date": fields.DateTime(description="Trading termination date"),
            "venue_currency": fields.String(description="Trading currency"),
            "venue_status": fields.String(description="Venue-specific status"),
        },
    )

    # Venue statistics model
    venue_statistics = api.model(
        "VenueStatistics",
        {
            "total_mics": fields.Integer(description="Total number of MIC codes", example=1247),
            "operating_mics": fields.Integer(description="Number of operating MICs", example=890),
            "segment_mics": fields.Integer(description="Number of segment MICs", example=357),
            "status_breakdown": fields.Raw(description="Breakdown by status"),
            "top_countries": fields.List(
                fields.Raw(description="Country with venue count"),
                description="Top countries by venue count"
            ),
            "venues_with_instruments": fields.Integer(description="Venues with instruments"),
            "total_trading_venues": fields.Integer(description="Total trading venue records"),
        },
    )

    # Country summary model
    country_summary = api.model(
        "CountrySummary",
        {
            "country_code": fields.String(required=True, description="ISO country code"),
            "total_mics": fields.Integer(description="Total MICs in country"),
            "operating_mics": fields.Integer(description="Operating MICs in country"),
            "segment_mics": fields.Integer(description="Segment MICs in country"),
        },
    )

    # Response models
    venue_list_response = api.model(
        "VenueListResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(venue_summary), description="List of venues"),
            "pagination": fields.Nested(common_models["pagination_meta"], description="Pagination info"),
        },
    )

    venue_detail_response = api.model(
        "VenueDetailResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(venue_with_segments, description="Detailed venue information"),
        },
    )

    venue_instruments_response = api.model(
        "VenueInstrumentsResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(venue_instrument), description="List of instruments"),
            "pagination": fields.Nested(common_models["pagination_meta"], description="Pagination info"),
        },
    )

    venue_search_response = api.model(
        "VenueSearchResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(venue_summary), description="Search results"),
        },
    )

    venue_statistics_response = api.model(
        "VenueStatisticsResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(venue_statistics, description="Venue statistics"),
        },
    )

    venue_countries_response = api.model(
        "VenueCountriesResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(country_summary), description="Countries with venue counts"),
        },
    )

    return {
        "venue_summary": venue_summary,
        "venue_detail": venue_detail,
        "venue_with_segments": venue_with_segments,
        "venue_instrument": venue_instrument,
        "venue_statistics": venue_statistics,
        "country_summary": country_summary,
        "venue_list_response": venue_list_response,
        "venue_detail_response": venue_detail_response,
        "venue_instruments_response": venue_instruments_response,
        "venue_search_response": venue_search_response,
        "venue_statistics_response": venue_statistics_response,
        "venue_countries_response": venue_countries_response,
    }