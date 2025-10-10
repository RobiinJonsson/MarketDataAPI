"""
File Management API Resources

This module contains Flask-RESTx resource definitions for file management endpoints.
Migrated from routes/file_management.py to provide proper Swagger documentation.
"""

import logging

from flask import current_app, request
from flask_restx import Namespace, Resource

from ...constants import ErrorMessages, HTTPStatus, ResponseFields

logger = logging.getLogger(__name__)


def create_file_resources(api, models):
    """
    Create and register file management API resources.

    Args:
        api: Flask-RESTx API instance
        models: Dictionary of registered models

    Returns:
        Namespace: Files namespace with registered resources
    """

    # Create namespace
    files_ns = api.namespace("files", description="File management operations")

    # Get model references
    file_models = models["files"]
    common_models = models["common"]

    @files_ns.route("/")
    class FilesList(Resource):
        @files_ns.doc(
            description="Get all files organized by type with optional filters",
            params={
                "type": "Filter by file type",
                "extension": "Filter by file extension",
                "limit": "Maximum number of files to return",
                "offset": "Number of files to skip",
            },
            responses={
                HTTPStatus.OK: ("Files list", file_models["files_list_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.marshal_with(file_models["files_list_response"])
        def get(self):
            """Get all files organized by type with optional filters"""
            try:
                from ...services.file_management_service import FileManagementService

                file_type = request.args.get("type")
                extension = request.args.get("extension")
                limit = request.args.get("limit", type=int)
                offset = request.args.get("offset", 0, type=int)

                service = FileManagementService()
                all_files = service.get_all_files()  # This returns {"firds": [...], "fitrs": [...]}
                
                # Convert FileInfo objects to dictionaries for JSON serialization
                def file_info_to_dict(file_info):
                    return {
                        "name": file_info.name,
                        "path": file_info.path,
                        "size": file_info.size,
                        "created": file_info.created.isoformat() if file_info.created else None,
                        "modified": file_info.modified.isoformat() if file_info.modified else None,
                        "file_type": file_info.file_type,
                        "dataset_type": file_info.dataset_type
                    }
                
                # Convert all FileInfo objects to dictionaries
                serialized_files = {}
                for ftype, files in all_files.items():
                    serialized_files[ftype] = [file_info_to_dict(f) for f in files]
                
                # Apply filters if requested
                if file_type and file_type in serialized_files:
                    # Filter to specific type (firds or fitrs)
                    filtered_files = {file_type: serialized_files[file_type]}
                else:
                    filtered_files = serialized_files
                
                # Apply extension filter if specified
                if extension:
                    for ftype in filtered_files:
                        filtered_files[ftype] = [
                            f for f in filtered_files[ftype] 
                            if f["name"].endswith(f".{extension}")
                        ]
                
                # Apply pagination if specified
                if limit or offset:
                    for ftype in filtered_files:
                        files = filtered_files[ftype]
                        start_idx = offset or 0
                        end_idx = start_idx + (limit or len(files))
                        filtered_files[ftype] = files[start_idx:end_idx]

                # Calculate totals for metadata
                total_files = sum(len(files) for files in filtered_files.values())
                
                # Flatten files list for the "files" field (all files in one list)
                all_files_list = []
                for file_list in filtered_files.values():
                    all_files_list.extend(file_list)

                return {
                    "files": all_files_list,
                    "total": total_files,
                    "by_type": filtered_files
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving files: {str(e)}")
                return {
                    ResponseFields.STATUS: "error",
                    ResponseFields.ERROR: {
                        "code": str(HTTPStatus.INTERNAL_SERVER_ERROR),
                        ResponseFields.MESSAGE: str(e),
                    },
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/esma")
    class ESMAFiles(Resource):
        @files_ns.doc(
            description="Get available ESMA files from the registry",
            responses={
                HTTPStatus.OK: ("ESMA files", file_models["esma_files_response"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.marshal_with(file_models["esma_files_response"])
        def get(self):
            """Get available ESMA files from the registry"""
            try:
                from ...services.file_management_service import FileManagementService

                service = FileManagementService()
                result = service.get_available_esma_files()

                return result, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving ESMA files: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/download")
    class FileDownload(Resource):
        @files_ns.doc(
            description="Download and parse ESMA files",
            responses={
                HTTPStatus.OK: ("Download results", file_models["file_download_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.expect(file_models["file_download_request"])
        @files_ns.marshal_with(file_models["file_download_response"])
        def post(self):
            """Download and parse ESMA files"""
            try:
                from ...services.file_management_service import FileManagementService

                data = request.get_json()
                if not data or not data.get("files"):
                    return {
                        ResponseFields.ERROR: "Files list is required"
                    }, HTTPStatus.BAD_REQUEST

                files = data.get("files", [])
                parse = data.get("parse", True)
                overwrite = data.get("overwrite", False)

                service = FileManagementService()
                result = service.download_and_parse_files(
                    files=files,
                    parse=parse,
                    overwrite=overwrite
                )

                return result, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error downloading files: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/stats/detailed")
    class DetailedFileStats(Resource):
        @files_ns.doc(
            description="Get detailed file statistics with filtering",
            params={
                "type": "Filter by file type",
                "extension": "Filter by file extension",
                "date_from": "Filter files from date (YYYY-MM-DD)",
                "date_to": "Filter files to date (YYYY-MM-DD)",
            },
            responses={
                HTTPStatus.OK: ("Detailed statistics", file_models["detailed_file_stats"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.marshal_with(file_models["detailed_file_stats"])
        def get(self):
            """Get detailed file statistics with filtering"""
            try:
                from ...services.file_management_service import FileManagementService

                file_type = request.args.get("type")
                extension = request.args.get("extension")
                date_from = request.args.get("date_from")
                date_to = request.args.get("date_to")

                service = FileManagementService()
                result = service.get_detailed_file_stats(
                    file_type=file_type,
                    extension=extension,
                    date_from=date_from,
                    date_to=date_to
                )

                return result, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving detailed file stats: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/stats")
    class FileStats(Resource):
        @files_ns.doc(
            description="Get storage statistics",
            responses={
                HTTPStatus.OK: ("File statistics", file_models["file_stats"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.marshal_with(file_models["file_stats"])
        def get(self):
            """Get storage statistics"""
            try:
                from ...services.file_management_service import FileManagementService

                service = FileManagementService()
                result = service.get_file_stats()

                return result, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving file stats: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

        @files_ns.doc(
            description="Delete files based on criteria",
            responses={
                HTTPStatus.OK: ("Files deleted", common_models["success_model"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        def delete(self):
            """Delete files based on criteria"""
            try:
                from ...services.file_management_service import FileManagementService

                # Get query parameters for deletion criteria
                file_type = request.args.get("type")
                pattern = request.args.get("pattern")
                older_than_days = request.args.get("older_than_days", type=int)

                if not any([file_type, pattern, older_than_days]):
                    return {
                        ResponseFields.ERROR: "At least one deletion criteria must be provided"
                    }, HTTPStatus.BAD_REQUEST

                service = FileManagementService()
                result = service.delete_files(
                    file_type=file_type,
                    pattern=pattern,
                    older_than_days=older_than_days
                )

                return {
                    ResponseFields.MESSAGE: "Files deleted successfully",
                    "deleted_count": result.get("deleted_count", 0),
                    "deleted_files": result.get("deleted_files", []),
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error deleting files: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/summary")
    class FileSummary(Resource):
        @files_ns.doc(
            description="Get file summary information",
            responses={
                HTTPStatus.OK: ("File summary", common_models["success_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        def get(self):
            """Get file summary information"""
            try:
                from ...services.file_management_service import FileManagementService

                service = FileManagementService()
                result = service.get_file_summary()

                return {
                    ResponseFields.MESSAGE: "File summary retrieved successfully",
                    "summary": result,
                }, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error retrieving file summary: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/download-by-criteria")
    class FileDownloadByCriteria(Resource):
        @files_ns.doc(
            description="Download files by specified criteria",
            responses={
                HTTPStatus.OK: ("Download results", file_models["file_download_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.expect(file_models["file_criteria"])
        @files_ns.marshal_with(file_models["file_download_response"])
        def post(self):
            """Download files by specified criteria"""
            try:
                from ...services.file_management_service import FileManagementService

                data = request.get_json()
                if not data:
                    return {
                        ResponseFields.ERROR: ErrorMessages.INVALID_REQUEST_BODY
                    }, HTTPStatus.BAD_REQUEST

                service = FileManagementService()
                result = service.download_by_criteria(data)

                return result, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error downloading files by criteria: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    @files_ns.route("/auto-cleanup")
    class AutoCleanup(Resource):
        @files_ns.doc(
            description="Auto cleanup old files based on retention policies",
            responses={
                HTTPStatus.OK: ("Cleanup results", file_models["cleanup_response"]),
                HTTPStatus.BAD_REQUEST: ("Invalid request", common_models["error_model"]),
                HTTPStatus.INTERNAL_SERVER_ERROR: ("Server error", common_models["error_model"]),
            },
        )
        @files_ns.expect(file_models["auto_cleanup_request"])
        @files_ns.marshal_with(file_models["cleanup_response"])
        def post(self):
            """Auto cleanup old files based on retention policies"""
            try:
                from ...services.file_management_service import FileManagementService

                data = request.get_json() or {}
                dry_run = data.get("dry_run", True)
                keep_days = data.get("keep_days", 30)
                file_types = data.get("file_types", [])

                service = FileManagementService()
                result = service.auto_cleanup(
                    dry_run=dry_run,
                    keep_days=keep_days,
                    file_types=file_types
                )

                return result, HTTPStatus.OK

            except Exception as e:
                logger.error(f"Error in auto cleanup: {str(e)}")
                return {
                    ResponseFields.ERROR: ErrorMessages.INTERNAL_SERVER_ERROR,
                    "details": str(e),
                }, HTTPStatus.INTERNAL_SERVER_ERROR

    return files_ns