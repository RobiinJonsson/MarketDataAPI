import { BasePage } from './BasePage';
import { ApiServiceFactory, InstrumentService, TransparencyService } from '../services';
import type { Instrument, TransparencyCalculation } from '../types/api';

interface CFIDecodeResult {
  cfi_code: string;
  category?: string;
  category_description?: string;
  group?: string;
  group_description?: string;
  description?: string;
  attributes?: string;
  decoded_attributes?: Record<string, string>;
}

interface InstrumentTypeCount {
  type: string;
  code: string;
  description: string;
  count: number;
}

/**
 * Enhanced Instruments Hub Page
 * Comprehensive instrument management with tabs for listing, CFI classification, and transparency
 */
export default class InstrumentsPage extends BasePage {
  private instrumentService: InstrumentService;
  private transparencyService: TransparencyService;
  
  // Current tab state
  private currentTab: 'listing' | 'cfi-classification' | 'transparency' = 'listing';
  
  // Listing tab state
  private currentFilters: {
    type?: string;
    currency?: string;
    search?: string;
  } = {};
  private availableTypes: string[] = [];
  
  // CFI Classification tab state
  private cfiCode: string = '';
  private cfiDecodeResult: CFIDecodeResult | null = null;
  private cfiSearchResults: Instrument[] = [];
  private selectedInstrumentType: string = '';
  private loading: boolean = false;
  private error: string | null = null;
  private totalRecords: number = 0;
  
  private cfiInstrumentTypes: InstrumentTypeCount[] = [
    { type: 'Equities', code: 'E', description: 'Shares, stocks, and equity-like securities', count: 0 },
    { type: 'Debt Securities', code: 'D', description: 'Bonds, notes, and other debt instruments', count: 0 },
    { type: 'Collective Investment', code: 'C', description: 'Funds, ETFs, and investment vehicles', count: 0 },
    { type: 'Futures', code: 'F', description: 'Future contracts and forwards', count: 0 },
    { type: 'Options', code: 'O', description: 'Option contracts', count: 0 },
    { type: 'Swaps', code: 'S', description: 'Swap agreements', count: 0 },
    { type: 'Rights', code: 'R', description: 'Rights and warrants', count: 0 },
    { type: 'Structured Products', code: 'H', description: 'Structured and hybrid products', count: 0 },
    { type: 'Interest Rate', code: 'I', description: 'Interest rate instruments', count: 0 },
    { type: 'Commodities', code: 'J', description: 'Commodity-based instruments', count: 0 },
  ];
  
  // Transparency tab state
  private transparencyCalculations: TransparencyCalculation[] = [];
  private allTransparencyCalculations: TransparencyCalculation[] = [];
  private transparencyTotalFromAPI: number = 0;
  private transparencyStats: { total: number; equity: number; nonEquity: number; liquid: number } = {
    total: 0,
    equity: 0,
    nonEquity: 0,
    liquid: 0
  };
  private transparencyFilters: any = {};

  // Pagination state for both tabs
  private instrumentsCurrentPage = 1;
  private instrumentsItemsPerPage = 25;
  private instrumentsTotalCount = 0;
  private instruments: Instrument[] = [];
  
  private transparencyCurrentPage = 1;
  private transparencyItemsPerPage = 25;
  private transparencyTotalCount = 0;

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    super(container, params);
    this.instrumentService = ApiServiceFactory.getInstance().instruments;
    this.transparencyService = ApiServiceFactory.getInstance().transparency;
    
