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
 * Entities Management Page
 * Legal entity relationships and LEI information with GLEIF integration
 */
export default class EntitiesPage extends BasePage {
  private legalEntityService = new LegalEntityService();
  private entities: LegalEntity[] = [];
  private currentPage = 1;
  private itemsPerPage = 10;
  private searchQuery = '';
  private totalCount = 0;
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      ${this.createSectionHeader('Entity Management', 'Legal entity relationships, hierarchies, and LEI information with GLEIF integration')}
      
      <!-- Search and Filter Bar -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <input 
              type="text" 
              id="entitySearch"
              placeholder="Search by LEI, entity name, or country..." 
              class="w-full border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value="${this.searchQuery}"
            >
          </div>
          <div class="flex gap-2">
            <select id="countryFilter" class="border border-gray-300 rounded-md px-3 py-2 bg-white">
              <option value="">All Countries</option>
              <option value="SE">Sweden</option>
              <option value="FI">Finland</option>
              <option value="NO">Norway</option>
              <option value="DK">Denmark</option>
              <option value="EE">Estonia</option>
              <option value="LV">Latvia</option>
              <option value="LT">Lithuania</option>
            </select>
            <button id="searchBtn" class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors">
              Search
            </button>
            <button id="clearBtn" class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 transition-colors">
              Clear
            </button>
          </div>
        </div>
      </div>

      <!-- Main Content Area -->
      <div class="grid grid-cols-1 gap-6">
        
        <!-- Entities List -->
        <div>
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="p-6 border-b border-gray-200">
              <div class="flex justify-between items-center">
                <h3 class="text-lg font-semibold text-gray-900">Legal Entities</h3>
                <div class="flex items-center space-x-2">
                  <span class="text-sm text-gray-600">Show:</span>
                  <select id="itemsPerPage" class="border border-gray-300 rounded px-2 py-1 text-sm">
                    <option value="10">10</option>
                    <option value="25">25</option>
                    <option value="50">50</option>
                  </select>
                </div>
              </div>
            </div>
            
            <!-- Loading State -->
            <div id="loadingState" class="p-8 text-center hidden">
              <div class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Loading entities...
              </div>
            </div>
            
            <!-- Entities Table -->
            <div id="entitiesTable" class="overflow-x-auto">
              <!-- Table will be populated by JavaScript -->
            </div>
            
