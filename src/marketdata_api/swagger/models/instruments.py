"""
Instrument Swagger Models

This module contains all Swagger model definitions for instrument-related endpoints,
including CFI operations and enrichment functionality.
"""

from flask_restx import fields


def create_instrument_models(api, common_models):
    """
    Create instrument-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common model definitions

    Returns:
        dict: Dictionary of instrument model definitions
    """

    # Basic instrument model
    instrument_base = api.model(
        "InstrumentBase",
        {
            "id": fields.String(required=True, description="Internal instrument ID"),
            "isin": fields.String(
                required=True,
                description="International Securities Identification Number",
                example="US0378331005",
            ),
            "type": fields.String(required=True, description="Instrument type", example="equity"),
            "symbol": fields.String(description="Trading symbol", example="AAPL"),
            "full_name": fields.String(description="Full instrument name", example="Apple Inc."),
            "currency": fields.String(description="Trading currency", example="USD"),
            "cfi_code": fields.String(description="6-character CFI code", example="ESVUFR"),
            "mic_code": fields.String(description="Market Identification Code", example="XNYS"),
            "created_at": fields.DateTime(description="Creation timestamp"),
            "updated_at": fields.DateTime(description="Last update timestamp"),
        },
    )

    # Classification model
    classification_model = api.model(
        "Classification",
        {
            "cfi_code": fields.String(description="CFI code"),
            "category": fields.String(description="CFI category"),
            "group": fields.String(description="CFI group"),
            "attributes": fields.String(description="CFI attributes"),
            "business_type": fields.String(description="Business instrument type"),
        },
    )

    # Issuer model
    issuer_model = api.model(
        "Issuer",
        {
            "lei": fields.String(description="Legal Entity Identifier"),
            "name": fields.String(description="Issuer name"),
            "jurisdiction": fields.String(description="Issuer jurisdiction"),
        },
    )

    # Detailed instrument model
    instrument_detailed = api.inherit(
        "InstrumentDetailed",
        instrument_base,
        {
            "classification": fields.Nested(
                classification_model, description="CFI classification details"
            ),
            "issuer": fields.Nested(issuer_model, description="Issuer information"),
            "figi_mapping": fields.Raw(description="FIGI mapping data"),
            "legal_entity": fields.Raw(description="Legal entity information"),
            "trading_venues": fields.List(
                fields.Raw, description="Trading venues where instrument is listed"
            ),
        },
    )

    # Instrument list response
    instrument_list_response = api.model(
        "InstrumentListResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(instrument_base)),
            "meta": fields.Nested(common_models["pagination_meta"]),
        },
    )

    # Instrument detail response
    instrument_detail_response = api.model(
        "InstrumentDetailResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(instrument_detailed),
        },
    )

    # Venue information model
    venue_info = api.model(
        "VenueInfo",
        {
            "venue_id": fields.String(description="Venue identifier"),
            "venue_name": fields.String(description="Venue name"),
            "mic_code": fields.String(description="Market Identification Code"),
            "country": fields.String(description="Venue country"),
            "is_primary": fields.Boolean(description="Whether this is the primary venue"),
        },
    )

    # Instrument venues response
    instrument_venues_response = api.model(
        "InstrumentVenuesResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(
                api.model(
                    "VenuesData",
                    {
                        "isin": fields.String(required=True, description="Instrument ISIN"),
                        "instrument_type": fields.String(
                            required=True, description="Instrument type"
                        ),
                        "venue_count": fields.Integer(
                            required=True, description="Number of venues"
                        ),
                        "venues": fields.List(
                            fields.Nested(venue_info), description="Venue details"
                        ),
                    },
                )
            ),
        },
    )

    # Enrichment result model
    enrichment_result = api.model(
        "EnrichmentResult",
        {
            "before": fields.Boolean(description="Had data before enrichment"),
            "after": fields.Boolean(description="Has data after enrichment"),
            "changed": fields.Boolean(description="Whether data changed during enrichment"),
        },
    )

    # Instrument enrichment response
    instrument_enrichment_response = api.model(
        "InstrumentEnrichmentResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "message": fields.String(required=True, description="Enrichment result message"),
            "id": fields.String(required=True, description="Instrument ID"),
            "isin": fields.String(required=True, description="Instrument ISIN"),
            "enrichment_results": fields.Nested(
                api.model(
                    "EnrichmentResults",
                    {
                        "figi": fields.Nested(
                            enrichment_result, description="FIGI enrichment result"
                        ),
                        "lei": fields.Nested(
                            enrichment_result, description="LEI enrichment result"
                        ),
                    },
                )
            ),
        },
    )

    # Valid types response
    valid_types_response = api.model(
        "ValidTypesResponse",
        {
            "valid_types": fields.List(
                fields.String, required=True, description="List of valid instrument types"
            ),
            "message": fields.String(required=True, description="Description message"),
        },
    )

    # CFI decoded attributes
    cfi_decoded_attributes = api.model(
        "CFIDecodedAttributes",
        {
            "voting_rights": fields.String(description="Voting rights description"),
            "ownership_restrictions": fields.String(
                description="Ownership restrictions description"
            ),
            "payment_status": fields.String(description="Payment status description"),
            "form": fields.String(description="Form description"),
        },
    )

    # CFI information response
    cfi_info_response = api.model(
        "CFIInfoResponse",
        {
            "cfi_code": fields.String(required=True, description="The CFI code"),
            "category": fields.String(description="CFI category letter"),
            "category_description": fields.String(description="CFI category description"),
            "group": fields.String(description="CFI group letter"),
            "group_description": fields.String(description="CFI group description"),
            "attributes": fields.String(description="CFI attributes (4 characters)"),
            "decoded_attributes": fields.Nested(
                cfi_decoded_attributes, description="Decoded CFI attributes"
            ),
            "business_type": fields.String(description="Business instrument type"),
            "fitrs_patterns": fields.List(
                fields.String, description="FITRS file patterns for this CFI"
            ),
            "is_equity": fields.Boolean(description="Whether this is an equity instrument"),
            "is_debt": fields.Boolean(description="Whether this is a debt instrument"),
            "is_collective_investment": fields.Boolean(
                description="Whether this is a collective investment"
            ),
            "is_derivative": fields.Boolean(description="Whether this is a derivative"),
        },
    )

    # Instrument CFI classification response
    instrument_cfi_classification = api.model(
        "InstrumentCFIClassification",
        {
            "isin": fields.String(required=True, description="Instrument ISIN"),
            "instrument_id": fields.String(required=True, description="Internal instrument ID"),
            "current_instrument_type": fields.String(
                description="Current instrument type in database"
            ),
            "cfi_classification": fields.Nested(
                cfi_info_response, description="Full CFI classification"
            ),
            "consistency_check": fields.Nested(
                api.model(
                    "ConsistencyCheck",
                    {
                        "cfi_suggests_type": fields.String(
                            description="Type suggested by CFI code"
                        ),
                        "current_type": fields.String(description="Current type in database"),
                        "is_consistent": fields.Boolean(
                            description="Whether CFI and database types match"
                        ),
                    },
                ),
                description="Consistency analysis between CFI and database",
            ),
        },
    )

    # Instrument creation request
    instrument_create_request = api.model(
        "InstrumentCreateRequest",
        {
            "isin": fields.String(required=True, description="ISIN code", example="US0378331005"),
            "type": fields.String(required=True, description="Instrument type", example="equity"),
            "cfi_code": fields.String(
                required=False, description="CFI code for validation (optional)"
            ),
            "symbol": fields.String(required=False, description="Trading symbol (optional)"),
            "name": fields.String(required=False, description="Instrument name (optional)"),
            "currency": fields.String(required=False, description="Trading currency (optional)"),
            "mic_code": fields.String(
                required=False, description="Market Identification Code (optional)"
            ),
        },
    )

    return {
        "instrument_base": instrument_base,
        "instrument_detailed": instrument_detailed,
        "instrument_list_response": instrument_list_response,
        "instrument_detail_response": instrument_detail_response,
        "instrument_venues_response": instrument_venues_response,
        "instrument_enrichment_response": instrument_enrichment_response,
        "valid_types_response": valid_types_response,
        "cfi_info_response": cfi_info_response,
        "instrument_cfi_classification": instrument_cfi_classification,
        "instrument_create_request": instrument_create_request,
        "classification_model": classification_model,
        "issuer_model": issuer_model,
        "venue_info": venue_info,
    }
