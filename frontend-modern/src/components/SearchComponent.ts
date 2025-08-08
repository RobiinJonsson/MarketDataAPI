import { instrumentApi } from '../utils/api.js';
import { isValidISIN, showLoading, showError, formatDate, formatNumber } from '../utils/helpers.js';
import type { InstrumentSearchResult } from '../types/api.js';

export class SearchComponent {
  private container: HTMLElement;
  private searchInput!: HTMLInputElement;
  private searchButton!: HTMLButtonElement;
  private resultsContainer!: HTMLElement;

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
          <h3 class="text-lg font-semibold text-gray-900">Search Instruments</h3>
          <p class="mt-1 text-sm text-gray-600">Enter an ISIN to search for instrument data</p>
        </div>
        
        <form id="search-form" class="space-y-4">
          <div class="flex gap-3">
            <div class="flex-1">
              <input
                type="text"
                id="search-input"
                class="input-field"
                placeholder="Enter ISIN (e.g., US0378331005)"
                pattern="^[A-Z]{2}[A-Z0-9]{9}\\d$"
                title="Please enter a valid 12-character ISIN"
                required
              />
            </div>
            <button type="submit" id="search-button" class="btn btn-primary">
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
      this.handleSearch();
    });

    this.searchInput.addEventListener('input', () => {
      const isValid = isValidISIN(this.searchInput.value);
      this.searchButton.disabled = !isValid;
      this.searchButton.classList.toggle('opacity-50', !isValid);
    });
  }

  private async handleSearch(): Promise<void> {
    const isin = this.searchInput.value.trim().toUpperCase();
    
    if (!isValidISIN(isin)) {
      showError(this.resultsContainer, 'Please enter a valid ISIN');
      return;
    }

    showLoading(this.resultsContainer, 'Searching for instrument...');
    
    const response = await instrumentApi.search(isin);
    
    if (response.status === 'error') {
      showError(this.resultsContainer, response.error || 'Search failed');
      return;
    }

    if (!response.data) {
      this.renderNoResults(isin);
      return;
    }

    this.renderResults(response.data);
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

  private renderResults(data: InstrumentSearchResult): void {
    const { instrument, transparency_data, figi_data } = data;
    
    this.resultsContainer.innerHTML = `
      <div class="space-y-6">
        <!-- Instrument Overview -->
        <div class="card">
          <div class="card-header">
            <h4 class="text-lg font-semibold text-gray-900">Instrument Details</h4>
          </div>
          <dl class="grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
            <div>
              <dt class="text-sm font-medium text-gray-500">ISIN</dt>
              <dd class="text-sm text-gray-900 font-mono">${instrument.isin}</dd>
            </div>
            ${instrument.symbol ? `
              <div>
                <dt class="text-sm font-medium text-gray-500">Symbol</dt>
                <dd class="text-sm text-gray-900">${instrument.symbol}</dd>
              </div>
            ` : ''}
            ${instrument.name ? `
              <div>
                <dt class="text-sm font-medium text-gray-500">Name</dt>
                <dd class="text-sm text-gray-900">${instrument.name}</dd>
              </div>
            ` : ''}
            ${instrument.cfi ? `
              <div>
                <dt class="text-sm font-medium text-gray-500">CFI</dt>
                <dd class="text-sm text-gray-900 font-mono">${instrument.cfi}</dd>
              </div>
            ` : ''}
            <div>
              <dt class="text-sm font-medium text-gray-500">Created</dt>
              <dd class="text-sm text-gray-900">${formatDate(instrument.created_at)}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Updated</dt>
              <dd class="text-sm text-gray-900">${formatDate(instrument.updated_at)}</dd>
            </div>
          </dl>
        </div>

        <!-- Transparency Data -->
        ${this.renderTransparencyData(transparency_data)}

        <!-- FIGI Data -->
        ${this.renderFigiData(figi_data)}
      </div>
    `;
  }

  private renderTransparencyData(transparencyData?: any[]): string {
    if (!transparencyData || transparencyData.length === 0) {
      return `
        <div class="card">
          <div class="card-header">
            <h4 class="text-lg font-semibold text-gray-900">Transparency Data</h4>
          </div>
          <p class="text-gray-600">No transparency calculations found</p>
        </div>
      `;
    }

    const latestCalc = transparencyData[0];
    return `
      <div class="card">
        <div class="card-header">
          <h4 class="text-lg font-semibold text-gray-900">Transparency Data</h4>
          <span class="text-sm text-gray-500">${transparencyData.length} calculation(s)</span>
        </div>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl font-bold text-gray-900">${formatNumber(latestCalc.total_transactions_executed)}</div>
            <div class="text-sm text-gray-600">Total Transactions</div>
          </div>
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl font-bold text-gray-900">${formatNumber(latestCalc.total_volume_executed)}</div>
            <div class="text-sm text-gray-600">Total Volume</div>
          </div>
          <div class="text-center p-4 bg-gray-50 rounded-lg">
            <div class="text-2xl font-bold text-gray-900">${latestCalc.liquidity ? 'Yes' : 'No'}</div>
            <div class="text-sm text-gray-600">Liquid</div>
          </div>
        </div>
      </div>
    `;
  }

  private renderFigiData(figiData?: any[]): string {
    if (!figiData || figiData.length === 0) {
      return `
        <div class="card">
          <div class="card-header">
            <h4 class="text-lg font-semibold text-gray-900">FIGI Data</h4>
          </div>
          <p class="text-gray-600">No FIGI data found</p>
        </div>
      `;
    }

    return `
      <div class="card">
        <div class="card-header">
          <h4 class="text-lg font-semibold text-gray-900">FIGI Data</h4>
          <span class="text-sm text-gray-500">${figiData.length} record(s)</span>
        </div>
        <div class="space-y-3">
          ${figiData.map(figi => `
            <div class="p-3 bg-gray-50 rounded-lg">
              <div class="font-medium text-gray-900">${figi.name || 'N/A'}</div>
              <div class="text-sm text-gray-600 font-mono">${figi.figi}</div>
              ${figi.ticker ? `<div class="text-sm text-gray-600">Ticker: ${figi.ticker}</div>` : ''}
              ${figi.exch_code ? `<div class="text-sm text-gray-600">Exchange: ${figi.exch_code}</div>` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}
