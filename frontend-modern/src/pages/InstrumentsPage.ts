import { BasePage } from './BasePage';
import { ApiServiceFactory, InstrumentService } from '../services';
import type { Instrument } from '../types/api';

/**
 * Instruments Hub Page
 * Comprehensive instrument listing and analysis
 */
export default class InstrumentsPage extends BasePage {
  private instrumentService: InstrumentService;
  private currentFilters: {
    type?: string;
    currency?: string;
    isin?: string;
  } = {};
  private availableTypes: string[] = [];

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    super(container, params);
    this.instrumentService = ApiServiceFactory.getInstance().instruments;
  }
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      ${this.createSectionHeader('Instruments Hub', 'Comprehensive instrument analysis with type-specific attributes and CFI decoding')}
      
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
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody id="instruments-tbody" class="bg-white divide-y divide-gray-200">
              <tr>
                <td colspan="9" class="px-6 py-8 text-center text-gray-500">
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

    // Setup event listeners
    this.setupEventListeners();

    // Load instrument types and initial data
    await this.loadInstrumentTypes();
    this.loadInstrumentsList();
  }

  private setupEventListeners(): void {
    const searchBtn = this.container.querySelector('#search-btn') as HTMLButtonElement;
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        this.updateFiltersFromForm();
        this.loadInstrumentsList();
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
        <td colspan="9" class="px-6 py-8 text-center text-gray-500">
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
          <td colspan="9" class="px-6 py-8 text-center text-gray-500">
            No instruments found matching your criteria.
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = instruments.map(instrument => `
      <tr class="hover:bg-gray-50">
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
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
          <a href="#" data-route="/instruments/${instrument.isin}" class="text-blue-600 hover:text-blue-900">View Details</a>
        </td>
      </tr>
    `).join('');
  }

  private showInstrumentError(message: string): void {
    const tbody = this.container.querySelector('#instruments-tbody');
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="px-6 py-8 text-center text-red-500">
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