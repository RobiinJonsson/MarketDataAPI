import { BasePage } from './BasePage';

/**
 * DataOps Management Page
 * Professional data operations with ESMA integration and file management
 */
export default class DataOpsPage extends BasePage {
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      ${this.createSectionHeader('DataOps Center', 'Professional data operations with ESMA integration, file management, and batch processing')}
      
      ${this.createTabs([
        { id: 'files', label: 'File Management', active: true },
        { id: 'esma', label: 'ESMA Downloads' },
        { id: 'storage', label: 'Storage Analytics' },
        { id: 'operations', label: 'Batch Operations' }
      ])}

      <!-- File Management Tab -->
      <div data-tab-pane="files">
        <!-- Storage Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          <div class="bg-blue-50 p-4 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-blue-700 text-sm font-medium">FIRDS Files</p>
                <p class="text-2xl font-bold text-blue-900">32</p>
              </div>
              <svg class="w-8 h-8 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
          
          <div class="bg-green-50 p-4 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-green-700 text-sm font-medium">FITRS Files</p>
                <p class="text-2xl font-bold text-green-900">13</p>
              </div>
              <svg class="w-8 h-8 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
          
          <div class="bg-purple-50 p-4 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-purple-700 text-sm font-medium">Total Size</p>
                <p class="text-2xl font-bold text-purple-900">2.1GB</p>
              </div>
              <svg class="w-8 h-8 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
              </svg>
            </div>
          </div>
          
          <div class="bg-orange-50 p-4 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-orange-700 text-sm font-medium">Last Updated</p>
                <p class="text-lg font-bold text-orange-900">2h ago</p>
              </div>
              <svg class="w-8 h-8 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- File Operations -->
        <div class="flex space-x-4 mb-6">
          <button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
            Refresh Files
          </button>
          <button class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors">
            Download Latest
          </button>
          <button class="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors">
            Auto-Cleanup
          </button>
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
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Modified</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">FULINS_E_20251018_01of02.zip</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      FIRDS
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">125.3 MB</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">2 hours ago</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button class="text-blue-600 hover:text-blue-900">Download</button>
                    <button class="text-red-600 hover:text-red-900">Delete</button>
                  </td>
                </tr>
                <tr class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">FITRS_20251018.zip</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      FITRS
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">45.7 MB</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">3 hours ago</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button class="text-blue-600 hover:text-blue-900">Download</button>
                    <button class="text-red-600 hover:text-red-900">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        `, 'Recent Files')}
      </div>

      <!-- ESMA Downloads Tab -->
      <div data-tab-pane="esma" class="hidden">
        ${this.createCard(`
          <div class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 011 1v1a1 1 0 01-1 1H4a1 1 0 01-1-1v-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
            <h3 class="text-lg font-medium text-gray-900 mb-2">ESMA Data Downloads</h3>
            <p class="text-gray-600 mb-6">Direct integration with ESMA FIRDS and FITRS data sources</p>
            <button class="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors">
              Configure ESMA Integration
            </button>
          </div>
        `, 'ESMA Integration')}
      </div>

      <!-- Storage Analytics Tab -->
      <div data-tab-pane="storage" class="hidden">
        ${this.createCard(`
          <div class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
            </svg>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Storage Analytics</h3>
            <p class="text-gray-600">Detailed storage usage and trends analysis</p>
          </div>
        `, 'Storage Analytics')}
      </div>

      <!-- Batch Operations Tab -->
      <div data-tab-pane="operations" class="hidden">
        ${this.createCard(`
          <div class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
            </svg>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Batch Operations</h3>
            <p class="text-gray-600">Bulk data processing and management operations</p>
          </div>
        `, 'Batch Operations')}
      </div>
    `;

    this.initializeTabs();
  }
}