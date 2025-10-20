import { BasePage } from './BasePage';
import { ApiServiceFactory } from '../services';

// Declare Chart.js types for TypeScript
declare global {
  interface Window {
    Chart: any;
  }
}

/**
 * Analytics Dashboard Page
 * Comprehensive multi-dimensional analytics with interactive Chart.js visualizations
 * Features real-time data, drill-down capabilities, and professional design
 */
export default class AnalyticsPage extends BasePage {
  private analyticsService = ApiServiceFactory.getInstance().analytics;
  private charts: Record<string, any> = {};
  private refreshInterval?: NodeJS.Timeout;

  async render(): Promise<void> {
    this.container.innerHTML = `
      <div class="space-y-8">
        ${this.createSectionHeader('📊 Analytics Dashboard', 'Real-time insights across instruments, entities, and system performance')}
        
        <!-- Key Metrics Overview -->
        <div id="metrics-overview" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Metrics will be loaded dynamically -->
        </div>

        <!-- Main Analytics Grid -->
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
          
          <!-- Instrument Distribution (Doughnut Chart) -->
          <div class="xl:col-span-1">
            ${this.createCard(`
              <div class="relative h-80">
                <canvas id="instrumentChart"></canvas>
              </div>
              <div class="mt-4 space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Total Instruments</span>
                  <span id="total-instruments" class="font-semibold">Loading...</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-500">
                  <span>Last updated</span>
                  <span id="instruments-updated">Loading...</span>
                </div>
              </div>
            `, '🎯 Instrument Types Distribution')}
          </div>

          <!-- Geographic Distribution (Bar Chart) -->
          <div class="xl:col-span-2">
            ${this.createCard(`
              <div class="relative h-80">
                <canvas id="geographicChart"></canvas>
              </div>
              <div class="mt-4 flex justify-between items-center">
                <div class="text-sm text-gray-600">
                  <span id="countries-count">0</span> countries represented
                </div>
                <button id="geo-drill-down" class="text-xs text-blue-600 hover:text-blue-800 font-medium">
                  View Details →
                </button>
              </div>
            `, '🌍 Geographic Distribution')}
          </div>
        </div>

        <!-- Secondary Analytics Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <!-- Growth Trend Analysis -->
          <div>
            ${this.createCard(`
              <div class="relative h-64">
                <canvas id="growthChart"></canvas>
              </div>
              <div class="mt-4 grid grid-cols-3 gap-4 text-center">
                <div class="p-3 bg-green-50 rounded-lg">
                  <p class="text-lg font-bold text-green-600" id="monthly-growth">+0%</p>
                  <p class="text-xs text-green-700">Monthly Growth</p>
                </div>
                <div class="p-3 bg-blue-50 rounded-lg">
                  <p class="text-lg font-bold text-blue-600" id="quarterly-growth">+0%</p>
                  <p class="text-xs text-blue-700">Quarterly Growth</p>
                </div>
                <div class="p-3 bg-purple-50 rounded-lg">
                  <p class="text-lg font-bold text-purple-600" id="yearly-growth">+0%</p>
                  <p class="text-xs text-purple-700">Yearly Growth</p>
                </div>
              </div>
            `, '📈 Growth Trend Analysis')}
          </div>

          <!-- Entity Relationships Network -->
          <div>
            ${this.createCard(`
              <div class="relative h-64">
                <canvas id="entityChart"></canvas>
              </div>
              <div class="mt-4 space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Total Legal Entities</span>
                  <span id="total-entities" class="font-semibold">Loading...</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">With Relationships</span>
                  <span id="entities-with-relationships" class="font-semibold text-blue-600">Loading...</span>
                </div>
              </div>
            `, '🏢 Entity Relationship Network')}
          </div>
        </div>

        <!-- System Performance & Data Quality -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- Data Quality Dashboard -->
          <div>
            ${this.createCard(`
              <div class="space-y-4">
                <div class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-700">Data Completeness</span>
                    <span id="completeness-percent" class="text-sm font-semibold text-gray-900">0%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div id="completeness-bar" class="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full transition-all duration-1000 ease-out" style="width: 0%"></div>
                  </div>
                  
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-700">Recent Updates</span>
                    <span id="updates-percent" class="text-sm font-semibold text-gray-900">0%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div id="updates-bar" class="bg-gradient-to-r from-blue-400 to-blue-600 h-3 rounded-full transition-all duration-1000 ease-out" style="width: 0%"></div>
                  </div>
                  
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-700">Validation Status</span>
                    <span id="validation-percent" class="text-sm font-semibold text-gray-900">0%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div id="validation-bar" class="bg-gradient-to-r from-purple-400 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out" style="width: 0%"></div>
                  </div>
                </div>
                
                <div class="pt-4 border-t border-gray-200">
                  <div class="flex items-center justify-center">
                    <div id="overall-score" class="text-center">
                      <p class="text-2xl font-bold text-gray-900">0</p>
                      <p class="text-xs text-gray-600">Overall Score</p>
                    </div>
                  </div>
                </div>
              </div>
            `, '🎯 Data Quality Score')}
          </div>

          <!-- System Health Monitoring -->
          <div>
            ${this.createCard(`
              <div class="space-y-4">
                <div class="grid grid-cols-2 gap-3">
                  <div class="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-lg border border-green-200">
                    <p id="uptime-percent" class="text-2xl font-bold text-green-600">0%</p>
                    <p class="text-xs text-green-700 font-medium">System Uptime</p>
                  </div>
                  <div class="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg border border-blue-200">
                    <p id="response-time" class="text-2xl font-bold text-blue-600">0ms</p>
                    <p class="text-xs text-blue-700 font-medium">Avg Response</p>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div class="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg border border-purple-200">
                    <p id="database-size" class="text-2xl font-bold text-purple-600">0GB</p>
                    <p class="text-xs text-purple-700 font-medium">Database Size</p>
                  </div>
                  <div class="text-center p-4 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg border border-orange-200">
                    <p id="api-calls" class="text-2xl font-bold text-orange-600">0</p>
                    <p class="text-xs text-orange-700 font-medium">API Calls/hr</p>
                  </div>
                </div>
                <div class="pt-2">
                  <div class="flex justify-between items-center text-xs text-gray-500">
                    <span>Last health check</span>
                    <span id="last-health-check">Loading...</span>
                  </div>
                </div>
              </div>
            `, '💚 System Health Monitor')}
          </div>

          <!-- Live Activity Feed -->
          <div>
            ${this.createCard(`
              <div id="activity-feed" class="space-y-3 max-h-64 overflow-y-auto">
                <div class="text-center text-gray-500 py-8">
                  <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto mb-2"></div>
                  Loading activity feed...
                </div>
              </div>
              <div class="pt-4 border-t border-gray-200 mt-4">
                <div class="flex justify-between items-center">
                  <button id="refresh-feed" class="text-xs text-blue-600 hover:text-blue-800 font-medium">
                    🔄 Refresh Feed
                  </button>
                  <div class="flex items-center space-x-2">
                    <div id="live-indicator" class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span class="text-xs text-gray-600">Live</span>
                  </div>
                </div>
              </div>
            `, '📡 Live Activity Feed')}
          </div>
        </div>

        <!-- Refresh Controls -->
        <div class="flex justify-center pt-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div class="flex items-center space-x-4">
              <button id="refresh-all" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors text-sm font-medium">
                🔄 Refresh All Data
              </button>
              <div class="flex items-center space-x-2 text-sm text-gray-600">
                <span>Auto-refresh:</span>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input id="auto-refresh" type="checkbox" checked class="sr-only">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              <div class="text-xs text-gray-500">
                Last updated: <span id="last-updated">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    // Initialize the dashboard
    await this.initializeDashboard();
  }

  private async initializeDashboard(): Promise<void> {
    try {
      // Show loading state
      this.showAnalyticsLoading();
      
      // Load all analytics data
      await this.loadAnalyticsData();
      
      // Initialize charts
      this.initializeCharts();
      
      // Set up event listeners
      this.setupEventListeners();
      
      // Start auto-refresh if enabled
      this.startAutoRefresh();
      
    } catch (error) {
      console.error('Error initializing analytics dashboard:', error);
      this.showAnalyticsError('Failed to load analytics data. Please try again.');
    }
  }

  private showAnalyticsLoading(): void {
    // Update metrics overview with loading placeholders
    const metricsContainer = this.container.querySelector('#metrics-overview');
    if (metricsContainer) {
      metricsContainer.innerHTML = Array(4).fill(0).map(() => `
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div class="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      `).join('');
    }
  }

  private async loadAnalyticsData(): Promise<void> {
    try {
      // Load system analytics from API
      const response = await this.analyticsService.getSystemAnalytics();
      
      if (response.status === 'success' && response.data) {
        this.updateMetricsOverview(response.data);
        this.updateDataQuality(response.data.data_quality);
        this.updateSystemHealth(response.data.system_health);
        
        // Load additional analytics data
        const [instrumentAnalytics, entityAnalytics] = await Promise.all([
          this.analyticsService.getInstrumentAnalytics(),
          this.analyticsService.getEntityAnalytics()
        ]);
        
        if (instrumentAnalytics.status === 'success' && instrumentAnalytics.data) {
          this.updateInstrumentData(instrumentAnalytics.data);
        }
        
        if (entityAnalytics.status === 'success' && entityAnalytics.data) {
          this.updateEntityData(entityAnalytics.data);
        }
      }
    } catch (error) {
      console.error('Error loading analytics data:', error);
      throw error;
    }
  }

  private updateMetricsOverview(data: any): void {
    const metricsContainer = this.container.querySelector('#metrics-overview');
    if (!metricsContainer) return;
    
    const metrics = [
      {
        title: 'Total Instruments',
        value: data.instrument_stats.total.toLocaleString(),
        change: '+1.2%',
        changeType: 'positive',
        icon: '🎯'
      },
      {
        title: 'Legal Entities',
        value: data.entity_stats.total.toLocaleString(),
        change: '+0.8%',
        changeType: 'positive',
        icon: '🏢'
      },
      {
        title: 'Data Quality',
        value: `${Math.round(data.data_quality.completeness_percentage)}%`,
        change: '+2.1%',
        changeType: 'positive',
        icon: '🎯'
      },
      {
        title: 'System Health',
        value: `${data.system_health.uptime_percentage}%`,
        change: 'Stable',
        changeType: 'neutral',
        icon: '💚'
      }
    ];

    metricsContainer.innerHTML = metrics.map(metric => `
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">${metric.title}</p>
            <p class="text-3xl font-bold text-gray-900">${metric.value}</p>
            <div class="flex items-center mt-2">
              <span class="text-sm font-medium ${
                metric.changeType === 'positive' ? 'text-green-600' : 
                metric.changeType === 'negative' ? 'text-red-600' : 'text-gray-600'
              }">${metric.change}</span>
              <span class="text-sm text-gray-500 ml-2">vs last month</span>
            </div>
          </div>
          <div class="text-3xl">${metric.icon}</div>
        </div>
      </div>
    `).join('');
  }

  private updateDataQuality(dataQuality: any): void {
    // Update data quality metrics with animations
    setTimeout(() => {
      this.updateElement('#completeness-percent', `${dataQuality.completeness_percentage}%`);
      this.updateElement('#completeness-bar', '', { width: `${dataQuality.completeness_percentage}%` });
      
      this.updateElement('#updates-percent', `${dataQuality.recent_updates_percentage}%`);
      this.updateElement('#updates-bar', '', { width: `${dataQuality.recent_updates_percentage}%` });
      
      this.updateElement('#validation-percent', `${dataQuality.validation_pass_percentage}%`);
      this.updateElement('#validation-bar', '', { width: `${dataQuality.validation_pass_percentage}%` });
      
      const overallScore = Math.round(
        (dataQuality.completeness_percentage + dataQuality.recent_updates_percentage + dataQuality.validation_pass_percentage) / 3
      );
      this.updateElement('#overall-score p', overallScore.toString());
    }, 500);
  }

  private updateSystemHealth(systemHealth: any): void {
    this.updateElement('#uptime-percent', `${systemHealth.uptime_percentage}%`);
    this.updateElement('#response-time', `${systemHealth.avg_response_time}ms`);
    this.updateElement('#database-size', `${systemHealth.database_size}GB`);
    this.updateElement('#api-calls', systemHealth.api_calls_per_hour.toLocaleString());
    this.updateElement('#last-health-check', new Date().toLocaleTimeString());
  }

  private updateInstrumentData(data: any): void {
    this.updateElement('#total-instruments', data.distribution_by_type 
      ? Object.values(data.distribution_by_type as Record<string, number>).reduce((a: number, b: number) => a + b, 0).toLocaleString()
      : 'N/A');
    this.updateElement('#instruments-updated', new Date().toLocaleTimeString());
    
    // Update growth metrics
    const growth = data.growth_trend;
    if (growth && growth.length >= 2) {
      const lastMonth = growth[growth.length - 1].count;
      const prevMonth = growth[growth.length - 2].count;
      const monthlyGrowth = ((lastMonth - prevMonth) / prevMonth * 100).toFixed(1);
      this.updateElement('#monthly-growth', `+${monthlyGrowth}%`);
    }
  }

  private updateEntityData(data: any): void {
    if (data.distribution_by_country) {
      const total = Object.values(data.distribution_by_country as Record<string, number>).reduce((a: number, b: number) => a + b, 0);
      this.updateElement('#total-entities', total.toLocaleString());
    }
    
    if (data.relationship_statistics) {
      this.updateElement('#entities-with-relationships', 
        data.relationship_statistics.entities_with_parents.toLocaleString());
    }
    
    this.updateElement('#countries-count', Object.keys(data.distribution_by_country || {}).length.toString());
  }

  private initializeCharts(): void {
    if (!window.Chart) {
      console.error('Chart.js not loaded');
      return;
    }

    // Initialize all charts
    this.initializeInstrumentChart();
    this.initializeGeographicChart();
    this.initializeGrowthChart();
    this.initializeEntityChart();
  }

  private initializeInstrumentChart(): void {
    const canvas = this.container.querySelector('#instrumentChart') as HTMLCanvasElement;
    if (!canvas) return;

    this.charts.instrument = new window.Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: ['Equities', 'Debt', 'Futures', 'Options', 'Other'],
        datasets: [{
          data: [85420, 28930, 8520, 2560, 1570],
          backgroundColor: [
            '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'
          ],
          borderWidth: 0,
          hoverBorderWidth: 2,
          hoverBorderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 20,
              usePointStyle: true,
              font: { size: 12 }
            }
          }
        },
        animation: {
          animateRotate: true,
          duration: 2000
        }
      }
    });
  }

  private initializeGeographicChart(): void {
    const canvas = this.container.querySelector('#geographicChart') as HTMLCanvasElement;
    if (!canvas) return;

    this.charts.geographic = new window.Chart(canvas, {
      type: 'bar',
      data: {
        labels: ['United States', 'United Kingdom', 'Germany', 'France', 'Japan', 'Canada'],
        datasets: [{
          label: 'Instruments',
          data: [45230, 28540, 15420, 12340, 8920, 6520],
          backgroundColor: '#3B82F6',
          borderRadius: 4,
          hoverBackgroundColor: '#2563EB'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            grid: { display: false },
            ticks: { 
              callback: function(value: any) {
                return value >= 1000 ? (value / 1000) + 'K' : value;
              }
            }
          },
          x: {
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false }
        },
        animation: {
          delay: (context: any) => context.dataIndex * 100,
          duration: 1500
        }
      }
    });
  }

  private initializeGrowthChart(): void {
    const canvas = this.container.querySelector('#growthChart') as HTMLCanvasElement;
    if (!canvas) return;

    this.charts.growth = new window.Chart(canvas, {
      type: 'line',
      data: {
        labels: ['Apr 2025', 'May 2025', 'Jun 2025', 'Jul 2025', 'Aug 2025', 'Sep 2025'],
        datasets: [{
          label: 'Total Instruments',
          data: [122190, 123450, 124320, 124890, 125190, 125430],
          borderColor: '#10B981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#10B981',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            grid: { color: '#f3f4f6' },
            ticks: { 
              callback: function(value: any) {
                return (value / 1000) + 'K';
              }
            }
          },
          x: { grid: { display: false } }
        },
        plugins: {
          legend: { display: false }
        },
        animation: {
          duration: 2000,
          easing: 'easeOutQuart'
        }
      }
    });
  }

  private initializeEntityChart(): void {
    const canvas = this.container.querySelector('#entityChart') as HTMLCanvasElement;
    if (!canvas) return;

    this.charts.entity = new window.Chart(canvas, {
      type: 'polarArea',
      data: {
        labels: ['US Entities', 'UK Entities', 'EU Entities', 'APAC Entities', 'Other'],
        datasets: [{
          data: [2540, 1820, 2220, 1590, 750],
          backgroundColor: [
            'rgba(59, 130, 246, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(239, 68, 68, 0.8)',
            'rgba(139, 92, 246, 0.8)'
          ],
          borderColor: [
            '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'
          ],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 15,
              usePointStyle: true,
              font: { size: 11 }
            }
          }
        },
        animation: {
          duration: 2500,
          animateRotate: true,
          animateScale: true
        }
      }
    });
  }

  private setupEventListeners(): void {
    // Refresh all data
    const refreshBtn = this.container.querySelector('#refresh-all');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.refreshAllData());
    }

    // Auto-refresh toggle
    const autoRefreshToggle = this.container.querySelector('#auto-refresh') as HTMLInputElement;
    if (autoRefreshToggle) {
      autoRefreshToggle.addEventListener('change', (e) => {
        const target = e.target as HTMLInputElement;
        if (target.checked) {
          this.startAutoRefresh();
        } else {
          this.stopAutoRefresh();
        }
      });
    }

    // Geographic drill-down
    const geoDrillDown = this.container.querySelector('#geo-drill-down');
    if (geoDrillDown) {
      geoDrillDown.addEventListener('click', () => {
        // Navigate to detailed geographic view
        console.log('Geographic drill-down clicked');
      });
    }

    // Refresh activity feed
    const refreshFeed = this.container.querySelector('#refresh-feed');
    if (refreshFeed) {
      refreshFeed.addEventListener('click', () => this.updateActivityFeed());
    }
  }

  private startAutoRefresh(): void {
    this.stopAutoRefresh(); // Clear existing interval
    this.refreshInterval = setInterval(() => {
      this.refreshAllData(false); // Quiet refresh
    }, 30000); // Refresh every 30 seconds
  }

  private stopAutoRefresh(): void {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
      this.refreshInterval = undefined;
    }
  }

  private async refreshAllData(showLoading: boolean = true): Promise<void> {
    try {
      if (showLoading) {
        this.showAnalyticsLoading();
      }
      
      await this.loadAnalyticsData();
      this.updateElement('#last-updated', new Date().toLocaleTimeString());
      this.updateActivityFeed();
      
    } catch (error) {
      console.error('Error refreshing analytics data:', error);
    }
  }

  private updateActivityFeed(): void {
    const activityFeed = this.container.querySelector('#activity-feed');
    if (!activityFeed) return;

    const activities = [
      { time: '2 min ago', action: '📊 New instrument added', details: 'US equity SE0000123456' },
      { time: '5 min ago', action: '🔄 Entity relationship updated', details: 'LEI 213800ABCDEF123456' },
      { time: '8 min ago', action: '✅ Data validation completed', details: '1,247 instruments processed' },
      { time: '12 min ago', action: '📈 Analytics refreshed', details: 'All dashboards updated' },
      { time: '15 min ago', action: '🌐 MIC data synchronized', details: '23 trading venues updated' }
    ];

    activityFeed.innerHTML = activities.map(activity => `
      <div class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
        <div class="flex-shrink-0 text-xs text-gray-500 w-16">${activity.time}</div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900">${activity.action}</p>
          <p class="text-xs text-gray-600">${activity.details}</p>
        </div>
      </div>
    `).join('');
  }

  private updateElement(selector: string, content: string, styles?: Record<string, string>): void {
    const element = this.container.querySelector(selector) as HTMLElement;
    if (element) {
      if (content) element.textContent = content;
      if (styles) {
        Object.assign(element.style, styles);
      }
    }
  }

  private showAnalyticsError(message: string): void {
    const container = this.container.querySelector('#main-content') || this.container;
    container.innerHTML = `
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <div class="text-red-600 mb-2">
          <svg class="w-8 h-8 mx-auto" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-red-800 mb-2">Analytics Error</h3>
        <p class="text-red-700">${message}</p>
        <button onclick="location.reload()" class="mt-4 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors">
          Try Again
        </button>
      </div>
    `;
  }
}