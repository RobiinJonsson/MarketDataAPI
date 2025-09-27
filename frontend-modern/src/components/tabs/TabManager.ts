import { BaseTabRenderer } from './BaseTabRenderer';
import { OverviewTabRenderer } from './OverviewTabRenderer';
import { LeiTabRenderer } from './LeiTabRenderer';
import { TransparencyTabRenderer } from './TransparencyTabRenderer';
import { CfiTabRenderer } from './CfiTabRenderer';
import { VenuesTabRenderer } from './VenuesTabRenderer';
import { ComprehensiveInstrumentData } from '../../types/api';

export class TabManager {
  private renderers: Map<string, BaseTabRenderer>;
  private activeTab: string = 'overview';

  constructor() {
    this.renderers = new Map();
    this.initializeRenderers();
  }

  private initializeRenderers(): void {
    const renderers = [
      new OverviewTabRenderer(),
      new LeiTabRenderer(),
      new TransparencyTabRenderer(),
      new CfiTabRenderer(),
      new VenuesTabRenderer()
    ];

    renderers.forEach(renderer => {
      this.renderers.set(renderer.getTabId(), renderer);
    });
  }

  /**
   * Render the complete tab interface
   */
  renderTabs(data: ComprehensiveInstrumentData): string {
    console.log('TabManager rendering with data:', data);
    const enabledTabs = this.getEnabledTabs(data);
    console.log('Enabled tabs:', enabledTabs.map(tab => tab.getTabId()));
    
    if (enabledTabs.length === 0) {
      return '<div class="text-center py-8 text-gray-500">No data available for display</div>';
    }

    // Ensure active tab is enabled
    if (!enabledTabs.some(tab => tab.getTabId() === this.activeTab)) {
      this.activeTab = enabledTabs[0].getTabId();
    }
    console.log('Active tab:', this.activeTab);

    return `
      <!-- Tab Navigation -->
      <div class="border-b border-gray-200">
        <nav class="flex space-x-8 px-6" role="tablist">
          ${enabledTabs.map(renderer => this.renderTabButton(renderer, data)).join('')}
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="p-6">
        ${enabledTabs.map(renderer => this.renderTabContent(renderer, data)).join('')}
      </div>
    `;
  }

  /**
   * Render a single tab button
   */
  private renderTabButton(renderer: BaseTabRenderer, data: ComprehensiveInstrumentData): string {
    const tabId = renderer.getTabId();
    const isActive = this.activeTab === tabId;
    const badgeCount = renderer.getBadgeCount(data);
    
    const countBadge = badgeCount !== undefined ? 
      `<span class="ml-2 bg-gray-100 text-gray-900 text-xs font-medium px-2.5 py-0.5 rounded-full">${badgeCount}</span>` : 
      '';
    
    return `
      <button 
        data-tab="${tabId}" 
        class="tab-button py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
          isActive 
            ? 'border-blue-500 text-blue-600' 
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }"
      >
        ${renderer.getTabLabel()}${countBadge}
      </button>
    `;
  }

  /**
   * Render a single tab content
   */
  private renderTabContent(renderer: BaseTabRenderer, data: ComprehensiveInstrumentData): string {
    const tabId = renderer.getTabId();
    const isActive = this.activeTab === tabId;
    
    console.log(`Rendering content for tab ${tabId}, active: ${isActive}`);
    const content = renderer.render(data);
    console.log(`Tab ${tabId} content length:`, content.length);
    
    return `
      <div id="tab-${tabId}" class="tab-content ${isActive ? '' : 'hidden'}">
        ${content}
      </div>
    `;
  }

  /**
   * Get all enabled tab renderers for the given data
   */
  private getEnabledTabs(data: ComprehensiveInstrumentData): BaseTabRenderer[] {
    return Array.from(this.renderers.values()).filter(renderer => 
      renderer.isEnabled(data)
    );
  }

  /**
   * Switch to a specific tab
   */
  switchTab(tabId: string): void {
    if (this.renderers.has(tabId)) {
      this.activeTab = tabId;
    }
  }

  /**
   * Get the current active tab ID
   */
  getActiveTab(): string {
    return this.activeTab;
  }

  /**
   * Bind event listeners for tab switching
   */
  bindTabEvents(container: HTMLElement): void {
    const tabButtons = container.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        e.preventDefault();
        const target = e.currentTarget as HTMLElement;
        const tabId = target.getAttribute('data-tab');
        
        if (tabId) {
          this.switchTab(tabId);
          this.updateTabDisplay(container);
        }
      });
    });
  }

  /**
   * Update the visual display when switching tabs
   */
  private updateTabDisplay(container: HTMLElement): void {
    // Update button states
    const tabButtons = container.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
      const tabId = button.getAttribute('data-tab');
      const isActive = tabId === this.activeTab;
      
      button.className = `tab-button py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
        isActive 
          ? 'border-blue-500 text-blue-600' 
          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
      }`;
    });

    // Update content visibility
    const tabContents = container.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
      const tabId = content.id.replace('tab-', '');
      const isActive = tabId === this.activeTab;
      
      if (isActive) {
        content.classList.remove('hidden');
      } else {
        content.classList.add('hidden');
      }
    });
  }

  /**
   * Get a specific renderer by ID
   */
  getRenderer(tabId: string): BaseTabRenderer | undefined {
    return this.renderers.get(tabId);
  }

  /**
   * Get all available renderers
   */
  getAllRenderers(): BaseTabRenderer[] {
    return Array.from(this.renderers.values());
  }
}
