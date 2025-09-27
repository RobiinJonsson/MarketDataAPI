import { BaseTabRenderer } from './BaseTabRenderer';
import { ComprehensiveInstrumentData } from '../../types/api';
import { formatDate } from '../../utils/helpers';
import { formatInstrumentType } from '../../utils/formatters/dataFormatters';

export class OverviewTabRenderer extends BaseTabRenderer {
  getTabId(): string {
    return 'overview';
  }

  getTabLabel(): string {
    return 'Overview';
  }

  render(data: ComprehensiveInstrumentData): string {
    const { instrument } = data;

    if (!instrument) {
      return this.renderNoDataState('No Instrument Data', 'Unable to load instrument information');
    }

    return this.renderTwoColumnGrid(`
      <div class="space-y-4">
        ${this.renderSectionHeader('Basic Information')}
        ${this.renderDefinitionList([
          { label: 'ISIN', value: instrument.isin, isCode: true },
          { label: 'Type', value: formatInstrumentType(instrument.instrument_type) },
          { label: 'Short Name', value: instrument.short_name },
          { label: 'CFI Code', value: instrument.cfi_code, isCode: true },
          { label: 'Currency', value: instrument.currency }
        ])}
      </div>

      <div class="space-y-4">
        ${this.renderSectionHeader('FIGI Information')}
        ${this.renderDefinitionList([
          { label: 'FIGI', value: instrument.figi, isCode: true },
          { label: 'Composite FIGI', value: instrument.composite_figi, isCode: true },
          { label: 'Market Sector', value: instrument.market_sector },
          { label: 'Security Type', value: instrument.security_type },
          { label: 'Ticker', value: instrument.ticker }
        ])}
      </div>

      <div class="space-y-4 md:col-span-2">
        ${this.renderSectionHeader('Metadata')}
        <dl class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="flex justify-between md:block">
            <dt class="text-sm font-medium text-gray-500">Created</dt>
            <dd class="text-sm text-gray-900">${formatDate(instrument.created_at)}</dd>
          </div>
          <div class="flex justify-between md:block">
            <dt class="text-sm font-medium text-gray-500">Updated</dt>
            <dd class="text-sm text-gray-900">${formatDate(instrument.updated_at)}</dd>
          </div>
          <div class="flex justify-between md:block">
            <dt class="text-sm font-medium text-gray-500">Trading Venues</dt>
            <dd class="text-sm text-gray-900">${instrument.trading_venues_count || 0}</dd>
          </div>
        </dl>
      </div>
    `);
  }
}
