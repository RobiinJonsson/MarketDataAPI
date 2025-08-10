import { isValidISIN, showLoading, showError, formatDate, formatNumber } from '../utils/helpers';

interface ComprehensiveInstrumentData {
  instrument: any;
  transparency: any[];
  venues: any[];
  lei_data?: any;
  parent_child_relationships?: any;
}

export class ComprehensiveSearchComponent {
  private container: HTMLElement;
  private searchInput!: HTMLInputElement;
  private searchButton!: HTMLButtonElement;
  private resultsContainer!: HTMLElement;
  private activeTab: string = 'overview';

  constructor(containerId: string) {
    this.container = document.getElementById(containerId)!;
    this.init();
  }

  private init(): void {
    this.render();
    this.bindEvents();
  }

  private render(): void {
    this.container.innerHTML = `
      <div class="card">
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Comprehensive Instrument Search</h3>
          <p class="mt-1 text-sm text-gray-600">Enter an ISIN to view complete instrument profile with LEI, transparency, CFI, and FIGI data</p>
        </div>
        
        <form id="search-form" class="space-y-4">
          <div class="flex gap-3">
            <div class="flex-1">
              <input
                type="text"
                id="search-input"
                class="input-field"
                placeholder="Enter ISIN (e.g., SE0000242455)"
                pattern="^[A-Z]{2}[A-Z0-9]{9}\\d$"
                title="Please enter a valid 12-character ISIN"
                required
              />
            </div>
            <button type="submit" id="search-button" class="btn btn-primary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              Search
            </button>
          </div>
          <p class="text-sm text-gray-500">
            Looking to create or manage instruments? Visit the 
            <a href="/admin.html" class="text-primary-600 hover:text-primary-700 font-medium">Admin Portal</a>.
          </p>
        </form>
        
        <div id="search-results" class="mt-6"></div>
      </div>
    `;

    this.searchInput = this.container.querySelector('#search-input')!;
    this.searchButton = this.container.querySelector('#search-button')!;
    this.resultsContainer = this.container.querySelector('#search-results')!;
  }