    // Set initial tab from URL parameter
    if (params.tab) {
      const validTabs: Array<'listing' | 'cfi-classification' | 'transparency'> = ['listing', 'cfi-classification', 'transparency'];
      if (validTabs.includes(params.tab as any)) {
        this.currentTab = params.tab as 'listing' | 'cfi-classification' | 'transparency';
        console.log('Setting initial tab from URL parameter:', this.currentTab);
      }
    }
  }
  
  async render(): Promise<void> {
    await this.loadInstrumentTypeCounts();
    this.updateUI();
    
    // Load data for the initial tab
    this.loadTabData(this.currentTab);
  }

  private loadTabData(tab: 'listing' | 'cfi-classification' | 'transparency'): void {
    if (tab === 'listing') {
      // Load instruments for listing tab
      this.loadInstrumentsPaginated();
    } else if (tab === 'transparency') {
      // Load transparency data using new paginated approach
      this.transparencyCurrentPage = 1;
      this.transparencyFilters = {};
      this.loadTransparencyPaginated();
    }
    // CFI classification tab loads data on demand when user interacts with it
  }

  private async loadInstrumentTypeCounts(): Promise<void> {
    try {
      this.loading = true;
      this.error = null;
      
      // Load counts efficiently from stats endpoint in a single API call
      const statsResponse = await this.instrumentService.getInstrumentStats();
      const cfiTypeBreakdown = statsResponse.data.cfi_type_breakdown || {};
      
      // Update counts using the stats response
      this.cfiInstrumentTypes = this.cfiInstrumentTypes.map(type => ({
        ...type,
        count: cfiTypeBreakdown[type.code] || 0
      }));
      
    } catch (error) {
      console.error('Error loading instrument type counts:', error);
      this.error = 'Failed to load instrument statistics';
    } finally {
      this.loading = false;
    }
  }

  private updateUI(): void {
    this.container.innerHTML = this.renderContent();
    this.setupEventListeners();
    
    // Load initial data for the current tab
    if (this.currentTab === 'listing') {
      this.loadInstrumentTypes();
      this.loadInstrumentsPaginated();
    }
  }

  private renderContent(): string {
    return `
      ${this.createSectionHeader('Instruments Hub', 'Comprehensive instrument management with CFI classification and transparency analysis')}
      
      <!-- Tab Navigation -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button
            class="tab-button ${this.currentTab === 'listing' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'} whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
            data-tab="listing"
          >
            Instruments Listing
          </button>
          <button
            class="tab-button ${this.currentTab === 'cfi-classification' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'} whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
            data-tab="cfi-classification"
          >
            CFI Classification
          </button>
          <button
            class="tab-button ${this.currentTab === 'transparency' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'} whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
            data-tab="transparency"
          >
            Transparency
          </button>
        </nav>
      </div>

      ${this.error ? `
        <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p class="text-red-800">${this.error}</p>
        </div>
      ` : ''}

      <!-- Tab Content -->
      ${this.renderTabContent()}
    `;
  }

  private renderTabContent(): string {
    switch (this.currentTab) {
      case 'listing':
        return this.renderListingTab();
      case 'cfi-classification':
        return this.renderCFIClassificationTab();
      case 'transparency':
        return this.renderTransparencyTab();
      default:
        return this.renderListingTab();
    }
  }

  private renderListingTab(): string {
    return `
      <!-- Search and Filter Bar -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Instrument Type</label>
            <select id="instruments-type-filter" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">All Types</option>
              <!-- Types will be populated dynamically -->
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Currency</label>
            <select id="instruments-currency-filter" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">All Currencies</option>
              <option value="EUR">EUR</option>
              <option value="USD">USD</option>
              <option value="GBP">GBP</option>
              <option value="SEK">SEK</option>
              <option value="NOK">NOK</option>
              <option value="DKK">DKK</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Search ISIN</label>
            <input id="instruments-isin-filter" type="text" placeholder="e.g. SE0000242455" class="w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          <div class="flex items-end">
            <button id="instruments-search-btn" class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
              Search
            </button>
          </div>
        </div>
      </div>

      <!-- Instruments Table -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="p-6 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-900">Instruments</h3>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">Show:</span>
              <select id="instruments-items-per-page" class="border border-gray-300 rounded px-2 py-1 text-sm">
                <option value="10">10</option>
                <option value="25" selected>25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Loading State -->
        <div id="instruments-loading" class="p-8 text-center hidden">
          <div class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading instruments...
          </div>
        </div>
        
        <!-- Instruments Table -->
        <div id="instruments-table" class="overflow-x-auto">
          <!-- Table will be populated by JavaScript -->
        </div>
        
        <!-- Pagination -->
        <div id="instruments-pagination" class="p-4 border-t border-gray-200 bg-gray-50">
          <!-- Pagination will be populated by JavaScript -->
        </div>
      </div>
    `;
  }

  private renderCFIClassificationTab(): string {
    return `
      <div class="space-y-6">
        
        <!-- CFI Code Lookup Section -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h2 class="text-xl font-semibold mb-4">CFI Code Lookup</h2>
          
          <div class="flex gap-4 mb-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-2">CFI Code (6 characters)</label>
              <input
                type="text"
                id="cfi-input"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., ESVUFR"
                maxlength="6"
                value="${this.cfiCode}"
              />
            </div>
            <button
              id="cfi-lookup-btn"
              class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 ${this.loading ? 'opacity-50 cursor-not-allowed' : ''}"
              ${this.loading ? 'disabled' : ''}
            >
              ${this.loading ? 'Decoding...' : 'Decode CFI'}
            </button>
          </div>

          ${this.cfiDecodeResult ? `
            <div class="bg-gray-50 p-4 rounded-md">
              <h3 class="font-medium mb-2">CFI Classification: ${this.cfiDecodeResult.cfi_code}</h3>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="font-medium">Category:</span> ${this.cfiDecodeResult.category || 'N/A'}
                  ${this.cfiDecodeResult.category_description ? `<br><span class="text-gray-500 text-xs">${this.cfiDecodeResult.category_description}</span>` : ''}
                </div>
                <div>
                  <span class="font-medium">Group:</span> ${this.cfiDecodeResult.group || 'N/A'}
                  ${this.cfiDecodeResult.group_description ? `<br><span class="text-gray-500 text-xs">${this.cfiDecodeResult.group_description}</span>` : ''}
                </div>
                <div class="col-span-2">
                  <span class="font-medium">Description:</span> ${
                    this.cfiDecodeResult.description || 
                    (this.cfiDecodeResult.category_description && this.cfiDecodeResult.group_description ? 
                      `${this.cfiDecodeResult.category_description} - ${this.cfiDecodeResult.group_description}` : 
                      'N/A')
                  }
                </div>
                ${(this.cfiDecodeResult as any).decoded_attributes && Object.keys((this.cfiDecodeResult as any).decoded_attributes).length > 0 ? `
                  <div class="col-span-2">
                    <span class="font-medium">Decoded Attributes:</span>
                    <ul class="mt-1 space-y-1">
                      ${Object.entries((this.cfiDecodeResult as any).decoded_attributes).map(([key, value]) => `
                        <li class="text-gray-600">• <span class="capitalize">${key.replace(/_/g, ' ')}</span>: ${value}</li>
                      `).join('')}
                    </ul>
                  </div>
                ` : this.cfiDecodeResult.attributes ? `
                  <div class="col-span-2">
                    <span class="font-medium">Raw Attributes:</span>
                    <div class="text-gray-600 font-mono text-sm">${this.cfiDecodeResult.attributes}</div>
                  </div>
                ` : ''}
              </div>
            </div>
          ` : ''}
        </div>

        <!-- Instrument Type Categories -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h2 class="text-xl font-semibold mb-4">Instrument Categories</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            ${this.cfiInstrumentTypes.map((type: InstrumentTypeCount) => `
              <div 
                class="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer ${this.selectedInstrumentType === type.type ? 'ring-2 ring-blue-500 bg-blue-50' : ''}"
                data-instrument-type="${type.type}" data-instrument-code="${type.code}"
              >
                <div class="flex items-center justify-between mb-2">
                  <h3 class="font-medium text-gray-900">${type.type}</h3>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ${type.code}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">${type.description}</p>
                <div class="text-lg font-bold text-blue-600">${type.count.toLocaleString()}</div>
                <div class="text-xs text-gray-500">instruments</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- CFI Search Results -->
        ${this.cfiSearchResults.length > 0 ? `
          <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold mb-4">
              ${this.selectedInstrumentType ? `${this.selectedInstrumentType} Instruments` : 'CFI Search Results'}
              <span class="text-sm font-normal text-gray-500 ml-2">(${this.totalRecords.toLocaleString()} total)</span>
            </h2>
            
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISIN</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CFI Code</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Currency</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Market</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  ${this.cfiSearchResults.map((instrument: Instrument) => `
                    <tr class="hover:bg-gray-50">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                        <a href="#/instruments/${instrument.isin}" class="hover:underline">${instrument.isin}</a>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.short_name || 'N/A'}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          ${instrument.cfi_code || 'N/A'}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.currency || 'N/A'}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.market || 'N/A'}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }

  private renderTransparencyTab(): string {
    return `
      <div class="space-y-6">
        
        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-gradient-to-r from-indigo-500 to-indigo-600 text-white p-6 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-indigo-100">Total Calculations</p>
                <p class="text-2xl font-bold" id="total-calculations">Loading...</p>
              </div>
              <svg class="w-8 h-8 text-indigo-200" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-blue-100">FULECR Files (Equity)</p>
                <p class="text-2xl font-bold" id="equity-calculations">Loading...</p>
              </div>
              <svg class="w-8 h-8 text-blue-200" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-purple-100">FULNCR Files (Non-Equity)</p>
                <p class="text-2xl font-bold" id="non-equity-calculations">Loading...</p>
              </div>
              <svg class="w-8 h-8 text-purple-200" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
              </svg>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-lg shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-green-100">Active Trading</p>
                <p class="text-2xl font-bold" id="liquid-calculations">Loading...</p>
              </div>
              <svg class="w-8 h-8 text-green-200" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <!-- Transparency Filters -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h2 class="text-xl font-semibold mb-4">Transparency Filters</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">FIRDS File Type</label>
              <select
                id="transparency-file-type"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All File Types</option>
                <option value="FULECR_E">Equity (FULECR_E)</option>
                <option value="FULECR_C">Collective Investment (FULECR_C)</option>
                <option value="FULECR_R">Rights (FULECR_R)</option>
                <option value="FULNCR_D">Debt (FULNCR_D)</option>
                <option value="FULNCR_F">Futures (FULNCR_F)</option>
                <option value="FULNCR_O">Options (FULNCR_O)</option>
                <option value="FULNCR_S">Swaps (FULNCR_S)</option>
                <option value="FULNCR_J">Warrants (FULNCR_J)</option>
                <option value="FULNCR_H">Structured (FULNCR_H)</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Instrument Type</label>
              <select
                id="transparency-instrument-type"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Instrument Types</option>
                <option value="SHRS">Shares (SHRS)</option>
                <option value="BOND">Bonds (BOND)</option>
                <option value="DERV">Derivatives (DERV)</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Trading Activity</label>
              <select
                id="transparency-activity"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Activity Levels</option>
                <option value="active">Active Trading</option>
                <option value="inactive">No Trading</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Search ISIN</label>
              <input
                id="transparency-isin-search"
                type="text"
                placeholder="e.g. SE0000108656"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div class="mt-4 flex gap-2">
            <button
              id="apply-transparency-filters"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Apply Filters
            </button>
            <button
              id="clear-transparency-filters"
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Clear Filters
            </button>
          </div>
        </div>

        <!-- Transparency Results -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="p-6 border-b border-gray-200">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-semibold text-gray-900">Transparency Calculations</h3>
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-600">Show:</span>
                <select id="transparency-items-per-page" class="border border-gray-300 rounded px-2 py-1 text-sm">
                  <option value="10">10</option>
                  <option value="25" selected>25</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                </select>
              </div>
            </div>
          </div>
          
          <!-- Loading State -->
          <div id="transparency-loading" class="p-8 text-center hidden">
            <div class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading transparency calculations...
            </div>
          </div>
          
          <!-- Transparency Table -->
          <div id="transparency-table" class="overflow-x-auto">
            <!-- Table will be populated by JavaScript -->
          </div>
          
          <!-- Pagination -->
          <div id="transparency-pagination" class="p-4 border-t border-gray-200 bg-gray-50">
            <!-- Pagination will be populated by JavaScript -->
          </div>
        </div>
      </div>
    `;
  }

  private setupEventListeners(): void {
    // Tab switching
    const tabButtons = this.container.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        const tab = target.getAttribute('data-tab') as 'listing' | 'cfi-classification' | 'transparency';
        if (tab) {
          this.handleTabSwitch(tab);
        }
      });
    });

    // Instruments listing tab event listeners
    const instrumentsSearchBtn = this.container.querySelector('#instruments-search-btn') as HTMLButtonElement;
    const instrumentsItemsPerPageSelect = this.container.querySelector('#instruments-items-per-page') as HTMLSelectElement;
    
    if (instrumentsSearchBtn) {
      instrumentsSearchBtn.addEventListener('click', () => {
        this.updateInstrumentsFiltersFromForm();
        this.instrumentsCurrentPage = 1;
        this.loadInstrumentsPaginated();
      });
    }
    
    if (instrumentsItemsPerPageSelect) {
      instrumentsItemsPerPageSelect.addEventListener('change', (e) => {
        this.instrumentsItemsPerPage = parseInt((e.target as HTMLSelectElement).value);
        this.instrumentsCurrentPage = 1;
        this.loadInstrumentsPaginated();
      });
    }

    // CFI Classification tab event listeners
    const cfiInput = this.container.querySelector('#cfi-input') as HTMLInputElement;
    const cfiLookupBtn = this.container.querySelector('#cfi-lookup-btn') as HTMLButtonElement;
    
    if (cfiInput) {
      cfiInput.addEventListener('input', (e) => {
        const target = e.target as HTMLInputElement;
        this.cfiCode = target.value.toUpperCase();
      });
      
      cfiInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.handleCFICodeLookup();
        }
      });
    }
    
    if (cfiLookupBtn) {
      cfiLookupBtn.addEventListener('click', () => {
        this.handleCFICodeLookup();
      });
    }

    // CFI instrument type cards
    const instrumentTypeCards = this.container.querySelectorAll('[data-instrument-type]');
    instrumentTypeCards.forEach(card => {
      card.addEventListener('click', () => {
        const type = card.getAttribute('data-instrument-type') || '';
        const code = card.getAttribute('data-instrument-code') || '';
        this.handleInstrumentTypeSelect({ type, code, description: '', count: 0 });
      });
    });

    // Transparency tab event listeners
    const applyTransparencyBtn = this.container.querySelector('#apply-transparency-filters') as HTMLButtonElement;
    const clearTransparencyBtn = this.container.querySelector('#clear-transparency-filters') as HTMLButtonElement;
    
    if (applyTransparencyBtn) {
      applyTransparencyBtn.addEventListener('click', () => {
        this.handleApplyTransparencyFilters();
      });
    }
    
    if (clearTransparencyBtn) {
      clearTransparencyBtn.addEventListener('click', () => {
        // Clear form fields
        const fileTypeSelect = this.container.querySelector('#transparency-file-type') as HTMLSelectElement;
        const instrumentTypeSelect = this.container.querySelector('#transparency-instrument-type') as HTMLSelectElement;
        const activitySelect = this.container.querySelector('#transparency-activity') as HTMLSelectElement;
        const isinInput = this.container.querySelector('#transparency-isin-search') as HTMLInputElement;
        
        if (fileTypeSelect) fileTypeSelect.value = '';
        if (instrumentTypeSelect) instrumentTypeSelect.value = '';
        if (activitySelect) activitySelect.value = '';
        if (isinInput) isinInput.value = '';
        
        // Clear filters and reload data
        this.transparencyFilters = {};
        this.transparencyCurrentPage = 1;
        this.loadTransparencyPaginated();
      });
    }

    // Transparency pagination event listeners
    const transparencyItemsPerPageSelect = this.container.querySelector('#transparency-items-per-page') as HTMLSelectElement;
    
    if (transparencyItemsPerPageSelect) {
      transparencyItemsPerPageSelect.addEventListener('change', (e) => {
        this.transparencyItemsPerPage = parseInt((e.target as HTMLSelectElement).value);
        this.transparencyCurrentPage = 1;
        this.loadTransparencyPaginated();
      });
    }
  }

  private updateInstrumentsFiltersFromForm(): void {
    const typeSelect = this.container.querySelector('#instruments-type-filter') as HTMLSelectElement;
    const currencySelect = this.container.querySelector('#instruments-currency-filter') as HTMLSelectElement;
    const isinInput = this.container.querySelector('#instruments-isin-filter') as HTMLInputElement;

    this.currentFilters = {
      type: typeSelect?.value || undefined,
      currency: currencySelect?.value || undefined,
      search: isinInput?.value?.trim() || undefined,
    };
    
    console.log('Updated instruments filters:', this.currentFilters);
  }



  private async selectInstrument(isin: string): Promise<void> {
    // Navigate to instrument detail page
    window.location.hash = `#/instruments/${isin}`;
  }

  private showInstrumentError(message: string): void {
    const tbody = this.container.querySelector('#instruments-tbody');
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="px-6 py-8 text-center text-red-500">
            <div class="flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              ${message}
            </div>
          </td>
        </tr>
      `;
    }
  }

  // Tab and event handlers
  private handleTabSwitch(tab: 'listing' | 'cfi-classification' | 'transparency'): void {
    this.currentTab = tab;
    this.error = null;
    this.cfiSearchResults = [];
    this.selectedInstrumentType = '';
    
    if (tab === 'listing') {
      // Load instruments for listing tab
      this.loadInstrumentsPaginated();
    } else if (tab === 'transparency') {
      // Load transparency data using new paginated approach
      this.transparencyCurrentPage = 1;
      this.transparencyFilters = {};
      this.loadTransparencyPaginated();
    }
    
    this.updateUI();
  }

  private async handleCFICodeLookup(): Promise<void> {
    if (!this.cfiCode || this.cfiCode.length < 6) {
      this.error = 'CFI code must be 6 characters long';
      this.updateUI();
      return;
    }

    try {
      this.loading = true;
      this.error = null;
      this.updateUI();
      
      // Decode CFI code
      const decodeResponse = await this.instrumentService.decodeCfi(this.cfiCode);
      
      if (decodeResponse.status === 'success' && decodeResponse.data) {
        this.cfiDecodeResult = decodeResponse.data;
        
        // Search for instruments with this CFI code
        const filters = { cfi_code: this.cfiCode };
        const searchResponse = await this.instrumentService.listInstruments(filters, { page: 1, per_page: 10 });
        
        this.cfiSearchResults = searchResponse.data || [];
      } else {
        this.error = decodeResponse.message || 'Invalid CFI code';
      }
      
    } catch (error) {
      console.error('Error decoding CFI code:', error);
      this.error = 'Failed to decode CFI code';
    } finally {
      this.loading = false;
      this.updateUI();
    }
  }

  private async handleInstrumentTypeSelect(instrumentType: InstrumentTypeCount): Promise<void> {
    try {
      this.loading = true;
      this.error = null;
      this.selectedInstrumentType = instrumentType.type;
      this.cfiSearchResults = [];
      this.updateUI();
      
      const filters = { cfi_type: instrumentType.code };
      const response = await this.instrumentService.listInstruments(filters, { page: 1, per_page: 20 });
      
      if (response.status === 'success' && response.data) {
        this.cfiSearchResults = response.data;
        this.totalRecords = response.meta?.total || 0;
      }
      
    } catch (error) {
      console.error('Error loading instruments by type:', error);
      this.error = `Failed to load ${instrumentType.type} instruments`;
    } finally {
      this.loading = false;
      this.updateUI();
    }
  }

  private async handleLoadTransparencyData(): Promise<void> {
    try {
      this.loading = true;
      this.error = null;
      this.updateUI();
      
      console.log('Loading all transparency data...');
      
      // Get statistics with separate lightweight API calls (like HomePage approach)
      const [totalResponse, equityResponse, nonEquityResponse] = await Promise.allSettled([
        this.transparencyService.getTransparencyCalculations({ page: 1, per_page: 1 }, { timeout: 30000 }),
        this.transparencyService.getTransparencyCalculations({ page: 1, per_page: 1, file_type: 'FULECR' }, { timeout: 30000 }),
        this.transparencyService.getTransparencyCalculations({ page: 1, per_page: 1, file_type: 'FULNCR' }, { timeout: 30000 })
      ]);
      
      // Store statistics from API metadata
      if (totalResponse.status === 'fulfilled' && totalResponse.value.status === 'success' && totalResponse.value.data) {
        this.transparencyTotalFromAPI = totalResponse.value.data.pagination.total;
        console.log('Total calculations:', this.transparencyTotalFromAPI);
      }
      
      let equityTotal = 0;
      if (equityResponse.status === 'fulfilled' && equityResponse.value.status === 'success' && equityResponse.value.data) {
        equityTotal = equityResponse.value.data.pagination.total;
        console.log('Equity calculations:', equityTotal);
      }
      
      let nonEquityTotal = 0;
      if (nonEquityResponse.status === 'fulfilled' && nonEquityResponse.value.status === 'success' && nonEquityResponse.value.data) {
        nonEquityTotal = nonEquityResponse.value.data.pagination.total;
        console.log('Non-equity calculations:', nonEquityTotal);
      }
      
      // Store the statistics for later use
      this.transparencyStats = {
        total: this.transparencyTotalFromAPI,
        equity: equityTotal,
        nonEquity: nonEquityTotal,
        liquid: 0 // We'll calculate this from loaded data as it requires field inspection
      };
      
      if (this.transparencyTotalFromAPI > 0) {
        const totalPages = Math.ceil(this.transparencyTotalFromAPI / 100);
        
        console.log(`Found ${this.transparencyTotalFromAPI} total calculations across ${totalPages} pages`);          // Now load all data efficiently
          const firstResponse = await this.transparencyService.getTransparencyCalculations(
            { page: 1, per_page: 100 },
            { timeout: 30000 }
          );
          
          if (firstResponse.status === 'success' && firstResponse.data) {
            let allCalculations = [...firstResponse.data.calculations];
            let successfullyLoadedPages = 1;

            // Store initial data and show immediately
            this.allTransparencyCalculations = [...allCalculations];
            this.applyTransparencyFilters();
            this.updateUI();
            console.log(`Showing initial page 1 with ${this.transparencyCalculations.length} calculations`);

            // Load remaining pages in background if needed
            if (totalPages > 1) {
              this.loadRemainingTransparencyPages(allCalculations, totalPages, successfullyLoadedPages);
            }
          }
        }
      } catch (error) {
      console.error('Error loading transparency data:', error);
      this.error = 'Failed to load transparency calculations';
      this.transparencyCalculations = [];
      this.allTransparencyCalculations = [];
      this.transparencyTotalFromAPI = 0;
    } finally {
      this.loading = false;
      this.updateUI();
      // Update statistics after UI is rendered - always do this for transparency tab
      if (this.currentTab === 'transparency') {
        setTimeout(() => this.updateTransparencyStatistics(), 200);
      }
    }
  }

  private applyTransparencyFilters(): void {
    if (!this.allTransparencyCalculations) {
      return;
    }

    let calculations = [...this.allTransparencyCalculations];
    
    // Apply client-side filtering
    if (this.transparencyFilters.file_type) {
      calculations = calculations.filter(calc => 
        calc.file_type === this.transparencyFilters.file_type
      );
    }
    
    if (this.transparencyFilters.instrument_type) {
      calculations = calculations.filter(calc => 
        calc.instrument_type === this.transparencyFilters.instrument_type
      );
    }
    
    if (this.transparencyFilters.activity) {
      if (this.transparencyFilters.activity === 'active') {
        calculations = calculations.filter(calc => 
          calc.transparency_analysis?.has_trading_activity === true
        );
      } else if (this.transparencyFilters.activity === 'inactive') {
        calculations = calculations.filter(calc => 
          calc.transparency_analysis?.has_trading_activity === false
        );
      }
    }
    
    if (this.transparencyFilters.isin) {
      calculations = calculations.filter(calc => 
        calc.isin?.toLowerCase().includes(this.transparencyFilters.isin.toLowerCase())
      );
    }
    
    this.transparencyCalculations = calculations;
    this.totalRecords = calculations.length;
    
    console.log('Applied filters:', this.transparencyFilters);
    console.log('Filtered results:', calculations.length, 'of', this.allTransparencyCalculations.length);
  }

  private async loadRemainingTransparencyPages(allCalculations: TransparencyCalculation[], totalPages: number, successfullyLoadedPages: number): Promise<void> {
    console.log(`Loading remaining ${totalPages - 1} pages in background...`);
    
    for (let page = 2; page <= totalPages; page++) {
      try {
        console.log(`Background loading page ${page} of ${totalPages}...`);
        
        const pageResponse = await this.transparencyService.getTransparencyCalculations(
          { page, per_page: 100 },
          { timeout: 30000 }
        );
        
        if (pageResponse.status === 'success' && pageResponse.data) {
          // Add new data to existing calculations
          allCalculations.push(...pageResponse.data.calculations);
          this.allTransparencyCalculations = [...allCalculations];
          
          // Reapply filters and update UI with new data
          this.applyTransparencyFilters();
          this.updateUI();
          
          successfullyLoadedPages++;
          console.log(`Background loaded page ${page}: ${pageResponse.data.calculations.length} calculations (total: ${this.allTransparencyCalculations.length})`);
        } else {
          console.error(`Failed to background load page ${page}:`, pageResponse);
        }
        
        // Small delay between requests
        if (page < totalPages) {
          await new Promise(resolve => setTimeout(resolve, 200));
        }
        
      } catch (error) {
        console.error(`Error background loading page ${page}:`, error);
        // Continue with next page on error
      }
    }
    
    console.log(`Background loading complete: ${successfullyLoadedPages}/${totalPages} pages loaded with ${this.allTransparencyCalculations.length} total calculations`);
  }

  private hasActiveTransparencyFilters(): boolean {
    return !!(
      this.transparencyFilters.file_type || 
      this.transparencyFilters.instrument_type || 
      this.transparencyFilters.activity || 
      this.transparencyFilters.isin
    );
  }

  private updateTransparencyStatistics(): void {
    // Only update if we're on transparency tab
    if (this.currentTab !== 'transparency') {
      console.log('Skipping transparency stats update - not on transparency tab');
      return;
    }
    
    const filtersActive = this.hasActiveTransparencyFilters();
    console.log('Updating transparency statistics with', this.transparencyCalculations.length, 'calculations, filters active:', filtersActive);
    
    const totalElement = this.container.querySelector('#total-calculations');
    const equityElement = this.container.querySelector('#equity-calculations');
    const nonEquityElement = this.container.querySelector('#non-equity-calculations');  
    const liquidElement = this.container.querySelector('#liquid-calculations');
    
    console.log('Found DOM elements:', { 
      total: !!totalElement,
      equity: !!equityElement, 
      nonEquity: !!nonEquityElement, 
      liquid: !!liquidElement,
      containerExists: !!this.container
    });
    
    if (totalElement) {
      // If filters are active, show filtered count; otherwise use full dataset stats
      const totalCount = filtersActive ? 
        this.transparencyTotalCount : 
        this.transparencyStats.total;
      totalElement.textContent = new Intl.NumberFormat('en-US').format(totalCount);
      console.log('Updated total count:', totalCount, '(filters active:', filtersActive, ', full dataset total:', this.transparencyStats.total, ', filtered total:', this.transparencyTotalCount, ')');
    } else {
      console.log('total-calculations element not found');
    }
    
    if (equityElement) {
      // If filters are active, use filtered data; otherwise use pre-calculated stats
      const equityCount = filtersActive ? 
        this.transparencyCalculations.filter(c => c.file_type?.includes('FULECR')).length :
        (this.transparencyStats.equity > 0 ? this.transparencyStats.equity : this.transparencyCalculations.filter(c => c.file_type?.includes('FULECR')).length);
      equityElement.textContent = new Intl.NumberFormat('en-US').format(equityCount);
      console.log('Updated equity count:', equityCount, '(filters active:', filtersActive, ', from pre-calc:', this.transparencyStats.equity, ', filtered:', this.transparencyCalculations.filter(c => c.file_type?.includes('FULECR')).length, ')');
    } else {
      console.log('equity-calculations element not found');
    }
    
    if (nonEquityElement) {
      // If filters are active, use filtered data; otherwise use pre-calculated stats
      const nonEquityCount = filtersActive ? 
        this.transparencyCalculations.filter(c => c.file_type?.includes('FULNCR')).length :
        (this.transparencyStats.nonEquity > 0 ? this.transparencyStats.nonEquity : this.transparencyCalculations.filter(c => c.file_type?.includes('FULNCR')).length);
      nonEquityElement.textContent = new Intl.NumberFormat('en-US').format(nonEquityCount);
      console.log('Updated non-equity count:', nonEquityCount, '(filters active:', filtersActive, ', from pre-calc:', this.transparencyStats.nonEquity, ', filtered:', this.transparencyCalculations.filter(c => c.file_type?.includes('FULNCR')).length, ')');
    } else {
      console.log('non-equity-calculations element not found');
    }
    
    if (liquidElement) {
      // Active Trading always uses filtered data since it's dynamic
      const liquidCount = this.transparencyCalculations.filter(c => c.transparency_analysis?.has_trading_activity).length;
      liquidElement.textContent = new Intl.NumberFormat('en-US').format(liquidCount);
      console.log('Updated liquid count:', liquidCount);
    } else {
      console.log('liquid-calculations element not found');
    }
  }

  private handleApplyTransparencyFilters(): void {
    // Get filter values from form
    const fileTypeSelect = this.container.querySelector('#transparency-file-type') as HTMLSelectElement;
    const instrumentTypeSelect = this.container.querySelector('#transparency-instrument-type') as HTMLSelectElement;
    const activitySelect = this.container.querySelector('#transparency-activity') as HTMLSelectElement;
    const isinInput = this.container.querySelector('#transparency-isin-search') as HTMLInputElement;
    
    // Update internal filter state
    this.transparencyFilters = {
      file_type: fileTypeSelect?.value || undefined,
      instrument_type: instrumentTypeSelect?.value || undefined,
      activity: activitySelect?.value || undefined,
      isin: isinInput?.value?.trim() || undefined
    };
    
    // Reset to first page and load with filters
    this.transparencyCurrentPage = 1;
    this.loadTransparencyPaginated();
  }

  private async loadInstrumentTypes(): Promise<void> {
    try {
      const response = await this.instrumentService.getInstrumentTypes();
      if (response.status === 'success' && response.data?.instrument_types) {
        this.availableTypes = response.data.instrument_types;
        this.populateTypeDropdown();
      }
    } catch (error) {
      console.error('Error loading instrument types:', error);
      // Fallback to default types
      this.availableTypes = ['equity', 'debt', 'future', 'option'];
      this.populateTypeDropdown();
    }
  }

  private populateTypeDropdown(): void {
    const typeSelect = this.container.querySelector('#instruments-type-filter') as HTMLSelectElement;
    if (!typeSelect) {
      console.warn('instruments-type-filter element not found');
      return;
    }

    // Clear existing options except "All Types"
    typeSelect.innerHTML = '<option value="">All Types</option>';

    // Add available types
    this.availableTypes.forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = this.formatInstrumentType(type);
      typeSelect.appendChild(option);
    });
    
    console.log('Populated type dropdown with', this.availableTypes.length, 'types:', this.availableTypes);
  }

  // Instruments listing pagination methods
  private async loadInstrumentsPaginated(): Promise<void> {
    this.setInstrumentsLoadingState(true);
    
    try {
      console.log('Loading instruments with filters:', this.currentFilters);
      const response = await this.instrumentService.listInstruments(
        this.currentFilters,
        { 
          page: this.instrumentsCurrentPage, 
          per_page: this.instrumentsItemsPerPage 
        }
      );

      console.log('Instruments API response:', response);
      console.log('Total count:', response.meta?.total);
      console.log('Returned instruments:', response.data?.length);

      this.instruments = response.data || [];
      this.instrumentsTotalCount = response.meta?.total || 0;
      
      this.renderInstrumentsTable();
      this.renderInstrumentsPagination();
      
    } catch (error) {
      console.error('Failed to load instruments:', error);
      this.showInstrumentsError('Failed to load instruments. Please try again.');
    } finally {
      this.setInstrumentsLoadingState(false);
    }
  }

  private setInstrumentsLoadingState(loading: boolean): void {
    const loadingElement = this.container.querySelector('#instruments-loading');
    const tableElement = this.container.querySelector('#instruments-table');
    
    if (loadingElement && tableElement) {
      if (loading) {
        loadingElement.classList.remove('hidden');
        tableElement.innerHTML = '';
      } else {
        loadingElement.classList.add('hidden');
      }
    }
  }

  private renderInstrumentsTable(): void {
    const tableContainer = this.container.querySelector('#instruments-table');
    if (!tableContainer) return;

    if (this.instruments.length === 0) {
      tableContainer.innerHTML = `
        <div class="p-8 text-center text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No instruments found</p>
          <p class="text-sm mt-1">Try adjusting your search criteria</p>
        </div>
      `;
      return;
    }

    const tableHTML = `
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISIN</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CFI Code</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Currency</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Authority</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trading Venue</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          ${this.instruments.map(instrument => this.renderInstrumentRow(instrument)).join('')}
        </tbody>
      </table>
    `;

    tableContainer.innerHTML = tableHTML;
  }

  private renderInstrumentRow(instrument: Instrument): string {
    return `
      <tr class="hover:bg-gray-50 cursor-pointer" onclick="window.location.hash = '#/instruments/${instrument.isin}'">
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-mono text-blue-600">${instrument.isin}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${this.getTypeColor(instrument.instrument_type)}">
            ${this.formatInstrumentType(instrument.instrument_type)}
          </span>
        </td>
        <td class="px-6 py-4">
          <div class="text-sm font-medium text-gray-900">${instrument.short_name || 'N/A'}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-mono text-gray-900">${instrument.cfi_code || 'N/A'}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.currency || 'N/A'}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.competent_authority || 'N/A'}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.relevant_trading_venue || 'N/A'}</td>
      </tr>
    `;
  }

  private renderInstrumentsPagination(): void {
    const paginationContainer = this.container.querySelector('#instruments-pagination');
    if (!paginationContainer) return;

    const totalPages = Math.ceil(this.instrumentsTotalCount / this.instrumentsItemsPerPage);
    const startItem = (this.instrumentsCurrentPage - 1) * this.instrumentsItemsPerPage + 1;
    const endItem = Math.min(this.instrumentsCurrentPage * this.instrumentsItemsPerPage, this.instrumentsTotalCount);

    if (totalPages <= 1) {
      paginationContainer.innerHTML = `
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-700">
            Showing ${this.instrumentsTotalCount} instruments
          </div>
        </div>
      `;
      return;
    }

    const pagination = `
      <div class="flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Showing ${startItem} to ${endItem} of ${this.instrumentsTotalCount} instruments
        </div>
        <div class="flex space-x-2">
          <button 
            id="instruments-prev-page" 
            class="px-3 py-1 border border-gray-300 rounded text-sm ${this.instrumentsCurrentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}"
            ${this.instrumentsCurrentPage === 1 ? 'disabled' : ''}
          >
            Previous
          </button>
          
          <div class="flex space-x-1">
            ${this.renderInstrumentsPageNumbers(totalPages)}
          </div>
          
          <button 
            id="instruments-next-page" 
            class="px-3 py-1 border border-gray-300 rounded text-sm ${this.instrumentsCurrentPage === totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}"
            ${this.instrumentsCurrentPage === totalPages ? 'disabled' : ''}
          >
            Next
          </button>
        </div>
      </div>
    `;

    paginationContainer.innerHTML = pagination;
    this.attachInstrumentsPaginationListeners();
  }

  private renderInstrumentsPageNumbers(totalPages: number): string {
    const pages: string[] = [];
    const showPages = 5;
    let startPage = Math.max(1, this.instrumentsCurrentPage - Math.floor(showPages / 2));
    let endPage = Math.min(totalPages, startPage + showPages - 1);

    if (endPage - startPage < showPages - 1) {
      startPage = Math.max(1, endPage - showPages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(`
        <button 
          class="px-3 py-1 border border-gray-300 rounded text-sm instruments-page-btn ${i === this.instrumentsCurrentPage ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}"
          data-page="${i}"
        >
          ${i}
        </button>
      `);
    }

    return pages.join('');
  }

  private attachInstrumentsPaginationListeners(): void {
    const prevBtn = this.container.querySelector('#instruments-prev-page');
    const nextBtn = this.container.querySelector('#instruments-next-page');
    const pageButtons = this.container.querySelectorAll('.instruments-page-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (this.instrumentsCurrentPage > 1) {
          this.instrumentsCurrentPage--;
          this.loadInstrumentsPaginated();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(this.instrumentsTotalCount / this.instrumentsItemsPerPage);
        if (this.instrumentsCurrentPage < totalPages) {
          this.instrumentsCurrentPage++;
          this.loadInstrumentsPaginated();
        }
      });
    }

    pageButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const page = parseInt((e.target as HTMLElement).getAttribute('data-page') || '1');
        this.instrumentsCurrentPage = page;
        this.loadInstrumentsPaginated();
      });
    });
  }

  private showInstrumentsError(message: string): void {
    const tableContainer = this.container.querySelector('#instruments-table');
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

  // Transparency pagination methods
  private async loadTransparencyPaginated(): Promise<void> {
    this.setTransparencyLoadingState(true);
    
    try {
      const requestParams = {
        page: this.transparencyCurrentPage,
        per_page: this.transparencyItemsPerPage,
        ...this.transparencyFilters
      };
      
      console.log('Loading transparency with params:', requestParams);
      
      const response = await this.transparencyService.getTransparencyCalculations(requestParams);

      if (response.status === 'success' && response.data) {
        this.transparencyCalculations = response.data.calculations;
        this.transparencyTotalCount = response.data.pagination?.total || 0;
        
        console.log('Transparency API response:', {
          totalCalculations: this.transparencyCalculations.length,
          totalCount: this.transparencyTotalCount,
          pagination: response.data.pagination,
          currentPage: this.transparencyCurrentPage,
          filters: this.transparencyFilters
        });
        
        // Update statistics on first load only
        if (this.transparencyCurrentPage === 1) {
          console.log('Loading statistics for first page load...');
          // Load separate statistics call for accurate counts
          this.loadTransparencyStatistics();
        } else {
          // Update statistics with current data for subsequent pages
          this.updateTransparencyStatistics();
        }
        
        this.renderTransparencyTablePaginated();
        this.renderTransparencyPagination();
      }
      
    } catch (error) {
      console.error('Failed to load transparency calculations:', error);
      this.showTransparencyError('Failed to load transparency calculations. Please try again.');
    } finally {
      this.setTransparencyLoadingState(false);
    }
  }

  private setTransparencyLoadingState(loading: boolean): void {
    const loadingElement = this.container.querySelector('#transparency-loading');
    const tableElement = this.container.querySelector('#transparency-table');
    
    if (loadingElement && tableElement) {
      if (loading) {
        loadingElement.classList.remove('hidden');
        tableElement.innerHTML = '';
      } else {
        loadingElement.classList.add('hidden');
      }
    }
  }

  private renderTransparencyTablePaginated(): void {
    const tableContainer = this.container.querySelector('#transparency-table');
    if (!tableContainer) return;

    if (this.transparencyCalculations.length === 0) {
      tableContainer.innerHTML = `
        <div class="p-8 text-center text-gray-500">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No transparency calculations found</p>
          <p class="text-sm mt-1">Try adjusting your filter criteria</p>
        </div>
      `;
      return;
    }

    const tableHTML = `
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISIN</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">FIRDS File</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Instrument Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Activity Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transactions</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Period</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          ${this.transparencyCalculations.map(calc => this.renderTransparencyRow(calc)).join('')}
        </tbody>
      </table>
    `;

    tableContainer.innerHTML = tableHTML;
  }

  private renderTransparencyRow(calc: TransparencyCalculation): string {
    return `
      <tr class="hover:bg-gray-50 cursor-pointer" onclick="window.location.hash = '#/transparency/${calc.isin}'">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
          ${calc.isin}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${calc.file_type?.includes('FULECR') ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}">
            ${calc.file_type || 'N/A'}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
            ${calc.instrument_type || 'N/A'}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">
          <span class="${calc.transparency_analysis?.has_trading_activity ? 'text-green-600 font-medium' : 'text-gray-500'}">
            ${calc.transparency_analysis?.liquidity_status || 'N/A'}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${calc.volume ? new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(calc.volume) : 'N/A'}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${calc.transactions ? new Intl.NumberFormat('en-US').format(calc.transactions) : 'N/A'}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          ${calc.from_date || 'N/A'} to ${calc.to_date || 'N/A'}
        </td>
      </tr>
    `;
  }

  private renderTransparencyPagination(): void {
    const paginationContainer = this.container.querySelector('#transparency-pagination');
    if (!paginationContainer) return;

    const totalPages = Math.ceil(this.transparencyTotalCount / this.transparencyItemsPerPage);
    const startItem = (this.transparencyCurrentPage - 1) * this.transparencyItemsPerPage + 1;
    const endItem = Math.min(this.transparencyCurrentPage * this.transparencyItemsPerPage, this.transparencyTotalCount);

    if (totalPages <= 1) {
      paginationContainer.innerHTML = `
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-700">
            Showing ${this.transparencyTotalCount} calculations
          </div>
        </div>
      `;
      return;
    }

    const pagination = `
      <div class="flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Showing ${startItem} to ${endItem} of ${this.transparencyTotalCount} calculations
        </div>
        <div class="flex space-x-2">
          <button 
            id="transparency-prev-page" 
            class="px-3 py-1 border border-gray-300 rounded text-sm ${this.transparencyCurrentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}"
            ${this.transparencyCurrentPage === 1 ? 'disabled' : ''}
          >
            Previous
          </button>
          
          <div class="flex space-x-1">
            ${this.renderTransparencyPageNumbers(totalPages)}
          </div>
          
          <button 
            id="transparency-next-page" 
            class="px-3 py-1 border border-gray-300 rounded text-sm ${this.transparencyCurrentPage === totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}"
            ${this.transparencyCurrentPage === totalPages ? 'disabled' : ''}
          >
            Next
          </button>
        </div>
      </div>
    `;

    paginationContainer.innerHTML = pagination;
    this.attachTransparencyPaginationListeners();
  }

  private renderTransparencyPageNumbers(totalPages: number): string {
    const pages: string[] = [];
    const showPages = 5;
    let startPage = Math.max(1, this.transparencyCurrentPage - Math.floor(showPages / 2));
    let endPage = Math.min(totalPages, startPage + showPages - 1);

    if (endPage - startPage < showPages - 1) {
      startPage = Math.max(1, endPage - showPages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(`
        <button 
          class="px-3 py-1 border border-gray-300 rounded text-sm transparency-page-btn ${i === this.transparencyCurrentPage ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}"
          data-page="${i}"
        >
          ${i}
        </button>
      `);
    }

    return pages.join('');
  }

  private attachTransparencyPaginationListeners(): void {
    const prevBtn = this.container.querySelector('#transparency-prev-page');
    const nextBtn = this.container.querySelector('#transparency-next-page');
    const pageButtons = this.container.querySelectorAll('.transparency-page-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (this.transparencyCurrentPage > 1) {
          this.transparencyCurrentPage--;
          this.loadTransparencyPaginated();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(this.transparencyTotalCount / this.transparencyItemsPerPage);
        if (this.transparencyCurrentPage < totalPages) {
          this.transparencyCurrentPage++;
          this.loadTransparencyPaginated();
        }
      });
    }

    pageButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const page = parseInt((e.target as HTMLElement).getAttribute('data-page') || '1');
        this.transparencyCurrentPage = page;
        this.loadTransparencyPaginated();
      });
    });
  }

  private showTransparencyError(message: string): void {
    const tableContainer = this.container.querySelector('#transparency-table');
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

  private async loadTransparencyStatistics(): Promise<void> {
    try {
      // Get total count
      const totalResponse = await this.transparencyService.getTransparencyCalculations({
        page: 1,
        per_page: 1
      });
      
      // Get equity count  
      const equityResponse = await this.transparencyService.getTransparencyCalculations({
        page: 1,
        per_page: 1,
        file_type: 'FULECR'
      });
      
      // Get non-equity count
      const nonEquityResponse = await this.transparencyService.getTransparencyCalculations({
        page: 1,
        per_page: 1,
        file_type: 'FULNCR'
      });
      
      this.transparencyStats = {
        total: totalResponse.data?.pagination?.total || 0,
        equity: equityResponse.data?.pagination?.total || 0,
        nonEquity: nonEquityResponse.data?.pagination?.total || 0,
        liquid: 0  // Will be calculated from loaded data
      };
      
      console.log('Loaded transparency statistics:', this.transparencyStats);
      this.updateTransparencyStatistics();
      
    } catch (error) {
      console.error('Failed to load transparency statistics:', error);
      // Use fallback calculation from current data
      this.updateTransparencyStatistics();
    }
  }

  private formatDate(value?: string): string {
    if (!value) return '';
    try {
      return new Date(value).toLocaleDateString();
    } catch {
      return value;
    }
  }

  private getTypeColor(type?: string): string {
    switch (type?.toLowerCase()) {
      case 'equity': return 'bg-blue-100 text-blue-800';
      case 'debt': return 'bg-green-100 text-green-800';
      case 'future': return 'bg-purple-100 text-purple-800';
      case 'option': return 'bg-yellow-100 text-yellow-800';
      case 'collective_investment': return 'bg-indigo-100 text-indigo-800';
      case 'structured': return 'bg-red-100 text-red-800';
      case 'spot': return 'bg-pink-100 text-pink-800';
      case 'forward': return 'bg-orange-100 text-orange-800';
      case 'rights': return 'bg-teal-100 text-teal-800';
      case 'swap': return 'bg-cyan-100 text-cyan-800';
      case 'strategy': return 'bg-emerald-100 text-emerald-800';
      case 'financing': return 'bg-lime-100 text-lime-800';
      case 'referential': return 'bg-violet-100 text-violet-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  private formatInstrumentType(type?: string): string {
    if (!type) return 'Unknown';
    // Convert snake_case to Title Case
    return type
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
}