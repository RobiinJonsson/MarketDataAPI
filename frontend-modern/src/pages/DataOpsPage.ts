import { BasePage } from './BasePage';
import { ApiServiceFactory } from '../services';
import type { FileInfo, FileStats } from '../types/api';

/**
 * DataOps Management Page
 * Professional data operations with ESMA integration and real file management
 */
export default class DataOpsPage extends BasePage {
  private fileService = ApiServiceFactory.getInstance().files;
  private currentFiles: FileInfo[] = [];
  private currentStats: FileStats | null = null;
  private currentFilters: {
    type?: 'FIRDS' | 'FITRS' | 'OTHER';
    status?: 'active' | 'outdated' | 'processing';
  } = {};

  async render(): Promise<void> {
    this.container.innerHTML = `
      <div class="space-y-6">
        ${this.createSectionHeader('🔧 DataOps Center', 'Professional data operations with ESMA integration, real-time file management, and batch processing')}
        
        ${this.createTabs([
          { id: 'files', label: 'File Management', active: true },
          { id: 'esma', label: 'ESMA Downloads' },
          { id: 'storage', label: 'Storage Analytics' },
          { id: 'operations', label: 'Batch Operations' }
        ])}

        <!-- File Management Tab -->
        <div data-tab-pane="files">
          <!-- Storage Statistics -->
          <div id="file-statistics" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <!-- Statistics will be loaded dynamically -->
            ${this.createLoadingStats()}
          </div>

          <!-- File Operations & Filters -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
              <!-- Filters -->
              <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">File Type</label>
                  <select id="type-filter" class="border border-gray-300 rounded-md px-3 py-2 bg-white">
                    <option value="">All Types</option>
                    <option value="FIRDS">FIRDS</option>
                    <option value="FITRS">FITRS</option>
                    <option value="OTHER">Other</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                  <select id="status-filter" class="border border-gray-300 rounded-md px-3 py-2 bg-white">
                    <option value="">All Status</option>
                    <option value="active">Active</option>
                    <option value="outdated">Outdated</option>
                    <option value="processing">Processing</option>
                  </select>
                </div>
                <div class="flex items-end">
                  <button id="apply-filters" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Apply Filters
                  </button>
                </div>
              </div>

              <!-- Operations -->
              <div class="flex space-x-3">
                <button id="refresh-files" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                  </svg>
                  <span>Refresh</span>
                </button>
                <button id="download-latest" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                  </svg>
                  <span>Download Latest</span>
                </button>
                <button id="auto-cleanup" class="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd"></path>
                    <path fill-rule="evenodd" d="M4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 3a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"></path>
                  </svg>
                  <span>Auto-Cleanup</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Files Table -->
          ${this.createCard(`
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">File Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Modified</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody id="files-tbody" class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                      <div class="flex items-center justify-center">
                        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
                        Loading files...
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          `, '📁 File Management')}
        </div>

        <!-- ESMA Downloads Tab -->
        <div data-tab-pane="esma" class="hidden">
          ${this.createCard(`
            <div class="space-y-6">
              <div class="text-center py-8">
                <div class="mx-auto w-12 h-12 text-blue-500 mb-4">
                  <svg fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">ESMA Data Downloads</h3>
                <p class="text-gray-600 mb-6">Download the latest FIRDS and FITRS files from ESMA</p>
                
                <div class="max-w-md mx-auto space-y-4">
                  <button id="download-firds" class="w-full bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors">
                    📊 Download Latest FIRDS Files
                  </button>
                  <button id="download-fitrs" class="w-full bg-green-600 text-white px-6 py-3 rounded-md hover:bg-green-700 transition-colors">
                    📈 Download Latest FITRS Files
                  </button>
                  <button id="download-all" class="w-full bg-purple-600 text-white px-6 py-3 rounded-md hover:bg-purple-700 transition-colors">
                    🚀 Download All Latest Files
                  </button>
                </div>
              </div>
            </div>
          `, '🌐 ESMA Downloads')}
        </div>

        <!-- Storage Analytics Tab -->
        <div data-tab-pane="storage" class="hidden">
          ${this.createCard(`
            <div id="storage-analytics">
              <div class="text-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p class="text-gray-600">Loading storage analytics...</p>
              </div>
            </div>
          `, '📊 Storage Analytics')}
        </div>

        <!-- Batch Operations Tab -->
        <div data-tab-pane="operations" class="hidden">
          ${this.createCard(`
            <div class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <div class="mx-auto w-12 h-12 text-gray-400 mb-4">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                      <path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z"></path>
                      <path fill-rule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clip-rule="evenodd"></path>
                    </svg>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">Batch Processing</h3>
                  <p class="text-gray-600 mb-4">Process multiple files simultaneously</p>
                  <button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Start Batch Job
                  </button>
                </div>
                
                <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-green-400 transition-colors">
                  <div class="mx-auto w-12 h-12 text-gray-400 mb-4">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15.586 13H14a1 1 0 01-1-1z" clip-rule="evenodd"></path>
                    </svg>
                  </div>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">File Optimization</h3>
                  <p class="text-gray-600 mb-4">Optimize and compress file storage</p>
                  <button class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors">
                    Optimize Files
                  </button>
                </div>
              </div>
            </div>
          `, '⚙️ Batch Operations')}
        </div>
      </div>
    `;

    // Initialize the page
    await this.initializeDataOps();
  }

