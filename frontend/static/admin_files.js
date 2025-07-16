class FileManager {
    constructor() {
        this.files = {};
        this.filteredFiles = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadFiles();
        this.loadStats();
    }

    bindEvents() {
        $('#refresh-files-btn').on('click', () => this.refreshFiles());
        $('#organize-files-btn').on('click', () => this.organizeFiles());
        $('#cleanup-files-btn').on('click', () => this.cleanupFiles());
        $('#apply-file-filters').on('click', () => this.applyFilters());
        
        // Filter change events
        $('#file-type-filter, #dataset-filter').on('change', () => this.applyFilters());
    }

    async loadFiles() {
        try {
            showSpinner();
            const response = await fetch('/api/v1/files');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.files = data;
            this.applyFilters();
            
            // Show success message if files were found
            const totalFiles = Object.values(data).reduce((sum, files) => sum + files.length, 0);
            if (totalFiles > 0) {
                showToast(`Loaded ${totalFiles} files successfully`, 'success');
            } else {
                showToast('No files found in downloads directory', 'info');
            }
        } catch (error) {
            console.error('Error loading files:', error);
            showToast('Error loading files: ' + error.message, 'error');
            // Initialize with empty data to prevent errors
            this.files = { firds: [], fitrs: [] };
            this.applyFilters();
        } finally {
            hideSpinner();
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/v1/files/stats');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.updateStatsDisplay(data);
        } catch (error) {
            console.error('Error loading stats:', error);
            // Set default values if stats can't be loaded
            this.updateStatsDisplay({ 
                firds: { count: 0, total_size_mb: 0 }, 
                fitrs: { count: 0, total_size_mb: 0 } 
            });
        }
    }

    updateStatsDisplay(stats) {
        $('#firds-count').text(stats.firds?.count || 0);
        $('#firds-size').text(stats.firds?.total_size_mb || 0);
        $('#fitrs-count').text(stats.fitrs?.count || 0);
        $('#fitrs-size').text(stats.fitrs?.total_size_mb || 0);
    }

    applyFilters() {
        const fileTypeFilter = $('#file-type-filter').val();
        const datasetFilter = $('#dataset-filter').val();
        
        let allFiles = [];
        
        // Flatten all files
        for (const [fileType, files] of Object.entries(this.files)) {
            allFiles = allFiles.concat(files);
        }
        
        // Apply filters
        this.filteredFiles = allFiles.filter(file => {
            if (fileTypeFilter && file.file_type !== fileTypeFilter) {
                return false;
            }
            if (datasetFilter && file.dataset_type !== datasetFilter) {
                return false;
            }
            return true;
        });
        
        this.renderFilesTable();
    }

    renderFilesTable() {
        const tbody = $('#files-tbody');
        tbody.empty();
        
        if (this.filteredFiles.length === 0) {
            tbody.append('<tr><td colspan="6" class="text-center">No files found</td></tr>');
            return;
        }
        
        this.filteredFiles.forEach(file => {
            const row = $(`
                <tr>
                    <td title="${file.name}">${this.truncateText(file.name, 40)}</td>
                    <td><span class="badge badge-${file.file_type}">${file.file_type.toUpperCase()}</span></td>
                    <td><span class="badge badge-dataset">${file.dataset_type}</span></td>
                    <td>${file.size_mb} MB</td>
                    <td>${this.formatDate(file.modified)}</td>
                    <td>
                        <button class="btn btn-small btn-danger" onclick="fileManager.deleteFile('${file.path}', '${file.name}')">
                            Delete
                        </button>
                    </td>
                </tr>
            `);
            tbody.append(row);
        });
    }

    async refreshFiles() {
        await this.loadFiles();
        await this.loadStats();
        showToast('Files refreshed successfully', 'success');
    }

    async organizeFiles() {
        try {
            showSpinner();
            const response = await fetch('/api/v1/files/organize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            
            if (response.ok) {
                const totalMoved = data.organized_count.firds + data.organized_count.fitrs;
                showToast(`Organized ${totalMoved} files successfully`, 'success');
                this.refreshFiles();
            } else {
                throw new Error(data.error || 'Failed to organize files');
            }
        } catch (error) {
            showToast('Error organizing files: ' + error.message, 'error');
        } finally {
            hideSpinner();
        }
    }

    async cleanupFiles() {
        const dryRun = $('#dry-run').is(':checked');
        const fileType = $('#file-type-filter').val() || null;
        
        try {
            showSpinner();
            const response = await fetch('/api/v1/files/cleanup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    file_type: fileType,
                    dry_run: dryRun
                })
            });
            const data = await response.json();
            
            if (response.ok) {
                const totalRemoved = data.removed_count.firds + data.removed_count.fitrs;
                const message = dryRun ? 
                    `Would remove ${totalRemoved} files (dry run)` : 
                    `Removed ${totalRemoved} files successfully`;
                showToast(message, 'success');
                
                if (!dryRun) {
                    this.refreshFiles();
                }
            } else {
                throw new Error(data.error || 'Failed to cleanup files');
            }
        } catch (error) {
            showToast('Error cleaning up files: ' + error.message, 'error');
        } finally {
            hideSpinner();
        }
    }

    async deleteFile(filePath, fileName) {
        if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
            return;
        }
        
        try {
            showSpinner();
            const response = await fetch('/api/v1/files/delete', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: filePath })
            });
            const data = await response.json();
            
            if (response.ok && data.success) {
                showToast('File deleted successfully', 'success');
                this.refreshFiles();
            } else {
                throw new Error(data.error || 'Failed to delete file');
            }
        } catch (error) {
            showToast('Error deleting file: ' + error.message, 'error');
        } finally {
            hideSpinner();
        }
    }

    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString() + ' ' + 
               new Date(dateString).toLocaleTimeString();
    }
}

// Initialize when DOM is ready
$(document).ready(function() {
    window.fileManager = new FileManager();
});
