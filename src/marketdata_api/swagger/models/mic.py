"""
MIC Code Swagger Models

This module contains all Swagger model definitions for Market Identification Code (MIC)
endpoints, including both local database and remote real-time operations.
"""

from flask_restx import fields


def create_mic_models(api, common_models):
    """
    Create MIC-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common model definitions

    Returns:
        dict: Dictionary of MIC model definitions
    """

    # Basic MIC model
    mic_base = api.model(
        "MICBase",
        {
            "mic": fields.String(
                required=True, description="4-character Market Identification Code", example="XNYS"
            ),
            "operating_mic": fields.String(
                description="Operating MIC for segment MICs", example="XNYS"
            ),
            "oprt_sgmt": fields.String(
                description="Operating/Segment indicator", enum=["OPRT", "SGMT"]
            ),
            "market_name": fields.String(
                required=True,
                description="Official market name",
                example="NEW YORK STOCK EXCHANGE, INC.",
            ),
            "legal_entity_name": fields.String(description="Legal entity operating the market"),
            "lei": fields.String(
                description="Legal Entity Identifier", example="549300DTUYXVMJXZNY12"
            ),
            "market_category_code": fields.String(
                description="Market category",
                enum=[
                    "APPA",
                    "REGULATED",
                    "MULTMK",
                    "SMN",
                    "OPEN",
                    "OTHR",
                    "SEFS",
                    "TRFS",
                    "CASP",
                    "IDQS",
                ],
            ),
            "acronym": fields.String(description="Market acronym", example="NYSE"),
            "iso_country_code": fields.String(
                required=True, description="ISO 3166-1 alpha-2 country code", example="US"
            ),
            "city": fields.String(description="City where market is located", example="NEW YORK"),
            "website": fields.String(description="Market website URL"),
            "status": fields.String(
                description="MIC status", enum=["ACTIVE", "EXPIRED", "DELETED", "MODIFIED"]
            ),
            "creation_date": fields.Date(description="Date when MIC was created"),
            "last_update_date": fields.Date(description="Date of last update"),
            "last_validation_date": fields.Date(description="Date of last validation"),
            "expiry_date": fields.Date(description="MIC expiry date if applicable"),
            "comments": fields.String(description="Additional comments about the MIC"),
        },
    )

    # MIC with venue relationships
    mic_detailed = api.inherit(
        "MICDetailed",
        mic_base,
        {
            "venue_count": fields.Integer(description="Number of trading venues using this MIC"),
            "segment_mics": fields.List(
                fields.Nested(mic_base), description="Segment MICs under this operating MIC"
            ),
            "trading_venues": fields.List(fields.Raw, description="Trading venues using this MIC"),
        },
    )

    # MIC list response
    mic_list_response = api.model(
        "MICListResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(mic_base)),
            "meta": fields.Nested(common_models["pagination_meta"]),
        },
    )

    # MIC detail response
    mic_detail_response = api.model(
        "MICDetailResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(mic_detailed),
        },
    )

    # MIC search request
    mic_search_request = api.model(
        "MICSearchRequest",
        {
            "name": fields.String(description="Search in market name"),
            "entity": fields.String(description="Search in legal entity name"),
            "country": fields.String(description="ISO country code filter"),
            "status": fields.String(
                description="Status filter", enum=["ACTIVE", "EXPIRED", "DELETED", "MODIFIED"]
            ),
            "category": fields.String(
                description="Category filter",
                enum=[
                    "APPA",
                    "REGULATED",
                    "MULTMK",
                    "SMN",
                    "OPEN",
                    "OTHR",
                    "SEFS",
                    "TRFS",
                    "CASP",
                    "IDQS",
                ],
            ),
            "mic_type": fields.String(description="MIC type filter", enum=["OPRT", "SGMT"]),
            "limit": fields.Integer(description="Maximum results", default=100),
        },
    )

    # Country statistics model
    country_stats = api.model(
        "CountryStats",
        {
            "country_code": fields.String(required=True, description="ISO country code"),
            "country_name": fields.String(description="Country name"),
            "total_mics": fields.Integer(required=True, description="Total MICs in country"),
            "active_mics": fields.Integer(description="Active MICs in country"),
            "operating_mics": fields.Integer(description="Operating MICs in country"),
            "segment_mics": fields.Integer(description="Segment MICs in country"),
            "markets": fields.List(
                fields.Nested(mic_base), description="Sample of markets in country"
            ),
        },
    )

    # MIC statistics response
    mic_statistics_response = api.model(
        "MICStatisticsResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(
                api.model(
                    "MICStatistics",
                    {
                        "total_mics": fields.Integer(description="Total MIC records"),
                        "active_mics": fields.Integer(description="Active MIC records"),
                        "operating_mics": fields.Integer(description="Operating MIC records"),
                        "segment_mics": fields.Integer(description="Segment MIC records"),
                        "countries_count": fields.Integer(
                            description="Number of countries with MICs"
                        ),
                        "last_update": fields.DateTime(description="Last data update timestamp"),
                        "data_quality": fields.Nested(
                            api.model(
                                "DataQuality",
                                {
                                    "mics_with_lei": fields.Integer(description="MICs with LEI"),
                                    "mics_with_website": fields.Integer(
                                        description="MICs with website"
                                    ),
                                    "orphaned_segments": fields.Integer(
                                        description="Segment MICs without operating MIC"
                                    ),
                                },
                            )
                        ),
                    },
                )
            ),
        },
    )

    # Load data request
    mic_load_request = api.model(
        "MICLoadRequest",
        {
            "source": fields.String(
                required=True, description="Data source", enum=["local", "remote"]
            ),
            "file_path": fields.String(description="Local file path (for local source)"),
            "force_update": fields.Boolean(
                description="Force update existing records", default=False
            ),
        },
    )

    # Load data response
    mic_load_response = api.model(
        "MICLoadResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "message": fields.String(required=True, description="Operation result message"),
            "data": fields.Nested(
                api.model(
                    "LoadResults",
                    {
                        "total_processed": fields.Integer(description="Total records processed"),
                        "created": fields.Integer(description="New records created"),
                        "updated": fields.Integer(description="Existing records updated"),
                        "skipped": fields.Integer(description="Records skipped"),
                        "errors": fields.Integer(description="Records with errors"),
                        "source": fields.String(description="Data source used"),
                        "file_info": fields.Nested(
                            api.model(
                                "FileInfo",
                                {
                                    "filename": fields.String(description="Source filename"),
                                    "size": fields.Integer(description="File size in bytes"),
                                    "last_modified": fields.DateTime(
                                        description="File modification time"
                                    ),
                                },
                            ),
                            description="Source file information",
                        ),
                    },
                )
            ),
        },
    )

    # Remote lookup response
    remote_mic_response = api.model(
        "RemoteMICResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(mic_base),
            "meta": fields.Nested(
                api.model(
                    "RemoteMeta",
                    {
                        "source": fields.String(description="Remote data source"),
                        "cached": fields.Boolean(description="Whether result was cached"),
                        "cache_expires": fields.DateTime(description="Cache expiry time"),
                        "last_updated": fields.DateTime(description="Remote data last update"),
                    },
                )
            ),
        },
    )

    # Remote validation response
    remote_validation_response = api.model(
        "RemoteValidationResponse",
        {
            "valid": fields.Boolean(required=True, description="Whether MIC code is valid"),
            "mic_code": fields.String(required=True, description="Validated MIC code"),
            "market_name": fields.String(description="Market name if valid"),
            "status": fields.String(description="MIC status if valid"),
            "message": fields.String(description="Validation message"),
        },
    )

    # Enum values response
    mic_enums_response = api.model(
        "MICEnumsResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(
                api.model(
                    "MICEnums",
                    {
                        "status_values": fields.List(
                            fields.String, description="Valid MIC status values"
                        ),
                        "category_values": fields.List(
                            fields.String, description="Valid market category values"
                        ),
                        "type_values": fields.List(
                            fields.String, description="Valid MIC type values"
                        ),
                    },
                )
            ),
        },
    )

    return {
        "mic_base": mic_base,
        "mic_detailed": mic_detailed,
        "mic_list_response": mic_list_response,
        "mic_detail_response": mic_detail_response,
        "mic_search_request": mic_search_request,
        "country_stats": country_stats,
        "mic_statistics_response": mic_statistics_response,
        "mic_load_request": mic_load_request,
        "mic_load_response": mic_load_response,
        "remote_mic_response": remote_mic_response,
        "remote_validation_response": remote_validation_response,
        "mic_enums_response": mic_enums_response,
    }
