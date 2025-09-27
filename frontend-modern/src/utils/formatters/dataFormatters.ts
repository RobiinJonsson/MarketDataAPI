/**
 * Financial data formatting utilities
 */

/**
 * Format currency values with K/M abbreviations for large numbers
 */
export function formatCurrency(value: number): string {
  if (isNaN(value) || value === null || value === undefined) {
    return '0';
  }
  
  if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + 'M';
  } else if (value >= 1000) {
    return (value / 1000).toFixed(1) + 'K';
  }
  return value.toLocaleString();
}

/**
 * Format a date range for display
 */
export function formatDateRange(fromDate: string, toDate: string): string {
  if (!fromDate || !toDate) return 'N/A';
  
  const from = new Date(fromDate);
  const to = new Date(toDate);
  
  if (isNaN(from.getTime()) || isNaN(to.getTime())) {
    return 'Invalid date range';
  }
  
  return `${from.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })} - ${to.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}`;
}

/**
 * Format large numbers with appropriate suffixes
 */
export function formatLargeNumber(value: number): string {
  if (isNaN(value) || value === null || value === undefined) {
    return '0';
  }
  
  if (value >= 1000000000) {
    return (value / 1000000000).toFixed(1) + 'B';
  } else if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + 'M';
  } else if (value >= 1000) {
    return (value / 1000).toFixed(1) + 'K';
  }
  return value.toString();
}

/**
 * Format percentage values
 */
export function formatPercentage(value: number, decimals: number = 1): string {
  if (isNaN(value) || value === null || value === undefined) {
    return '0.0%';
  }
  return `${value.toFixed(decimals)}%`;
}

/**
 * Calculate and format trend insights from time series data
 */
export function calculateTrendInsight(data: any[]): string {
  if (!data || data.length < 2) {
    return 'Insufficient data for trend analysis';
  }
  
  const volumes = data.map(d => d.total_volume_executed || 0).filter(v => !isNaN(v));
  const transactions = data.map(d => d.total_transactions_executed || 0).filter(t => !isNaN(t));
  
  if (volumes.length < 2 || transactions.length < 2) {
    return 'Insufficient valid data for trend analysis';
  }
  
  const volumeTrend = volumes[volumes.length - 1] > volumes[0] ? 'increasing' : 'decreasing';
  const transactionTrend = transactions[transactions.length - 1] > transactions[0] ? 'increasing' : 'decreasing';
  
  const volumeChange = volumes[0] !== 0 ? ((volumes[volumes.length - 1] - volumes[0]) / volumes[0] * 100) : 0;
  const transactionChange = transactions[0] !== 0 ? ((transactions[transactions.length - 1] - transactions[0]) / transactions[0] * 100) : 0;
  
  return `Trading volume is ${volumeTrend} (${formatPercentage(volumeChange)} change) and transaction count is ${transactionTrend} (${formatPercentage(transactionChange)} change) across the reporting periods.`;
}

/**
 * Format instrument type for display
 */
export function formatInstrumentType(type: string): string {
  if (!type) return 'Unknown';
  
  return type
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

/**
 * Format ISIN with proper spacing
 */
export function formatIsin(isin: string): string {
  if (!isin || isin.length !== 12) return isin;
  
  // Format as XX XXXXXXXXX X (country code, identifier, check digit)
  return `${isin.slice(0, 2)} ${isin.slice(2, 11)} ${isin.slice(11)}`;
}

/**
 * Format LEI status for display
 */
export function formatLeiStatus(status: string): string {
  if (!status) return 'Unknown';
  
  const statusMap: Record<string, string> = {
    'ISSUED': 'Active',
    'LAPSED': 'Lapsed',
    'MERGED': 'Merged',
    'RETIRED': 'Retired',
    'DUPLICATE': 'Duplicate',
    'PENDING_VALIDATION': 'Pending Validation',
    'PENDING_TRANSFER': 'Pending Transfer'
  };
  
  return statusMap[status.toUpperCase()] || status;
}

/**
 * Get status badge class for LEI status
 */
export function getLeiStatusBadgeClass(status: string): string {
  if (!status) return 'bg-gray-100 text-gray-800';
  
  const statusClasses: Record<string, string> = {
    'ISSUED': 'bg-green-100 text-green-800',
    'LAPSED': 'bg-red-100 text-red-800',
    'MERGED': 'bg-blue-100 text-blue-800',
    'RETIRED': 'bg-gray-100 text-gray-800',
    'DUPLICATE': 'bg-yellow-100 text-yellow-800',
    'PENDING_VALIDATION': 'bg-orange-100 text-orange-800',
    'PENDING_TRANSFER': 'bg-purple-100 text-purple-800'
  };
  
  return statusClasses[status.toUpperCase()] || 'bg-gray-100 text-gray-800';
}

/**
 * Format trading venue MIC code
 */
export function formatMicCode(mic: string): string {
  if (!mic) return 'Unknown';
  return mic.toUpperCase();
}

/**
 * Format boolean values for display
 */
export function formatBoolean(value: boolean | string): string {
  if (typeof value === 'string') {
    return value.toLowerCase() === 'true' ? 'Yes' : 'No';
  }
  return value ? 'Yes' : 'No';
}
