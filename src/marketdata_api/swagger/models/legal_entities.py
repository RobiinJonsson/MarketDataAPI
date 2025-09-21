"""
Legal Entity Swagger Models

This module contains all Swagger model definitions for legal entity-related endpoints,
including address and registration information.
"""

from flask_restx import fields


def create_legal_entity_models(api, common_models):
    """
    Create legal entity-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common model definitions

    Returns:
        dict: Dictionary of legal entity model definitions
    """

    # Basic legal entity model
    legal_entity_base = api.model(
        "LegalEntityBase",
        {
            "lei": fields.String(
                required=True,
                description="Legal Entity Identifier (20 characters)",
                example="549300DTUYXVMJXZNY12",
            ),
            "name": fields.String(required=True, description="Legal name of the entity"),
            "jurisdiction": fields.String(
                description="Jurisdiction code (ISO 3166-1)", example="US"
            ),
            "legal_form": fields.String(description="Legal form of the entity"),
            "status": fields.String(
                description="Current status", enum=["ACTIVE", "INACTIVE", "PENDING"]
            ),
            "created_at": fields.DateTime(description="Creation timestamp"),
            "updated_at": fields.DateTime(description="Last update timestamp"),
        },
    )

    # Address model
    entity_address_model = api.model(
        "EntityAddress",
        {
            "type": fields.String(
                description="Address type (e.g., HEADQUARTERS, LEGAL)",
                enum=["HEADQUARTERS", "LEGAL", "ALTERNATIVE"],
            ),
            "address_lines": fields.String(description="Complete address lines"),
            "country": fields.String(description="Country code (ISO 3166-1)", example="US"),
            "city": fields.String(description="City name"),
            "region": fields.String(description="Region/State code"),
            "postal_code": fields.String(description="Postal/ZIP code"),
        },
    )

    # Registration model
    entity_registration_model = api.model(
        "EntityRegistration",
        {
            "status": fields.String(
                description="Registration status",
                enum=[
                    "ISSUED",
                    "PENDING_VALIDATION",
                    "ISSUED_PENDING_EXCEPTION",
                    "PENDING_TRANSFER",
                    "CANCELLED",
                    "ANNULLED",
                    "RETIRED",
                    "MERGED",
                    "DUPLICATE",
                    "LAPSED",
                ],
            ),
            "initial_date": fields.DateTime(description="Initial registration date"),
            "last_update": fields.DateTime(description="Last update date"),
            "next_renewal": fields.DateTime(description="Next renewal date"),
            "managing_lou": fields.String(description="Managing Local Operating Unit"),
            "validation_sources": fields.String(description="Validation sources information"),
        },
    )

    # Detailed legal entity model
    legal_entity_detailed = api.inherit(
        "LegalEntityDetailed",
        legal_entity_base,
        {
            "registered_as": fields.String(description="How the entity is registered"),
            "bic": fields.String(description="Business Identifier Code (SWIFT BIC)"),
            "next_renewal_date": fields.DateTime(description="Next renewal date for LEI"),
            "registration_status": fields.String(description="Detailed registration status"),
            "managing_lou": fields.String(description="Managing Local Operating Unit"),
            "creation_date": fields.DateTime(description="Entity creation date"),
            "addresses": fields.List(
                fields.Nested(entity_address_model), description="Entity addresses"
            ),
            "registration": fields.Nested(
                entity_registration_model, description="Registration details"
            ),
        },
    )

    # Legal entity list response
    legal_entity_list_response = api.model(
        "LegalEntityListResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.List(fields.Nested(legal_entity_base)),
            "meta": fields.Nested(common_models["pagination_meta"]),
        },
    )

    # Legal entity detail response
    legal_entity_detail_response = api.model(
        "LegalEntityDetailResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(legal_entity_detailed),
        },
    )

    # Legal entity creation request
    legal_entity_create_request = api.model(
        "LegalEntityCreateRequest",
        {
            "lei": fields.String(
                required=True, description="Legal Entity Identifier", example="549300DTUYXVMJXZNY12"
            ),
            "name": fields.String(required=True, description="Legal name of the entity"),
            "jurisdiction": fields.String(description="Jurisdiction code", example="US"),
            "legal_form": fields.String(description="Legal form"),
            "status": fields.String(
                description="Entity status", enum=["ACTIVE", "INACTIVE", "PENDING"]
            ),
        },
    )

    # Legal entity search request
    legal_entity_search_request = api.model(
        "LegalEntitySearchRequest",
        {
            "name": fields.String(description="Search in entity name"),
            "jurisdiction": fields.String(description="Filter by jurisdiction"),
            "status": fields.String(description="Filter by status"),
            "legal_form": fields.String(description="Filter by legal form"),
            "limit": fields.Integer(description="Maximum results", default=100),
        },
    )

    return {
        "legal_entity_base": legal_entity_base,
        "legal_entity_detailed": legal_entity_detailed,
        "legal_entity_list_response": legal_entity_list_response,
        "legal_entity_detail_response": legal_entity_detail_response,
        "legal_entity_create_request": legal_entity_create_request,
        "legal_entity_search_request": legal_entity_search_request,
        "entity_address_model": entity_address_model,
        "entity_registration_model": entity_registration_model,
    }
