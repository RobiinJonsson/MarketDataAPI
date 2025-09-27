import { ComprehensiveInstrumentData } from '../../types/api';

/**
 * Base class for tab renderers
 */
export abstract class BaseTabRenderer {
  constructor() {}

  /**
   * Render the tab content
   */
  abstract render(data: ComprehensiveInstrumentData): string;

  /**
   * Get the tab identifier
   */
  abstract getTabId(): string;

  /**
   * Get the tab label for display
   */
  abstract getTabLabel(): string;

  /**
   * Get optional tab badge count
   */
  getBadgeCount(_data: ComprehensiveInstrumentData): number | undefined {
    return undefined;
  }

  /**
   * Check if tab should be enabled for given data
   */
  isEnabled(_data: ComprehensiveInstrumentData): boolean {
    return true;
  }

  /**
   * Common method to render no data state
   */
  protected renderNoDataState(title: string, message: string, icon?: string): string {
    const defaultIcon = `
      <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    `;

    return `
      <div class="text-center py-8">
        <div class="text-gray-400 mb-4">
          ${icon || defaultIcon}
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">${title}</h3>
        <p class="text-gray-600">${message}</p>
      </div>
    `;
  }

  /**
   * Render a definition list item
   */
  protected renderDefinitionItem(label: string, value: string, isCode: boolean = false): string {
    const valueClass = isCode ? 'text-sm text-gray-900 font-mono' : 'text-sm text-gray-900';
    return `
      <div class="flex justify-between">
        <dt class="text-sm font-medium text-gray-500">${label}</dt>
        <dd class="${valueClass}">${value || 'N/A'}</dd>
      </div>
    `;
  }

  /**
   * Render a section header
   */
  protected renderSectionHeader(title: string): string {
    return `<h3 class="font-semibold text-gray-900 mb-4">${title}</h3>`;
  }

  /**
   * Render a status badge
   */
  protected renderStatusBadge(status: string, className: string): string {
    return `
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${className}">
        ${status}
      </span>
    `;
  }

  /**
   * Render a metric card
   */
  protected renderMetricCard(title: string, value: string, color: string = 'blue'): string {
    return `
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="text-sm font-medium text-gray-500 mb-2">${title}</div>
        <div class="text-lg font-bold text-${color}-600">${value}</div>
      </div>
    `;
  }

  /**
   * Render a two-column grid container
   */
  protected renderTwoColumnGrid(content: string): string {
    return `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        ${content}
      </div>
    `;
  }

  /**
   * Render a definition list
   */
  protected renderDefinitionList(items: Array<{label: string, value: string, isCode?: boolean}>): string {
    const listItems = items.map(item => this.renderDefinitionItem(item.label, item.value, item.isCode)).join('');
    return `
      <dl class="space-y-3">
        ${listItems}
      </dl>
    `;
  }
}
