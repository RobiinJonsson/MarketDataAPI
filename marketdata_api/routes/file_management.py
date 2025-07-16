from flask import Blueprint, render_template, request, jsonify, current_app
from ..services.file_management_service import FileManagementService
import logging

file_management_bp = Blueprint('file_management', __name__)
logger = logging.getLogger(__name__)

@file_management_bp.route('/api/v1/files', methods=['GET'])
def get_files():
    """Get all files organized by type."""
    try:
        service = FileManagementService()
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

@file_management_bp.route('/api/v1/files/cleanup', methods=['POST'])
def cleanup_files():
    """Clean up old files."""
    try:
        data = request.get_json() or {}
        file_type = data.get('file_type')
        dry_run = data.get('dry_run', False)
        
        service = FileManagementService()
        removed_count = service.cleanup_old_files(file_type, dry_run)
        
        return jsonify({
            'removed_count': removed_count,
            'dry_run': dry_run
        })
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")
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
        
        return jsonify({'success': success})
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return jsonify({'error': str(e)}), 500

@file_management_bp.route('/api/v1/files/organize', methods=['POST'])
def organize_files():
    """Organize files into proper directories."""
    try:
        service = FileManagementService()
        organized_count = service.organize_files()
        
        return jsonify({'organized_count': organized_count})
    except Exception as e:
        logger.error(f"Error organizing files: {e}")
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
