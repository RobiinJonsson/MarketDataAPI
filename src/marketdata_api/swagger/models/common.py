"""
Common Swagger Models

This module contains common/shared Swagger model definitions used across
multiple API endpoints.
"""

from flask_restx import fields

from ...constants import ResponseFields


def create_common_models(api):
    """
    Create common Swagger models and return them as a dictionary.

    Args:
        api: Flask-RESTx API instance

    Returns:
        dict: Dictionary of common model definitions
    """

    # Error model
    error_model = api.model(
        "Error",
        {
            ResponseFields.STATUS: fields.String(
                required=True, description="Error status", enum=["error"]
            ),
            ResponseFields.ERROR: fields.Nested(
                api.model(
                    "ErrorDetails",
                    {
                        "code": fields.String(required=True, description="Error code"),
                        ResponseFields.MESSAGE: fields.String(
                            required=True, description="Error message description"
                        ),
                    },
                )
            ),
        },
    )

    # Pagination metadata
    pagination_meta = api.model(
        "PaginationMeta",
        {
            ResponseFields.PAGE: fields.Integer(description="Current page number"),
            ResponseFields.PER_PAGE: fields.Integer(description="Number of records per page"),
            ResponseFields.TOTAL: fields.Integer(description="Total number of records"),
            "has_next": fields.Boolean(description="Whether there are more pages"),
            "has_prev": fields.Boolean(description="Whether there are previous pages"),
        },
    )

    return {"error_model": error_model, "pagination_meta": pagination_meta}
