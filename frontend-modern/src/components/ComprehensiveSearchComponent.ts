import { isValidISIN, showLoading, showError, formatDate, formatNumber } from '../utils/helpers';

interface ComprehensiveInstrumentData {
  instrument: any;
  transparency: any[];
  venues: any[];
  lei_data?: any;
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

      // If instrument has LEI, fetch LEI data and relationships
      let leiData = null;
      if (actualInstrumentData.lei_id) {
        try {
          const [leiResponse, relationshipResponse] = await Promise.allSettled([
            this.fetchLeiData(actualInstrumentData.lei_id),
            this.fetchRelationshipData(actualInstrumentData.lei_id)
          ]);
          
          leiData = leiResponse.status === 'fulfilled' ? leiResponse.value?.data : null;
          const relationshipData = relationshipResponse.status === 'fulfilled' ? relationshipResponse.value?.data : null;
          
          // Merge relationship data into LEI data if both exist
          if (leiData && relationshipData && relationshipData.relationships) {
            // Convert the flat relationships array into the structured format the frontend expects
            const relationships: any = {
              direct_parent: null,
              ultimate_parent: null,
              direct_children: [],
              ultimate_children: [],
              parent_exceptions: []
            };
            
            // Process relationships
            relationshipData.relationships.forEach((rel: any) => {
              if (rel.child_lei === actualInstrumentData.lei_id) {
                // This entity is the child, so the relationship represents a parent
                const parentInfo = {
                  lei: rel.parent_lei,
                  name: rel.parent_name,
                  jurisdiction: rel.parent_jurisdiction,
                  relationship_status: rel.relationship_status,
                  relationship_period_start: rel.relationship_period_start,
                  relationship_period_end: rel.relationship_period_end
                };
                
                if (rel.relationship_type === 'DIRECT') {
                  relationships.direct_parent = parentInfo;
                } else if (rel.relationship_type === 'ULTIMATE') {
                  relationships.ultimate_parent = parentInfo;
                }
              } else if (rel.parent_lei === actualInstrumentData.lei_id) {
                // This entity is the parent, so the relationship represents a child
                const childInfo = {
                  lei: rel.child_lei,
                  name: rel.child_name,
                  jurisdiction: rel.child_jurisdiction,
                  relationship_status: rel.relationship_status,
                  relationship_period_start: rel.relationship_period_start,
                  relationship_period_end: rel.relationship_period_end
                };
                
                if (rel.relationship_type === 'DIRECT') {
                  relationships.direct_children.push(childInfo);
                } else if (rel.relationship_type === 'ULTIMATE') {
                  relationships.ultimate_children.push(childInfo);
                }
              }
            });
            
            leiData.relationships = relationships;
          }
          
          console.log('LEI Data with relationships:', leiData);
        } catch (error) {
          console.warn('Failed to fetch LEI data:', error);
        }
      }

