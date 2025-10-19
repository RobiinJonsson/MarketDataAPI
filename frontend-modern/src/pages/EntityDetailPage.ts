import { BasePage } from './BasePage';
import { LegalEntityService } from '../services/LegalEntityService';
import { LegalEntity as BaseLegalEntity } from '../types/api';

// Extended interface to match actual API response structure
interface LegalEntity extends BaseLegalEntity {
  jurisdiction?: string;
  bic?: string;
  addresses?: Array<{
    type: string;
    country: string;
    city: string;
    address_lines: string;
  }>;
  relationships?: {
    direct_children?: Array<{
      lei: string;
      name: string;
      jurisdiction: string;
      status: string;
    }>;
    direct_parent?: {
      lei: string;
      name: string;
      jurisdiction: string;
      status: string;
    };
  };
  status_indicators?: string[];
  display_status?: string;
  entity_counts?: {
    addresses_count: number;
    relationships_count: number;
    instruments_count: number;
  };
}

/**
 * Detailed Entity Page
 * Comprehensive legal entity data display with relationships and corporate structure
 */
export default class EntityDetailPage extends BasePage {
  private legalEntityService: LegalEntityService;
  private lei: string;

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    super(container, params);
    this.legalEntityService = new LegalEntityService();
    this.lei = params.lei || '';
    
