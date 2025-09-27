import { BaseTabRenderer } from './BaseTabRenderer';
import { ComprehensiveInstrumentData } from '../../types/api';
import { formatMicCode, formatBoolean } from '../../utils/formatters/dataFormatters';

export class VenuesTabRenderer extends BaseTabRenderer {
  getTabId(): string {
    return 'venues';
  }

  getTabLabel(): string {
    return 'Trading Venues';
  }

  isEnabled(data: ComprehensiveInstrumentData): boolean {
    return Array.isArray(data.venues) && data.venues.length > 0;
  }

  getBadgeCount(data: ComprehensiveInstrumentData): number | undefined {
    return Array.isArray(data.venues) ? data.venues.length : undefined;
  }

  render(data: ComprehensiveInstrumentData): string {
    const { venues } = data;

    if (!Array.isArray(venues) || venues.length === 0) {
      return this.renderNoDataState(
        'No Trading Venues',
        'This instrument is not currently traded on any registered venues in our database'
      );
    }

    return `
      <div class="space-y-6">
        ${this.renderVenuesOverview(venues)}
        ${this.renderVenuesTable(venues)}
      </div>
    `;
  }

  private renderVenuesOverview(venues: any[]): string {
    const activeVenues = venues.filter(v => v.is_active === true || v.is_active === 'true');
    const countries = Array.from(new Set(venues.map(v => v.country).filter(Boolean)));
    const segments = Array.from(new Set(venues.map(v => v.market_segment).filter(Boolean)));

    return `
      <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6">
        ${this.renderSectionHeader('Trading Overview')}
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          ${this.renderMetricCard('Total Venues', venues.length.toString())}
          ${this.renderMetricCard('Active Venues', activeVenues.length.toString(), 'green')}
          ${this.renderMetricCard('Countries', countries.length.toString(), 'purple')}
          ${this.renderMetricCard('Market Segments', segments.length.toString(), 'orange')}
        </div>
      </div>
    `;
  }

  private renderVenuesTable(venues: any[]): string {
    return `
      <div class="bg-white rounded-lg border border-gray-200">
        ${this.renderSectionHeader('Venue Details')}
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Venue</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">MIC Code</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Segment</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Currency</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              ${venues.map(venue => this.renderVenueRow(venue)).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  private renderVenueRow(venue: any): string {
    const isActive = venue.is_active === true || venue.is_active === 'true';
    
    return `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-medium text-gray-900">${venue.venue_name || venue.name || 'Unknown Venue'}</div>
          ${venue.venue_type ? `<div class="text-sm text-gray-500">${venue.venue_type}</div>` : ''}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-mono text-gray-900">${formatMicCode(venue.mic_code || venue.mic)}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm text-gray-900">${venue.country || 'N/A'}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm text-gray-900">${venue.market_segment || 'N/A'}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          ${this.renderStatusBadge(
            formatBoolean(isActive),
            isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          )}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${venue.currency || 'N/A'}
        </td>
      </tr>
    `;
  }
}
