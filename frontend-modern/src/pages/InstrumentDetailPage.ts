import { BasePage } from './BasePage';
import { ApiServiceFactory, InstrumentService } from '../services';
import type { InstrumentDetail } from '../types/api';

/**
 * Detailed Instrument Page
 * Comprehensive instrument data display with transparency, venues, and CFI decoding
 */
export default class InstrumentDetailPage extends BasePage {
  private instrumentService: InstrumentService;
  private isin: string;

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    super(container, params);
    this.instrumentService = ApiServiceFactory.getInstance().instruments;
    this.isin = params.isin || '';
    
    if (!this.isin) {
      throw new Error('ISIN parameter is required for InstrumentDetailPage');
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
              <span class="text-gray-600">Loading instrument details...</span>
            </div>
          </div>
        </div>
      </div>
    `;

    this.setupEventListeners();
    await this.loadInstrumentData();
  }

  private setupEventListeners(): void {
    // Set up navigation buttons
    const backBtn = this.container.querySelector('#back-btn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.history.back();
      });
    }

    const refreshBtn = this.container.querySelector('#refresh-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        this.loadInstrumentData();
      });
    }
  }

  private async loadInstrumentData(): Promise<void> {
    const mainContent = this.container.querySelector('#main-content');
    if (!mainContent) return;

    // Show loading state
    mainContent.innerHTML = `
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div class="flex items-center justify-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
          <span class="text-gray-600">Loading instrument details...</span>
        </div>
      </div>
    `;

    try {
      // Load instrument details (CFI info is included in the main response)
      const [instrumentResponse, venuesResponse] = await Promise.allSettled([
        this.instrumentService.getInstrument(this.isin),
        this.instrumentService.getInstrumentVenues(this.isin)
      ]);

      // Check if the main instrument request succeeded
      if (instrumentResponse.status === 'fulfilled' && instrumentResponse.value.status === 'success' && instrumentResponse.value.data) {
        this.renderInstrumentDetails(
          instrumentResponse.value.data,
          venuesResponse.status === 'fulfilled' && venuesResponse.value.status === 'success' ? venuesResponse.value.data : []
        );
      } else {
        // Try to get more specific error information
        let errorMessage = 'Instrument not found or failed to load';
        if (instrumentResponse.status === 'fulfilled' && instrumentResponse.value.status === 'error') {
          errorMessage = `Instrument ${this.isin} not found in database`;
        } else if (instrumentResponse.status === 'rejected') {
          errorMessage = `Network error loading instrument ${this.isin}`;
        }
        this.showError(errorMessage);
      }
    } catch (error) {
      console.error('Error loading instrument data:', error);
      console.error('ISIN:', this.isin);
      this.showError(`Error loading instrument data for ${this.isin}. Please check if this ISIN exists in the database.`);
    }
  }

  private renderInstrumentDetails(instrument: InstrumentDetail, venues: any[] = []): void {
    const mainContent = this.container.querySelector('#main-content');
    if (!mainContent) return;

    mainContent.innerHTML = `
      <div class="space-y-6">
        <!-- Header with Navigation -->
        ${this.renderHeader(instrument)}

        <!-- Summary Status and Statistics -->
        ${this.renderSummarySection(instrument)}

        <!-- Basic Information -->
        ${this.renderBasicInfoSection(instrument)}

        <!-- Type-Specific Attributes -->
        ${this.renderTypeSpecificSection(instrument)}

        <!-- Primary Venue Display -->
        ${(instrument as any).primary_venue_display ? this.renderPrimaryVenueSection((instrument as any).primary_venue_display) : ''}

        <!-- FIGI Information -->
        ${(instrument as any).figi_mappings && (instrument as any).figi_mappings.length > 0 ? this.renderFigiSection(instrument) : ''}

        <!-- CFI Classification -->
        ${this.renderCfiSection(instrument.cfi_decoded, instrument.cfi_code)}

        <!-- Legal Entity Information -->
        ${instrument.legal_entity ? this.renderLegalEntitySection(instrument.legal_entity) : ''}

        <!-- Trading Venues -->
        ${venues.length > 0 ? this.renderVenuesSection(venues) : ''}

        <!-- Type-Specific Details (Placeholders) -->
        ${this.renderDetailsSection(instrument)}
      </div>
    `;
    
    // Set up event listeners after content is rendered
    this.setupEventListeners();
  }

  private renderHeader(instrument: any): string {
    return `
      <div class="bg-white shadow-sm border border-gray-200 rounded-lg">
        <div class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <button id="back-btn" class="text-gray-600 hover:text-gray-900">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
              </button>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">${instrument.full_name || instrument.short_name}</h1>
                <div class="flex items-center space-x-4 mt-1">
                  <p class="text-sm text-gray-500 font-mono">ISIN: ${instrument.isin}</p>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${this.getTypeColor(instrument.instrument_type)}">
                    ${this.formatInstrumentType(instrument.instrument_type)}
                  </span>
                </div>
              </div>
            </div>
            <div class="flex space-x-3">
              <button id="refresh-btn" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
                Refresh
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  private renderSummarySection(instrument: any): string {
    return this.createCard(`
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600">${instrument.trading_venues_count || 0}</div>
          <div class="text-sm text-gray-500">Trading Venues</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">${instrument.status_indicators ? instrument.status_indicators.length : 0}</div>
          <div class="text-sm text-gray-500">Status Indicators</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-purple-600">${instrument.figi_mappings ? instrument.figi_mappings.length : 0}</div>
          <div class="text-sm text-gray-500">FIGI Mappings</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold ${instrument.cfi_code ? 'text-indigo-600' : 'text-gray-400'}">${instrument.cfi_code ? '✓' : '✗'}</div>
          <div class="text-sm text-gray-500">CFI Classified</div>
        </div>
      </div>
      ${instrument.status_indicators && instrument.status_indicators.length > 0 ? `
      <div class="mt-6">
        <h4 class="text-sm font-medium text-gray-700 mb-2">Status Indicators</h4>
        <div class="flex flex-wrap gap-2">
          ${instrument.status_indicators.map((status: string) => `
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${status.includes('[OK]') ? 'bg-green-100 text-green-800' : status.includes('[FIGI]') ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}">
              ${status}
            </span>
          `).join('')}
        </div>
      </div>
      ` : ''}
    `, 'Summary & Status');
  }

  private renderBasicInfoSection(instrument: any): string {
    return this.createCard(`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Full Name</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.full_name || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Short Name</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.short_name || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Currency</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.currency || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">LEI ID</label>
            <p class="mt-1 text-sm font-mono text-gray-900">${instrument.lei_id || 'N/A'}</p>
          </div>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Competent Authority</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.competent_authority || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Relevant Trading Venue</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.relevant_trading_venue || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Publication Date</label>
            <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.publication_from_date) || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Commodity Derivative</label>
            <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${instrument.commodity_derivative_indicator ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}">
              ${instrument.commodity_derivative_indicator ? 'Yes' : 'No'}
            </span>
          </div>
        </div>
      </div>
    `, 'Basic Information');
  }

  private renderPrimaryVenueSection(primaryVenue: any): string {
    return this.createCard(`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">MIC Code</label>
            <p class="mt-1 text-sm font-mono text-gray-900">${primaryVenue.mic_code || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Market Name</label>
            <p class="mt-1 text-sm text-gray-900">${primaryVenue.market_name || 'N/A'}</p>
          </div>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Country Code</label>
            <p class="mt-1 text-sm text-gray-900">${primaryVenue.country_code || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Status</label>
            <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${primaryVenue.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
              ${primaryVenue.status || 'Unknown'}
            </span>
          </div>
        </div>
      </div>
    `, 'Primary Trading Venue');
  }

  private renderFigiSection(instrument: any): string {
    const firstFigi = instrument.figi_mappings[0];
    return this.createCard(`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">FIGI</label>
            <p class="mt-1 text-sm font-mono text-gray-900">${instrument.figi || firstFigi?.figi || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Composite FIGI</label>
            <p class="mt-1 text-sm font-mono text-gray-900">${instrument.composite_figi || firstFigi?.composite_figi || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Share Class FIGI</label>
            <p class="mt-1 text-sm font-mono text-gray-900">${instrument.share_class_figi || firstFigi?.share_class_figi || 'N/A'}</p>
          </div>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Security Type</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.security_type || firstFigi?.security_type || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Market Sector</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.market_sector || firstFigi?.market_sector || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Ticker</label>
            <p class="mt-1 text-sm text-gray-900">${instrument.ticker || firstFigi?.ticker || 'N/A'}</p>
          </div>
        </div>
      </div>
    `, 'FIGI Information');
  }

  private renderDetailsSection(instrument: any): string {
    const instrumentType = instrument.instrument_type?.toLowerCase();
    const detailsKey = `${instrumentType}_details`;
    const details = (instrument as any)[detailsKey];
    
    if (!details) return '';

    return this.createCard(`
      <div class="text-center py-8">
        <div class="text-gray-400 mb-4">
          <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-6a2 2 0 01-2-2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">${this.formatInstrumentType(instrumentType)} Analytics</h3>
        <p class="text-gray-500 mb-4">Advanced analytics and insights for this ${instrumentType} instrument</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          ${Object.entries(details).map(([key, value]) => `
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="font-medium text-gray-700">${this.formatAttributeName(key)}</div>
              <div class="text-gray-500 mt-1">${value === 'placeholder' ? 'Coming Soon' : value}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `, `${this.formatInstrumentType(instrumentType)} Details`);
  }

  private renderCfiSection(cfiDecoded: any, cfiCode?: string): string {
    // If we have CFI decoded info from the API, use it
    if (cfiDecoded && cfiDecoded.cfi_code) {
      return this.createCard(`
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">CFI Code</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${cfiDecoded.cfi_code}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Category</label>
              <p class="mt-1 text-sm text-gray-900">${cfiDecoded.category_description || cfiDecoded.category || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Group</label>
              <p class="mt-1 text-sm text-gray-900">${cfiDecoded.group_description || cfiDecoded.group || 'N/A'}</p>
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Attributes Code</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${cfiDecoded.attributes || 'N/A'}</p>
            </div>
            ${cfiDecoded.decoded_attributes ? `
            <div>
              <label class="block text-sm font-medium text-gray-700">Voting Rights</label>
              <p class="mt-1 text-sm text-gray-900">${cfiDecoded.decoded_attributes.voting_rights || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Payment Status</label>
              <p class="mt-1 text-sm text-gray-900">${cfiDecoded.decoded_attributes.payment_status || 'N/A'}</p>
            </div>
            ` : ''}
          </div>
        </div>
        ${cfiDecoded.decoded_attributes ? `
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-700 mb-3">Detailed CFI Attributes</label>
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              ${Object.entries(cfiDecoded.decoded_attributes).map(([key, value]) => `
                <div>
                  <span class="font-medium text-gray-700">${this.formatAttributeName(key)}:</span>
                  <span class="text-gray-900 ml-2">${value}</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
        ` : ''}
      `, 'CFI Classification');
    }
    
    // If we only have the CFI code from the instrument data
    if (cfiCode) {
      return this.createCard(`
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">CFI Code</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${cfiCode}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Category</label>
              <p class="mt-1 text-sm text-gray-900">${this.decodeCfiCategory(cfiCode)}</p>
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Status</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                CFI API Unavailable
              </span>
            </div>
          </div>
        </div>
      `, 'CFI Classification');
    }
    
    // No CFI information available
    return this.createCard(`
      <div class="text-center py-8">
        <p class="text-gray-500">No CFI classification data available</p>
      </div>
    `, 'CFI Classification');
  }

  private renderTypeSpecificSection(instrument: any): string {
    const instrumentType = instrument.instrument_type?.toLowerCase();
    
    // Equity-specific information
    if (instrumentType === 'equity' && instrument.equity_attributes) {
      return this.createCard(`
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Equity Type</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.equity_attributes.equity_type || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Enhanced Rights</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${instrument.equity_attributes.has_enhanced_rights ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
                ${instrument.equity_attributes.has_enhanced_rights ? 'Yes' : 'No'}
              </span>
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Classification</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.equity_attributes.classification_type || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Description</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.equity_attributes.instrument_description || 'N/A'}</p>
            </div>
          </div>
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }
    
    // Option-specific information
    if (instrumentType === 'option' && instrument.option_attributes) {
      return this.createCard(`
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Option Type</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${instrument.option_attributes.option_type === 'CALL' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                ${instrument.option_attributes.option_type_description || instrument.option_attributes.option_type || 'N/A'}
              </span>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Exercise Style</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.option_attributes.exercise_style_description || instrument.option_attributes.exercise_style || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Price Multiplier</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.option_attributes.price_multiplier || 'N/A'}</p>
            </div>
            ${instrument.option_attributes.underlying_isin ? `
            <div>
              <label class="block text-sm font-medium text-gray-700">Underlying Asset</label>
              <p class="mt-1 text-sm text-gray-900 font-mono text-blue-600 hover:text-blue-800 cursor-pointer" 
                 onclick="window.router.navigateTo('/instruments/${instrument.option_attributes.underlying_isin}')"
                 title="Click to view underlying instrument">
                ${instrument.option_attributes.underlying_isin}
              </p>
            </div>
            ` : ''}
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Expiration Date</label>
              <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.option_attributes.expiration_date) || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">First Trade Date</label>
              <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.option_attributes.first_trade_date) || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Option Category</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.option_attributes.option_category || 'N/A'}</p>
            </div>
          </div>
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }
    
    // Debt-specific information  
    if (instrumentType === 'debt' && instrument.debt_attributes) {
      return this.createCard(`
        <div class="space-y-6">
          <!-- Primary Debt Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Debt Type</label>
              <p class="mt-1 text-sm text-gray-900 font-medium">${instrument.debt_attributes.debt_type || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Interest Rate</label>
              <p class="mt-1 text-sm text-gray-900 font-mono text-lg ${instrument.debt_attributes.fixed_interest_rate ? 'text-green-600' : 'text-gray-500'}">${instrument.debt_attributes.fixed_interest_rate ? instrument.debt_attributes.fixed_interest_rate + '%' : 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Seniority</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${instrument.debt_attributes.seniority === 'Senior' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}">
                ${instrument.debt_attributes.seniority || instrument.debt_attributes.seniority_code || 'N/A'}
              </span>
            </div>
          </div>
          
          <!-- Maturity and Time Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Maturity Date</label>
              <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.debt_attributes.maturity_date) || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Years to Maturity</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.debt_attributes.years_to_maturity ? instrument.debt_attributes.years_to_maturity + ' years' : 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Days to Maturity</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.debt_attributes.days_to_maturity ? this.formatNumber(instrument.debt_attributes.days_to_maturity) + ' days' : 'N/A'}</p>
            </div>
          </div>
          
          <!-- Issuance Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Nominal Value per Unit</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.debt_attributes.nominal_value_per_unit ? this.formatCurrency(instrument.debt_attributes.nominal_value_per_unit, instrument.currency) : 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Total Issued Amount</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.debt_attributes.total_issued_nominal_amount ? this.formatCurrency(instrument.debt_attributes.total_issued_nominal_amount, instrument.currency) : 'N/A'}</p>
            </div>
          </div>
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }

    // Future-specific information
    if (instrumentType === 'future' && instrument.future_attributes) {
      return this.createCard(`
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Contract Type</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.future_attributes.contract_type || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Expiration Date</label>
              <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.future_attributes.expiration_date) || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Price Multiplier</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.future_attributes.price_multiplier || 'N/A'}</p>
            </div>
            ${instrument.future_attributes.underlying_isin ? `
            <div>
              <label class="block text-sm font-medium text-gray-700">Underlying Asset</label>
              <p class="mt-1 text-sm text-gray-900 font-mono text-blue-600 hover:text-blue-800 cursor-pointer" 
                 onclick="window.router.navigateTo('/instruments/${instrument.future_attributes.underlying_isin}')"
                 title="Click to view underlying instrument">
                ${instrument.future_attributes.underlying_isin}
              </p>
            </div>
            ` : ''}
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Delivery Type</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.future_attributes.delivery_type || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Contract Unit</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.future_attributes.contract_unit || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Contract Value</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.future_attributes.contract_value || 'N/A'}</p>
            </div>
          </div>
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }

    // Forward-specific information
    if (instrumentType === 'forward' && instrument.forward_attributes) {
      return this.createCard(`
        <div class="space-y-6">
          <!-- Forward Contract Overview -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Forward Type</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                ${instrument.forward_attributes.forward_type || 'Forward Contract'}
              </span>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Settlement Type</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${instrument.forward_attributes.settlement_type === 'CASH' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}">
                ${instrument.forward_attributes.settlement_description || instrument.forward_attributes.settlement_type || 'N/A'}
              </span>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Price Multiplier</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.forward_attributes.price_multiplier || 'N/A'}</p>
            </div>
          </div>

          <!-- Time Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Expiration Date</label>
              <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.forward_attributes.expiration_date) || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Years to Expiry</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.forward_attributes.years_to_expiry ? instrument.forward_attributes.years_to_expiry + ' years' : 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Term Classification</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${instrument.forward_attributes.term_classification === 'Long Term' ? 'bg-purple-100 text-purple-800' : instrument.forward_attributes.term_classification === 'Short Term' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'}">
                ${instrument.forward_attributes.term_classification || 'N/A'}
              </span>
            </div>
          </div>

          ${instrument.forward_attributes.underlying_summary ? `
          <!-- Underlying Assets -->
          <div class="bg-orange-50 rounded-lg p-4">
            <h4 class="text-sm font-medium text-orange-900 mb-3">Underlying Assets</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-orange-700">Asset Summary</label>
                <p class="mt-1 text-sm text-orange-900">${instrument.forward_attributes.underlying_summary}</p>
              </div>
              ${instrument.forward_attributes.underlying_isin ? `
              <div>
                <label class="block text-xs font-medium text-orange-700">Single Underlying</label>
                <p class="mt-1 text-sm text-orange-900 font-mono text-blue-600 hover:text-blue-800 cursor-pointer" 
                   onclick="window.router.navigateTo('/instruments/${instrument.forward_attributes.underlying_isin}')"
                   title="Click to view underlying instrument">
                  ${instrument.forward_attributes.underlying_isin}
                </p>
              </div>
              ` : ''}
              ${instrument.forward_attributes.basket_isin ? `
              <div>
                <label class="block text-xs font-medium text-orange-700">Basket ISIN</label>
                <p class="mt-1 text-sm text-orange-900 font-mono text-blue-600 hover:text-blue-800 cursor-pointer" 
                   onclick="window.router.navigateTo('/instruments/${instrument.forward_attributes.basket_isin}')"
                   title="Click to view basket composition">
                  ${instrument.forward_attributes.basket_isin}
                </p>
              </div>
              ` : ''}
              ${instrument.forward_attributes.basket_size ? `
              <div>
                <label class="block text-xs font-medium text-orange-700">Basket Size</label>
                <p class="mt-1 text-sm text-orange-900 font-mono">${instrument.forward_attributes.basket_size} assets</p>
              </div>
              ` : ''}
            </div>
          </div>
          ` : ''}

          ${instrument.forward_attributes.currency_pair || instrument.forward_attributes.fx_type ? `
          <!-- FX Forward Specifics -->
          <div class="bg-green-50 rounded-lg p-4">
            <h4 class="text-sm font-medium text-green-900 mb-3">Foreign Exchange Details</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${instrument.forward_attributes.currency_pair ? `
              <div>
                <label class="block text-xs font-medium text-green-700">Currency Pair</label>
                <p class="mt-1 text-sm text-green-900 font-mono text-lg">${instrument.forward_attributes.currency_pair}</p>
              </div>
              ` : ''}
              ${instrument.forward_attributes.fx_type ? `
              <div>
                <label class="block text-xs font-medium text-green-700">FX Type</label>
                <p class="mt-1 text-sm text-green-900">${instrument.forward_attributes.fx_type}</p>
              </div>
              ` : ''}
            </div>
          </div>
          ` : ''}

          ${instrument.forward_attributes.reference_rate || instrument.forward_attributes.interest_term ? `
          <!-- Interest Rate Forward Specifics -->
          <div class="bg-blue-50 rounded-lg p-4">
            <h4 class="text-sm font-medium text-blue-900 mb-3">Interest Rate Details</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              ${instrument.forward_attributes.reference_rate ? `
              <div>
                <label class="block text-xs font-medium text-blue-700">Reference Rate</label>
                <p class="mt-1 text-sm text-blue-900 font-mono">${instrument.forward_attributes.reference_rate}</p>
              </div>
              ` : ''}
              ${instrument.forward_attributes.interest_term ? `
              <div>
                <label class="block text-xs font-medium text-blue-700">Interest Term</label>
                <p class="mt-1 text-sm text-blue-900">${instrument.forward_attributes.interest_term}</p>
              </div>
              ` : ''}
            </div>
          </div>
          ` : ''}

          <!-- Additional Forward Details -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Classification</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.forward_attributes.classification || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Days to Expiry</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.forward_attributes.days_to_expiry ? this.formatNumber(instrument.forward_attributes.days_to_expiry) + ' days' : 'N/A'}</p>
            </div>
          </div>
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }

    // Swap-specific information
    if (instrumentType === 'swap' && instrument.swap_attributes) {
      const isInterestRateSwap = instrument.swap_attributes.swap_category === 'Interest Rate';
      const isCreditSwap = instrument.swap_attributes.swap_category === 'Credit';
      const isOISSwap = instrument.swap_attributes.swap_type === 'OIS Interest Rate Swap';
      
      return this.createCard(`
        <div class="space-y-6">
          <!-- Primary Swap Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Swap Type</label>
              <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${isCreditSwap ? 'bg-red-100 text-red-800' : isOISSwap ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}">
                ${instrument.swap_attributes.swap_type || 'N/A'}
              </span>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Classification</label>
              <p class="mt-1 text-sm text-gray-900 font-medium">${instrument.swap_attributes.classification || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Settlement</label>
              <p class="mt-1 text-sm text-gray-900">${instrument.swap_attributes.settlement_description || instrument.swap_attributes.settlement_type || 'N/A'}</p>
            </div>
          </div>

          <!-- Expiry and Time Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Expiration Date</label>
              <p class="mt-1 text-sm text-gray-900">${this.formatDate(instrument.swap_attributes.expiration_date) || 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Years to Expiry</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.swap_attributes.years_to_expiry ? instrument.swap_attributes.years_to_expiry + ' years' : 'N/A'}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Days to Expiry</label>
              <p class="mt-1 text-sm text-gray-900 font-mono">${instrument.swap_attributes.days_to_expiry ? this.formatNumber(instrument.swap_attributes.days_to_expiry) + ' days' : 'N/A'}</p>
            </div>
          </div>

          ${isInterestRateSwap ? `
          <!-- Interest Rate Swap Specifics -->
          <div class="bg-blue-50 rounded-lg p-4">
            <h4 class="text-sm font-medium text-blue-900 mb-3">${isOISSwap ? 'Overnight Index Swap (OIS) Details' : 'Interest Rate Details'}</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-medium text-blue-700">Reference Index</label>
                <p class="mt-1 text-sm text-blue-900 font-mono">${instrument.swap_attributes.reference_index || 'N/A'}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-blue-700">${isOISSwap ? 'Tenor' : 'Floating Term'}</label>
                <p class="mt-1 text-sm text-blue-900">${instrument.swap_attributes.floating_term || 'N/A'}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-blue-700">${isOISSwap ? 'Compounding Frequency' : 'Rate Frequency'}</label>
                <p class="mt-1 text-sm text-blue-900">${instrument.swap_attributes.reference_rate_frequency || 'N/A'}</p>
              </div>
            </div>
            ${isOISSwap ? `
            <div class="mt-3 p-3 bg-purple-50 border border-purple-200 rounded-lg">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <span class="w-5 h-5 bg-purple-100 rounded-full flex items-center justify-center">
                    <span class="text-xs font-bold text-purple-600">OIS</span>
                  </span>
                </div>
                <div class="ml-3">
                  <p class="text-xs text-purple-800">
                    <strong>Overnight Index Swap:</strong> Exchanges fixed rate for compounded overnight rate (${instrument.swap_attributes.reference_index}) over ${instrument.swap_attributes.floating_term} term
                  </p>
                </div>
              </div>
            </div>
            ` : ''}
          </div>
          ` : ''}

          ${isCreditSwap && instrument.swap_attributes.underlying_basket_isin ? `
          <!-- Credit Default Swap Specifics -->
          <div class="bg-red-50 rounded-lg p-4">
            <h4 class="text-sm font-medium text-red-900 mb-3">Credit Basket Information</h4>
            <div>
              <label class="block text-xs font-medium text-red-700">Underlying Basket</label>
              <p class="mt-1 text-sm text-red-900 font-mono text-blue-600 hover:text-blue-800 cursor-pointer" 
                 onclick="window.router.navigateTo('/instruments/${instrument.swap_attributes.underlying_basket_isin}')"
                 title="Click to view basket composition">
                ${instrument.swap_attributes.underlying_basket_isin}
              </p>
            </div>
          </div>
          ` : ''}
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }
    
    // For other instrument types, show basic information or attributes if available
    const attributeKey = `${instrumentType}_attributes`;
    const attributes = (instrument as any)[attributeKey];
    
    if (attributes && typeof attributes === 'object') {
      return this.createCard(`
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          ${Object.entries(attributes).map(([key, value]) => `
            <div>
              <label class="block text-sm font-medium text-gray-700">${this.formatAttributeName(key)}</label>
              <p class="mt-1 text-sm text-gray-900">${typeof value === 'boolean' ? (value ? 'Yes' : 'No') : (value || 'N/A')}</p>
            </div>
          `).join('')}
        </div>
      `, `${this.formatInstrumentType(instrumentType)} Details`);
    }
    
    return this.createCard(`
      <div class="text-center py-8">
        <p class="text-gray-500">Type-specific details for ${this.formatInstrumentType(instrumentType)} instruments</p>
        ${instrument.processed_attributes ? `
        <div class="mt-4">
          <button class="text-blue-600 hover:text-blue-800 text-sm" onclick="document.querySelector('#processed-attributes').scrollIntoView()">
            View processed attributes below ↓
          </button>
        </div>
        ` : ''}
      </div>
    `, `${this.formatInstrumentType(instrumentType)} Details`);
  }

  private renderLegalEntitySection(legalEntity: any): string {
    return this.createCard(`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">LEI</label>
            <p class="mt-1 text-sm font-mono text-gray-900">${legalEntity.lei || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Legal Name</label>
            <p class="mt-1 text-sm text-gray-900">${legalEntity.name || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Jurisdiction</label>
            <p class="mt-1 text-sm text-gray-900">${legalEntity.jurisdiction || 'N/A'}</p>
          </div>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Status</label>
            <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${legalEntity.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
              ${legalEntity.status || legalEntity.entity_status || 'N/A'}
            </span>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Legal Form</label>
            <p class="mt-1 text-sm text-gray-900 font-mono">${legalEntity.legal_form || 'N/A'}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Creation Date</label>
            <p class="mt-1 text-sm text-gray-900">${this.formatDate(legalEntity.creation_date) || 'N/A'}</p>
          </div>
        </div>
      </div>
    `, 'Legal Entity Information');
  }

  private renderVenuesSection(venues: any[]): string {
    return this.createCard(`
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">MIC</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Segment</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            ${venues.map(venue => `
              <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">${venue.mic || 'N/A'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${venue.name || 'N/A'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${venue.country || 'N/A'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${venue.segment || 'N/A'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `, 'Trading Venues');
  }



  private formatDate(value?: string): string {
    if (!value) return '';
    try {
      return new Date(value).toLocaleDateString();
    } catch {
      return value;
    }
  }

  private formatInstrumentType(type?: string): string {
    if (!type) return 'Unknown';
    return type
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  private decodeCfiCategory(cfiCode: string): string {
    if (!cfiCode || cfiCode.length === 0) return 'N/A';
    
    const categoryMap: Record<string, string> = {
      'E': 'Equities',
      'D': 'Debt instruments',
      'C': 'Collective investment vehicles',
      'R': 'Entitlements (rights)',
      'O': 'Options',
      'F': 'Futures',
      'S': 'Swaps',
      'H': 'Non-standardized derivatives',
      'I': 'Spot',
      'J': 'Forwards',
      'K': 'Strategies',
      'L': 'Financing',
      'T': 'Referential instruments',
      'M': 'Others/miscellaneous'
    };
    
    const category = cfiCode.charAt(0).toUpperCase();
    return categoryMap[category] || `Unknown category (${category})`;
  }

  private formatAttributeName(key: string): string {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
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

  protected showError(message: string): void {
    const mainContent = this.container.querySelector('#main-content');
    if (mainContent) {
      mainContent.innerHTML = `
        <div class="bg-white rounded-lg shadow-sm border border-red-200 p-8">
          <div class="flex items-center justify-center text-red-600">
            <svg class="w-8 h-8 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span class="text-lg">${message}</span>
          </div>
        </div>
      `;
    }
  }

  private formatNumber(value: number): string {
    return new Intl.NumberFormat().format(value);
  }

  private formatCurrency(value: number, currency?: string): string {
    const currencyCode = currency || 'EUR';
    try {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currencyCode,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    } catch {
      return `${this.formatNumber(value)} ${currencyCode}`;
    }
  }
}