      const comprehensiveData: ComprehensiveInstrumentData = {
        instrument: actualInstrumentData,
        transparency: actualTransparencyData,
        venues: actualVenuesData,
        lei_data: leiData
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

  private async fetchRelationshipData(lei: string) {
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
              <dt class="text-sm font-medium text-gray-500">Type</dt>
              <dd class="text-sm text-gray-900 capitalize">${instrument.instrument_type}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Short Name</dt>
              <dd class="text-sm text-gray-900">${instrument.short_name || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">CFI Code</dt>
              <dd class="text-sm text-gray-900 font-mono">${instrument.cfi_code || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Currency</dt>
              <dd class="text-sm text-gray-900">${instrument.currency || 'N/A'}</dd>
            </div>
          </dl>
        </div>

        <div class="space-y-4">
          <h3 class="font-semibold text-gray-900">FIGI Information</h3>
          <dl class="space-y-3">
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">FIGI</dt>
              <dd class="text-sm text-gray-900 font-mono">${instrument.figi || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Composite FIGI</dt>
              <dd class="text-sm text-gray-900 font-mono">${instrument.composite_figi || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Market Sector</dt>
              <dd class="text-sm text-gray-900">${instrument.market_sector || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Security Type</dt>
              <dd class="text-sm text-gray-900">${instrument.security_type || 'N/A'}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-sm font-medium text-gray-500">Ticker</dt>
              <dd class="text-sm text-gray-900">${instrument.ticker || 'N/A'}</dd>
            </div>
          </dl>
        </div>

        <div class="space-y-4 md:col-span-2">
          <h3 class="font-semibold text-gray-900">Metadata</h3>
          <dl class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="flex justify-between md:block">
              <dt class="text-sm font-medium text-gray-500">Created</dt>
              <dd class="text-sm text-gray-900">${formatDate(instrument.created_at)}</dd>
            </div>
            <div class="flex justify-between md:block">
              <dt class="text-sm font-medium text-gray-500">Updated</dt>
              <dd class="text-sm text-gray-900">${formatDate(instrument.updated_at)}</dd>
            </div>
            <div class="flex justify-between md:block">
              <dt class="text-sm font-medium text-gray-500">Trading Venues</dt>
              <dd class="text-sm text-gray-900">${instrument.trading_venues_count || 0}</dd>
            </div>
          </dl>
        </div>
      </div>
    `;
  }

  private renderLeiTab(data: ComprehensiveInstrumentData): string {
    const { instrument, lei_data } = data;
    
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
                <dd class="text-sm text-gray-900">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${lei_data.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                    ${lei_data.status || 'N/A'}
                  </span>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Registered As</dt>
                <dd class="text-sm text-gray-900">${lei_data.registered_as || 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Managing LOU</dt>
                <dd class="text-sm text-gray-900">${lei_data.managing_lou || 'N/A'}</dd>
              </div>
              ${lei_data.bic ? `
                <div>
                  <dt class="text-sm font-medium text-gray-500">BIC</dt>
                  <dd class="text-sm text-gray-900 font-mono">${lei_data.bic}</dd>
                </div>
              ` : ''}
              ${lei_data.next_renewal_date ? `
                <div>
                  <dt class="text-sm font-medium text-gray-500">Next Renewal</dt>
                  <dd class="text-sm text-gray-900">${formatDate(lei_data.next_renewal_date)}</dd>
                </div>
              ` : ''}
            ` : '<div class="col-span-2 text-sm text-gray-500">LEI details not available</div>'}
          </dl>
        </div>

        <!-- Addresses -->
        ${lei_data && lei_data.addresses && lei_data.addresses.length > 0 ? `
          <div class="bg-blue-50 rounded-lg p-4">
            <h3 class="font-semibold text-gray-900 mb-4">Addresses</h3>
            <div class="space-y-3">
              ${lei_data.addresses.map((address: any) => `
                <div class="bg-white rounded p-3">
                  <div class="flex justify-between items-start mb-2">
                    <h4 class="text-sm font-medium text-gray-700">${address.type || 'Address'}</h4>
                    <span class="text-xs text-gray-500">${address.country || ''}</span>
                  </div>
                  <div class="text-sm text-gray-600">
                    ${address.address_lines ? `<div>${address.address_lines}</div>` : ''}
                    ${address.city ? `<div>${address.city}${address.region ? `, ${address.region}` : ''}</div>` : ''}
                    ${address.postal_code ? `<div>${address.postal_code}</div>` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}

        <!-- Registration Details -->
        ${lei_data && lei_data.registration ? `
          <div class="bg-green-50 rounded-lg p-4">
            <h3 class="font-semibold text-gray-900 mb-4">Registration Details</h3>
            <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt class="text-sm font-medium text-gray-500">Registration Status</dt>
                <dd class="text-sm text-gray-900">${lei_data.registration.status || 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Last Update</dt>
                <dd class="text-sm text-gray-900">${lei_data.registration.last_update ? formatDate(lei_data.registration.last_update) : 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Initial Date</dt>
                <dd class="text-sm text-gray-900">${lei_data.registration.initial_date ? formatDate(lei_data.registration.initial_date) : 'N/A'}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Next Renewal</dt>
                <dd class="text-sm text-gray-900">${lei_data.registration.next_renewal ? formatDate(lei_data.registration.next_renewal) : 'N/A'}</dd>
              </div>
              ${lei_data.registration.validation_sources ? `
                <div class="md:col-span-2">
                  <dt class="text-sm font-medium text-gray-500">Validation Sources</dt>
                  <dd class="text-sm text-gray-900">${lei_data.registration.validation_sources}</dd>
                </div>
              ` : ''}
            </dl>
          </div>
        ` : ''}

        <!-- Parent-Child Relationships -->
        ${lei_data && lei_data.relationships ? `
          <div class="bg-purple-50 rounded-lg p-4">
            <h3 class="font-semibold text-gray-900 mb-4">Corporate Structure</h3>
            <div class="space-y-6">
              
              <!-- Hierarchical Tree View -->
              <div class="bg-white rounded-lg p-4 border border-gray-200">
                <div class="space-y-3">
                  
                  <!-- Ultimate Parent (if different from direct parent) -->
                  ${lei_data.relationships.ultimate_parent && lei_data.relationships.ultimate_parent.lei !== lei_data.relationships.direct_parent?.lei ? `
                    <div class="flex items-center text-sm">
                      <div class="flex-shrink-0 w-4 h-4 mr-3">
                        <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <div class="bg-blue-100 rounded-lg p-3 flex-1">
                        <div class="font-medium text-blue-900">${lei_data.relationships.ultimate_parent.name}</div>
                        <div class="text-xs text-blue-700 font-mono">${lei_data.relationships.ultimate_parent.lei}</div>
                        <div class="text-xs text-blue-600">${lei_data.relationships.ultimate_parent.jurisdiction} • Ultimate Parent</div>
                      </div>
                    </div>
                    
                    <!-- Connection line -->
                    <div class="flex justify-center">
                      <div class="w-px h-4 bg-gray-300"></div>
                    </div>
                  ` : ''}

                  <!-- Direct Parent -->
                  ${lei_data.relationships.direct_parent ? `
                    <div class="flex items-center text-sm">
                      <div class="flex-shrink-0 w-4 h-4 mr-3">
                        <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <div class="bg-green-100 rounded-lg p-3 flex-1">
                        <div class="font-medium text-green-900">${lei_data.relationships.direct_parent.name}</div>
                        <div class="text-xs text-green-700 font-mono">${lei_data.relationships.direct_parent.lei}</div>
                        <div class="text-xs text-green-600">${lei_data.relationships.direct_parent.jurisdiction} • Direct Parent</div>
                      </div>
                    </div>
                    
                    <!-- Connection line -->
                    <div class="flex justify-center">
                      <div class="w-px h-4 bg-gray-300"></div>
                    </div>
                  ` : ''}

                  <!-- Current Entity -->
                  <div class="flex items-center text-sm">
                    <div class="flex-shrink-0 w-4 h-4 mr-3">
                      <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z" clip-rule="evenodd"/>
                      </svg>
                    </div>
                    <div class="bg-purple-100 border-2 border-purple-300 rounded-lg p-3 flex-1">
                      <div class="font-bold text-purple-900">${lei_data.name}</div>
                      <div class="text-xs text-purple-700 font-mono">${instrument.lei_id}</div>
                      <div class="text-xs text-purple-600">${lei_data.jurisdiction} • Current Entity</div>
                    </div>
                  </div>

                  <!-- Direct Children -->
                  ${lei_data.relationships.direct_children && lei_data.relationships.direct_children.length > 0 ? `
                    <!-- Connection line -->
                    <div class="flex justify-center">
                      <div class="w-px h-4 bg-gray-300"></div>
                    </div>
                    
                    <!-- Children container -->
                    <div class="pl-7">
                      <div class="text-xs font-medium text-gray-600 mb-2">Direct Children (${lei_data.relationships.direct_children.length})</div>
                      <div class="space-y-2">
                        ${lei_data.relationships.direct_children.map((child: any) => `
                          <div class="flex items-center text-sm">
                            <div class="flex-shrink-0 w-4 h-4 mr-3">
                              <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-1-11a1 1 0 012 0v2h2a1 1 0 110 2h-2v2a1 1 0 11-2 0v-2H7a1 1 0 110-2h2V7z" clip-rule="evenodd"/>
                              </svg>
                            </div>
                            <div class="bg-orange-100 rounded-lg p-3 flex-1">
                              <div class="font-medium text-orange-900">${child.name}</div>
                              <div class="text-xs text-orange-700 font-mono">${child.lei}</div>
                              <div class="text-xs text-orange-600">${child.jurisdiction} • Direct Child</div>
                            </div>
                          </div>
                        `).join('')}
                      </div>
                    </div>
                  ` : ''}
                </div>
              </div>

              <!-- Parent Exceptions -->
              ${lei_data.relationships.parent_exceptions && lei_data.relationships.parent_exceptions.length > 0 ? `
                <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
                  <h4 class="text-sm font-medium text-amber-800 mb-3">Parent Reporting Exceptions</h4>
                  <div class="space-y-2">
                    ${lei_data.relationships.parent_exceptions.map((exception: any) => `
                      <div class="bg-white border border-amber-200 rounded p-3">
                        <div class="flex items-start justify-between">
                          <div>
                            <div class="text-sm font-medium text-amber-900">${exception.exception_type}</div>
                            <div class="text-sm text-amber-700 mt-1">${exception.exception_reason}</div>
                            <div class="text-xs text-amber-600 mt-1">Category: ${exception.exception_category}</div>
                          </div>
                          <span class="text-xs text-amber-500">${exception.last_updated ? formatDate(exception.last_updated) : ''}</span>
                        </div>
                        ${exception.provided_parent_name ? `
                          <div class="mt-2 text-xs text-amber-600">
                            Referenced Parent: ${exception.provided_parent_name}${exception.provided_parent_lei ? ` (${exception.provided_parent_lei})` : ''}
                          </div>
                        ` : ''}
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}

              <!-- Summary Stats -->
              <div class="bg-gray-100 rounded-lg p-4">
                <h4 class="text-sm font-medium text-gray-700 mb-3">Structure Summary</h4>
                <div class="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div class="text-lg font-semibold text-gray-900">${lei_data.relationships.direct_parent ? 1 : 0}</div>
                    <div class="text-xs text-gray-600">Direct Parent</div>
                  </div>
                  <div>
                    <div class="text-lg font-semibold text-gray-900">${lei_data.relationships.direct_children ? lei_data.relationships.direct_children.length : 0}</div>
                    <div class="text-xs text-gray-600">Direct Children</div>
                  </div>
                  <div>
                    <div class="text-lg font-semibold text-gray-900">${lei_data.relationships.parent_exceptions ? lei_data.relationships.parent_exceptions.length : 0}</div>
                    <div class="text-xs text-gray-600">Exceptions</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ` : '<div class="text-sm text-gray-500">Relationship data not available</div>'}
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
          <p class="text-gray-600">No MiFID II transparency calculations found for this instrument</p>
        </div>
      `;
    }

    // Separate data by methodology and sort by date
    const sintData = transparency.filter((calc: any) => calc.raw_data?.Mthdlgy === 'SINT').sort((a: any, b: any) => new Date(a.from_date).getTime() - new Date(b.from_date).getTime());
    const yearData = transparency.filter((calc: any) => calc.raw_data?.Mthdlgy === 'YEAR');
    
    return `
      <div class="space-y-6">
        <!-- MiFID II Overview -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 class="font-semibold text-blue-900 mb-2">MiFID II Transparency Data</h3>
          <p class="text-sm text-blue-700">
            This data shows transparency calculations under MiFID II/MiFIR requirements for trading venues and systematic internalisers.
            Includes liquidity indicators, large-in-scale thresholds, and market structure metrics.
          </p>
        </div>

        ${yearData.length > 0 ? `
        <!-- Annual Liquidity Assessment -->
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="font-semibold text-gray-900 mb-4">Annual Liquidity Assessment</h3>
          ${yearData.map((calc: any) => `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div class="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-lg text-center">
                <div class="text-sm font-medium text-green-700">Liquidity Status</div>
                <div class="text-xl font-bold ${calc.liquidity ? 'text-green-600' : 'text-red-600'}">
                  ${calc.liquidity ? 'LIQUID' : 'ILLIQUID'}
                </div>
              </div>
              
              ${calc.raw_data?.AvrgDalyTrnvr ? `
              <div class="bg-blue-50 p-4 rounded-lg text-center">
                <div class="text-sm font-medium text-blue-700">Avg Daily Turnover</div>
                <div class="text-lg font-bold text-blue-600">€${this.formatCurrency(calc.raw_data.AvrgDalyTrnvr)}</div>
              </div>
              ` : ''}
              
              ${calc.raw_data?.AvrgDalyNbOfTxs ? `
              <div class="bg-purple-50 p-4 rounded-lg text-center">
                <div class="text-sm font-medium text-purple-700">Avg Daily Transactions</div>
                <div class="text-lg font-bold text-purple-600">${formatNumber(calc.raw_data.AvrgDalyNbOfTxs)}</div>
              </div>
              ` : ''}
              
              ${calc.raw_data?.AvrgTxVal ? `
              <div class="bg-orange-50 p-4 rounded-lg text-center">
                <div class="text-sm font-medium text-orange-700">Avg Transaction Value</div>
                <div class="text-lg font-bold text-orange-600">€${this.formatCurrency(calc.raw_data.AvrgTxVal)}</div>
              </div>
              ` : ''}
            </div>
            
            <!-- Market Structure Thresholds -->
            ${calc.raw_data?.LrgInScale || calc.raw_data?.StdMktSz ? `
            <div class="mt-4 bg-gray-50 p-4 rounded-lg">
              <h4 class="font-medium text-gray-900 mb-3">Market Structure Thresholds</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                ${calc.raw_data?.LrgInScale ? `
                <div>
                  <span class="text-sm text-gray-600">Large-in-Scale (LIS) Threshold:</span>
                  <span class="ml-2 font-semibold">€${this.formatCurrency(calc.raw_data.LrgInScale)}</span>
                </div>
                ` : ''}
                ${calc.raw_data?.StdMktSz ? `
                <div>
                  <span class="text-sm text-gray-600">Standard Market Size:</span>
                  <span class="ml-2 font-semibold">€${this.formatCurrency(calc.raw_data.StdMktSz)}</span>
                </div>
                ` : ''}
              </div>
            </div>
            ` : ''}
          `).join('')}
        </div>
        ` : ''}

        ${sintData.length > 0 ? `
        <!-- Semi-Annual Trading Activity -->
        <div class="bg-white border border-gray-200 rounded-lg p-6">
          <h3 class="font-semibold text-gray-900 mb-4">Semi-Annual Trading Activity</h3>
          <div class="space-y-4">
            ${sintData.map((calc: any) => `
              <div class="border border-gray-100 rounded-lg p-4">
                <div class="flex justify-between items-center mb-3">
                  <h4 class="font-medium text-gray-900">
                    ${this.formatDateRange(calc.from_date, calc.to_date)}
                  </h4>
                  <span class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">SINT</span>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div class="text-center p-3 bg-blue-50 rounded">
                    <div class="text-xl font-bold text-blue-600">${formatNumber(calc.total_transactions_executed || 0)}</div>
                    <div class="text-sm text-blue-700">Total Transactions</div>
                  </div>
                  <div class="text-center p-3 bg-green-50 rounded">
                    <div class="text-xl font-bold text-green-600">€${this.formatCurrency(calc.total_volume_executed || 0)}</div>
                    <div class="text-sm text-green-700">Total Volume</div>
                  </div>
                  <div class="text-center p-3 bg-purple-50 rounded">
                    <div class="text-xl font-bold text-purple-600">
                      €${calc.total_transactions_executed > 0 ? this.formatCurrency((calc.total_volume_executed || 0) / calc.total_transactions_executed) : '0'}
                    </div>
                    <div class="text-sm text-purple-700">Avg per Transaction</div>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
          
          <!-- Trading Trend Visualization -->
          ${sintData.length > 1 ? `
          <div class="mt-6 p-4 bg-gray-50 rounded-lg">
            <h4 class="font-medium text-gray-900 mb-3">Volume Trend Analysis</h4>
            <div class="text-sm text-gray-600">
              ${this.calculateTrendInsight(sintData)}
            </div>
          </div>
          ` : ''}
        </div>
        ` : ''}

        <!-- Data Summary -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="font-semibold text-gray-900 mb-2">Data Summary</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span class="text-gray-600">Total Records:</span>
              <span class="ml-2 font-semibold">${transparency.length}</span>
            </div>
            <div>
              <span class="text-gray-600">Annual Assessments:</span>
              <span class="ml-2 font-semibold">${yearData.length}</span>
            </div>
            <div>
              <span class="text-gray-600">Semi-Annual Periods:</span>
              <span class="ml-2 font-semibold">${sintData.length}</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  private formatCurrency(value: number): string {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K';
    }
    return value.toLocaleString();
  }

  private formatDateRange(fromDate: string, toDate: string): string {
    const from = new Date(fromDate);
    const to = new Date(toDate);
    return `${from.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })} - ${to.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}`;
  }

  private calculateTrendInsight(data: any[]): string {
    if (data.length < 2) return 'Insufficient data for trend analysis';
    
    const volumes = data.map(d => d.total_volume_executed || 0);
    const transactions = data.map(d => d.total_transactions_executed || 0);
    
    const volumeTrend = volumes[volumes.length - 1] > volumes[0] ? 'increasing' : 'decreasing';
    const transactionTrend = transactions[transactions.length - 1] > transactions[0] ? 'increasing' : 'decreasing';
    
    const volumeChange = ((volumes[volumes.length - 1] - volumes[0]) / volumes[0] * 100).toFixed(1);
    const transactionChange = ((transactions[transactions.length - 1] - transactions[0]) / transactions[0] * 100).toFixed(1);
    
    return `Trading volume is ${volumeTrend} (${volumeChange}% change) and transaction count is ${transactionTrend} (${transactionChange}% change) across the reporting periods.`;
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
