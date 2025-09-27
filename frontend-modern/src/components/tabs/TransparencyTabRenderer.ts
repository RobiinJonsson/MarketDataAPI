import { BaseTabRenderer } from './BaseTabRenderer';
import { ComprehensiveInstrumentData } from '../../types/api';
import { formatCurrency, formatDateRange, calculateTrendInsight } from '../../utils/formatters/dataFormatters';
import { formatNumber } from '../../utils/helpers';

export class TransparencyTabRenderer extends BaseTabRenderer {
  getTabId(): string {
    return 'transparency';
  }

  getTabLabel(): string {
    return 'Transparency';
  }

  isEnabled(data: ComprehensiveInstrumentData): boolean {
    return Array.isArray(data.transparency) && data.transparency.length > 0;
  }

  getBadgeCount(data: ComprehensiveInstrumentData): number | undefined {
    return Array.isArray(data.transparency) ? data.transparency.length : undefined;
  }

  render(data: ComprehensiveInstrumentData): string {
    const { transparency } = data;

    if (!Array.isArray(transparency) || transparency.length === 0) {
      return this.renderNoDataState(
        'No Transparency Data',
        'No MiFID II transparency calculations are available for this instrument'
      );
    }

    return `
      <div class="space-y-6">
        ${this.renderTransparencyOverview(transparency)}
        ${this.renderCalculationPeriods(transparency)}
        ${this.renderTrendAnalysis(transparency)}
      </div>
    `;
  }

  private renderTransparencyOverview(transparency: any[]): string {
    const latest = transparency[0];
    if (!latest) return '';

    // Calculate metrics from FITRS data
    const totalTxs = latest.total_transactions_executed || 0;
    const totalVol = latest.total_volume_executed || 0;
    const avgTxValue = totalTxs > 0 ? totalVol / totalTxs : 0;
    
    // Calculate period length in days for daily averages
    const fromDate = new Date(latest.from_date);
    const toDate = new Date(latest.to_date);
    const periodDays = Math.ceil((toDate.getTime() - fromDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;
    
    const avgDailyTxs = periodDays > 0 ? totalTxs / periodDays : 0;
    const avgDailyVol = periodDays > 0 ? totalVol / periodDays : 0;

    return `
      <div class="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg p-6">
        ${this.renderSectionHeader('Latest Transparency Metrics')}
        <div class="mb-2 text-xs text-blue-700">
          Period: ${formatDateRange(latest.from_date, latest.to_date)} (${periodDays} days) • ${this.getAssetClassLabel(latest.file_type)}
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          ${this.renderMetricCard('Average Daily Volume', `€${formatCurrency(avgDailyVol)}`, 'blue')}
          ${this.renderMetricCard('Average Daily Transactions', formatNumber(avgDailyTxs), 'purple')}
          ${this.renderMetricCard('Average Transaction Value', `€${formatCurrency(avgTxValue)}`, 'orange')}
        </div>
        
        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          ${this.renderMetricCard('Total Transactions', formatNumber(totalTxs), 'gray')}
          ${this.renderMetricCard('Total Volume', `€${formatCurrency(totalVol)}`, 'gray')}
        </div>
      </div>
    `;
  }



  private renderCalculationPeriods(transparency: any[]): string {
    return `
      <div class="bg-white rounded-lg border border-gray-200">
        ${this.renderSectionHeader('Calculation Periods')}
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Period</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transactions</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Value</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Liquidity</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              ${transparency.map(calc => this.renderCalculationRow(calc)).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  private renderCalculationRow(calc: any): string {
    const avgValue = calc.total_transactions_executed > 0 
      ? (calc.total_volume_executed || 0) / calc.total_transactions_executed 
      : 0;

    return `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          ${formatDateRange(calc.from_date, calc.to_date)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-medium text-blue-600">${formatNumber(calc.total_transactions_executed || 0)}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          <div class="text-sm font-medium text-green-600">€${formatCurrency(calc.total_volume_executed || 0)}</div>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          €${formatCurrency(avgValue)}
        </td>
        <td class="px-6 py-4 whitespace-nowrap">
          ${this.renderLiquidityBadge(calc.liquidity)}
        </td>
      </tr>
    `;
  }

  private renderLiquidityBadge(liquidity: boolean | null): string {
    if (liquidity === null || liquidity === undefined) {
      return this.renderStatusBadge('N/A', 'bg-gray-100 text-gray-600');
    }
    
    const isLiquid = liquidity === true;
    return this.renderStatusBadge(
      isLiquid ? 'Liquid' : 'Illiquid',
      isLiquid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
    );
  }

  private renderTrendAnalysis(transparency: any[]): string {
    if (transparency.length < 2) {
      return `
        <div class="bg-yellow-50 rounded-lg p-4">
          ${this.renderSectionHeader('Trend Analysis')}
          <p class="text-sm text-yellow-700">At least 2 calculation periods are required for trend analysis.</p>
        </div>
      `;
    }

    const validData = transparency.filter(calc => 
      calc.total_transactions_executed != null && calc.total_volume_executed != null
    );
    const insight = calculateTrendInsight(validData);

    return `
      <div class="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6">
        ${this.renderSectionHeader('Trend Analysis')}
        <div class="space-y-4">
          <div class="bg-white rounded-lg p-4 border border-gray-200">
            <h4 class="text-sm font-medium text-gray-900 mb-2">Market Insight</h4>
            <p class="text-sm text-gray-700">${insight}</p>
          </div>
          
          ${this.renderTrendMetrics(validData)}
        </div>
      </div>
    `;
  }

  private renderTrendMetrics(data: any[]): string {
    if (data.length < 2) return '';

    const latest = data[0];
    const previous = data[1];

    const volumeChange = this.calculatePercentageChange(
      previous.total_volume_executed || 0,
      latest.total_volume_executed || 0
    );

    const transactionChange = this.calculatePercentageChange(
      previous.total_transactions_executed || 0,
      latest.total_transactions_executed || 0
    );

    return `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        ${this.renderTrendCard('Volume Change', volumeChange, 'volume')}
        ${this.renderTrendCard('Transaction Change', transactionChange, 'transactions')}
      </div>
    `;
  }

  private renderTrendCard(title: string, change: number, type: string): string {
    const isPositive = change > 0;
    const color = isPositive ? 'green' : 'red';
    const icon = isPositive ? '↗' : '↘';
    
    return `
      <div class="bg-white rounded-lg p-4 border border-gray-200">
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-600">${title}</span>
          <span class="text-lg font-bold text-${color}-600">
            ${icon} ${Math.abs(change).toFixed(1)}%
          </span>
        </div>
        <div class="text-xs text-gray-500 mt-1">
          Period-over-period ${type} trend
        </div>
      </div>
    `;
  }

  private calculatePercentageChange(previous: number, current: number): number {
    if (previous === 0) return current > 0 ? 100 : 0;
    return ((current - previous) / previous) * 100;
  }

  private getAssetClassLabel(fileType: string): string {
    if (!fileType) return 'Unknown Asset Class';
    
    // Handle FITRS file type patterns: FULECR_E, FULECR_N, etc.
    if (fileType.includes('_E')) return 'Equity';
    if (fileType.includes('_N')) return 'Non-Equity';
    if (fileType.includes('_D')) return 'Derivatives';
    if (fileType.includes('_B')) return 'Bonds';
    
    return fileType;
  }
}
