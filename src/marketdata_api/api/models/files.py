"""
File Management Swagger Models

This module contains Swagger model definitions for file management endpoints.
"""

from flask_restx import fields


def create_file_models(api, common_models):
    """
    Create and register file management Swagger models.

    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common models

    Returns:
        dict: Dictionary of file management models
    """

    # File info model
    file_info_model = api.model("FileInfo", {
        "filename": fields.String(required=True, description="File name"),
        "path": fields.String(description="Full file path"),
        "size": fields.Integer(description="File size in bytes"),
        "type": fields.String(description="File type/category"),
        "created_at": fields.DateTime(description="File creation timestamp"),
        "modified_at": fields.DateTime(description="Last modification timestamp"),
        "checksum": fields.String(description="File checksum/hash"),
    })

    # Files list response model
    files_list_response_model = api.model("FilesListResponse", {
        "files": fields.List(fields.Nested(file_info_model), description="List of files"),
        "total": fields.Integer(description="Total number of files"),
        "by_type": fields.Raw(description="Files grouped by type"),
    })

    # ESMA file model
    esma_file_model = api.model("ESMAFile", {
        "filename": fields.String(required=True, description="ESMA file name"),
        "download_url": fields.String(description="Download URL"),
        "file_type": fields.String(description="File type (FIRDS/FITRS)"),
        "date": fields.String(description="File date"),
        "size": fields.String(description="File size"),
        "available": fields.Boolean(description="Whether file is available for download"),
    })

    # ESMA files response model
    esma_files_response_model = api.model("ESMAFilesResponse", {
        "available_files": fields.List(fields.Nested(esma_file_model), description="Available ESMA files"),
        "total": fields.Integer(description="Total number of available files"),
        "last_updated": fields.DateTime(description="Last registry update"),
    })

    # File download request model
    file_download_request_model = api.model("FileDownloadRequest", {
        "files": fields.List(fields.String, required=True, description="List of file URLs or names to download"),
        "parse": fields.Boolean(description="Whether to parse files after download", default=True),
        "overwrite": fields.Boolean(description="Whether to overwrite existing files", default=False),
    })

    # File download response model
    file_download_response_model = api.model("FileDownloadResponse", {
        "downloaded": fields.List(fields.String, description="Successfully downloaded files"),
        "failed": fields.List(fields.String, description="Failed downloads"),
        "parsed": fields.List(fields.String, description="Successfully parsed files"),
        "total_downloaded": fields.Integer(description="Total files downloaded"),
        "total_parsed": fields.Integer(description="Total files parsed"),
    })

    # File statistics model
    file_stats_model = api.model("FileStatistics", {
        "total_files": fields.Integer(description="Total number of files"),
        "total_size": fields.String(description="Total size (human readable)"),
        "total_size_bytes": fields.Integer(description="Total size in bytes"),
        "by_type": fields.Raw(description="Statistics by file type"),
        "by_extension": fields.Raw(description="Statistics by file extension"),
        "oldest_file": fields.DateTime(description="Oldest file timestamp"),
        "newest_file": fields.DateTime(description="Newest file timestamp"),
    })

    # Detailed file statistics model
    detailed_file_stats_model = api.model("DetailedFileStatistics", {
        "files": fields.List(fields.Nested(file_info_model), description="Detailed file information"),
        "summary": fields.Nested(file_stats_model, description="Summary statistics"),
        "total": fields.Integer(description="Total matching files"),
    })

    # File criteria model for batch operations
    file_criteria_model = api.model("FileCriteria", {
        "file_types": fields.List(fields.String, description="File types to include"),
        "date_from": fields.String(description="Start date (YYYY-MM-DD)"),
        "date_to": fields.String(description="End date (YYYY-MM-DD)"),
        "instruments": fields.List(fields.String, description="Instrument types (C, D, E, etc.)"),
        "max_files": fields.Integer(description="Maximum number of files", default=50),
    })

    # Auto cleanup request model
    auto_cleanup_request_model = api.model("AutoCleanupRequest", {
        "dry_run": fields.Boolean(description="Whether to perform a dry run", default=True),
        "keep_days": fields.Integer(description="Number of days to keep files", default=30),
        "file_types": fields.List(fields.String, description="File types to clean up"),
    })

    # Cleanup response model
    cleanup_response_model = api.model("CleanupResponse", {
        "files_removed": fields.List(fields.String, description="Files that were/would be removed"),
        "space_freed": fields.String(description="Space freed (human readable)"),
        "space_freed_bytes": fields.Integer(description="Space freed in bytes"),
        "dry_run": fields.Boolean(description="Whether this was a dry run"),
    })

    return {
        "file_info": file_info_model,
        "files_list_response": files_list_response_model,
        "esma_file": esma_file_model,
        "esma_files_response": esma_files_response_model,
        "file_download_request": file_download_request_model,
        "file_download_response": file_download_response_model,
        "file_stats": file_stats_model,
        "detailed_file_stats": detailed_file_stats_model,
        "file_criteria": file_criteria_model,
        "auto_cleanup_request": auto_cleanup_request_model,
        "cleanup_response": cleanup_response_model,
    }