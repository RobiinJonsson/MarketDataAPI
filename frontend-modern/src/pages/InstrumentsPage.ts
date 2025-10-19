import { BasePage } from './BasePage';
import { InstrumentService } from '../services/InstrumentService';
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

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    super(container, params);
    this.instrumentService = new InstrumentService();
  }
  
  async render(): Promise<void> {
    this.container.innerHTML = `
      ${this.createSectionHeader('Instruments Hub', 'Comprehensive instrument analysis with type-specific attributes and CFI decoding')}
      
      <!-- Quick Filters -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Instrument Type</label>
            <select class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">All Types</option>
              <option value="equity">Equity</option>
              <option value="debt">Debt</option>
              <option value="future">Future</option>
              <option value="option">Option</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Currency</label>
            <select class="w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">All Currencies</option>
              <option value="EUR">EUR</option>
              <option value="USD">USD</option>
              <option value="GBP">GBP</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Search ISIN</label>
            <input type="text" placeholder="e.g. SE0000108656" class="w-full border border-gray-300 rounded-md px-3 py-2">
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
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Currency</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody id="instruments-tbody" class="bg-white divide-y divide-gray-200">
              <tr>
                <td colspan="6" class="px-6 py-8 text-center text-gray-500">
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

    // Load initial data
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
    const typeSelect = this.container.querySelector('select:nth-child(1)') as HTMLSelectElement;
    const currencySelect = this.container.querySelector('select:nth-child(2)') as HTMLSelectElement;
    const isinInput = this.container.querySelector('input[type="text"]') as HTMLInputElement;

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
        <td colspan="6" class="px-6 py-8 text-center text-gray-500">
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
          <td colspan="6" class="px-6 py-8 text-center text-gray-500">
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
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${instrument.full_name || instrument.short_name || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${this.getTypeColor(instrument.instrument_type)}">
            ${this.formatInstrumentType(instrument.instrument_type)}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${instrument.legal_entity?.jurisdiction || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${instrument.currency || 'N/A'}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
          <a href="#" data-route="/instruments/${instrument.isin}" class="text-blue-600 hover:text-blue-900">View Details</a>
        </td>
      </tr>
    `).join('');
  }

  private getTypeColor(type?: string): string {
    switch (type?.toLowerCase()) {
      case 'equity': return 'bg-blue-100 text-blue-800';
      case 'debt': return 'bg-green-100 text-green-800';
      case 'future': return 'bg-purple-100 text-purple-800';
      case 'option': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  private formatInstrumentType(type?: string): string {
    if (!type) return 'Unknown';
    return type.charAt(0).toUpperCase() + type.slice(1);
  }

  private showInstrumentError(message: string): void {
    const tbody = this.container.querySelector('#instruments-tbody');
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="6" class="px-6 py-8 text-center text-red-500">
            <div class="flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.268 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
              ${message}
            </div>
          </td>
        </tr>
      `;
    }
  }
}