  private createLoadingStats(): string {
    return Array(4).fill(0).map(() => `
      <div class="bg-gray-50 p-4 rounded-lg animate-pulse">
        <div class="flex items-center justify-between">
          <div>
            <div class="h-4 bg-gray-300 rounded w-20 mb-2"></div>
            <div class="h-8 bg-gray-300 rounded w-12"></div>
          </div>
          <div class="w-8 h-8 bg-gray-300 rounded"></div>
        </div>
      </div>
    `).join('');
  }

  private async initializeDataOps(): Promise<void> {
    try {
      // Load initial data
      await this.loadFileStatistics();
      await this.loadFilesList();
      
      // Setup event listeners
      this.setupEventListeners();
      
    } catch (error) {
      console.error('Error initializing DataOps:', error);
      this.showDataOpsError('Failed to load file data. Please try again.');
    }
  }

  private async loadFileStatistics(): Promise<void> {
    try {
      const response = await this.fileService.getFileStats();
      console.log('File stats response:', response); // Debug logging
      
      if (response.status === 'success' && response.data) {
        console.log('File stats data:', response.data); // Debug logging
        this.currentStats = response.data;
        this.updateStatistics(response.data);
      } else {
        console.warn('File stats response missing data:', response);
      }
    } catch (error) {
      console.error('Error loading file statistics:', error);
      this.showDataOpsError('Failed to load file statistics.');
    }
  }

  private updateStatistics(stats: FileStats): void {
    const statsContainer = this.container.querySelector('#file-statistics');
    if (!statsContainer) return;

    // Store for future use
    this.currentStats = stats;

    const formatSize = (bytes: number): string => {
      const sizes = ['B', 'KB', 'MB', 'GB'];
      if (!bytes || bytes === 0 || isNaN(bytes)) return '0 B';
      const i = Math.floor(Math.log(bytes) / Math.log(1024));
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    };

    const formatTime = (dateString: string): string => {
      try {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'Unknown';
        
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        
        if (diffDays > 0) return `${diffDays}d ago`;
        if (diffHours > 0) return `${diffHours}h ago`;
        return 'Just now';
      } catch {
        return 'Unknown';
      }
    };

    statsContainer.innerHTML = `
      <div class="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-400">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-700 text-sm font-medium">FIRDS Files</p>
            <p class="text-2xl font-bold text-blue-900">${stats.firds_files || 0}</p>
            <p class="text-xs text-blue-600">${formatSize(stats.firds_size)}</p>
          </div>
          <div class="text-3xl text-blue-500">📊</div>
        </div>
      </div>
      
      <div class="bg-green-50 p-4 rounded-lg border-l-4 border-green-400">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-700 text-sm font-medium">FITRS Files</p>
            <p class="text-2xl font-bold text-green-900">${stats.fitrs_files || 0}</p>
            <p class="text-xs text-green-600">${formatSize(stats.fitrs_size)}</p>
          </div>
          <div class="text-3xl text-green-500">📈</div>
        </div>
      </div>
      
      <div class="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-400">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-purple-700 text-sm font-medium">Total Files</p>
            <p class="text-2xl font-bold text-purple-900">${stats.total_files || 0}</p>
            <p class="text-xs text-purple-600">${formatSize(stats.total_size)}</p>
          </div>
          <div class="text-3xl text-purple-500">💾</div>
        </div>
      </div>
      
      <div class="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-400">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-orange-700 text-sm font-medium">Last Updated</p>
            <p class="text-lg font-bold text-orange-900">${formatTime(stats.last_updated)}</p>
            <p class="text-xs text-orange-600">${stats.last_updated ? new Date(stats.last_updated).toLocaleDateString() : 'Unknown'}</p>
          </div>
          <div class="text-3xl text-orange-500">🕒</div>
        </div>
      </div>
    `;
  }

