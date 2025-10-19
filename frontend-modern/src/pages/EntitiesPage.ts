import { BasePage } from './BasePage';

/**
 * Entities Management Page
 * Legal entity relationships and LEI information
 */
export default class EntitiesPage extends BasePage {
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      ${this.createSectionHeader('Entity Management', 'Legal entity relationships, hierarchies, and LEI information with visual mapping')}
      
      <!-- Search Bar -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex space-x-4">
          <div class="flex-1">
            <input 
              type="text" 
              placeholder="Search by LEI, entity name, or country..." 
              class="w-full border border-gray-300 rounded-md px-4 py-2"
            >
          </div>
          <button class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors">
            Search
          </button>
        </div>
      </div>

      <!-- Entities Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Entity List -->
        ${this.createCard(`
          <div class="space-y-4">
            <div class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-semibold text-gray-900">Skandinaviska Enskilda Banken AB</h4>
                  <p class="text-sm text-gray-600">LEI: F3JS33DEI6XQ4ZBPTN86</p>
                  <p class="text-sm text-gray-500">Sweden • Banking</p>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>
              <div class="mt-3 flex items-center text-sm text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                12 instruments linked
              </div>
            </div>
            
            <div class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-semibold text-gray-900">ABB Ltd</h4>
                  <p class="text-sm text-gray-600">LEI: CH0012221716000000</p>
                  <p class="text-sm text-gray-500">Switzerland • Industrial</p>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>
              <div class="mt-3 flex items-center text-sm text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                8 instruments linked
              </div>
            </div>
          </div>
        `, 'Legal Entities')}

        <!-- Relationship Visualization -->
        ${this.createCard(`
          <div class="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
            <div class="text-center">
              <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clip-rule="evenodd"></path>
              </svg>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Relationship Network</h3>
              <p class="text-gray-600">Visual entity relationship mapping</p>
              <p class="text-sm text-gray-400 mt-2">Interactive network visualization coming soon</p>
            </div>
          </div>
        `, 'Entity Relationships')}
      </div>

      <!-- Entity Details -->
      <div class="mt-6">
        ${this.createCard(`
          <div class="text-center py-8">
            <svg class="w-12 h-12 mx-auto text-gray-400 mb-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Select an Entity</h3>
            <p class="text-gray-600">Choose an entity from the list above to view detailed information, relationships, and associated instruments</p>
          </div>
        `, 'Entity Details')}
      </div>
    `;
  }
}