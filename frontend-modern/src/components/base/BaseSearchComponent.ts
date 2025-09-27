import { isValidISIN, showLoading, showError } from '../../utils/helpers';

export interface SearchComponentOptions {
  containerId: string;
  searchPlaceholder?: string;
  searchTitle?: string;
  searchDescription?: string;
  enableValidation?: boolean;
  onSearch?: (query: string) => Promise<void>;
  onError?: (error: Error) => void;
}

export abstract class BaseSearchComponent {
  protected container: HTMLElement;
  protected searchInput!: HTMLInputElement;
  protected searchButton!: HTMLButtonElement;
  protected resultsContainer!: HTMLElement;
  protected options: SearchComponentOptions;

  constructor(options: SearchComponentOptions) {
    this.options = {
      searchPlaceholder: 'Enter search term...',
      searchTitle: 'Search',
      searchDescription: 'Enter your search criteria',
      enableValidation: true,
      ...options
    };

    this.container = document.getElementById(this.options.containerId)!;
    if (!this.container) {
      throw new Error(`Container with ID '${this.options.containerId}' not found`);
    }

    this.init();
  }

  /**
   * Initialize the component
   */
  protected init(): void {
    this.render();
    this.bindEvents();
  }

  /**
   * Render the search interface
   */
  protected render(): void {
    this.container.innerHTML = `
      <div class="card">
        ${this.renderHeader()}
        ${this.renderSearchForm()}
        <div id="search-results" class="mt-6"></div>
      </div>
    `;

    this.searchInput = this.container.querySelector('#search-input')!;
    this.searchButton = this.container.querySelector('#search-button')!;
    this.resultsContainer = this.container.querySelector('#search-results')!;
  }

  /**
   * Render the component header
   */
  protected renderHeader(): string {
    return `
      <div class="card-header">
        <h3 class="text-lg font-semibold text-gray-900">${this.options.searchTitle}</h3>
        <p class="mt-1 text-sm text-gray-600">${this.options.searchDescription}</p>
      </div>
    `;
  }

  /**
   * Render the search form
   */
  protected renderSearchForm(): string {
    const validationAttrs = this.options.enableValidation ? 
      'pattern="^[A-Z]{2}[A-Z0-9]{9}[0-9]$" title="Please enter a valid 12-character ISIN"' : '';

    return `
      <form id="search-form" class="space-y-4">
        <div class="flex gap-3">
          <div class="flex-1">
            <input
              type="text"
              id="search-input"
              class="input-field"
              placeholder="${this.options.searchPlaceholder}"
              ${validationAttrs}
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
        ${this.renderAdditionalFormElements()}
      </form>
    `;
  }

  /**
   * Override this to add additional form elements
   */
  protected renderAdditionalFormElements(): string {
    return '';
  }

  /**
   * Bind event handlers
   */
  protected bindEvents(): void {
    const form = this.container.querySelector('#search-form')!;
    
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleSearch();
    });

    this.searchInput.addEventListener('input', () => {
      this.onInputChange();
    });

    // Additional event bindings can be added by subclasses
    this.bindAdditionalEvents();
  }

  /**
   * Override this to bind additional events
   */
  protected bindAdditionalEvents(): void {
    // Subclasses can override this method
  }

  /**
   * Handle input change events
   */
  protected onInputChange(): void {
    // Clear previous error states
    this.clearError();
  }

  /**
   * Handle search submission
   */
  protected async handleSearch(): Promise<void> {
    const query = this.getSearchQuery();
    
    if (!this.validateInput(query)) {
      return;
    }

    this.setLoading(true);
    
    try {
      if (this.options.onSearch) {
        await this.options.onSearch(query);
      } else {
        await this.performSearch(query);
      }
    } catch (error) {
      this.handleError(error as Error);
    } finally {
      this.setLoading(false);
    }
  }

  /**
   * Get the current search query
   */
  protected getSearchQuery(): string {
    return this.searchInput.value.trim().toUpperCase();
  }

  /**
   * Validate the search input
   */
  protected validateInput(query: string): boolean {
    if (!query) {
      this.showError('Please enter a search term');
      return false;
    }

    if (this.options.enableValidation && !isValidISIN(query)) {
      this.showError('Please enter a valid 12-character ISIN');
      return false;
    }

    return true;
  }

  /**
   * Abstract method - subclasses must implement search logic
   */
  protected abstract performSearch(query: string): Promise<void>;

  /**
   * Set loading state
   */
  protected setLoading(loading: boolean): void {
    this.searchButton.disabled = loading;
    
    if (loading) {
      showLoading(this.resultsContainer, 'Searching...');
      this.searchButton.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Searching...
      `;
    } else {
      this.searchButton.innerHTML = `
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        Search
      `;
    }
  }

  /**
   * Handle errors
   */
  protected handleError(error: Error): void {
    console.error('Search error:', error);
    
    if (this.options.onError) {
      this.options.onError(error);
    } else {
      this.showError(error.message || 'An error occurred during search');
    }
  }

  /**
   * Show error message
   */
  protected showError(message: string): void {
    showError(this.resultsContainer, message);
  }

  /**
   * Clear error state
   */
  protected clearError(): void {
    // Remove any existing error displays
    const errorElements = this.resultsContainer.querySelectorAll('.alert-error');
    errorElements.forEach(element => element.remove());
  }

  /**
   * Clear results
   */
  public clearResults(): void {
    this.resultsContainer.innerHTML = '';
  }

  /**
   * Get the results container element
   */
  protected getResultsContainer(): HTMLElement {
    return this.resultsContainer;
  }

  /**
   * Get the search input element
   */
  protected getSearchInput(): HTMLInputElement {
    return this.searchInput;
  }

  /**
   * Programmatically set search value
   */
  public setSearchValue(value: string): void {
    this.searchInput.value = value;
  }

  /**
   * Programmatically trigger search
   */
  public triggerSearch(): void {
    this.handleSearch();
  }

  /**
   * Check if component is currently loading
   */
  public isLoading(): boolean {
    return this.searchButton.disabled;
  }
}
