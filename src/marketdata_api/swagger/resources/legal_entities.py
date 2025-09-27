"""
Legal Entity API Resources - Working Implementation

This module contains the actual working legal entity endpoints with business logic,
migrated from the old swagger.py but organized in the new modular structure.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, Pagination, ResponseFields

logger = logging.getLogger(__name__)


def create_legal_entity_resources(api, models):
    """
    Create and register legal entity-related API resources with actual working endpoints.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Legal entities namespace with registered resources
    """

    # Create namespace
    legal_entities_ns = api.namespace("legal-entities", description="Legal entity operations")

    # Get model references
    legal_entity_models = models["legal_entities"]
    common_models = models["common"]

    @legal_entities_ns.route("/")
    class LegalEntityList(Resource):
        @legal_entities_ns.doc(
            description="Retrieves a paginated list of legal entities",
            params={
                "status": 'Filter by entity status (e.g., "ACTIVE", "INACTIVE", "PENDING")',
                "jurisdiction": "Filter by jurisdiction code (ISO 3166-1)",
                "legal_form": "Filter by legal form",
                "name": "Search by entity name (case-insensitive)",
                "page": f"Page number for paginated results (default: {Pagination.DEFAULT_PAGE})",
                "per_page": f"Number of records per page (default: {Pagination.DEFAULT_PER_PAGE}, max: {Pagination.MAX_PER_PAGE})",
                "limit": "Maximum number of records to return",
                "offset": "Number of records to skip",
            },
            responses={
                HTTPStatus.OK: ("Success", legal_entity_models["legal_entity_list_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        @legal_entities_ns.marshal_with(legal_entity_models["legal_entity_list_response"])
        def get(self):
            """Retrieves a paginated list of legal entities"""
            from ...interfaces.factory.services_factory import ServicesFactory

            try:
                # Query parameters for filtering
                status = request.args.get("status")
                jurisdiction = request.args.get("jurisdiction")
                limit = request.args.get("limit", Pagination.DEFAULT_LIMIT, type=int)
                offset = request.args.get("offset", Pagination.DEFAULT_OFFSET, type=int)
                page = request.args.get("page", Pagination.DEFAULT_PAGE, type=int)
                per_page = min(
                    request.args.get("per_page", Pagination.DEFAULT_PER_PAGE, type=int),
                    Pagination.MAX_PER_PAGE,
                )

                # Create filters dictionary only if we have filters to apply
                filters = {}
                if status:
                    filters["status"] = status
                if jurisdiction:
                    filters["jurisdiction"] = jurisdiction

                service = ServicesFactory.get_legal_entity_service()
                session, entities = service.get_all_entities(
                    limit=limit, offset=offset, filters=filters if filters else None
                )

                result = []
                for entity in entities:
                    result.append(
                        {
                            "lei": entity.lei,
                            "name": entity.name,
                            "jurisdiction": entity.jurisdiction,
                            "legal_form": entity.legal_form,
                            "status": entity.status,
                        }
                    )

                session.close()
                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result,
                    ResponseFields.META: {
                        ResponseFields.PAGE: page,
                        ResponseFields.PER_PAGE: per_page,
                        ResponseFields.TOTAL: len(result),
                    },
                }

            except Exception as e:
                logger.error(f"Error in swagger list_entities: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @legal_entities_ns.route("/<string:lei>")
    @legal_entities_ns.param("lei", "Legal Entity Identifier (20 characters)")
    class LegalEntityDetail(Resource):
        @legal_entities_ns.doc(
            description="Retrieves detailed information about a specific legal entity by its LEI",
            responses={
                HTTPStatus.OK: ("Success", legal_entity_models["legal_entity_detail_response"]),
                HTTPStatus.NOT_FOUND: ("Legal entity not found", common_models["error_model"]),
                HTTPStatus.UNAUTHORIZED: ("Unauthorized", common_models["error_model"]),
            },
        )
        def get(self, lei):
            """Retrieves detailed information about a specific legal entity by its LEI"""
            from ...interfaces.factory.services_factory import ServicesFactory

            try:
                service = ServicesFactory.get_legal_entity_service()
                session, entity = service.get_entity(lei)

                if not entity:
                    return {
                        ResponseFields.STATUS: "error",
                        ResponseFields.ERROR: {
                            "code": str(HTTPStatus.NOT_FOUND),
                            ResponseFields.MESSAGE: ErrorMessages.ENTITY_NOT_FOUND,
                        },
                    }, HTTPStatus.NOT_FOUND

                # Use the model's comprehensive API response method
                result = entity.to_api_response(
                    include_relationships=False, include_addresses=True, include_registration=True
                )

                session.close()

                return {
                    ResponseFields.STATUS: ResponseFields.SUCCESS_STATUS,
                    ResponseFields.DATA: result,
                }

            except Exception as e:
                logger.error(f"Error in swagger get_entity: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return legal_entities_ns
