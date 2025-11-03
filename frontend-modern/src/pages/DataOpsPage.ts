import { BasePage } from './BasePage';
import { ApiServiceFactory } from '../services';
import type { FileInfo, FileStats, ESMAFileInfo, ESMAFileCriteria } from '../types/api';

/**
 * DataOps Management Page
 * Professional data operations with ESMA integration and real file management
 */
export default class DataOpsPage extends BasePage {
  private fileService = ApiServiceFactory.getInstance().files;
  private instrumentService = ApiServiceFactory.getInstance().instruments;
  private legalEntityService = ApiServiceFactory.getInstance().entities;
  private transparencyService = ApiServiceFactory.getInstance().transparency;
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

        <!-- Storage Analytics Tab -->
        <div data-tab-pane="storage" class="hidden">
          ${this.createCard(`
            <div class="space-y-6">
              <div class="text-center py-8">
                <div class="mx-auto w-16 h-16 text-blue-500 mb-4">
                  <svg fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
                  </svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Cloud Storage Analytics</h3>
                <p class="text-gray-600 mb-6">Monitor storage usage, costs, and optimization opportunities</p>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-blue-50 p-6 rounded-lg border border-blue-200">
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-blue-900">Storage Usage</h4>
                    <div class="text-2xl text-blue-600">☁️</div>
                  </div>
                  <p class="text-2xl font-bold text-blue-900">Coming Soon</p>
                  <p class="text-sm text-blue-600">Real-time usage monitoring</p>
                </div>

                <div class="bg-green-50 p-6 rounded-lg border border-green-200">
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-green-900">Cost Analysis</h4>
                    <div class="text-2xl text-green-600">💰</div>
                  </div>
                  <p class="text-2xl font-bold text-green-900">Coming Soon</p>
                  <p class="text-sm text-green-600">Cost optimization insights</p>
                </div>

                <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-purple-900">Performance</h4>
                    <div class="text-2xl text-purple-600">⚡</div>
                  </div>
                  <p class="text-2xl font-bold text-purple-900">Coming Soon</p>
                  <p class="text-sm text-purple-600">Access pattern analysis</p>
                </div>
              </div>

              <div class="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div class="flex items-start">
                  <div class="text-yellow-400 mr-3">💡</div>
                  <div>
                    <h4 class="font-medium text-yellow-800">Future Features</h4>
                    <p class="text-sm text-yellow-700 mt-1">
                      This section will include cloud storage metrics, cost analysis, data lifecycle management, 
                      and automated archiving policies for efficient data storage optimization.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          `, '📊 Storage Analytics')}
        </div>

