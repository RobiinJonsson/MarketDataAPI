import { BasePage } from './BasePage';
import { apiServices } from '../services';
import type { 
  VenueSummary, 
  VenueDetail, 
  VenueListFilters, 
  VenueListResponse,
  VenueStatistics,
  CountrySummary
} from '../types/api';

/**
 * Venues & MIC Codes Page
 * Comprehensive venue management with filtering, search, and detailed views
 */
export default class VenuesPage extends BasePage {
  private currentFilters: VenueListFilters = {};
  private currentPage = 1;
  private perPage = 50;
  private totalPages = 0;
  private venues: VenueSummary[] = [];
  private countries: CountrySummary[] = [];
  private statistics: VenueStatistics | null = null;

  async render(): Promise<void> {
    this.showLoading('Loading venues and MIC codes...');

    try {
      // Load initial data
      await this.loadCountries();
      await this.loadStatistics();
      await this.loadVenues();
      
      this.renderPage();
      this.setupEventListeners();
    } catch (error) {
      console.error('Error loading venues page:', error);
      this.showError('Failed to load venues data');
    }
  }

  private async loadCountries(): Promise<void> {
    try {
      const response = await apiServices.venues.getVenueCountries();
      this.countries = response.data || [];
    } catch (error) {
      console.error('Error loading countries:', error);
    }
  }

