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
    isin?: string;
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
  private transparencyFilters: any = {};

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    super(container, params);
    this.instrumentService = ApiServiceFactory.getInstance().instruments;
    this.transparencyService = ApiServiceFactory.getInstance().transparency;
  }
  
  async render(): Promise<void> {
    await this.loadInstrumentTypeCounts();
    this.updateUI();
  }

  private async loadInstrumentTypeCounts(): Promise<void> {
    try {
      this.loading = true;
      this.error = null;
      
      // Load counts for each CFI instrument type  
      const promises = this.cfiInstrumentTypes.map(async (type) => {
        const filters = { cfi_type: type.code };
        const response = await this.instrumentService.listInstruments(filters, { page: 1, per_page: 1 });
        
        return {
          ...type,
          count: response.meta?.total || 0
        };
      });
      
      this.cfiInstrumentTypes = await Promise.all(promises);
      
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
      this.loadInstrumentsList();
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
      <!-- Quick Filters -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Instrument Type</label>
            <select id="type-filter" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">All Types</option>
              <!-- Types will be populated dynamically -->
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Currency</label>
            <select id="currency-filter" class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">All Currencies</option>
              <option value="EUR">EUR</option>
              <option value="USD">USD</option>
              <option value="GBP">GBP</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Search ISIN</label>
            <input id="isin-filter" type="text" placeholder="e.g. SE0000242455" class="w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          <div class="flex items-end">
            <button id="search-btn" class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
              Search
            </button>
          </div>
        </div>
      </div>

      <!-- Results Table -->
      ${this.createCard(`
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISIN</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CFI Code</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Currency</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Authority</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trading Venue</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Publication Date</th>
              </tr>
            </thead>
            <tbody id="instruments-tbody" class="bg-white divide-y divide-gray-200">
              <tr>
                <td colspan="8" class="px-6 py-8 text-center text-gray-500">
                  <div class="flex items-center justify-center">
                    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
                    Loading instruments...
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      `, 'Instruments List')}
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
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.name || 'N/A'}</td>
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
        ${this.transparencyCalculations.length > 0 ? `
          <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-semibold mb-4">
              Transparency Calculations
              <span class="text-sm font-normal text-gray-500 ml-2">(${this.totalRecords.toLocaleString()} total)</span>
            </h2>
            
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
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
                  ${this.transparencyCalculations.map((calc: TransparencyCalculation) => `
                    <tr class="hover:bg-gray-50 cursor-pointer instrument-row" data-isin="${calc.isin}">
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
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        ` : this.loading ? `
          <div class="bg-white p-6 rounded-lg shadow text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p class="text-gray-600">Loading transparency data...</p>
          </div>
        ` : `
          <div class="bg-white p-6 rounded-lg shadow text-center">
            <p class="text-gray-600">Click "Apply Filters" to load transparency calculations</p>
          </div>
        `}
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

    // Listing tab event listeners
    const searchBtn = this.container.querySelector('#search-btn') as HTMLButtonElement;
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        this.updateFiltersFromForm();
        this.loadInstrumentsList();
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
        
        // Clear filters and show all data
        this.transparencyFilters = {};
        this.applyTransparencyFilters();
        this.updateUI();
        // Update statistics after UI is rendered
        setTimeout(() => this.updateTransparencyStatistics(), 200);
      });
    }
  }

  private updateFiltersFromForm(): void {
    const typeSelect = this.container.querySelector('#type-filter') as HTMLSelectElement;
    const currencySelect = this.container.querySelector('#currency-filter') as HTMLSelectElement;
    const isinInput = this.container.querySelector('#isin-filter') as HTMLInputElement;

    this.currentFilters = {
      type: typeSelect?.value || undefined,
      currency: currencySelect?.value || undefined,
      isin: isinInput?.value?.trim() || undefined,
    };
  }

  private async loadInstrumentsList(): Promise<void> {
    const tbody = this.container.querySelector('#instruments-tbody');
    if (!tbody) return;

    // Show loading state
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="px-6 py-8 text-center text-gray-500">
          <div class="flex items-center justify-center">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
            Loading instruments...
          </div>
        </td>
      </tr>
    `;

    try {
      // Fetch instruments from API
      const response = await this.instrumentService.listInstruments(
        {
          type: this.currentFilters.type,
          currency: this.currentFilters.currency,
        },
        { page: 1, limit: 20 }
      );

      if (response.status === 'success' && response.data) {
        // Handle the actual API response structure
        const instruments = Array.isArray(response.data) ? response.data : [];
        this.renderInstrumentsTable(instruments);
      } else {
        this.showInstrumentError('Failed to load instruments');
      }
    } catch (error) {
      console.error('Error loading instruments:', error);
      this.showInstrumentError('Error loading instruments. Please try again.');
    }
  }

  private renderInstrumentsTable(instruments: Instrument[]): void {
    const tbody = this.container.querySelector('#instruments-tbody');
    if (!tbody) return;

    if (instruments.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="px-6 py-8 text-center text-gray-500">
            No instruments found matching your criteria.
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = instruments.map(instrument => `
      <tr class="hover:bg-gray-50 cursor-pointer instrument-row" data-isin="${instrument.isin}">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
          ${instrument.isin || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${this.getTypeColor(instrument.instrument_type)}">
            ${this.formatInstrumentType(instrument.instrument_type)}
          </span>
        </td>
        <td class="px-6 py-4 text-sm text-gray-900" style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">
          ${instrument.short_name || instrument.full_name || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
          ${instrument.cfi_code || instrument.cfi || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${instrument.currency || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${instrument.competent_authority || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${instrument.relevant_trading_venue || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${this.formatDate(instrument.publication_from_date || undefined) || 'N/A'}
        </td>
      </tr>
    `).join('');

    // Attach click listeners to instrument rows
    this.attachInstrumentRowListeners();
  }

  private attachInstrumentRowListeners(): void {
    const instrumentRows = this.container.querySelectorAll('.instrument-row');
    instrumentRows.forEach(row => {
      row.addEventListener('click', async () => {
        const isin = row.getAttribute('data-isin');
        if (isin) {
          await this.selectInstrument(isin);
        }
      });
    });
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
    
    if (tab === 'transparency') {
      // Only load data if we don't have it already
      if (this.allTransparencyCalculations.length === 0) {
        this.handleLoadTransparencyData();
      } else {
        // Reset filters and show all data
        this.transparencyFilters = {};
        this.applyTransparencyFilters();
        this.updateUI();
        // Update statistics after UI is rendered
        setTimeout(() => this.updateTransparencyStatistics(), 200);
      }
    } else {
      this.transparencyCalculations = [];
      this.updateUI();
    }
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
      
      // Load first page to get total count
      const firstResponse = await this.transparencyService.getTransparencyCalculations(
        { page: 1, per_page: 100 }, // API max is 100
        { timeout: 60000 }
      );
      
      if (firstResponse.status === 'success' && firstResponse.data) {
        let allCalculations = [...firstResponse.data.calculations];
        const totalRecords = firstResponse.data.pagination.total;
        const totalPages = Math.ceil(totalRecords / 100);
        
        console.log(`Loading ${totalRecords} total calculations across ${totalPages} pages`);
        
        // Load remaining pages if needed
        if (totalPages > 1) {
          const remainingPages = [];
          for (let page = 2; page <= totalPages; page++) {
            remainingPages.push(
              this.transparencyService.getTransparencyCalculations(
                { page, per_page: 100 },
                { timeout: 60000 }
              )
            );
          }
          
          const remainingResponses = await Promise.allSettled(remainingPages);
          
          remainingResponses.forEach((result, index) => {
            if (result.status === 'fulfilled' && result.value.status === 'success' && result.value.data) {
              allCalculations.push(...result.value.data.calculations);
              console.log(`Loaded page ${index + 2}: ${result.value.data.calculations.length} calculations`);
            } else {
              console.error(`Failed to load page ${index + 2}:`, result);
            }
          });
        }
        
        // Store all data for filtering
        this.allTransparencyCalculations = allCalculations;
        console.log('Loaded transparency calculations:', this.allTransparencyCalculations.length);
        // Apply current filters (which will be empty initially)
        this.applyTransparencyFilters();
        console.log('After filtering:', this.transparencyCalculations.length);
      }
      
    } catch (error) {
      console.error('Error loading transparency data:', error);
      this.error = 'Failed to load transparency calculations';
      this.transparencyCalculations = [];
      this.allTransparencyCalculations = [];
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

  private updateTransparencyStatistics(): void {
    // Only update if we're on transparency tab
    if (this.currentTab !== 'transparency') {
      console.log('Skipping transparency stats update - not on transparency tab');
      return;
    }
    
    console.log('Updating transparency statistics with', this.transparencyCalculations.length, 'calculations');
    
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
      const totalCount = this.transparencyCalculations.length;
      totalElement.textContent = new Intl.NumberFormat('en-US').format(totalCount);
      console.log('Updated total count:', totalCount);
    } else {
      console.log('total-calculations element not found');
    }
    
    if (equityElement) {
      const equityCount = this.transparencyCalculations.filter(c => c.file_type?.includes('FULECR')).length;
      equityElement.textContent = new Intl.NumberFormat('en-US').format(equityCount);
      console.log('Updated equity count:', equityCount);
    } else {
      console.log('equity-calculations element not found');
    }
    
    if (nonEquityElement) {
      const nonEquityCount = this.transparencyCalculations.filter(c => c.file_type?.includes('FULNCR')).length;
      nonEquityElement.textContent = new Intl.NumberFormat('en-US').format(nonEquityCount);
      console.log('Updated non-equity count:', nonEquityCount);
    } else {
      console.log('non-equity-calculations element not found');
    }
    
    if (liquidElement) {
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
    
    // Apply filters to existing data
    this.applyTransparencyFilters();
    
    // Update UI to show filtered results
    this.updateUI();
    
    // Update statistics after UI is rendered
    setTimeout(() => this.updateTransparencyStatistics(), 200);
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
    const typeSelect = this.container.querySelector('#type-filter') as HTMLSelectElement;
    if (!typeSelect) return;

    // Clear existing options except "All Types"
    typeSelect.innerHTML = '<option value="">All Types</option>';

    // Add available types
    this.availableTypes.forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = this.formatInstrumentType(type);
      typeSelect.appendChild(option);
    });
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