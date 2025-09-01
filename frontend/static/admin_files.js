class FileManager {
    constructor() {
        this.files = {};
        this.filteredFiles = [];
        this.initialized = false;
    }

    init() {
        if (this.initialized) return;
        
        this.bindEvents();
        this.loadFiles();
        this.loadStats();
        this.initialized = true;
    }

    bindEvents() {
        $('#refresh-files-btn').on('click', () => this.refreshFiles());
        $('#auto-cleanup-btn').on('click', () => this.autoCleanupFiles());
        $('#download-files-btn').on('click', () => this.showDownloadDialog());
        $('#apply-file-filters').on('click', () => this.applyFilters());
        
        // Filter change events
        $('#file-type-filter, #dataset-filter').on('change', () => this.applyFilters());
        
        // Download dialog events
        $('#download-dialog-close, #download-dialog-cancel').on('click', () => this.hideDownloadDialog());
        $('#execute-download-btn').on('click', () => this.executeDownload());
        $('#load-available-files').on('click', () => this.loadAvailableESMAFiles());
        // Remove auto-search on filter change - only search when button is clicked
        
        // Select all files checkbox functionality
        $('#select-all-files').on('change', function() {
            $('.file-checkbox').prop('checked', this.checked);
        });
        
        // File delete button event delegation
        $(document).on('click', '.file-delete-btn', (e) => {
            const button = $(e.target);
            const filePath = button.data('file-path');
            const fileName = button.data('file-name');
            this.deleteFile(filePath, fileName);
        });
    }

    async loadFiles() {
        try {
            AdminUtils.showSpinner();
            const response = await fetch('/api/v1/files');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Handle both filtered and unfiltered response formats
            if (data.filtered_files) {
                // Filtered response format
                this.files = { all: data.filtered_files };
                AdminUtils.showToast(`Loaded ${data.total_count} files successfully`, 'success');
            } else {
                // Original format: { firds: [], fitrs: [] }
                this.files = data;
                const totalFiles = Object.values(data).reduce((sum, files) => sum + files.length, 0);
                if (totalFiles > 0) {
                    AdminUtils.showToast(`Loaded ${totalFiles} files successfully`, 'success');
                } else {
                    AdminUtils.showToast('No files found in downloads directory', 'info');
                }
            }
            
            this.applyFilters();
        } catch (error) {
            console.error('Error loading files:', error);
            AdminUtils.showToast('Error loading files: ' + error.message, 'error');
            // Initialize with empty data to prevent errors
            this.files = { firds: [], fitrs: [] };
            this.applyFilters();
        } finally {
            AdminUtils.hideSpinner();
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
        $('#firds-size').text((stats.firds?.total_size_mb || 0).toFixed(1));
        $('#fitrs-count').text(stats.fitrs?.count || 0);
        $('#fitrs-size').text((stats.fitrs?.total_size_mb || 0).toFixed(1));
    }

    applyFilters() {
        const fileTypeFilter = $('#file-type-filter').val();
        const datasetFilter = $('#dataset-filter').val();
        
        let allFiles = [];
        
        // Handle both response formats
        if (this.files.all) {
            // Filtered response format
            allFiles = this.files.all;
        } else {
            // Original format: flatten all files
            for (const [fileType, files] of Object.entries(this.files)) {
                allFiles = allFiles.concat(files);
            }
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
                        <button class="btn btn-small btn-danger file-delete-btn" 
                                data-file-path="${file.path}" 
                                data-file-name="${file.name}">
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
        AdminUtils.showToast('Files refreshed successfully', 'success');
    }

    async autoCleanupFiles() {
        console.log('autoCleanupFiles called');
        if (!confirm('Auto-cleanup will remove outdated files and keep only the latest files per pattern within your configured date range. Continue?')) {
            console.log('User cancelled auto-cleanup');
            return;
        }
        
        try {
            AdminUtils.showSpinner();
            const response = await fetch('/api/v1/files/auto-cleanup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            
            if (response.ok) {
                const totalRemoved = data.total_removed;
                AdminUtils.showToast(`Auto-cleanup completed: removed ${totalRemoved} outdated files`, 'success');
                this.refreshFiles();
            } else {
                throw new Error(data.error || 'Failed to perform auto-cleanup');
            }
        } catch (error) {
            AdminUtils.showToast('Error during auto-cleanup: ' + error.message, 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    }

    showDownloadDialog() {
        $('#download-dialog').show();
        this.loadAvailableESMAFiles();
    }

    hideDownloadDialog() {
        $('#download-dialog').hide();
    }

    async loadAvailableESMAFiles() {
        try {
            const fileType = $('#download-file-type').val() || 'firds';
            const assetType = $('#download-asset-type').val();
            const dateFrom = $('#download-date-from').val();
            const dateTo = $('#download-date-to').val();
            
            const params = new URLSearchParams({
                datasets: fileType,
                ...(assetType && { asset_type: assetType }),
                ...(dateFrom && { date_from: dateFrom }),
                ...(dateTo && { date_to: dateTo })
            });
            
            const response = await fetch(`/api/v1/esma-files?${params}`);
            const data = await response.json();
            
            if (response.ok) {
                // Use all files from backend response without additional filtering
                let files = data.files;
                this.renderAvailableFiles(files);
                $('#available-files-count').text(`${files.length} files available`);
            } else {
                throw new Error(data.error || 'Failed to load available files');
            }
        } catch (error) {
            console.error('Error loading ESMA files:', error);
            AdminUtils.showToast('Error loading available files: ' + error.message, 'error');
        }
    }

    renderAvailableFiles(files) {
        const tbody = $('#available-files-tbody');
        tbody.empty();
        
        if (files.length === 0) {
            tbody.append('<tr><td colspan="4" class="text-center">No files found</td></tr>');
            return;
        }
        
        files.forEach(file => {
            const row = $(`
                <tr>
                    <td>
                        <input type="checkbox" class="file-checkbox" value="${file.download_link}" 
                               data-filename="${file.file_name}">
                    </td>
                    <td title="${file.file_name}">${this.truncateText(file.file_name, 40)}</td>
                    <td>${file.publication_date || file.creation_date}</td>
                    <td>${file.instrument_type || file.file_type}</td>
                </tr>
            `);
            tbody.append(row);
        });
    }

    async executeDownload() {
        const selectedFiles = $('.file-checkbox:checked');
        if (selectedFiles.length === 0) {
            AdminUtils.showToast('Please select at least one file to download', 'warning');
            return;
        }
        
        const urls = selectedFiles.map((_, el) => $(el).val()).get();
        const forceUpdate = $('#force-update-download').is(':checked');
        
        // Show progress bar
        this.showDownloadProgress();
        this.updateProgress(0, `Starting download of ${urls.length} files...`);
        
        try {
            AdminUtils.showSpinner();
            
            // Simulate progress updates (since we don't have streaming progress from backend)
            let progress = 10;
            this.updateProgress(progress, 'Sending request to server...');
            
            const progressInterval = setInterval(() => {
                if (progress < 90) {
                    progress += Math.random() * 20;
                    this.updateProgress(Math.min(progress, 90), 'Downloading files...');
                }
            }, 500);
            
            const response = await fetch('/api/v1/files/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    urls: urls,
                    force_update: forceUpdate
                })
            });
            
            clearInterval(progressInterval);
            this.updateProgress(95, 'Processing results...');
            
            const data = await response.json();
            
            if (response.ok) {
                this.updateProgress(100, 'Download completed!');
                
                const summary = data.summary;
                const message = `Download completed: ${summary.successful} successful, ${summary.failed} failed, ${summary.skipped} skipped`;
                AdminUtils.showToast(message, 'success');
                
                // Show cleanup info if available
                if (data.results.cleanup_performed) {
                    const cleanup = data.results.cleanup_performed;
                    const cleanupTotal = cleanup.firds + cleanup.fitrs;
                    if (cleanupTotal > 0) {
                        AdminUtils.showToast(`Auto-cleanup: removed ${cleanupTotal} outdated files`, 'info');
                    }
                }
                
                // Hide progress after a delay
                setTimeout(() => {
                    this.hideDownloadProgress();
                    this.hideDownloadDialog();
                }, 1500);
                
                this.refreshFiles();
            } else {
                clearInterval(progressInterval);
                this.hideDownloadProgress();
                throw new Error(data.error || 'Failed to download files');
            }
        } catch (error) {
            this.hideDownloadProgress();
            AdminUtils.showToast('Error downloading files: ' + error.message, 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    }

    showDownloadProgress() {
        $('#download-progress').show();
    }

    hideDownloadProgress() {
        $('#download-progress').hide();
        this.updateProgress(0, 'Preparing download...');
    }

    updateProgress(percentage, message) {
        const progressFill = $('#progress-fill');
        const progressText = $('#progress-text');
        const currentFile = $('#current-file');
        
        progressFill.css('width', percentage + '%');
        progressText.text(Math.round(percentage) + '%');
        currentFile.text(message);
    }

    async deleteFile(filePath, fileName) {
        if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
            return;
        }
        
        try {
            AdminUtils.showSpinner();
            const response = await fetch('/api/v1/files/delete', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: filePath })
            });
            const data = await response.json();
            
            if (response.ok && data.success) {
                AdminUtils.showToast('File deleted successfully', 'success');
                this.refreshFiles();
            } else {
                throw new Error(data.error || 'Failed to delete file');
            }
        } catch (error) {
            AdminUtils.showToast('Error deleting file: ' + error.message, 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    }

    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    formatDate(dateString) {
        if (!dateString) return '-';
        try {
            return new Date(dateString).toLocaleDateString() + ' ' + 
                   new Date(dateString).toLocaleTimeString();
        } catch (error) {
            return dateString;
        }
    }
}

// Initialize when DOM is ready but don't call init() until needed
$(document).ready(function() {
    console.log('Creating FileManager instance...');
    window.fileManager = new FileManager();
    console.log('FileManager instance created, not initialized yet');
});