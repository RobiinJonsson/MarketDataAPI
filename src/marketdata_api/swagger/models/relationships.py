"""
Relationships Swagger Models

This module contains all Swagger model definitions for entity relationship endpoints.
"""

from flask_restx import fields


def create_relationship_models(api, common_models):
    """
    Create relationship-related Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common model definitions

    Returns:
        dict: Dictionary of relationship model definitions
    """

    # Basic relationship model
    relationship_base = api.model(
        "RelationshipBase",
        {
            "relationship_type": fields.String(
                required=True, description="Type of relationship", enum=["DIRECT", "ULTIMATE"]
            ),
            "relationship_status": fields.String(
                required=True, description="Status of the relationship", enum=["ACTIVE", "INACTIVE"]
            ),
            "parent_lei": fields.String(required=True, description="LEI of the parent entity"),
            "parent_name": fields.String(description="Name of the parent entity"),
            "parent_jurisdiction": fields.String(description="Jurisdiction of the parent entity"),
            "child_lei": fields.String(required=True, description="LEI of the child entity"),
            "child_name": fields.String(description="Name of the child entity"),
            "child_jurisdiction": fields.String(description="Jurisdiction of the child entity"),
            "relationship_period_start": fields.DateTime(
                description="Start date of the relationship"
            ),
            "relationship_period_end": fields.DateTime(description="End date of the relationship"),
            "percentage_ownership": fields.Float(description="Percentage of ownership (0-100)"),
        },
    )

    # Entity summary for relationships
    entity_summary = api.model(
        "EntitySummary",
        {
            "lei": fields.String(required=True, description="Legal Entity Identifier"),
            "name": fields.String(required=True, description="Entity name"),
            "jurisdiction": fields.String(description="Entity jurisdiction"),
            "legal_form": fields.String(description="Legal form"),
            "status": fields.String(description="Entity status"),
        },
    )

    # Relationship list response
    relationship_list_response = api.model(
        "RelationshipListResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(
                api.model(
                    "RelationshipData",
                    {
                        "entity": fields.Nested(
                            entity_summary, required=True, description="The queried entity"
                        ),
                        "relationships": fields.List(
                            fields.Nested(relationship_base),
                            required=True,
                            description="List of relationships",
                        ),
                    },
                )
            ),
            "meta": fields.Nested(common_models["pagination_meta"]),
        },
    )

    # Relationship creation request
    relationship_create_request = api.model(
        "RelationshipCreateRequest",
        {
            "parent_lei": fields.String(required=True, description="LEI of the parent entity"),
            "child_lei": fields.String(required=True, description="LEI of the child entity"),
            "relationship_type": fields.String(
                required=True, description="Type of relationship", enum=["DIRECT", "ULTIMATE"]
            ),
            "relationship_status": fields.String(
                description="Status of the relationship",
                enum=["ACTIVE", "INACTIVE"],
                default="ACTIVE",
            ),
            "percentage_ownership": fields.Float(description="Percentage of ownership (0-100)"),
            "relationship_period_start": fields.DateTime(
                description="Start date of the relationship"
            ),
            "relationship_period_end": fields.DateTime(description="End date of the relationship"),
        },
    )

    # Relationship hierarchy response
    relationship_hierarchy_response = api.model(
        "RelationshipHierarchyResponse",
        {
            "status": fields.String(required=True, description="Response status", enum=["success"]),
            "data": fields.Nested(
                api.model(
                    "HierarchyData",
                    {
                        "root_entity": fields.Nested(entity_summary, description="Root entity"),
                        "hierarchy": fields.Raw(
                            description="Hierarchical structure of relationships"
                        ),
                        "total_entities": fields.Integer(description="Total entities in hierarchy"),
                        "max_depth": fields.Integer(description="Maximum depth of hierarchy"),
                    },
                )
            ),
        },
    )

    return {
        "relationship_base": relationship_base,
        "entity_summary": entity_summary,
        "relationship_list_response": relationship_list_response,
        "relationship_create_request": relationship_create_request,
        "relationship_hierarchy_response": relationship_hierarchy_response,
    }
