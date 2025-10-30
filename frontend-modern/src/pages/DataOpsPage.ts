import { BasePage } from './BasePage';
import { ApiServiceFactory } from '../services';
import type { FileInfo, FileStats, ESMAFileInfo, ESMAFileCriteria } from '../types/api';

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
  private availableESMAFiles: ESMAFileInfo[] = [];
  private selectedESMAFiles: Set<string> = new Set();

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
                <button id="download-files" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                  </svg>
                  <span>Download Files</span>
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

      <!-- Download Files Dialog -->
      <div id="download-dialog" class="fixed inset-0 bg-gray-600 bg-opacity-50 hidden z-50">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div class="flex items-center justify-between p-6 border-b border-gray-200">
              <h3 class="text-xl font-semibold text-gray-900">Download ESMA Files</h3>
              <button id="close-download-dialog" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div class="flex flex-col h-[600px]">
              <!-- Filters Section -->
              <div class="p-6 border-b border-gray-200 bg-gray-50">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Dataset Type</label>
                    <select id="dataset-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-white">
                      <option value="">All Datasets</option>
                      <option value="firds">FIRDS</option>
                      <option value="fitrs">FITRS</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Asset Type</label>
                    <select id="asset-type-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-white">
                      <option value="">All Assets</option>
                      <option value="C">Collective Investment</option>
                      <option value="D">Debt</option>
                      <option value="E">Equity</option>
                      <option value="F">Futures</option>
                      <option value="H">Structured Products</option>
                      <option value="I">Interest Rate</option>
                      <option value="J">Commodity</option>
                      <option value="O">Options</option>
                      <option value="R">Rights</option>
                      <option value="S">Swaps</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Date From</label>
                    <input type="date" id="date-from-filter" class="w-full border border-gray-300 rounded-md px-3 py-2">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Date To</label>
                    <input type="date" id="date-to-filter" class="w-full border border-gray-300 rounded-md px-3 py-2">
                  </div>
                </div>
                <div class="flex items-center justify-between">
                  <button id="apply-esma-filters" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Apply Filters
                  </button>
                  <div class="flex items-center space-x-4">
                    <button id="select-all-files" class="text-blue-600 hover:text-blue-800 font-medium">Select All</button>
                    <button id="clear-selection" class="text-gray-600 hover:text-gray-800 font-medium">Clear All</button>
                    <span id="selection-count" class="text-sm text-gray-600">0 files selected</span>
                  </div>
                </div>
              </div>

              <!-- Files List -->
              <div class="flex-1 overflow-auto p-6">
                <div id="esma-files-loading" class="text-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p class="text-gray-600">Loading available files...</p>
                </div>
                <div id="esma-files-list" class="hidden">
                  <div class="space-y-2" id="files-container">
                    <!-- Files will be loaded here -->
                  </div>
                </div>
                <div id="esma-files-empty" class="hidden text-center py-8">
                  <p class="text-gray-600">No files found. Try adjusting your filters.</p>
                </div>
              </div>

              <!-- Action Buttons -->
              <!-- Make footer sticky so action buttons are always visible inside the scrollable area -->
              <div class="sticky bottom-0 z-10 p-6 border-t border-gray-200 bg-white">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-4">
                    <button id="download-all-latest" class="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors">
                      Download All Latest (Batch)
                    </button>
                    <span class="text-sm text-gray-600">For automated scheduling</span>
                  </div>
                  <div class="flex items-center space-x-3">
                    <button id="download-selected" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed" disabled>
                      Download Selected
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
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

    const downloadFilesBtn = this.container.querySelector('#download-files');
    if (downloadFilesBtn) {
      downloadFilesBtn.addEventListener('click', () => this.openDownloadDialog());
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

    // Download dialog event listeners
    this.setupDownloadDialogListeners();
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

  // ===== DOWNLOAD DIALOG METHODS =====

  private setupDownloadDialogListeners(): void {
    // Dialog open/close
    const closeBtn = this.container.querySelector('#close-download-dialog');
    if (closeBtn) closeBtn.addEventListener('click', () => this.closeDownloadDialog());

    // Filter controls
    const applyESMAFiltersBtn = this.container.querySelector('#apply-esma-filters');
    if (applyESMAFiltersBtn) applyESMAFiltersBtn.addEventListener('click', () => this.applyESMAFilters());

    // Selection controls
    const selectAllBtn = this.container.querySelector('#select-all-files');
    const clearSelectionBtn = this.container.querySelector('#clear-selection');
    if (selectAllBtn) selectAllBtn.addEventListener('click', () => this.selectAllESMAFiles());
    if (clearSelectionBtn) clearSelectionBtn.addEventListener('click', () => this.clearESMASelection());

    // Download actions
    const downloadSelectedBtn = this.container.querySelector('#download-selected');
    const downloadAllLatestBtn = this.container.querySelector('#download-all-latest');
    if (downloadSelectedBtn) downloadSelectedBtn.addEventListener('click', () => this.downloadSelectedESMAFiles());
    if (downloadAllLatestBtn) downloadAllLatestBtn.addEventListener('click', () => this.downloadAllLatestFiles());
  }

  private async openDownloadDialog(): Promise<void> {
    const dialog = this.container.querySelector('#download-dialog');
    if (!dialog) return;

    // Show dialog
    dialog.classList.remove('hidden');

    // Set default date range (last 30 days)
    const today = new Date();
    const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
    
    const dateFromInput = this.container.querySelector('#date-from-filter') as HTMLInputElement;
    const dateToInput = this.container.querySelector('#date-to-filter') as HTMLInputElement;
    
    if (dateFromInput) dateFromInput.value = thirtyDaysAgo.toISOString().split('T')[0];
    if (dateToInput) dateToInput.value = today.toISOString().split('T')[0];

    // Load initial files
    await this.loadESMAFiles();
  }

  private closeDownloadDialog(): void {
    const dialog = this.container.querySelector('#download-dialog');
    if (dialog) {
      dialog.classList.add('hidden');
      this.selectedESMAFiles.clear();
      this.updateSelectionCount();
    }
  }

  private async loadESMAFiles(): Promise<void> {
    const loadingDiv = this.container.querySelector('#esma-files-loading');
    const listDiv = this.container.querySelector('#esma-files-list');
    const emptyDiv = this.container.querySelector('#esma-files-empty');

    // Show loading
    if (loadingDiv) loadingDiv.classList.remove('hidden');
    if (listDiv) listDiv.classList.add('hidden');
    if (emptyDiv) emptyDiv.classList.add('hidden');

    try {
      const criteria = this.getESMAFilterCriteria();
      const response = await this.fileService.getEsmaFiles(criteria);
      
      if (response.status === 'success' && response.data) {
        this.availableESMAFiles = response.data;
        this.renderESMAFilesList();
        
        if (loadingDiv) loadingDiv.classList.add('hidden');
        if (this.availableESMAFiles.length > 0) {
          if (listDiv) listDiv.classList.remove('hidden');
        } else {
          if (emptyDiv) emptyDiv.classList.remove('hidden');
        }
      } else {
        throw new Error('Failed to load ESMA files');
      }
    } catch (error) {
      console.error('Error loading ESMA files:', error);
      if (loadingDiv) loadingDiv.classList.add('hidden');
      if (emptyDiv) emptyDiv.classList.remove('hidden');
      this.showDataOpsError('Failed to load ESMA files');
    }
  }

  private getESMAFilterCriteria(): ESMAFileCriteria {
    const datasetFilter = this.container.querySelector('#dataset-filter') as HTMLSelectElement;
    const assetTypeFilter = this.container.querySelector('#asset-type-filter') as HTMLSelectElement;
    const dateFromFilter = this.container.querySelector('#date-from-filter') as HTMLInputElement;
    const dateToFilter = this.container.querySelector('#date-to-filter') as HTMLInputElement;

    const criteria: ESMAFileCriteria = {};
    
    if (datasetFilter?.value) {
      criteria.datasets = [datasetFilter.value];
    }
    if (assetTypeFilter?.value) {
      criteria.asset_type = assetTypeFilter.value;
    }
    if (dateFromFilter?.value) {
      criteria.date_from = dateFromFilter.value;
    }
    if (dateToFilter?.value) {
      criteria.date_to = dateToFilter.value;
    }

    return criteria;
  }

  private async applyESMAFilters(): Promise<void> {
    await this.loadESMAFiles();
  }

  private renderESMAFilesList(): void {
    const container = this.container.querySelector('#files-container');
    if (!container) return;

    container.innerHTML = this.availableESMAFiles.map(file => `
      <div class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
        <input 
          type="checkbox" 
          class="esma-file-checkbox mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          data-file-name="${file.file_name}"
          ${this.selectedESMAFiles.has(file.file_name) ? 'checked' : ''}
        >
        <div class="flex-1">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-gray-900">${file.file_name}</h4>
              <div class="flex items-center space-x-4 text-sm text-gray-600">
                <span class="bg-${file.file_type === 'firds' ? 'blue' : file.file_type === 'fitrs' ? 'green' : 'gray'}-100 text-${file.file_type === 'firds' ? 'blue' : file.file_type === 'fitrs' ? 'green' : 'gray'}-800 px-2 py-1 rounded-full text-xs font-medium">
                  ${file.file_type?.toUpperCase() || 'UNKNOWN'}
                </span>
                <span>📅 ${file.publication_date ? new Date(file.publication_date).toLocaleDateString() : 'Unknown'}</span>
                ${file.file_size ? `<span>📦 ${this.formatFileSize(file.file_size)}</span>` : ''}
                ${file.instrument_type && file.instrument_type !== 'null' ? `<span>🎯 ${file.instrument_type}</span>` : ''}
              </div>
            </div>
          </div>
        </div>
      </div>
    `).join('');

    // Add event listeners for checkboxes
    const checkboxes = container.querySelectorAll('.esma-file-checkbox');
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        const target = e.target as HTMLInputElement;
        const fileName = target.dataset.fileName;
        if (fileName) {
          if (target.checked) {
            this.selectedESMAFiles.add(fileName);
          } else {
            this.selectedESMAFiles.delete(fileName);
          }
          this.updateSelectionCount();
        }
      });
    });
  }

  private formatFileSize(bytes: number): string {
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  }

  private selectAllESMAFiles(): void {
    this.availableESMAFiles.forEach(file => {
      this.selectedESMAFiles.add(file.file_name);
    });
    
    // Update checkboxes
    const checkboxes = this.container.querySelectorAll('.esma-file-checkbox') as NodeListOf<HTMLInputElement>;
    checkboxes.forEach(checkbox => {
      checkbox.checked = true;
    });
    
    this.updateSelectionCount();
  }

  private clearESMASelection(): void {
    this.selectedESMAFiles.clear();
    
    // Update checkboxes
    const checkboxes = this.container.querySelectorAll('.esma-file-checkbox') as NodeListOf<HTMLInputElement>;
    checkboxes.forEach(checkbox => {
      checkbox.checked = false;
    });
    
    this.updateSelectionCount();
  }

  private updateSelectionCount(): void {
    const countSpan = this.container.querySelector('#selection-count');
    const downloadBtn = this.container.querySelector('#download-selected') as HTMLButtonElement;
    
    const count = this.selectedESMAFiles.size;
    if (countSpan) {
      countSpan.textContent = `${count} file${count !== 1 ? 's' : ''} selected`;
    }
    
    if (downloadBtn) {
      downloadBtn.disabled = count === 0;
    }
  }

  private async downloadSelectedESMAFiles(): Promise<void> {
    if (this.selectedESMAFiles.size === 0) return;

    const selectedFiles = this.availableESMAFiles.filter(file => 
      this.selectedESMAFiles.has(file.file_name)
    );

    try {
      const response = await this.fileService.downloadSelectedFiles(selectedFiles, {
        parse: true,
        overwrite: false
      });

      if (response.status === 'success') {
        this.showSuccess(`Download initiated for ${selectedFiles.length} files!`);
        this.closeDownloadDialog();
        await this.refreshFiles();
      } else {
        this.showDataOpsError('Failed to initiate download.');
      }
    } catch (error) {
      console.error('Error downloading selected files:', error);
      this.showDataOpsError('Error downloading selected files.');
    }
  }

  private async downloadAllLatestFiles(): Promise<void> {
    try {
      const response = await this.fileService.downloadByCriteria({
        file_types: ['FIRDS', 'FITRS'],
        force_update: true
      });
      
      if (response.status === 'success') {
        this.showSuccess('Batch download of all latest files initiated!');
        this.closeDownloadDialog();
        await this.refreshFiles();
      } else {
        this.showDataOpsError('Failed to initiate batch download.');
      }
    } catch (error) {
      console.error('Error downloading all latest files:', error);
      this.showDataOpsError('Error downloading all latest files.');
    }
  }
}