  private async loadFilesList(): Promise<void> {
    try {
      const response = await this.fileService.listFiles(this.currentFilters);
      
      if (response.status === 'success' && response.data) {
        this.currentFiles = response.data;
        this.updateFilesTable(response.data);
      }
    } catch (error) {
      console.error('Error loading files list:', error);
      this.showFilesError('Failed to load files list.');
    }
  }

  private updateFilesTable(files: FileInfo[]): void {
    const tbody = this.container.querySelector('#files-tbody');
    if (!tbody) return;

    if (files.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="6" class="px-6 py-8 text-center text-gray-500">
            <div class="text-center">
              <div class="text-4xl mb-2">📁</div>
              <p class="text-lg font-medium">No files found</p>
              <p class="text-sm">Try adjusting your filters or refresh the data</p>
            </div>
          </td>
        </tr>
      `;
      return;
    }

    const formatSize = (bytes: number): string => {
      const sizes = ['B', 'KB', 'MB', 'GB'];
      if (bytes === 0) return '0 B';
      const i = Math.floor(Math.log(bytes) / Math.log(1024));
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    };

    const formatTime = (dateString: string): string => {
      try {
        const date = new Date(dateString);
        return date.toLocaleString();
      } catch {
        return 'Unknown';
      }
    };

    const getStatusBadge = (status: string): string => {
      const statusConfig = {
        active: { class: 'bg-green-100 text-green-800', icon: '✅' },
        outdated: { class: 'bg-yellow-100 text-yellow-800', icon: '⚠️' },
        processing: { class: 'bg-blue-100 text-blue-800', icon: '🔄' }
      };
      const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.active;
      return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.class}">
        ${config.icon} ${status.charAt(0).toUpperCase() + status.slice(1)}
      </span>`;
    };

    const getTypeBadge = (type: string): string => {
      const typeConfig = {
        FIRDS: { class: 'bg-blue-100 text-blue-800', icon: '📊' },
        FITRS: { class: 'bg-green-100 text-green-800', icon: '📈' },
        OTHER: { class: 'bg-gray-100 text-gray-800', icon: '📄' }
      };
      const config = typeConfig[type as keyof typeof typeConfig] || typeConfig.OTHER;
      return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.class}">
        ${config.icon} ${type}
      </span>`;
    };

    tbody.innerHTML = files.map(file => `
      <tr class="hover:bg-gray-50 cursor-pointer" data-file="${file.name}">
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="flex items-center">
            <div class="text-lg mr-3">📁</div>
            <div>
              <div class="text-sm font-medium text-gray-900">${file.name}</div>
              ${file.dataset ? `<div class="text-xs text-gray-500">${file.dataset}</div>` : ''}
            </div>
          </div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          ${getTypeBadge(file.type)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
          ${formatSize(file.size)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          ${getStatusBadge(file.status)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          ${formatTime(file.modified)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
          <div class="flex space-x-2">
            <button class="text-blue-600 hover:text-blue-900 transition-colors" data-action="download" data-file="${file.name}">
              📥 Download
            </button>
            <button class="text-green-600 hover:text-green-900 transition-colors" data-action="info" data-file="${file.name}">
              ℹ️ Info
            </button>
            <button class="text-red-600 hover:text-red-900 transition-colors" data-action="delete" data-file="${file.name}">
              🗑️ Delete
            </button>
          </div>
        </td>
      </tr>
    `).join('');

    // Add click listeners for file actions
    this.attachFileActionListeners();
  }

  private setupEventListeners(): void {
    // Filter controls
    const applyFiltersBtn = this.container.querySelector('#apply-filters');
    if (applyFiltersBtn) {
      applyFiltersBtn.addEventListener('click', () => this.applyFilters());
    }

    // File operations
    const refreshBtn = this.container.querySelector('#refresh-files');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.refreshFiles());
    }

    const downloadLatestBtn = this.container.querySelector('#download-latest');
    if (downloadLatestBtn) {
      downloadLatestBtn.addEventListener('click', () => this.downloadLatest());
    }

    const autoCleanupBtn = this.container.querySelector('#auto-cleanup');
    if (autoCleanupBtn) {
      autoCleanupBtn.addEventListener('click', () => this.performAutoCleanup());
    }

    // ESMA download buttons
    const downloadFirdsBtn = this.container.querySelector('#download-firds');
    if (downloadFirdsBtn) {
      downloadFirdsBtn.addEventListener('click', () => this.downloadEsmaFiles('FIRDS'));
    }

    const downloadFitrsBtn = this.container.querySelector('#download-fitrs');
    if (downloadFitrsBtn) {
      downloadFitrsBtn.addEventListener('click', () => this.downloadEsmaFiles('FITRS'));
    }

    const downloadAllBtn = this.container.querySelector('#download-all');
    if (downloadAllBtn) {
      downloadAllBtn.addEventListener('click', () => this.downloadEsmaFiles('ALL'));
    }
  }

  private attachFileActionListeners(): void {
    const actionButtons = this.container.querySelectorAll('[data-action]');
    actionButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        e.stopPropagation();
        const action = button.getAttribute('data-action');
        const fileName = button.getAttribute('data-file');
        if (action && fileName) {
          this.handleFileAction(action, fileName);
        }
      });
    });
  }

  private async applyFilters(): Promise<void> {
    const typeFilter = this.container.querySelector('#type-filter') as HTMLSelectElement;
    const statusFilter = this.container.querySelector('#status-filter') as HTMLSelectElement;

    this.currentFilters = {
      ...(typeFilter?.value && { type: typeFilter.value as 'FIRDS' | 'FITRS' | 'OTHER' }),
      ...(statusFilter?.value && { status: statusFilter.value as 'active' | 'outdated' | 'processing' })
    };

    await this.loadFilesList();
  }

  private async refreshFiles(): Promise<void> {
    const refreshBtn = this.container.querySelector('#refresh-files') as HTMLButtonElement;
    if (refreshBtn) {
      refreshBtn.innerHTML = `<svg class="animate-spin w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path></svg>Refreshing...`;
      refreshBtn.disabled = true;
    }

    try {
      await Promise.all([
        this.loadFileStatistics(),
        this.loadFilesList()
      ]);
    } finally {
      if (refreshBtn) {
        refreshBtn.innerHTML = `<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path></svg><span>Refresh</span>`;
        refreshBtn.disabled = false;
      }
    }
  }

  private async downloadLatest(): Promise<void> {
    try {
      const response = await this.fileService.downloadByCriteria({
        file_types: ['FIRDS', 'FITRS'],
        force_update: true
      });
      
      if (response.status === 'success') {
        this.showSuccess('Latest files download initiated!');
        await this.refreshFiles();
      } else {
        this.showDataOpsError('Failed to initiate download.');
      }
    } catch (error) {
      console.error('Error downloading latest files:', error);
      this.showDataOpsError('Error downloading latest files.');
    }
  }

  private async performAutoCleanup(): Promise<void> {
    if (!confirm('This will remove outdated files. Continue?')) return;

    try {
      const response = await this.fileService.autoCleanup({
        dry_run: false,
        max_age_days: 30,
        keep_latest: 5
      });
      
      if (response.status === 'success') {
        this.showSuccess('Auto-cleanup completed successfully!');
        await this.refreshFiles();
      } else {
        this.showDataOpsError('Auto-cleanup failed.');
      }
    } catch (error) {
      console.error('Error during auto-cleanup:', error);
      this.showDataOpsError('Error during auto-cleanup.');
    }
  }

  private async downloadEsmaFiles(type: 'FIRDS' | 'FITRS' | 'ALL'): Promise<void> {
    try {
      const fileTypes = type === 'ALL' ? ['FIRDS', 'FITRS'] : [type];
      
      const response = await this.fileService.downloadByCriteria({
        file_types: fileTypes,
        force_update: true
      });
      
      if (response.status === 'success') {
        this.showSuccess(`${type} download from ESMA initiated!`);
      } else {
        this.showDataOpsError(`Failed to download ${type} files.`);
      }
    } catch (error) {
      console.error(`Error downloading ${type} files:`, error);
      this.showDataOpsError(`Error downloading ${type} files.`);
    }
  }

  private handleFileAction(action: string, fileName: string): void {
    const file = this.currentFiles.find(f => f.name === fileName);
    if (!file) return;

    switch (action) {
      case 'download':
        this.downloadFile(file);
        break;
      case 'info':
        this.showFileInfo(file);
        break;
      case 'delete':
        this.deleteFile(file);
        break;
    }
  }

  private async downloadFile(file: FileInfo): Promise<void> {
    try {
      // This would typically trigger a download
      console.log('Downloading file:', file.name);
      this.showSuccess(`Download initiated for ${file.name}`);
    } catch (error) {
      console.error('Error downloading file:', error);
      this.showDataOpsError('Error downloading file.');
    }
  }

  private showFileInfo(file: FileInfo): void {
    const formatSize = (bytes: number): string => {
      const sizes = ['B', 'KB', 'MB', 'GB'];
      if (bytes === 0) return '0 B';
      const i = Math.floor(Math.log(bytes) / Math.log(1024));
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    };

    // Use currentStats if available
    const totalFiles = this.currentStats ? this.currentStats.total_files : 'Unknown';
    const totalSize = this.currentStats ? formatSize(this.currentStats.total_size) : 'Unknown';

    alert(`File Information:
    
Name: ${file.name}
Type: ${file.type}
Size: ${formatSize(file.size)}
Status: ${file.status}
Modified: ${new Date(file.modified).toLocaleString()}
${file.dataset ? `Dataset: ${file.dataset}` : ''}
Path: ${file.path}

System Summary:
Total Files: ${totalFiles}
Total Size: ${totalSize}`);
  }

  private async deleteFile(file: FileInfo): Promise<void> {
    if (!confirm(`Are you sure you want to delete ${file.name}?`)) return;

    try {
      // This would call the delete API endpoint
      console.log('Deleting file:', file.name);
      this.showSuccess(`${file.name} marked for deletion`);
      await this.refreshFiles();
    } catch (error) {
      console.error('Error deleting file:', error);
      this.showDataOpsError('Error deleting file.');
    }
  }

  private showFilesError(message: string): void {
    const tbody = this.container.querySelector('#files-tbody');
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="6" class="px-6 py-8 text-center text-red-500">
            <div class="text-center">
              <div class="text-4xl mb-2">❌</div>
              <p class="text-lg font-medium">Error Loading Files</p>
              <p class="text-sm">${message}</p>
              <button onclick="location.reload()" class="mt-4 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors">
                Retry
              </button>
            </div>
          </td>
        </tr>
      `;
    }
  }

  private showDataOpsError(message: string): void {
    // Simple error display - could be enhanced with a toast system
    console.error(message);
    alert(message);
  }

  private showSuccess(message: string): void {
    // Simple success display - could be enhanced with a toast system
    console.log(message);
    alert(message);
  }
}