/**
 * Base Page Class
 * Provides common functionality for all pages
 */

export abstract class BasePage {
  protected container: HTMLElement;
  protected params: Record<string, string>;

  constructor(container: HTMLElement, params: Record<string, string> = {}) {
    this.container = container;
    this.params = params;
  }

  /**
   * Render the page content
   */
  abstract render(): Promise<void>;

  /**
   * Cleanup when leaving the page
   */
  cleanup(): void {
    // Override in subclasses if cleanup is needed
  }

  /**
   * Show loading state
   */
  protected showLoading(message: string = 'Loading...'): void {
    this.container.innerHTML = `
      <div class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">${message}</span>
      </div>
    `;
  }

  /**
   * Show error state
   */
  protected showError(message: string, details?: string): void {
    this.container.innerHTML = `
      <div class="bg-red-50 border border-red-200 rounded-lg p-6">
        <div class="flex items-center mb-3">
          <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
          <h3 class="text-red-800 font-medium">Error</h3>
        </div>
        <p class="text-red-700 mb-2">${message}</p>
        ${details ? `<p class="text-red-600 text-sm">${details}</p>` : ''}
        <button 
          onclick="window.location.reload()" 
          class="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      </div>
    `;
  }

  /**
   * Create a section header
   */
  protected createSectionHeader(title: string, description?: string): string {
    return `
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">${title}</h1>
        ${description ? `<p class="text-gray-600">${description}</p>` : ''}
      </div>
    `;
  }

  /**
   * Create a card container
   */
  protected createCard(content: string, title?: string): string {
    return `
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        ${title ? `
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">${title}</h3>
          </div>
        ` : ''}
        <div class="p-6">
          ${content}
        </div>
      </div>
    `;
  }

  /**
   * Create tabs
   */
  protected createTabs(tabs: Array<{id: string, label: string, active?: boolean}>): string {
    return `
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          ${tabs.map(tab => `
            <button 
              data-tab="${tab.id}"
              class="tab-button py-2 px-1 border-b-2 font-medium text-sm transition-colors
                     ${tab.active ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
            >
              ${tab.label}
            </button>
          `).join('')}
        </nav>
      </div>
    `;
  }

  /**
   * Initialize tab functionality
   */
  protected initializeTabs(): void {
    this.container.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      if (target.hasAttribute('data-tab')) {
        const tabId = target.getAttribute('data-tab');
        
        // Update tab buttons
        this.container.querySelectorAll('.tab-button').forEach(btn => {
          btn.classList.remove('border-blue-500', 'text-blue-600');
          btn.classList.add('border-transparent', 'text-gray-500');
        });
        
        target.classList.add('border-blue-500', 'text-blue-600');
        target.classList.remove('border-transparent', 'text-gray-500');
        
        // Update tab panes
        this.container.querySelectorAll('[data-tab-pane]').forEach(pane => {
          pane.classList.add('hidden');
        });
        
        const activePane = this.container.querySelector(`[data-tab-pane="${tabId}"]`);
        if (activePane) {
          activePane.classList.remove('hidden');
        }
      }
    });
  }
}