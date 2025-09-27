import { BaseSearchComponent, SearchComponentOptions } from './base/BaseSearchComponent';
import { TabManager } from './tabs/TabManager';
import { instrumentDataService } from '../services/InstrumentDataService';
import { ComprehensiveInstrumentData } from '../types/api';

/**
 * Comprehensive instrument search component combining all data sources
 */
export class ComprehensiveSearchComponent extends BaseSearchComponent {
  private tabManager: TabManager;
  private currentData: ComprehensiveInstrumentData | null = null;

  constructor(containerId: string) {
    const options: SearchComponentOptions = {
      containerId,
      searchPlaceholder: 'Enter ISIN (e.g., SE0000242455)',
      searchTitle: 'Comprehensive Instrument Search',
      searchDescription: 'Enter an ISIN to view complete instrument profile with LEI, transparency, CFI, and FIGI data',
      enableValidation: true
    };

    super(options);
    this.tabManager = new TabManager();
  }

  /**
   * Override to add admin portal link
   */
  protected renderAdditionalFormElements(): string {
    return `
      <p class="text-sm text-gray-500">
        Looking to create or manage instruments? Visit the 
        <a href="/admin.html" class="text-primary-600 hover:text-primary-700 font-medium">Admin Portal</a>.
      </p>
    `;
  }

  /**
   * Implement the required performSearch method
   */
  protected async performSearch(isin: string): Promise<void> {
    try {
      console.log(`Starting search for ISIN: ${isin}`);
      this.currentData = await instrumentDataService.fetchComprehensiveInstrumentData(isin);
      console.log('Comprehensive data fetched:', this.currentData);
      
      // Log each data section for debugging
      console.log('- Instrument data:', this.currentData.instrument);
      console.log('- Transparency data:', this.currentData.transparency);
      console.log('- Venues data:', this.currentData.venues);
      console.log('- LEI data:', this.currentData.lei_data);
      
      this.renderResults(this.currentData);
    } catch (error) {
      console.error('Search error:', error);
      this.renderNoResults(isin);
    }
  }

  protected renderResults(data: ComprehensiveInstrumentData): void {
    const resultsContainer = this.getResultsContainer();
    resultsContainer.innerHTML = this.tabManager.renderTabs(data);
    
    // Bind tab event handlers for interactivity
    this.tabManager.bindTabEvents(resultsContainer);
    
    // Debug: Log the data to console
    console.log('Rendering results with data:', data);
  }

  protected renderNoResults(isin: string): void {
    const resultsContainer = this.getResultsContainer();
    resultsContainer.innerHTML = `
      <div class="bg-red-50 border border-red-200 p-4 rounded-md">
        <p class="text-red-800">No results found for ISIN: ${isin}</p>
        <p class="text-red-600 text-sm mt-2">Please check the ISIN format and try again.</p>
      </div>
    `;
  }
}