    if (!this.lei) {
      throw new Error('LEI parameter is required for EntityDetailPage');
    }
  }
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      <div class="min-h-screen bg-gray-50">
        <!-- Main Content -->
        <div id="main-content" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- Loading State -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <div class="flex items-center justify-center">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
              <span class="text-gray-600">Loading entity details...</span>
            </div>
          </div>
        </div>
      </div>
    `;

    this.setupEventListeners();
    await this.loadEntityData();
  }

  private setupEventListeners(): void {
    // Set up navigation buttons
    const backBtn = this.container.querySelector('#back-btn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.history.back();
      });
    }

    // Entity navigation buttons
    const viewEntitiesBtn = this.container.querySelector('#view-entities-btn');
    if (viewEntitiesBtn) {
      viewEntitiesBtn.addEventListener('click', () => {
        window.location.hash = '#/entities';
      });
    }
  }

  private async loadEntityData(): Promise<void> {
    try {
      const response = await this.legalEntityService.getEntity(this.lei);
      const entity = response.data;
      
      if (entity) {
        await this.renderEntityDetail(entity);
      } else {
        this.showErrorState('Entity not found');
      }
    } catch (error) {
      console.error('Failed to load entity:', error);
      this.showErrorState('Failed to load entity details');
    }
  }

  private async renderEntityDetail(entity: LegalEntity): Promise<void> {
    const parentEntity = entity.relationships?.direct_parent;
    const childEntities = entity.relationships?.direct_children || [];
    const addresses = entity.addresses || [];
    
    this.container.innerHTML = `
      <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <div class="bg-white border-b border-gray-200 sticky top-0 z-10">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <button id="back-btn" class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                  </svg>
                </button>
                <div>
                  <h1 class="text-2xl font-bold text-gray-900">${entity.name}</h1>
                  <p class="text-sm text-gray-600">LEI: ${entity.lei}</p>
                </div>
              </div>
              <div class="flex space-x-3">
                <button id="view-entities-btn" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  View All Entities
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Main Entity Information (Left Column) -->
            <div class="lg:col-span-2 space-y-8">
              
              <!-- Basic Information Card -->
              <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="p-6 border-b border-gray-200">
                  <h2 class="text-xl font-semibold text-gray-900">Entity Information</h2>
                </div>
                <div class="p-6">
                  <dl class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Legal Entity Identifier (LEI)</dt>
                      <dd class="text-lg font-mono text-gray-900 bg-gray-50 p-2 rounded">${entity.lei}</dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Entity Name</dt>
                      <dd class="text-lg text-gray-900">${entity.name}</dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Jurisdiction</dt>
                      <dd class="text-lg text-gray-900">${entity.jurisdiction || entity.country || 'N/A'}</dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Status</dt>
                      <dd class="text-lg">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                          entity.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }">
                          ${entity.status || 'Unknown'}
                        </span>
                      </dd>
                    </div>
                    ${entity.legal_form ? `
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Legal Form</dt>
                      <dd class="text-lg text-gray-900">${entity.legal_form}</dd>
                    </div>
                    ` : ''}
                    ${entity.bic ? `
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">BIC Code</dt>
                      <dd class="text-lg font-mono text-gray-900 bg-gray-50 p-2 rounded">${entity.bic}</dd>
                    </div>
                    ` : ''}
                    ${entity.registration_date ? `
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Registration Date</dt>
                      <dd class="text-lg text-gray-900">${new Date(entity.registration_date).toLocaleDateString()}</dd>
                    </div>
                    ` : ''}
                    ${entity.last_update ? `
                    <div>
                      <dt class="text-sm font-medium text-gray-500 mb-1">Last Update</dt>
                      <dd class="text-lg text-gray-900">${new Date(entity.last_update).toLocaleDateString()}</dd>
                    </div>
                    ` : ''}
                  </dl>
                </div>
              </div>

              <!-- Addresses Card -->
              ${addresses.length > 0 ? `
              <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="p-6 border-b border-gray-200">
                  <h2 class="text-xl font-semibold text-gray-900">Addresses (${addresses.length})</h2>
                </div>
                <div class="p-6">
                  <div class="space-y-6">
                    ${addresses.map(address => `
                    <div class="border border-gray-200 rounded-lg p-4">
                      <div class="flex items-start justify-between">
                        <div class="flex-1">
                          <h3 class="font-medium text-gray-900">${address.type}</h3>
                          <div class="mt-2 text-gray-600">
                            <p>${address.address_lines}</p>
                            <p>${address.city}, ${address.country}</p>
                          </div>
                        </div>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          ${address.type}
                        </span>
                      </div>
                    </div>
                    `).join('')}
                  </div>
                </div>
              </div>
              ` : ''}

              <!-- Corporate Relationships Card -->
              ${(parentEntity || childEntities.length > 0) ? `
              <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="p-6 border-b border-gray-200">
                  <h2 class="text-xl font-semibold text-gray-900">Corporate Relationships</h2>
                </div>
                <div class="p-6">
                  
                  ${parentEntity ? `
                  <!-- Parent Entity -->
                  <div class="mb-8">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Parent Entity</h3>
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div class="flex items-center justify-between">
                        <div>
                          <h4 class="font-medium text-blue-900">${parentEntity.name}</h4>
                          <p class="text-sm text-blue-700">LEI: ${parentEntity.lei}</p>
                          <p class="text-sm text-blue-600">${parentEntity.jurisdiction}</p>
                        </div>
                        <button onclick="window.location.hash='#/entities/${parentEntity.lei}'" class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                          View Details
                        </button>
                      </div>
                    </div>
                  </div>
                  ` : ''}

                  ${childEntities.length > 0 ? `
                  <!-- Child Entities -->
                  <div>
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Subsidiaries (${childEntities.length})</h3>
                    <div class="space-y-3">
                      ${childEntities.map(child => `
                      <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                          <div>
                            <h4 class="font-medium text-green-900">${child.name}</h4>
                            <p class="text-sm text-green-700">LEI: ${child.lei}</p>
                            <p class="text-sm text-green-600">${child.jurisdiction}</p>
                          </div>
                          <button onclick="window.location.hash='#/entities/${child.lei}'" class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors">
                            View Details
                          </button>
                        </div>
                      </div>
                      `).join('')}
                    </div>
                  </div>
                  ` : ''}
                </div>
              </div>
              ` : ''}
            </div>

            <!-- Sidebar (Right Column) -->
            <div class="lg:col-span-1 space-y-6">
              
              <!-- Quick Stats Card -->
              <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="p-6 border-b border-gray-200">
                  <h3 class="text-lg font-semibold text-gray-900">Quick Stats</h3>
                </div>
                <div class="p-6">
                  <div class="space-y-4">
                    ${entity.entity_counts ? `
                    <div class="flex justify-between">
                      <span class="text-gray-600">Addresses</span>
                      <span class="font-semibold">${entity.entity_counts.addresses_count}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600">Relationships</span>
                      <span class="font-semibold">${entity.entity_counts.relationships_count}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600">Instruments</span>
                      <span class="font-semibold">${entity.entity_counts.instruments_count}</span>
                    </div>
                    ` : ''}
                    <div class="flex justify-between">
                      <span class="text-gray-600">Parent Entity</span>
                      <span class="font-semibold">${parentEntity ? 'Yes' : 'No'}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600">Subsidiaries</span>
                      <span class="font-semibold">${childEntities.length}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Status Indicators Card -->
              ${entity.status_indicators && entity.status_indicators.length > 0 ? `
              <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="p-6 border-b border-gray-200">
                  <h3 class="text-lg font-semibold text-gray-900">Status Indicators</h3>
                </div>
                <div class="p-6">
                  <div class="space-y-2">
                    ${entity.status_indicators.map(indicator => `
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      ${indicator}
                    </span>
                    `).join('')}
                  </div>
                </div>
              </div>
              ` : ''}

              <!-- Actions Card -->
              <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="p-6 border-b border-gray-200">
                  <h3 class="text-lg font-semibold text-gray-900">Actions</h3>
                </div>
                <div class="p-6 space-y-3">
                  <button class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    View Related Instruments
                  </button>
                  <button class="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors">
                    Export Entity Data
                  </button>
                  <button onclick="navigator.clipboard.writeText('${entity.lei}')" class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                    Copy LEI
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    this.setupEventListeners();
  }

  private showErrorState(message: string): void {
    this.container.innerHTML = `
      <div class="min-h-screen bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
            <svg class="mx-auto h-16 w-16 text-red-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 class="text-xl font-semibold text-gray-900 mb-2">Error Loading Entity</h2>
            <p class="text-gray-600 mb-4">${message}</p>
            <div class="space-x-3">
              <button id="back-btn" class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors">
                Go Back
              </button>
              <button id="view-entities-btn" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                View All Entities
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

    this.setupEventListeners();
  }
}