  private bindEvents(): void {
    const form = this.container.querySelector('#search-form')!;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleComprehensiveSearch();
    });

    this.searchInput.addEventListener('input', () => {
      const isValid = isValidISIN(this.searchInput.value);
      this.searchButton.disabled = !isValid;
      this.searchButton.classList.toggle('opacity-50', !isValid);
    });
  }

  private async handleComprehensiveSearch(): Promise<void> {
    const isin = this.searchInput.value.trim().toUpperCase();
    
    if (!isValidISIN(isin)) {
      showError(this.resultsContainer, 'Please enter a valid ISIN');
      return;
    }

    showLoading(this.resultsContainer, 'Loading comprehensive instrument data...');
    
    try {
      // Fetch data from multiple endpoints in parallel
      console.log(`Starting comprehensive search for ISIN: ${isin}`);
      
      const [instrumentResponse, transparencyResponse, venuesResponse] = await Promise.allSettled([
        this.fetchInstrumentData(isin),
        this.fetchTransparencyData(isin),
        this.fetchVenuesData(isin)
      ]);

      console.log('Promise.allSettled results:', {
        instrument: instrumentResponse.status,
        transparency: transparencyResponse.status,
        venues: venuesResponse.status
      });

      // Extract successful responses
      const instrumentData = instrumentResponse.status === 'fulfilled' ? instrumentResponse.value : null;
      const transparencyData = transparencyResponse.status === 'fulfilled' ? transparencyResponse.value : [];
      const venuesData = venuesResponse.status === 'fulfilled' ? venuesResponse.value : [];

      console.log('Fetched data:', {
        instrument: instrumentData,
        transparency: transparencyData,
        venues: venuesData
      });

      if (!instrumentData) {
        this.renderNoResults(isin);
        return;
      }

      // Extract actual data from API response structures
      const actualInstrumentData = instrumentData?.data || null;
      const actualTransparencyData = Array.isArray(transparencyData?.data) ? transparencyData.data : [];
      const actualVenuesData = Array.isArray(venuesData?.data?.venues) ? venuesData.data.venues : [];

      console.log('Extracted actual data:', {
        instrument: actualInstrumentData,
        transparency: actualTransparencyData,
        venues: actualVenuesData
      });

      if (!actualInstrumentData) {
        this.renderNoResults(isin);
        return;
      }

      // If instrument has LEI, fetch LEI relationships
      let leiData = null;
      let parentChildData = null;
      if (actualInstrumentData.lei_id) {
        try {
          const [leiResponse, relationshipResponse] = await Promise.allSettled([
            this.fetchLeiData(actualInstrumentData.lei_id),
            this.fetchParentChildData(actualInstrumentData.lei_id)
          ]);
          
          leiData = leiResponse.status === 'fulfilled' ? leiResponse.value : null;
          parentChildData = relationshipResponse.status === 'fulfilled' ? relationshipResponse.value : null;
        } catch (error) {
          console.warn('Failed to fetch LEI data:', error);
        }
      }

      const comprehensiveData: ComprehensiveInstrumentData = {
        instrument: actualInstrumentData,
        transparency: actualTransparencyData,
        venues: actualVenuesData,
        lei_data: leiData,
        parent_child_relationships: parentChildData
      };

      this.renderComprehensiveResults(comprehensiveData);
    } catch (error) {
      console.error('Search error:', error);
      showError(this.resultsContainer, 'Failed to load instrument data. Please try again.');
    }
  }

  private async fetchInstrumentData(isin: string) {
    const response = await fetch(`/api/v1/instruments/${isin}`);
    if (!response.ok) throw new Error('Instrument not found');
    return await response.json();
  }

  private async fetchTransparencyData(isin: string) {
    try {
      const response = await fetch(`/api/v1/transparency/isin/${isin}`);
      if (!response.ok) return [];
      return await response.json();
    } catch {
      return [];
    }
  }

  private async fetchVenuesData(isin: string) {
    try {
      console.log(`Fetching venues data for ISIN: ${isin}`);
      const url = `/api/v1/instruments/${isin}/venues`;
      console.log(`Venues URL: ${url}`);
      
      const response = await fetch(url);
      console.log(`Venues response status: ${response.status}`);
      
      if (!response.ok) {
        console.warn(`Venues request failed with status: ${response.status}`);
        return [];
      }
      
      // Get the raw response text first to handle invalid JSON
      const responseText = await response.text();
      
      try {
        // Fix invalid JSON by replacing NaN with null
        const cleanedResponseText = responseText.replace(/:\s*NaN\s*([,}])/g, ': null$1');
        console.log('Cleaned venues response (fixed NaN values)');
        
        const data = JSON.parse(cleanedResponseText);
        console.log('Venues response data:', data);
        return data;
      } catch (jsonError) {
        console.error('JSON parsing error for venues response:', jsonError);
        console.log('Response text (first 1000 chars):', responseText.substring(0, 1000));
        return [];
      }
    } catch (error) {
      console.error('Error fetching venues data:', error);
      return [];
    }
  }

  private async fetchLeiData(lei: string) {
    try {
      const response = await fetch(`/api/v1/legal-entities/${lei}`);
      if (!response.ok) return null;
      return await response.json();
    } catch {
      return null;
    }
  }

  private async fetchParentChildData(lei: string) {
    try {
      const response = await fetch(`/api/v1/relationships/${lei}`);
      if (!response.ok) return null;
      return await response.json();
    } catch {
      return null;
    }
  }

  private renderNoResults(isin: string): void {
    this.resultsContainer.innerHTML = `
      <div class="text-center py-8">
        <div class="text-gray-400 mb-4">
          <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No instrument found</h3>
        <p class="text-gray-600 mb-4">No instrument was found for ISIN: <strong>${isin}</strong></p>
        <a href="/admin.html" class="btn btn-primary">Create New Instrument</a>
      </div>
    `;
  }

  private renderComprehensiveResults(data: ComprehensiveInstrumentData): void {
    const { instrument } = data;
    
    this.resultsContainer.innerHTML = `
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <!-- Header with instrument name -->
        <div class="px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold text-gray-900">${instrument.full_name || instrument.short_name}</h2>
              <p class="text-sm text-gray-600 font-mono">${instrument.isin}</p>
            </div>
            <div class="text-right">
              <div class="text-sm text-gray-500">Type</div>
              <div class="font-medium text-gray-900 capitalize">${instrument.instrument_type}</div>
            </div>
          </div>
        </div>

        <!-- Tab Navigation -->
        <div class="border-b border-gray-200">
          <nav class="flex space-x-8 px-6" role="tablist">
            ${this.renderTabButton('Overview', 'overview')}
            ${this.renderTabButton('Legal Entity', 'lei')}
            ${this.renderTabButton('Transparency', 'transparency', Array.isArray(data.transparency) ? data.transparency.length : 0)}
            ${this.renderTabButton('CFI Classification', 'cfi')}
            ${this.renderTabButton('FIGI Mapping', 'figi')}
            ${this.renderTabButton('Trading Venues', 'venues', Array.isArray(data.venues) ? data.venues.length : 0)}
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <div id="tab-overview" class="tab-content ${this.activeTab === 'overview' ? '' : 'hidden'}">
            ${this.renderOverviewTab(data)}
          </div>
          <div id="tab-lei" class="tab-content ${this.activeTab === 'lei' ? '' : 'hidden'}">
            ${this.renderLeiTab(data)}
          </div>
          <div id="tab-transparency" class="tab-content ${this.activeTab === 'transparency' ? '' : 'hidden'}">
            ${this.renderTransparencyTab(data)}
          </div>
          <div id="tab-cfi" class="tab-content ${this.activeTab === 'cfi' ? '' : 'hidden'}">
            ${this.renderCfiTab(data)}
          </div>
          <div id="tab-figi" class="tab-content ${this.activeTab === 'figi' ? '' : 'hidden'}">
            ${this.renderFigiTab(data)}
          </div>
          <div id="tab-venues" class="tab-content ${this.activeTab === 'venues' ? '' : 'hidden'}">
            ${this.renderVenuesTab(data)}
          </div>
        </div>
      </div>
    `;

    // Bind tab click events
    this.bindTabEvents();
  }

  private renderTabButton(label: string, tabKey: string, count?: number): string {
    const isActive = this.activeTab === tabKey;
    const countBadge = count !== undefined ? `<span class="ml-2 bg-gray-100 text-gray-900 text-xs font-medium px-2.5 py-0.5 rounded-full">${count}</span>` : '';
    
    return `
      <button 
        data-tab="${tabKey}" 
        class="tab-button py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
          isActive 
            ? 'border-blue-500 text-blue-600' 
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }"
      >
        ${label}${countBadge}
      </button>
    `;
  }

  private bindTabEvents(): void {
    const tabButtons = this.resultsContainer.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const tabKey = (e.target as HTMLElement).dataset.tab!;
        this.switchTab(tabKey);
      });
    });
  }

  private switchTab(tabKey: string): void {
    this.activeTab = tabKey;
    
    // Update button states
    const tabButtons = this.resultsContainer.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
      const isActive = button.getAttribute('data-tab') === tabKey;
      button.className = `tab-button py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
        isActive 
          ? 'border-blue-500 text-blue-600' 
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
      }`;
    });

    // Update content visibility
    const tabContents = this.resultsContainer.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
      const contentId = content.id.replace('tab-', '');
      content.classList.toggle('hidden', contentId !== tabKey);
    });
  }

  private renderOverviewTab(data: ComprehensiveInstrumentData): string {
    const { instrument } = data;
    return `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <h3 class="font-semibold text-gray-900">Basic Information</h3>
          <dl class="space-y-3">
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">ISIN</dt>
              <dd class="text-sm text-gray-900 font-mono">${instrument.isin}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Symbol</dt>
              <dd class="text-sm text-gray-900">${instrument.short_name || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Currency</dt>
              <dd class="text-sm text-gray-900">${instrument.currency || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Type</dt>
              <dd class="text-sm text-gray-900 capitalize">${instrument.instrument_type}</dd>
            </div>
          </dl>
        </div>

        <div class="space-y-4">
          <h3 class="font-semibold text-gray-900">Metadata</h3>
          <dl class="space-y-3">
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Created</dt>
              <dd class="text-sm text-gray-900">${formatDate(instrument.created_at)}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Updated</dt>
              <dd class="text-sm text-gray-900">${formatDate(instrument.updated_at)}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Trading Venues</dt>
              <dd class="text-sm text-gray-900">${instrument.trading_venues_count || 0}</dd>
            </div>
          </dl>
        </div>
      </div>
    `;
  }

  private renderLeiTab(data: ComprehensiveInstrumentData): string {
    const { instrument, lei_data, parent_child_relationships } = data;
    
    if (!instrument.lei_id) {
      return `
        <div class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No LEI Information</h3>
          <p class="text-gray-600">This instrument does not have an associated Legal Entity Identifier (LEI)</p>
        </div>
      `;
    }

    return `
      <div class="space-y-6">
        <!-- LEI Details -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-semibold text-gray-900 mb-4">Legal Entity Information</h3>
          <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <dt class="text-sm font-medium text-gray-500">LEI</dt>
              <dd class="text-sm text-gray-900 font-mono">${instrument.lei_id}</dd>
            </div>
            ${lei_data ? `
              <div>
                <dt class="text-sm font-medium text-gray-500">Entity Name</dt>
                <dd class="text-sm text-gray-900">${lei_data.name || 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Jurisdiction</dt>
                <dd class="text-sm text-gray-900">${lei_data.jurisdiction || 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Legal Form</dt>
                <dd class="text-sm text-gray-900">${lei_data.legal_form || 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Status</dt>
                <dd class="text-sm text-gray-900">${lei_data.status || 'N/A'}</dd>
              </div>
            ` : '<div class="col-span-2 text-sm text-gray-500">LEI details not available</div>'}
          </dl>
        </div>

        <!-- Parent-Child Relationships -->
        ${parent_child_relationships ? `
          <div class="bg-blue-50 rounded-lg p-4">
            <h3 class="font-semibold text-gray-900 mb-4">Corporate Structure</h3>
            <div class="space-y-3">
              ${parent_child_relationships.parents ? `
                <div>
                  <h4 class="text-sm font-medium text-gray-700">Parent Entities</h4>
                  <div class="mt-2 space-y-2">
                    ${parent_child_relationships.parents.map((parent: any) => `
                      <div class="text-sm text-gray-600">
                        <span class="font-mono">${parent.lei}</span> - ${parent.name || 'Unknown'}
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}
              ${parent_child_relationships.children ? `
                <div>
                  <h4 class="text-sm font-medium text-gray-700">Child Entities</h4>
                  <div class="mt-2 space-y-2">
                    ${parent_child_relationships.children.map((child: any) => `
                      <div class="text-sm text-gray-600">
                        <span class="font-mono">${child.lei}</span> - ${child.name || 'Unknown'}
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}
            </div>
          </div>
        ` : '<div class="text-sm text-gray-500">Parent-child relationship data not available</div>'}
      </div>
    `;
  }

  private renderTransparencyTab(data: ComprehensiveInstrumentData): string {
    const { transparency } = data;
    
    console.log('Rendering transparency tab with data:', transparency);
    
    if (!transparency || !Array.isArray(transparency) || transparency.length === 0) {
      return `
        <div class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No Transparency Data</h3>
          <p class="text-gray-600">No transparency calculations found for this instrument</p>
        </div>
      `;
    }

    return `
      <div class="space-y-6">
        ${transparency.map((calc: any, index: number) => `
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex justify-between items-start mb-4">
              <h3 class="font-semibold text-gray-900">Calculation ${index + 1}</h3>
              <span class="text-xs text-gray-500">${formatDate(calc.created_at || calc.calculation_date)}</span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="text-center p-3 bg-white rounded">
                <div class="text-2xl font-bold text-gray-900">${formatNumber(calc.total_transactions_executed || 0)}</div>
                <div class="text-sm text-gray-600">Total Transactions</div>
              </div>
              <div class="text-center p-3 bg-white rounded">
                <div class="text-2xl font-bold text-gray-900">${formatNumber(calc.total_volume_executed || 0)}</div>
                <div class="text-sm text-gray-600">Total Volume</div>
              </div>
              <div class="text-center p-3 bg-white rounded">
                <div class="text-2xl font-bold ${calc.liquidity ? 'text-green-600' : 'text-red-600'}">${calc.liquidity ? 'Liquid' : 'Illiquid'}</div>
                <div class="text-sm text-gray-600">Status</div>
              </div>
            </div>
            
            ${calc.avg_daily_volume ? `
              <div class="mt-4 text-sm text-gray-600">
                <strong>Average Daily Volume:</strong> ${formatNumber(calc.avg_daily_volume)}
              </div>
            ` : ''}
          </div>
        `).join('')}
      </div>
    `;
  }

  private renderCfiTab(data: ComprehensiveInstrumentData): string {
    const { instrument } = data;
    
    if (!instrument.cfi_code) {
      return `
        <div class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No CFI Code</h3>
          <p class="text-gray-600">This instrument does not have a Classification of Financial Instruments (CFI) code</p>
        </div>
      `;
    }

    return `
      <div class="space-y-6">
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-semibold text-gray-900 mb-4">CFI Classification</h3>
          <div class="text-center mb-6">
            <div class="text-3xl font-mono font-bold text-gray-900 tracking-widest">${instrument.cfi_code}</div>
            <div class="text-sm text-gray-500 mt-1">Classification of Financial Instruments</div>
          </div>
          
          ${instrument.cfi_decoded ? `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">Category</dt>
                <dd class="text-sm text-gray-900">${instrument.cfi_decoded.category_description || 'N/A'} (${instrument.cfi_decoded.category || ''})</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Group</dt>
                <dd class="text-sm text-gray-900">${instrument.cfi_decoded.group_description || 'N/A'} (${instrument.cfi_decoded.group || ''})</dd>
              </div>
              ${instrument.cfi_decoded.attributes ? `
                <div class="md:col-span-2">
                  <dt class="text-sm font-medium text-gray-500 mb-2">Attributes</dt>
                  <dd class="text-sm text-gray-900">
                    <div class="grid grid-cols-2 gap-2">
                      ${Object.entries(instrument.cfi_decoded.attributes).map(([key, value]) => `
                        <div><strong>${key}:</strong> ${value}</div>
                      `).join('')}
                    </div>
                  </dd>
                </div>
              ` : ''}
            </div>
          ` : `
            <div class="text-sm text-gray-500">CFI code breakdown not available</div>
          `}
        </div>
      </div>
    `;
  }

  private renderFigiTab(data: ComprehensiveInstrumentData): string {
    const { instrument } = data;
    
    if (!instrument.figi_mapping) {
      return `
        <div class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No FIGI Mapping</h3>
          <p class="text-gray-600">This instrument does not have Financial Instrument Global Identifier (FIGI) mapping</p>
        </div>
      `;
    }

    const figi = instrument.figi_mapping;
    return `
      <div class="space-y-6">
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-semibold text-gray-900 mb-4">FIGI Mapping</h3>
          <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <dt class="text-sm font-medium text-gray-500">FIGI</dt>
              <dd class="text-sm text-gray-900 font-mono">${figi.figi}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Composite FIGI</dt>
              <dd class="text-sm text-gray-900 font-mono">${figi.composite_figi || 'N/A'}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Share Class FIGI</dt>
              <dd class="text-sm text-gray-900 font-mono">${figi.share_class_figi || 'N/A'}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Security Type</dt>
              <dd class="text-sm text-gray-900">${figi.security_type || 'N/A'}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Market Sector</dt>
              <dd class="text-sm text-gray-900">${figi.market_sector || 'N/A'}</dd>
            </div>
          </dl>
        </div>
      </div>
    `;
  }

  private renderVenuesTab(data: ComprehensiveInstrumentData): string {
    const { venues } = data;
    
    console.log('Rendering venues tab with data:', venues);
    
    if (!venues || !Array.isArray(venues) || venues.length === 0) {
      return `
        <div class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No Trading Venues</h3>
          <p class="text-gray-600">No trading venues found for this instrument</p>
        </div>
      `;
    }

    return `
      <div class="space-y-4">
        <h3 class="font-semibold text-gray-900">Trading Venues (${venues.length})</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          ${venues.map((venue: any) => `
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="font-medium text-gray-900">${venue.name || venue.mic || 'Unknown Venue'}</div>
              ${venue.mic ? `<div class="text-sm text-gray-600 font-mono">${venue.mic}</div>` : ''}
              ${venue.country ? `<div class="text-sm text-gray-600">${venue.country}</div>` : ''}
              ${venue.status ? `<div class="text-xs text-gray-500 mt-2">Status: ${venue.status}</div>` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}