            <!-- Pagination -->
            <div id="paginationContainer" class="p-4 border-t border-gray-200 bg-gray-50">
              <!-- Pagination will be populated by JavaScript -->
            </div>
          </div>
        </div>
      </div>
    `;

    this.attachEventListeners();
    await this.loadEntities();
  }

  private attachEventListeners(): void {
    // Search functionality
    const searchInput = document.getElementById('entitySearch') as HTMLInputElement;
    const searchBtn = document.getElementById('searchBtn') as HTMLButtonElement;
    const clearBtn = document.getElementById('clearBtn') as HTMLButtonElement;
    const countryFilter = document.getElementById('countryFilter') as HTMLSelectElement;
    const itemsPerPageSelect = document.getElementById('itemsPerPage') as HTMLSelectElement;

    if (searchInput) {
      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.performSearch();
        }
      });
    }

    if (searchBtn) {
      searchBtn.addEventListener('click', () => this.performSearch());
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => this.clearSearch());
    }

    if (countryFilter) {
      countryFilter.addEventListener('change', () => this.performSearch());
    }

    if (itemsPerPageSelect) {
      itemsPerPageSelect.addEventListener('change', (e) => {
        this.itemsPerPage = parseInt((e.target as HTMLSelectElement).value);
        this.currentPage = 1;
        this.loadEntities();
      });
    }
  }

  private async performSearch(): Promise<void> {
    const searchInput = document.getElementById('entitySearch') as HTMLInputElement;
    
    this.searchQuery = searchInput?.value.trim() || '';
    this.currentPage = 1;
    
    await this.loadEntities();
  }

  private async clearSearch(): Promise<void> {
    const searchInput = document.getElementById('entitySearch') as HTMLInputElement;
    const countryFilter = document.getElementById('countryFilter') as HTMLSelectElement;
    
    if (searchInput) searchInput.value = '';
    if (countryFilter) countryFilter.value = '';
    
    this.searchQuery = '';
    this.currentPage = 1;
    
    await this.loadEntities();
  }

  private async loadEntities(): Promise<void> {
    this.setLoadingState(true);
    
    try {
      const countryFilter = document.getElementById('countryFilter') as HTMLSelectElement;
      const jurisdiction = countryFilter?.value || '';
      
      const response = await this.legalEntityService.listEntities({
        search: this.searchQuery || undefined,
        country: jurisdiction || undefined
      }, {
        limit: this.itemsPerPage,
        offset: (this.currentPage - 1) * this.itemsPerPage
      });

      this.entities = response.data || [];
      this.totalCount = response.meta?.total || 0;
      
      this.renderEntitiesTable();
      this.renderPagination();
      this.updateStatistics();
      
    } catch (error) {
      console.error('Failed to load entities:', error);
      this.showError('Failed to load entities. Please try again.');
    } finally {
      this.setLoadingState(false);
    }
  }

  private setLoadingState(loading: boolean): void {
    const loadingElement = document.getElementById('loadingState');
    const tableElement = document.getElementById('entitiesTable');
    
    if (loadingElement && tableElement) {
      if (loading) {
        loadingElement.classList.remove('hidden');
        tableElement.innerHTML = '';
      } else {
        loadingElement.classList.add('hidden');
      }
    }
  }

  private renderEntitiesTable(): void {
    const tableContainer = document.getElementById('entitiesTable');
    if (!tableContainer) return;

    if (this.entities.length === 0) {
      tableContainer.innerHTML = `
        <div class="p-8 text-center text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No entities found</p>
          <p class="text-sm mt-1">Try adjusting your search criteria</p>
        </div>
      `;
      return;
    }

    const tableHTML = `
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">LEI</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Entity Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Jurisdiction</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Relationships</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          ${this.entities.map(entity => this.renderEntityRow(entity)).join('')}
        </tbody>
      </table>
    `;

    tableContainer.innerHTML = tableHTML;
    this.attachEntityRowListeners();
  }

  private renderEntityRow(entity: LegalEntity): string {
    const statusColor = entity.status === 'ACTIVE' ? 'text-green-600' : 'text-gray-500';
    const relationshipCount = (entity.relationships?.direct_children?.length || 0) + 
                            (entity.relationships?.direct_parent ? 1 : 0);
    
    return `
      <tr class="hover:bg-gray-50 cursor-pointer entity-row" data-lei="${entity.lei}">
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-mono text-gray-900">${entity.lei}</div>
        </td>
        <td class="px-6 py-4">
          <div class="text-sm font-medium text-gray-900">${entity.name}</div>
          ${entity.legal_form ? `<div class="text-xs text-gray-500">${entity.legal_form}</div>` : ''}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm text-gray-900">${entity.jurisdiction}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="text-sm ${statusColor}">${entity.status}</span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${relationshipCount > 0 ? `${relationshipCount} related` : 'None'}
        </td>
      </tr>
    `;
  }

  private attachEntityRowListeners(): void {
    const entityRows = document.querySelectorAll('.entity-row');
    entityRows.forEach(row => {
      row.addEventListener('click', async () => {
        const lei = row.getAttribute('data-lei');
        if (lei) {
          await this.selectEntity(lei);
        }
      });
    });
  }

  private async selectEntity(lei: string): Promise<void> {
    // Navigate to entity detail page
    window.location.hash = `#/entities/${lei}`;
  }

  private renderPagination(): void {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    const totalPages = Math.ceil(this.totalCount / this.itemsPerPage);
    const startItem = (this.currentPage - 1) * this.itemsPerPage + 1;
    const endItem = Math.min(this.currentPage * this.itemsPerPage, this.totalCount);

    if (totalPages <= 1) {
      paginationContainer.innerHTML = `
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-700">
            Showing ${this.totalCount} entities
          </div>
        </div>
      `;
      return;
    }

    const pagination = `
      <div class="flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Showing ${startItem} to ${endItem} of ${this.totalCount} entities
        </div>
        <div class="flex space-x-2">
          <button 
            id="prevPage" 
            class="px-3 py-1 border border-gray-300 rounded text-sm ${this.currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}"
            ${this.currentPage === 1 ? 'disabled' : ''}
          >
            Previous
          </button>
          
          <div class="flex space-x-1">
            ${this.renderPageNumbers(totalPages)}
          </div>
          
          <button 
            id="nextPage" 
            class="px-3 py-1 border border-gray-300 rounded text-sm ${this.currentPage === totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}"
            ${this.currentPage === totalPages ? 'disabled' : ''}
          >
            Next
          </button>
        </div>
      </div>
    `;

    paginationContainer.innerHTML = pagination;
    this.attachPaginationListeners();
  }

  private renderPageNumbers(totalPages: number): string {
    const pages: string[] = [];
    const showPages = 5;
    let startPage = Math.max(1, this.currentPage - Math.floor(showPages / 2));
    let endPage = Math.min(totalPages, startPage + showPages - 1);

    if (endPage - startPage < showPages - 1) {
      startPage = Math.max(1, endPage - showPages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(`
        <button 
          class="px-3 py-1 border border-gray-300 rounded text-sm page-btn ${i === this.currentPage ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}"
          data-page="${i}"
        >
          ${i}
        </button>
      `);
    }

    return pages.join('');
  }

  private attachPaginationListeners(): void {
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    const pageButtons = document.querySelectorAll('.page-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (this.currentPage > 1) {
          this.currentPage--;
          this.loadEntities();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(this.totalCount / this.itemsPerPage);
        if (this.currentPage < totalPages) {
          this.currentPage++;
          this.loadEntities();
        }
      });
    }

    pageButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const page = parseInt((e.target as HTMLElement).getAttribute('data-page') || '1');
        this.currentPage = page;
        this.loadEntities();
      });
    });
  }

  private updateStatistics(): void {
    // Statistics are now shown in the table header or could be added as a summary card
    console.log(`Loaded ${this.entities.length} entities of ${this.totalCount} total`);
  }

  protected showError(message: string): void {
    const tableContainer = document.getElementById('entitiesTable');
    if (tableContainer) {
      tableContainer.innerHTML = `
        <div class="p-8 text-center text-red-500">
          <svg class="mx-auto h-12 w-12 text-red-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="font-medium">${message}</p>
        </div>
      `;
    }
  }
}