import { BasePage } from './BasePage';

/**
 * Swagger API Documentation Page
 * Embedded Swagger UI for API testing and documentation
 */
export default class SwaggerPage extends BasePage {
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      ${this.createSectionHeader('API Documentation', 'Interactive Swagger UI for testing and documentation')}
      
      <!-- Swagger Embed -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-medium text-gray-900">MarketData API v1</h3>
            <a 
              href="http://localhost:5000/api/v1/swagger" 
              target="_blank"
              class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors text-sm"
            >
              Open in New Tab
            </a>
          </div>
        </div>
        
        <!-- Iframe Container -->
        <div class="relative" style="height: 80vh;">
          <iframe 
            src="http://localhost:5000/api/v1/swagger"
            class="w-full h-full border-0"
            title="Swagger UI"
          ></iframe>
        </div>
      </div>

      <!-- API Quick Links -->
      <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        
        ${this.createCard(`
          <div class="space-y-3">
            <h4 class="font-semibold text-gray-900">Core Endpoints</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">GET /instruments</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">GET /entities</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">GET /transparency</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
            </div>
          </div>
        `, '')}

        ${this.createCard(`
          <div class="space-y-3">
            <h4 class="font-semibold text-gray-900">Data Management</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">GET /files</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">POST /files/download</span>
                <span class="text-blue-600 font-mono text-xs">POST</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">GET /mic</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
            </div>
          </div>
        `, '')}

        ${this.createCard(`
          <div class="space-y-3">
            <h4 class="font-semibold text-gray-900">Advanced Features</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">GET /relationships</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">GET /schema</span>
                <span class="text-green-600 font-mono text-xs">200</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">POST /schema/validate</span>
                <span class="text-blue-600 font-mono text-xs">POST</span>
              </div>
            </div>
          </div>
        `, '')}
      </div>
    `;
  }
}