  private async loadStatistics(): Promise<void> {
    try {
      const response = await apiServices.venues.getVenueStatistics();
      this.statistics = response.data || null;
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  }

  private async loadVenues(): Promise<void> {
    try {
      const response = await apiServices.venues.getVenues(
        this.currentFilters, 
        this.currentPage, 
        this.perPage
      );
      
      // Handle actual API response structure: { status, data: VenueSummary[], pagination: {...} }
      const venueResponse = response as VenueListResponse;
      this.venues = venueResponse.data || [];
      this.totalPages = venueResponse.pagination?.pages || 0;
    } catch (error) {
      console.error('Error loading venues:', error);
      throw error;
    }
  }

  private renderPage(): void {
    this.container.innerHTML = `
      ${this.createSectionHeader('Trading Venues & MIC Codes', 'Market identification codes and venue relationships with comprehensive filtering')}
      
      <!-- Statistics Cards -->
      ${this.renderStatisticsCards()}
      
      <!-- Filters and Controls -->
      ${this.renderFiltersSection()}
      
      <!-- Venues Grid -->
      ${this.renderVenuesSection()}
    `;
  }

  private renderStatisticsCards(): string {
    if (!this.statistics) return '';

    return `
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100">Total MIC Codes</p>
              <p class="text-2xl font-bold">${this.statistics.total_mics.toLocaleString()}</p>
            </div>
            <svg class="w-8 h-8 text-blue-200" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
            </svg>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-lg shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100">Operating MICs</p>
              <p class="text-2xl font-bold">${this.statistics.operating_mics.toLocaleString()}</p>
            </div>
            <svg class="w-8 h-8 text-green-200" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100">Segment MICs</p>
              <p class="text-2xl font-bold">${this.statistics.segment_mics.toLocaleString()}</p>
            </div>
            <svg class="w-8 h-8 text-purple-200" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"></path>
            </svg>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-6 rounded-lg shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-orange-100">Active Venues</p>
              <p class="text-2xl font-bold">${this.statistics.venues_with_instruments.toLocaleString()}</p>
            </div>
            <svg class="w-8 h-8 text-orange-200" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"></path>
            </svg>
          </div>
        </div>
      </div>
    `;
  }

  private renderFiltersSection(): string {
    const countryOptions = this.countries.map(country => 
      `<option value="${country.country_code}">${country.country_code} (${country.total_mics})</option>`
    ).join('');

    return `
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Filters & Search</h3>
          <button id="clear-filters" class="text-sm text-blue-600 hover:text-blue-800">Clear All</button>
        </div>
        
        <!-- Search Bar -->
        <div class="mb-4">
          <div class="relative">
            <input
              type="text"
              id="venue-search"
              placeholder="Search venues, MIC codes, or legal entities..."
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value="${this.currentFilters.search || ''}"
            />
            <svg class="absolute left-3 top-3 w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
            </svg>
          </div>
        </div>
        
        <!-- Filter Controls -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Country</label>
            <select id="filter-country" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">
              <option value="">All Countries</option>
              ${countryOptions}
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select id="filter-status" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">
              <option value="">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="EXPIRED">Expired</option>
              <option value="SUSPENDED">Suspended</option>
              <option value="UPDATED">Updated</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">MIC Type</label>
            <select id="filter-mic-type" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">
              <option value="">All Types</option>
              <option value="OPRT">Operating MIC</option>
              <option value="SGMT">Segment MIC</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Has Instruments</label>
            <select id="filter-has-instruments" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500">
              <option value="">All Venues</option>
              <option value="true">With Instruments</option>
              <option value="false">Without Instruments</option>
            </select>
          </div>
          
          <div class="flex items-end">
            <button 
              id="apply-filters" 
              class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500"
            >
              Apply Filters
            </button>
          </div>
        </div>
      </div>
    `;
  }

  private renderVenuesSection(): string {
    return `
      <div class="bg-white rounded-lg shadow-md">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Venues</h3>
            <p class="text-sm text-gray-600">Showing ${this.venues.length} venues</p>
          </div>
          <div class="flex items-center space-x-4">
            <select id="per-page-select" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
              <option value="25" ${this.perPage === 25 ? 'selected' : ''}>25 per page</option>
              <option value="50" ${this.perPage === 50 ? 'selected' : ''}>50 per page</option>
              <option value="100" ${this.perPage === 100 ? 'selected' : ''}>100 per page</option>
            </select>
          </div>
        </div>
        
        <!-- Venues Grid -->
        <div class="p-6">
          ${this.venues.length > 0 ? this.renderVenuesGrid() : this.renderEmptyState()}
        </div>
        
        <!-- Pagination -->
        ${this.totalPages > 1 ? this.renderPagination() : ''}
      </div>
    `;
  }

  private renderVenuesGrid(): string {
    return `
      <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        ${this.venues.map(venue => this.renderVenueCard(venue)).join('')}
      </div>
    `;
  }

  private renderVenueCard(venue: VenueSummary): string {
    const statusColor = this.getStatusColor(venue.status);
    const typeColor = venue.operation_type === 'OPRT' ? 'text-blue-600 bg-blue-100' : 'text-purple-600 bg-purple-100';

    return `
      <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer venue-card" data-mic="${venue.mic_code}">
        <!-- Header -->
        <div class="flex items-start justify-between mb-3">
          <div>
            <h4 class="font-semibold text-gray-900 text-lg">${venue.mic_code}</h4>
            <span class="inline-block px-2 py-1 text-xs rounded ${typeColor}">${venue.operation_type || 'N/A'}</span>
          </div>
          <span class="inline-block px-2 py-1 text-xs rounded ${statusColor}">${venue.status || 'Unknown'}</span>
        </div>
        
        <!-- Market Name -->
        <div class="mb-3">
          <p class="font-medium text-gray-800 line-clamp-2">${venue.market_name}</p>
          ${venue.legal_entity_name ? `<p class="text-sm text-gray-600 mt-1 line-clamp-1">${venue.legal_entity_name}</p>` : ''}
        </div>
        
        <!-- Location & Details -->
        <div class="space-y-2 text-sm text-gray-600">
          ${venue.country_code || venue.city ? `
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"></path>
              </svg>
              <span>${[venue.city, venue.country_code].filter(Boolean).join(', ')}</span>
            </div>
          ` : ''}
          
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>${venue.instrument_count} instruments</span>
          </div>
          
          ${venue.operating_mic && venue.operating_mic !== venue.mic_code ? `
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span>Operating MIC: ${venue.operating_mic}</span>
            </div>
          ` : ''}
        </div>
        
        <!-- Footer -->
        <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between">
          <span class="text-xs text-gray-500">
            ${venue.last_update_date ? `Updated ${new Date(venue.last_update_date).toLocaleDateString()}` : 'No update date'}
          </span>
          <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">View Details →</button>
        </div>
      </div>
    `;
  }

  private renderEmptyState(): string {
    return `
      <div class="text-center py-12">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm2 2h8v8H6V6z" clip-rule="evenodd"></path>
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No venues found</h3>
        <p class="text-gray-600">Try adjusting your filters or search criteria.</p>
      </div>
    `;
  }

  private renderPagination(): string {
    const startPage = Math.max(1, this.currentPage - 2);
    const endPage = Math.min(this.totalPages, this.currentPage + 2);
    const pages = [];

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return `
      <div class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="flex items-center text-sm text-gray-600">
          <span>Page ${this.currentPage} of ${this.totalPages}</span>
        </div>
        
        <div class="flex items-center space-x-1">
          <!-- Previous -->
          <button 
            id="prev-page" 
            ${this.currentPage <= 1 ? 'disabled' : ''} 
            class="px-3 py-2 rounded-lg border ${this.currentPage <= 1 ? 'text-gray-400 cursor-not-allowed' : 'text-gray-600 hover:bg-gray-100'}"
          >
            Previous
          </button>
          
          <!-- Page Numbers -->
          ${pages.map(page => `
            <button 
              class="page-btn px-3 py-2 rounded-lg border ${page === this.currentPage ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}" 
              data-page="${page}"
            >
              ${page}
            </button>
          `).join('')}
          
          <!-- Next -->
          <button 
            id="next-page" 
            ${this.currentPage >= this.totalPages ? 'disabled' : ''} 
            class="px-3 py-2 rounded-lg border ${this.currentPage >= this.totalPages ? 'text-gray-400 cursor-not-allowed' : 'text-gray-600 hover:bg-gray-100'}"
          >
            Next
          </button>
        </div>
      </div>
    `;
  }

  private getStatusColor(status?: string): string {
    switch (status) {
      case 'ACTIVE': return 'text-green-600 bg-green-100';
      case 'EXPIRED': return 'text-red-600 bg-red-100';
      case 'SUSPENDED': return 'text-yellow-600 bg-yellow-100';
      case 'UPDATED': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }

  private setupEventListeners(): void {
    // Search functionality
    const searchInput = document.getElementById('venue-search') as HTMLInputElement;
    if (searchInput) {
      let searchTimeout: NodeJS.Timeout;
      searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          this.currentFilters.search = searchInput.value;
          this.currentPage = 1;
          this.applyFiltersAndReload();
        }, 300);
      });
    }

    // Filter controls
    this.setupFilterListeners();

    // Pagination
    this.setupPaginationListeners();

    // Venue cards
    this.setupVenueCardListeners();

    // Per page selector
    const perPageSelect = document.getElementById('per-page-select') as HTMLSelectElement;
    if (perPageSelect) {
      perPageSelect.addEventListener('change', () => {
        this.perPage = parseInt(perPageSelect.value);
        this.currentPage = 1;
        this.applyFiltersAndReload();
      });
    }

    // Clear filters
    const clearFilters = document.getElementById('clear-filters');
    if (clearFilters) {
      clearFilters.addEventListener('click', () => {
        this.currentFilters = {};
        this.currentPage = 1;
        this.applyFiltersAndReload();
      });
    }
  }

  private setupFilterListeners(): void {
    const filterIds = ['filter-country', 'filter-status', 'filter-mic-type', 'filter-has-instruments'];
    const filterKeys = ['country', 'status', 'mic_type', 'has_instruments'];

    filterIds.forEach((id, index) => {
      const element = document.getElementById(id) as HTMLSelectElement;
      if (element) {
        element.value = this.currentFilters[filterKeys[index] as keyof VenueListFilters] || '';
        element.addEventListener('change', () => {
          this.currentFilters[filterKeys[index] as keyof VenueListFilters] = element.value || undefined;
        });
      }
    });

    const applyButton = document.getElementById('apply-filters');
    if (applyButton) {
      applyButton.addEventListener('click', () => {
        this.currentPage = 1;
        this.applyFiltersAndReload();
      });
    }
  }

  private setupPaginationListeners(): void {
    // Previous/Next buttons
    const prevButton = document.getElementById('prev-page');
    if (prevButton && !prevButton.hasAttribute('disabled')) {
      prevButton.addEventListener('click', () => {
        if (this.currentPage > 1) {
          this.currentPage--;
          this.applyFiltersAndReload();
        }
      });
    }

    const nextButton = document.getElementById('next-page');
    if (nextButton && !nextButton.hasAttribute('disabled')) {
      nextButton.addEventListener('click', () => {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
          this.applyFiltersAndReload();
        }
      });
    }

    // Page number buttons
    document.querySelectorAll('.page-btn').forEach(button => {
      button.addEventListener('click', () => {
        const page = parseInt(button.getAttribute('data-page') || '1');
        this.currentPage = page;
        this.applyFiltersAndReload();
      });
    });
  }

  private setupVenueCardListeners(): void {
    document.querySelectorAll('.venue-card').forEach(card => {
      card.addEventListener('click', () => {
        const micCode = card.getAttribute('data-mic');
        if (micCode) {
          this.showVenueDetail(micCode);
        }
      });
    });
  }

  private async applyFiltersAndReload(): Promise<void> {
    this.showLoading('Applying filters...');
    
    try {
      await this.loadVenues();
      this.renderPage();
      this.setupEventListeners();
    } catch (error) {
      console.error('Error applying filters:', error);
      this.showError('Failed to apply filters');
    }
  }

  private async showVenueDetail(micCode: string): Promise<void> {
    try {
      // Show loading in modal or navigate to detail view
      // For now, let's create a simple modal
      const response = await apiServices.venues.getVenueDetail(micCode, true, 50);
      const venue = response.data;

      if (venue) {
        this.showVenueModal(venue);
      }
    } catch (error) {
      console.error('Error loading venue detail:', error);
      alert('Failed to load venue details');
    }
  }

  private showVenueModal(venue: VenueDetail): void {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto mx-4">
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-gray-900">${venue.mic_code} - ${venue.market_name}</h2>
            <button class="text-gray-500 hover:text-gray-700" onclick="this.closest('.fixed').remove()">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
              </svg>
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Basic Info -->
            <div>
              <h3 class="text-lg font-semibold mb-3">Basic Information</h3>
              <div class="space-y-2 text-sm">
                <div><span class="font-medium">Legal Entity:</span> ${venue.legal_entity_name || 'N/A'}</div>
                <div><span class="font-medium">Country:</span> ${venue.country_code || 'N/A'}</div>
                <div><span class="font-medium">City:</span> ${venue.city || 'N/A'}</div>
                <div><span class="font-medium">Status:</span> <span class="px-2 py-1 rounded text-xs ${this.getStatusColor(venue.status)}">${venue.status || 'Unknown'}</span></div>
                <div><span class="font-medium">Type:</span> ${venue.operation_type || 'N/A'}</div>
                ${venue.website ? `<div><span class="font-medium">Website:</span> <a href="${venue.website}" target="_blank" class="text-blue-600 hover:underline">${venue.website}</a></div>` : ''}
              </div>
            </div>
            
            <!-- Additional Info -->
            <div>
              <h3 class="text-lg font-semibold mb-3">Additional Details</h3>
              <div class="space-y-2 text-sm">
                ${venue.lei ? `<div><span class="font-medium">LEI:</span> ${venue.lei}</div>` : ''}
                ${venue.acronym ? `<div><span class="font-medium">Acronym:</span> ${venue.acronym}</div>` : ''}
                <div><span class="font-medium">Instruments:</span> ${venue.instrument_count}</div>
                ${venue.operating_mic && venue.operating_mic !== venue.mic_code ? `<div><span class="font-medium">Operating MIC:</span> ${venue.operating_mic}</div>` : ''}
                ${venue.creation_date ? `<div><span class="font-medium">Created:</span> ${new Date(venue.creation_date).toLocaleDateString()}</div>` : ''}
                ${venue.last_update_date ? `<div><span class="font-medium">Last Updated:</span> ${new Date(venue.last_update_date).toLocaleDateString()}</div>` : ''}
              </div>
            </div>
          </div>
          
          ${venue.segment_mics && venue.segment_mics.length > 0 ? `
            <div class="mt-6">
              <h3 class="text-lg font-semibold mb-3">Segment MICs</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                ${venue.segment_mics.map(seg => `
                  <div class="border border-gray-200 rounded p-3">
                    <div class="font-medium">${seg.mic_code}</div>
                    <div class="text-sm text-gray-600">${seg.market_name}</div>
                    <span class="text-xs px-2 py-1 rounded ${this.getStatusColor(seg.status)}">${seg.status || 'Unknown'}</span>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}
          
          ${venue.instruments && venue.instruments.length > 0 ? `
            <div class="mt-6">
              <h3 class="text-lg font-semibold mb-3">Sample Instruments (${venue.instruments.length} shown)</h3>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ISIN</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Currency</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    ${venue.instruments.slice(0, 10).map(inst => `
                      <tr>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">${inst.isin}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${inst.instrument_name || 'N/A'}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${inst.instrument_type || 'N/A'}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${inst.venue_currency || 'N/A'}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          ` : ''}
        </div>
      </div>
    `;

    document.body.appendChild(modal);
  }
}