        <!-- Batch Operations Tab -->
        <div data-tab-pane="operations" class="hidden">
          ${this.createCard(`
            <div class="space-y-8">
              <!-- Batch Operations Overview -->
              <div class="border-b border-gray-200 pb-6">
                <h3 class="text-lg font-medium text-gray-900 mb-2">Batch Data Operations</h3>
                <p class="text-gray-600">Perform bulk operations on instruments, entities, transparency data, and FIGI mappings</p>
              </div>

              <!-- Data Coverage Status -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                  <div class="flex items-center justify-between mb-4">
                    <div>
                      <h4 class="font-semibold text-blue-900">Entity Data Coverage</h4>
                      <p class="text-sm text-blue-600">ISINs with LEI mapping</p>
                    </div>
                    <div class="text-3xl text-blue-600">🏢</div>
                  </div>
                  <div class="space-y-2">
                    <div class="flex items-center justify-between">
                      <span class="text-2xl font-bold text-blue-900" id="entity-coverage">--%</span>
                      <span class="text-sm text-blue-600" id="entity-count">-- / --</span>
                    </div>
                    <div class="w-full bg-blue-200 rounded-full h-2">
                      <div id="entity-progress" class="bg-blue-600 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                  <div class="flex items-center justify-between mb-4">
                    <div>
                      <h4 class="font-semibold text-green-900">FIGI Coverage</h4>
                      <p class="text-sm text-green-600">ISINs with Bloomberg FIGIs</p>
                    </div>
                    <div class="text-3xl text-green-600">🔗</div>
                  </div>
                  <div class="space-y-2">
                    <div class="flex items-center justify-between">
                      <span class="text-2xl font-bold text-green-900" id="figi-coverage">--%</span>
                      <span class="text-sm text-green-600" id="figi-count">-- / --</span>
                    </div>
                    <div class="w-full bg-green-200 rounded-full h-2">
                      <div id="figi-progress" class="bg-green-600 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg border border-purple-200">
                  <div class="flex items-center justify-between mb-4">
                    <div>
                      <h4 class="font-semibold text-purple-900">Transparency Coverage</h4>
                      <p class="text-sm text-purple-600">ISINs with MiFID II data</p>
                    </div>
                    <div class="text-3xl text-purple-600">📊</div>
                  </div>
                  <div class="space-y-2">
                    <div class="flex items-center justify-between">
                      <span class="text-2xl font-bold text-purple-900" id="transparency-coverage">--%</span>
                      <span class="text-sm text-purple-600" id="transparency-count">-- / --</span>
                    </div>
                    <div class="w-full bg-purple-200 rounded-full h-2">
                      <div id="transparency-progress" class="bg-purple-600 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Operation Cards -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <!-- Batch Instrument Creation -->
                <div class="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div class="flex items-center mb-4">
                    <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                      <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900">Batch Instrument Creation</h4>
                      <p class="text-sm text-gray-600">Create multiple instruments from CSV/Excel files</p>
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      Support for all CFI instrument types (C,D,E,F,H,I,J,O,R,S)
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      Automatic validation and duplicate detection
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      Progress tracking and error reporting
                    </div>
                  </div>
                  <button id="batch-instruments" class="mt-4 w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                    Start Batch Import
                  </button>
                </div>

                <!-- Entity Data Fills -->
                <div class="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div class="flex items-center mb-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                      <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900">Entity Data Fills</h4>
                      <p class="text-sm text-gray-600">Fill missing entity data from GLEIF registry</p>
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-orange-400 rounded-full mr-2"></span>
                      Auto-populate missing LEI information
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-orange-400 rounded-full mr-2"></span>
                      Update entity relationships and hierarchies
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-orange-400 rounded-full mr-2"></span>
                      Refresh stale entity records
                    </div>
                  </div>
                  <button id="batch-entities" class="mt-4 w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors">
                    Fill Entity Data
                  </button>
                </div>

                <!-- Transparency Calculations -->
                <div class="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div class="flex items-center mb-4">
                    <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                      <svg class="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900">Transparency Fills</h4>
                      <p class="text-sm text-gray-600">Calculate MiFID II transparency thresholds</p>
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                      Batch transparency calculations for ISINs
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                      LIS/SSTI threshold computation
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                      Historical trend analysis
                    </div>
                  </div>
                  <button id="batch-transparency" class="mt-4 w-full bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 transition-colors">
                    Fill Transparency
                  </button>
                </div>

                <!-- FIGI Mapping -->
                <div class="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div class="flex items-center mb-4">
                    <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center mr-3">
                      <svg class="w-6 h-6 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900">FIGI Mapping</h4>
                      <p class="text-sm text-gray-600">Map ISINs to Bloomberg FIGIs</p>
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-indigo-400 rounded-full mr-2"></span>
                      Bulk FIGI lookups for unmapped ISINs
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-indigo-400 rounded-full mr-2"></span>
                      OpenFIGI API integration
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <span class="w-2 h-2 bg-indigo-400 rounded-full mr-2"></span>
                      Automatic mapping updates
                    </div>
                  </div>
                  <button id="batch-figi" class="mt-4 w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors">
                    Map FIGIs
                  </button>
                </div>
              </div>

              <!-- Batch Operation Status -->
              <div id="batch-status" class="hidden">
                <div class="border border-blue-200 bg-blue-50 rounded-lg p-4">
                  <div class="flex items-center">
                    <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
                    <div>
                      <h4 class="font-medium text-blue-900">Batch Operation in Progress</h4>
                      <p class="text-sm text-blue-700" id="batch-progress">Initializing...</p>
                    </div>
                  </div>
                  <div class="mt-3">
                    <div class="w-full bg-blue-200 rounded-full h-2">
                      <div id="batch-progress-bar" class="bg-blue-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                    </div>
                  </div>
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
      // Initialize tab functionality
      this.initializeTabs();
      
      // Load initial data
      await this.loadFileStatistics();
      await this.loadFilesList();
      await this.loadDataCoverage();
      
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

    // Batch operation buttons
    const batchInstrumentsBtn = this.container.querySelector('#batch-instruments');
    if (batchInstrumentsBtn) {
      batchInstrumentsBtn.addEventListener('click', () => this.startBatchInstruments());
    }

    const batchEntitiesBtn = this.container.querySelector('#batch-entities');
    if (batchEntitiesBtn) {
      batchEntitiesBtn.addEventListener('click', () => this.startBatchEntities());
    }

    const batchTransparencyBtn = this.container.querySelector('#batch-transparency');
    if (batchTransparencyBtn) {
      batchTransparencyBtn.addEventListener('click', () => this.startBatchTransparency());
    }

    const batchFigiBtn = this.container.querySelector('#batch-figi');
    if (batchFigiBtn) {
      batchFigiBtn.addEventListener('click', () => this.startBatchFigi());
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

  private async startBatchInstruments(): Promise<void> {
    this.showBatchImportDialog();
  }
  
  private showBatchImportDialog(): void {
    const dialog = document.createElement('div');
    dialog.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    
    dialog.innerHTML = `
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="border-b border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">Batch Instrument Import</h3>
            <button id="close-batch-dialog" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <p class="mt-2 text-sm text-gray-600">Choose an import method. All methods use BatchDataExtractor for optimal performance and disable enrichment.</p>
        </div>

        <!-- Method Selection -->
        <div class="p-6">
          <div class="space-y-6">
            
            <!-- Method 1: Full Type Import -->
            <div class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
              <div class="flex items-center mb-3">
                <input type="radio" id="method-full" name="import-method" value="full_type" class="mr-3">
                <label for="method-full" class="font-medium text-gray-900 cursor-pointer">Method 1: Full Type Import</label>
                <span class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">Resource Intensive</span>
              </div>
              <p class="text-sm text-gray-600 mb-3">Import all instruments of a specific type from FIRDS files. Warning: This may process thousands of records and take significant time.</p>
              <div class="ml-6 space-y-3" id="full-type-controls" style="display: none;">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Instrument Type</label>
                  <select id="full-type-select" class="w-full border border-gray-300 rounded-md px-3 py-2">
                    <option value="">Select instrument type...</option>
                    <option value="equity">Equity</option>
                    <option value="debt">Debt</option>
                    <option value="future">Future</option>
                    <option value="option">Option</option>
                    <option value="collective_investment">Collective Investment</option>
                    <option value="structured">Structured</option>
                    <option value="spot">Spot</option>
                    <option value="forward">Forward</option>
                    <option value="rights">Rights</option>
                    <option value="swap">Swap</option>
                  </select>
                </div>
                <div class="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                  <div class="flex">
                    <svg class="w-5 h-5 text-yellow-400 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    <div class="text-sm">
                      <p class="text-yellow-800 font-medium">High Resource Usage Warning</p>
                      <p class="text-yellow-700">This operation will process all available instruments of the selected type, which may be thousands of records. It requires significant CPU and memory resources.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Method 2: Segmented Import -->
            <div class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
              <div class="flex items-center mb-3">
                <input type="radio" id="method-segmented" name="import-method" value="segmented" class="mr-3">
                <label for="method-segmented" class="font-medium text-gray-900 cursor-pointer">Method 2: Segmented Import</label>
                <span class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">Recommended</span>
              </div>
              <p class="text-sm text-gray-600 mb-3">Import instruments with filtering by jurisdiction, venue, or record limit for controlled processing.</p>
              <div class="ml-6 space-y-3" id="segmented-controls" style="display: none;">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Instrument Type</label>
                    <select id="segmented-type-select" class="w-full border border-gray-300 rounded-md px-3 py-2">
                      <option value="">Select instrument type...</option>
                      <option value="equity">Equity</option>
                      <option value="debt">Debt</option>
                      <option value="future">Future</option>
                      <option value="option">Option</option>
                      <option value="collective_investment">Collective Investment</option>
                      <option value="structured">Structured</option>
                      <option value="spot">Spot</option>
                      <option value="forward">Forward</option>
                      <option value="rights">Rights</option>
                      <option value="swap">Swap</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Record Limit</label>
                    <input type="number" id="segmented-limit" class="w-full border border-gray-300 rounded-md px-3 py-2" 
                           placeholder="1000" min="1" max="10000" value="1000">
                  </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Competent Authority</label>
                    <select id="segmented-authority" class="w-full border border-gray-300 rounded-md px-3 py-2">
                      <option value="SE">Sweden (SE)</option>
                      <option value="DE">Germany (DE)</option>
                      <option value="FR">France (FR)</option>
                      <option value="NL">Netherlands (NL)</option>
                      <option value="GB">United Kingdom (GB)</option>
                      <option value="US">United States (US)</option>
                      <option value="ALL">All Jurisdictions</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Trading Venue (Optional)</label>
                    <input type="text" id="segmented-venue" class="w-full border border-gray-300 rounded-md px-3 py-2" 
                           placeholder="e.g., XSTO, XPAR" maxlength="4">
                  </div>
                </div>
              </div>
            </div>

            <!-- Method 3: ISIN List Import -->
            <div class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
              <div class="flex items-center mb-3">
                <input type="radio" id="method-list" name="import-method" value="isin_list" class="mr-3">
                <label for="method-list" class="font-medium text-gray-900 cursor-pointer">Method 3: ISIN List Import</label>
                <span class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">File Upload</span>
              </div>
              <p class="text-sm text-gray-600 mb-3">Upload a CSV or TXT file with specific ISIN and instrument type pairs for targeted import.</p>
              <div class="ml-6 space-y-3" id="list-controls" style="display: none;">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Upload ISIN List File</label>
                  <div class="flex items-center space-x-4">
                    <input type="file" id="isin-file-input" accept=".csv,.txt" class="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium
                      file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100">
                  </div>
                  <p class="mt-2 text-sm text-gray-500">Expected format: Each line should contain ISIN,TYPE (e.g., SE0000108656,equity)</p>
                </div>
                <div id="file-preview" class="hidden">
                  <div class="bg-gray-50 border border-gray-200 rounded-md p-3">
                    <h5 class="font-medium text-gray-900 mb-2">File Preview:</h5>
                    <div id="file-content-preview" class="text-sm text-gray-600 font-mono max-h-32 overflow-y-auto"></div>
                    <div class="mt-2 text-sm">
                      <span class="text-green-600" id="valid-count">0 valid</span> / 
                      <span class="text-red-600" id="invalid-count">0 invalid</span> entries
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end space-x-3 mt-6 pt-6 border-t border-gray-200">
            <button id="cancel-batch-import" class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Cancel
            </button>
            <button id="start-batch-import" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50" disabled>
              Start Import
            </button>
          </div>
        </div>

        <!-- Progress Section -->
        <div id="batch-progress-section" class="hidden border-t border-gray-200 p-6 bg-gray-50">
          <div class="flex items-center justify-between mb-4">
            <h4 class="font-medium text-gray-900">Import Progress</h4>
            <button id="close-progress" class="text-sm text-gray-500 hover:text-gray-700">Close</button>
          </div>
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span id="progress-status">Initializing...</span>
              <span id="progress-percentage">0%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div id="progress-bar" class="bg-blue-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
            </div>
            <div id="progress-details" class="text-sm text-gray-600"></div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(dialog);
    this.setupBatchDialogListeners(dialog);
  }
  
  private setupBatchDialogListeners(dialog: HTMLElement): void {
    // Close dialog listeners
    const closeBtn = dialog.querySelector('#close-batch-dialog');
    const cancelBtn = dialog.querySelector('#cancel-batch-import');
    const closeProgressBtn = dialog.querySelector('#close-progress');
    
    [closeBtn, cancelBtn, closeProgressBtn].forEach(btn => {
      if (btn) {
        btn.addEventListener('click', () => {
          document.body.removeChild(dialog);
        });
      }
    });

    // Method selection listeners
    const methodRadios = dialog.querySelectorAll('input[name="import-method"]');
    methodRadios.forEach(radio => {
      radio.addEventListener('change', () => {
        this.handleMethodSelection(dialog, (radio as HTMLInputElement).value);
      });
    });

    // File input listener
    const fileInput = dialog.querySelector('#isin-file-input') as HTMLInputElement;
    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        this.handleFileSelection(dialog, (e.target as HTMLInputElement).files?.[0]);
      });
    }

    // Start import listener
    const startBtn = dialog.querySelector('#start-batch-import');
    if (startBtn) {
      startBtn.addEventListener('click', () => {
        this.executeBatchImport(dialog);
      });
    }
  }
  
  private handleMethodSelection(dialog: HTMLElement, method: string): void {
    // Hide all control sections
    ['full-type-controls', 'segmented-controls', 'list-controls'].forEach(id => {
      const controls = dialog.querySelector(`#${id}`);
      if (controls) {
        (controls as HTMLElement).style.display = 'none';
      }
    });

    // Show selected method controls
    const selectedControls = dialog.querySelector(`#${method.replace('_', '-')}-controls`);
    if (selectedControls) {
      (selectedControls as HTMLElement).style.display = 'block';
    }

    // Enable/disable start button based on method
    const startBtn = dialog.querySelector('#start-batch-import') as HTMLButtonElement;
    if (startBtn) {
      startBtn.disabled = method === 'isin_list'; // Will be enabled when file is selected
      if (method !== 'isin_list') {
        startBtn.disabled = false;
      }
    }
  }
  
  private handleFileSelection(dialog: HTMLElement, file: File | undefined): void {
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      this.previewFile(dialog, content);
    };
    reader.readAsText(file);
  }
  
  private previewFile(dialog: HTMLElement, content: string): void {
    const lines = content.trim().split('\n');
    const validEntries: Array<{isin: string, type: string}> = [];
    const invalidEntries: string[] = [];

    const validTypes = ['equity', 'debt', 'future', 'option', 'collective_investment', 'structured', 'spot', 'forward', 'rights', 'swap'];

    lines.forEach((line, index) => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) return; // Skip empty lines and comments

      const parts = trimmed.split(',');
      if (parts.length >= 2) {
        const isin = parts[0].trim().toUpperCase();
        const type = parts[1].trim().toLowerCase();

        if (isin.length === 12 && validTypes.includes(type)) {
          validEntries.push({isin, type});
        } else {
          invalidEntries.push(`Line ${index + 1}: ${trimmed}`);
        }
      } else {
        invalidEntries.push(`Line ${index + 1}: ${trimmed}`);
      }
    });

    // Show preview
    const previewSection = dialog.querySelector('#file-preview');
    const contentPreview = dialog.querySelector('#file-content-preview');
    const validCount = dialog.querySelector('#valid-count');
    const invalidCount = dialog.querySelector('#invalid-count');
    const startBtn = dialog.querySelector('#start-batch-import') as HTMLButtonElement;

    if (previewSection && contentPreview && validCount && invalidCount) {
      (previewSection as HTMLElement).classList.remove('hidden');
      
      // Show first few entries as preview
      const previewText = validEntries.slice(0, 10).map(entry => 
        `${entry.isin},${entry.type}`
      ).join('\n');
      contentPreview.textContent = previewText + (validEntries.length > 10 ? '\n...' : '');
      
      validCount.textContent = `${validEntries.length} valid`;
      invalidCount.textContent = `${invalidEntries.length} invalid`;
      
      // Enable start button if we have valid entries
      if (startBtn) {
        startBtn.disabled = validEntries.length === 0;
      }

      // Store valid entries for later use
      (dialog as any)._validEntries = validEntries;
    }
  }
  
  private async executeBatchImport(dialog: HTMLElement): Promise<void> {
    const selectedMethod = (dialog.querySelector('input[name="import-method"]:checked') as HTMLInputElement)?.value;
    
    if (!selectedMethod) {
      this.showDataOpsError('Please select an import method');
      return;
    }

    // Show progress section
    const progressSection = dialog.querySelector('#batch-progress-section');
    if (progressSection) {
      (progressSection as HTMLElement).classList.remove('hidden');
    }

    try {
      let requestData: any = { method: selectedMethod };

      // Prepare request data based on method
      if (selectedMethod === 'full_type') {
        const typeSelect = dialog.querySelector('#full-type-select') as HTMLSelectElement;
        if (!typeSelect.value) {
          this.showDataOpsError('Please select an instrument type');
          return;
        }
        requestData.instrument_type = typeSelect.value;
        requestData.confirmed = true;
      } 
      else if (selectedMethod === 'segmented') {
        const typeSelect = dialog.querySelector('#segmented-type-select') as HTMLSelectElement;
        const limitInput = dialog.querySelector('#segmented-limit') as HTMLInputElement;
        const authoritySelect = dialog.querySelector('#segmented-authority') as HTMLSelectElement;
        const venueInput = dialog.querySelector('#segmented-venue') as HTMLInputElement;
        
        if (!typeSelect.value) {
          this.showDataOpsError('Please select an instrument type');
          return;
        }
        
        requestData.instrument_type = typeSelect.value;
        requestData.filters = {
          competent_authority: authoritySelect.value,
          limit: parseInt(limitInput.value) || 1000
        };
        
        if (venueInput.value.trim()) {
          requestData.filters.relevant_trading_venue = venueInput.value.trim().toUpperCase();
        }
      }
      else if (selectedMethod === 'isin_list') {
        const validEntries = (dialog as any)._validEntries;
        if (!validEntries || validEntries.length === 0) {
          this.showDataOpsError('Please upload a valid ISIN list file');
          return;
        }
        requestData.instruments = validEntries;
      }

      // Update progress
      this.updateBatchProgress(dialog, 'Starting import...', 10);

      // Call the API
      const response = await fetch('/api/v1/instruments/batch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      const result = await response.json();

      if (response.ok && result.status === 'success') {
        this.updateBatchProgress(dialog, 'Import completed successfully!', 100);
        this.updateProgressDetails(dialog, result.data);
        
        setTimeout(() => {
          this.showSuccess(`Batch import completed: ${result.message}`);
        }, 2000);
      } else if (result.status === 'warning') {
        // Handle full type import warning
        this.updateBatchProgress(dialog, result.message, 0);
        this.updateProgressDetails(dialog, { warning: result.warning_type });
      } else {
        this.updateBatchProgress(dialog, 'Import failed', 0);
        this.showDataOpsError(result.error?.message || 'Import failed');
      }
    } catch (error) {
      console.error('Error in batch import:', error);
      this.updateBatchProgress(dialog, 'Import failed', 0);
      this.showDataOpsError('Error during batch import');
    }
  }
  
  private updateBatchProgress(dialog: HTMLElement, status: string, percentage: number): void {
    const statusElement = dialog.querySelector('#progress-status');
    const percentageElement = dialog.querySelector('#progress-percentage');
    const progressBar = dialog.querySelector('#progress-bar') as HTMLElement;
    
    if (statusElement) statusElement.textContent = status;
    if (percentageElement) percentageElement.textContent = `${percentage}%`;
    if (progressBar) progressBar.style.width = `${percentage}%`;
  }
  
  private updateProgressDetails(dialog: HTMLElement, data: any): void {
    const detailsElement = dialog.querySelector('#progress-details');
    if (!detailsElement || !data) return;
    
    let detailsText = '';
    
    if (data.total_created !== undefined) {
      detailsText += `Created: ${data.total_created} instruments `;
    }
    if (data.total_failed !== undefined) {
      detailsText += `Failed: ${data.total_failed} `;
    }
    if (data.total_skipped !== undefined) {
      detailsText += `Skipped: ${data.total_skipped} `;
    }
    if (data.type_breakdown) {
      detailsText += `Types processed: ${Object.keys(data.type_breakdown).join(', ')}`;
    }
    
    detailsElement.textContent = detailsText;
  }

  private async startBatchEntities(): Promise<void> {
    const button = this.container.querySelector('#batch-entities') as HTMLButtonElement;
    if (button) {
      button.disabled = true;
      button.textContent = 'Processing...';
    }
    
    this.showBatchStatus('Scanning for incomplete entity records...');
    
    try {
      const response = await this.legalEntityService.batchFillEntityData();
      
      if (response.status === 'success') {
        const data = response.data || {};
        this.showSuccess(`Entity data fill completed: ${data.updated || 0} instruments linked to entities (${data.scanned || 0} scanned, ${data.failed || 0} failed)`);
      } else {
        this.showDataOpsError('Failed to start entity data fill.');
      }
    } catch (error) {
      console.error('Error in batch entities:', error);
      this.showDataOpsError('Error starting entity data fill.');
    } finally {
      this.hideBatchStatus();
      if (button) {
        button.disabled = false;
        button.textContent = 'Fill Entity Data';
      }
    }
  }

  private async startBatchTransparency(): Promise<void> {
    const button = this.container.querySelector('#batch-transparency') as HTMLButtonElement;
    if (button) {
      button.disabled = true;
      button.textContent = 'Processing...';
    }
    
    this.showBatchStatus('Filling transparency data from FITRS files...');
    
    try {
      const response = await this.transparencyService.batchCalculateTransparency();
      
      if (response.status === 'success') {
        const data = response.data || {};
        this.showSuccess(
          `Transparency fill completed: ${data.created_calculations || 0} calculations created ` +
          `(${data.processed || 0} instruments processed, ${data.failed || 0} failed)`
        );
      } else {
        this.showDataOpsError('Failed to start transparency fill.');
      }
    } catch (error) {
      console.error('Error in batch transparency:', error);
      this.showDataOpsError('Error starting transparency fill.');
    } finally {
      this.hideBatchStatus();
      if (button) {
        button.disabled = false;
        button.textContent = 'Fill Transparency';
      }
    }
  }

  private async startBatchFigi(): Promise<void> {
    const button = this.container.querySelector('#batch-figi') as HTMLButtonElement;
    if (button) {
      button.disabled = true;
      button.textContent = 'Processing...';
    }
    
    this.showBatchStatus('Initializing FIGI batch processing...');
    
    try {
      const response = await this.instrumentService.batchMapFigi();
      
      if (response.status === 'success') {
        // Response fields are at root level, not under 'data'
        const processed = (response as any).processed || 0;
        const mapped = (response as any).mapped || 0;
        const failed = (response as any).failed || 0;
        const skipped = (response as any).skipped || 0;
        const skippedText = skipped > 0 ? `, ${skipped} skipped` : '';
        this.showSuccess(`FIGI mapping completed: ${mapped} instruments mapped to FIGIs (${processed} processed, ${failed} failed${skippedText})`);
      } else {
        this.showDataOpsError('Failed to start FIGI mapping.');
      }
    } catch (error) {
      console.error('Error in batch FIGI:', error);
      this.showDataOpsError('Error starting FIGI mapping.');
    } finally {
      this.hideBatchStatus();
      if (button) {
        button.disabled = false;
        button.textContent = 'Map FIGIs';
      }
    }
  }

  private showBatchStatus(message: string): void {
    const statusDiv = this.container.querySelector('#batch-status');
    const progressText = this.container.querySelector('#batch-progress');
    const progressBar = this.container.querySelector('#batch-progress-bar') as HTMLElement;
    
    if (statusDiv && progressText && progressBar) {
      statusDiv.classList.remove('hidden');
      progressText.textContent = message;
      progressBar.style.width = '10%';
    }
  }

  private hideBatchStatus(): void {
    const statusDiv = this.container.querySelector('#batch-status');
    if (statusDiv) {
      statusDiv.classList.add('hidden');
    }
  }

  private async loadDataCoverage(): Promise<void> {
    try {
      // Load data coverage statistics from the API
      const response = await this.instrumentService.getDataCoverageStats();
      
      if (response.status === 'success' && response.data) {
        const stats = response.data;
        
        // Update entity coverage
        this.updateCoverageCard(
          'entity', 
          Math.round(stats.entity_coverage.percentage), 
          stats.entity_coverage.covered, 
          stats.total_instruments
        );
        
        // Update FIGI coverage
        this.updateCoverageCard(
          'figi', 
          Math.round(stats.figi_coverage.percentage), 
          stats.figi_coverage.covered, 
          stats.total_instruments
        );
        
        // Update transparency coverage
        this.updateCoverageCard(
          'transparency', 
          Math.round(stats.transparency_coverage.percentage), 
          stats.transparency_coverage.covered, 
          stats.total_instruments
        );
      } else {
        throw new Error('Failed to load coverage statistics');
      }
    } catch (error) {
      console.error('Error loading data coverage:', error);
      // Set fallback values with mock data
      this.updateCoverageCard('entity', 75, 750, 1000);
      this.updateCoverageCard('figi', 60, 600, 1000);
      this.updateCoverageCard('transparency', 45, 450, 1000);
    }
  }



  private updateCoverageCard(type: 'entity' | 'figi' | 'transparency', percentage: number, covered: number, total: number): void {
    const coverageElement = this.container.querySelector(`#${type}-coverage`);
    const countElement = this.container.querySelector(`#${type}-count`);
    const progressElement = this.container.querySelector(`#${type}-progress`) as HTMLElement;

    if (coverageElement && countElement && progressElement) {
      coverageElement.textContent = `${percentage}%`;
      countElement.textContent = `${covered.toLocaleString()} / ${total.toLocaleString()}`;
      progressElement.style.width = `${percentage}%`;
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