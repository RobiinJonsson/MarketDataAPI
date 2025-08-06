from flask import Blueprint, render_template, request, jsonify, current_app
from ..services.file_management_service import FileManagementService
import logging

file_management_bp = Blueprint('file_management', __name__)
logger = logging.getLogger(__name__)

@file_management_bp.route('/api/v1/files', methods=['GET'])
def get_files():
    """Get all files organized by type with optional filters."""
    try:
        # Get query parameters
        file_type = request.args.get('file_type')
        dataset_type = request.args.get('dataset_type')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        limit = request.args.get('limit', type=int)
        
        service = FileManagementService()
        
        if any([file_type, dataset_type, date_from, date_to, limit]):
            # Use filtered search
            files = service.get_files_with_filters(
                file_type=file_type,
                dataset_type=dataset_type,
                date_from=date_from,
                date_to=date_to,
                limit=limit
            )
            # Convert to dictionary format - return as filtered_files
            result = {
                'filtered_files': [
                    {
                        'name': f.name,
                        'path': f.path,
                        'size': f.size,
                        'size_mb': round(f.size / (1024 * 1024), 2),
                        'created': f.created.isoformat(),
                        'modified': f.modified.isoformat(),
                        'file_type': f.file_type,
                        'dataset_type': f.dataset_type
                    }
                    for f in files
                ],
                'total_count': len(files),
                'filters_applied': {
                    'file_type': file_type,
                    'dataset_type': dataset_type,
                    'date_from': date_from,
                    'date_to': date_to,
                    'limit': limit
                }
            }
        else:
            # Use original method for all files
            files = service.get_all_files()
            # Convert FileInfo objects to dictionaries
            result = {}
            for file_type, file_list in files.items():
                result[file_type] = [
                    {
                        'name': f.name,
                        'path': f.path,
                        'size': f.size,
                        'size_mb': round(f.size / (1024 * 1024), 2),
                        'created': f.created.isoformat(),
                        'modified': f.modified.isoformat(),
                        'file_type': f.file_type,
                        'dataset_type': f.dataset_type
                    }
                    for f in file_list
                ]
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting files: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/esma-files', methods=['GET'])
def get_available_esma_files():
    """Get available ESMA files from the registry."""
    try:
        # Get query parameters
        datasets = request.args.getlist('datasets') or ['firds', 'fitrs']
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        file_type = request.args.get('file_type')
        
        service = FileManagementService()
        esma_files = service.get_available_esma_files(
            datasets=datasets,
            date_from=date_from,
            date_to=date_to,
            file_type=file_type
        )
        
        # Convert to dictionary format
        result = [
            {
                'file_name': f.file_name,
                'download_link': f.download_link,
                'file_type': f.file_type,
                'publication_date': f.publication_date,
                'creation_date': f.creation_date,
                'instrument_type': f.instrument_type,
                'file_size': f.file_size
            }
            for f in esma_files
        ]
        
        return jsonify({
            'files': result,
            'total_count': len(result),
            'filters': {
                'datasets': datasets,
                'date_from': date_from,
                'date_to': date_to,
                'file_type': file_type
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting ESMA files: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/download', methods=['POST'])
def download_and_parse_files():
    """Download and parse ESMA files."""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        force_update = data.get('force_update', False)
        
        if not urls:
            return jsonify({'error': 'No URLs provided'}), 400
        
        service = FileManagementService()
        results = service.download_and_parse_files(urls, force_update=force_update)
        
        return jsonify({
            'results': results,
            'summary': {
                'total_requested': len(urls),
                'successful': len(results['success']),
                'failed': len(results['failed']),
                'skipped': len(results['skipped'])
            }
        })
        
    except Exception as e:
        logger.error(f"Error downloading files: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/stats/detailed', methods=['GET'])
def get_detailed_file_stats():
    """Get detailed file statistics with filtering."""
    try:
        # Get query parameters
        dataset_types = request.args.getlist('dataset_types')
        file_types = request.args.getlist('file_types')
        
        service = FileManagementService()
        stats = service.get_file_stats_by_criteria(
            dataset_types=dataset_types if dataset_types else None,
            file_types=file_types if file_types else None
        )
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting detailed stats: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/stats', methods=['GET'])
def get_file_stats():
    """Get storage statistics."""
    try:
        service = FileManagementService()
        stats = service.get_storage_stats()
        
        # Convert datetime objects to ISO format
        for file_type, type_stats in stats.items():
            if type_stats['oldest_file']:
                type_stats['oldest_file'] = {
                    'name': type_stats['oldest_file'].name,
                    'modified': type_stats['oldest_file'].modified.isoformat()
                }
            if type_stats['newest_file']:
                type_stats['newest_file'] = {
                    'name': type_stats['newest_file'].name,
                    'modified': type_stats['newest_file'].modified.isoformat()
                }
        
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting file stats: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/delete', methods=['DELETE'])
def delete_file():
    """Delete a specific file."""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        if not file_path:
            return jsonify({'error': 'file_path is required'}), 400
        
        service = FileManagementService()
        success = service.delete_file(file_path)
        
        if success:
            return jsonify({'success': True, 'message': 'File deleted successfully'})
        else:
            return jsonify({'error': 'File not found or could not be deleted'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/summary', methods=['GET'])
def get_file_summary():
    """Get comprehensive file management summary."""
    try:
        service = FileManagementService()
        summary = service.get_file_management_summary()
        
        # Convert datetime objects for JSON serialization
        for file_type, stats in summary['storage_stats'].items():
            if stats['oldest_file']:
                stats['oldest_file'] = {
                    'name': stats['oldest_file'].name,
                    'modified': stats['oldest_file'].modified.isoformat()
                }
            if stats['newest_file']:
                stats['newest_file'] = {
                    'name': stats['newest_file'].name,
                    'modified': stats['newest_file'].modified.isoformat()
                }
        
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error getting file summary: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/download-by-criteria', methods=['POST'])
def download_by_criteria():
    """Download and parse files based on criteria."""
    try:
        data = request.get_json() or {}
        
        # Mandatory parameter
        file_type = data.get('file_type')
        if not file_type:
            return jsonify({'error': 'file_type is required (firds or fitrs)'}), 400
        
        # Optional parameters
        dataset = data.get('dataset')
        date = data.get('date')
        date_range = data.get('date_range')  # Expected as [start_date, end_date]
        force_update = data.get('force_update', False)
        
        # Validate date_range format
        if date_range:
            if not isinstance(date_range, list) or len(date_range) != 2:
                return jsonify({'error': 'date_range must be an array of [start_date, end_date]'}), 400
            date_range = tuple(date_range)
        
        # Validate file_type
        if file_type.lower() not in ['firds', 'fitrs']:
            return jsonify({'error': 'file_type must be "firds" or "fitrs"'}), 400
        
        service = FileManagementService()
        result = service.download_by_criteria(
            file_type=file_type.lower(),
            dataset=dataset,
            date=date,
            date_range=date_range,
            force_update=force_update
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in download_by_criteria: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/auto-cleanup', methods=['POST'])
def auto_cleanup_patterns():
    """Automatically clean up outdated files by pattern and date range."""
    try:
        service = FileManagementService()
        removed_count = service.auto_cleanup_outdated_patterns()
        
        return jsonify({
            'success': True,
            'message': 'Auto-cleanup completed',
            'files_removed': removed_count,
            'total_removed': sum(removed_count.values())
        })
    except Exception as e:
        logger.error(f"Error in auto_cleanup_patterns: {e}")
        return jsonify({'error': str(e)}), 500
