/**
 * MIC (Market Identifier Code) API Service
 * Handles both local database and remote ISO registry MIC operations
 */

import { BaseApiService } from './BaseApiService';
import {
  ApiResponse,
  MicCode,
  MicStatistics,
  CountryMicData,
  PaginationParams,
  RequestConfig
} from '../types/api';

export class MicService extends BaseApiService {
  
  // ===== LOCAL DATABASE OPERATIONS =====

  /**
   * List MIC codes from local database
   */
  async listMics(
    filters: {
      country?: string;
      status?: string;
      search?: string;
    } = {},
    pagination: PaginationParams = {},
    config?: RequestConfig
  ): Promise<ApiResponse<MicCode[]>> {
    const params = {
      ...filters,
      ...pagination,
    };
    
    return this.get<MicCode[]>('/mic/', params, config);
  }

  /**
   * Get MIC details by code
   */
  async getMic(micCode: string, config?: RequestConfig): Promise<ApiResponse<MicCode>> {
    return this.get<MicCode>(`/mic/${encodeURIComponent(micCode)}/`, {}, config);
  }

  /**
   * Get MIC segments
   */
  async getMicSegments(micCode: string, config?: RequestConfig): Promise<ApiResponse<MicCode[]>> {
    return this.get<MicCode[]>(`/mic/${encodeURIComponent(micCode)}/segments`, {}, config);
  }

  /**
   * Get countries with MIC statistics
   */
  async getCountries(config?: RequestConfig): Promise<ApiResponse<CountryMicData[]>> {
    return this.get<CountryMicData[]>('/mic/countries', {}, { ...config, cache: true });
  }

  /**
   * Search MIC codes
   */
  async searchMics(
    query: string,
    options: {
      country?: string;
      status?: string;
      limit?: number;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<MicCode[]>> {
    return this.get<MicCode[]>('/mic/search', {
      q: query,
      ...options,
    }, { ...config, cache: false });
  }

  /**
   * Get MIC statistics
   */
  async getMicStatistics(config?: RequestConfig): Promise<ApiResponse<MicStatistics>> {
    return this.get<MicStatistics>('/mic/statistics', {}, { ...config, cache: true });
  }

  /**
   * Load MIC data into local database
   */
  async loadMicData(
    options: {
      force_refresh?: boolean;
      source?: 'remote' | 'file';
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<any>> {
    return this.post<any>('/mic/load-data', options, {
      ...config,
      timeout: 120000, // 2 minutes for data loading
    });
  }

  /**
   * Get MIC enumerations
   */
  async getMicEnums(config?: RequestConfig): Promise<ApiResponse<{
    statuses: string[];
    countries: string[];
    market_types: string[];
  }>> {
    return this.get<any>('/mic/enums', {}, { ...config, cache: true });
  }

  // ===== REMOTE ISO REGISTRY OPERATIONS =====

  /**
   * Remote MIC lookup
   */
  async remoteLookup(micCode: string, config?: RequestConfig): Promise<ApiResponse<MicCode>> {
    return this.get<MicCode>(`/mic/remote/lookup/${encodeURIComponent(micCode)}`, {}, {
      ...config,
      timeout: 15000, // 15 seconds for remote calls
    });
  }

  /**
   * Remote MIC search
   */
  async remoteSearch(
    query: {
      name?: string;
      country?: string;
      city?: string;
      mic?: string;
    },
    config?: RequestConfig
  ): Promise<ApiResponse<MicCode[]>> {
    return this.get<MicCode[]>('/mic/remote/search', query, {
      ...config,
      timeout: 20000, // 20 seconds for remote search
      cache: false,
    });
  }

  /**
   * Get MICs by country from remote registry
   */
  async getRemoteCountryMics(countryCode: string, config?: RequestConfig): Promise<ApiResponse<MicCode[]>> {
    return this.get<MicCode[]>(`/mic/remote/country/${encodeURIComponent(countryCode)}`, {}, {
      ...config,
      timeout: 15000,
      cache: true, // Cache remote country data for 30 minutes
    });
  }

  /**
   * Validate MIC against remote registry
   */
  async validateMicRemote(micCode: string, config?: RequestConfig): Promise<ApiResponse<{
    valid: boolean;
    exists_locally: boolean;
    exists_remotely: boolean;
    differences?: Record<string, any>;
  }>> {
    return this.get<any>(`/mic/remote/validate/${encodeURIComponent(micCode)}`, {}, {
      ...config,
      timeout: 10000,
    });
  }

  /**
   * Clear remote cache
   */
  async clearRemoteCache(config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.delete<any>('/mic/remote/cache/clear', config);
  }

  // ===== CONVENIENCE METHODS =====

  /**
   * Get MICs by country
   */
  async getMicsByCountry(
    countryCode: string,
    includeSegments: boolean = false,
    config?: RequestConfig
  ): Promise<ApiResponse<MicCode[]>> {
    const params: any = { country: countryCode };
    if (includeSegments) {
      params.include_segments = true;
    }
    
    return this.listMics(params, {}, config);
  }

  /**
   * Get active MICs only
   */
  async getActiveMics(
    filters: {
      country?: string;
      search?: string;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<MicCode[]>> {
    return this.listMics({
      ...filters,
      status: 'ACTIVE',
    }, {}, config);
  }

  /**
   * Compare local vs remote MIC data
   */
  async compareMicData(micCode: string, config?: RequestConfig): Promise<ApiResponse<{
    local: MicCode | null;
    remote: MicCode | null;
    differences: string[];
    recommendation: string;
  }>> {
    try {
      const [localResponse, remoteResponse] = await Promise.allSettled([
        this.getMic(micCode, config),
        this.remoteLookup(micCode, config),
      ]);

      const local = localResponse.status === 'fulfilled' ? localResponse.value.data || null : null;
      const remote = remoteResponse.status === 'fulfilled' ? remoteResponse.value.data || null : null;

      const differences: string[] = [];
      let recommendation = 'No action needed';

      if (local && remote) {
        // Compare fields and identify differences
        if (local.name !== remote.name) {
          differences.push(`Name: "${local.name}" vs "${remote.name}"`);
        }
        if (local.status !== remote.status) {
          differences.push(`Status: "${local.status}" vs "${remote.status}"`);
        }
        
        if (differences.length > 0) {
          recommendation = 'Local data differs from remote registry';
        }
      } else if (!local && remote) {
        recommendation = 'MIC exists remotely but not locally - consider importing';
      } else if (local && !remote) {
        recommendation = 'MIC exists locally but not in remote registry - verify accuracy';
      }

      return {
        status: 'success',
        data: {
          local,
          remote,
          differences,
          recommendation,
        },
      };
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get MIC coverage statistics
   */
  async getMicCoverage(config?: RequestConfig): Promise<ApiResponse<{
    total_countries: number;
    countries_with_mics: number;
    coverage_percentage: number;
    top_countries: Array<{ country: string; mic_count: number }>;
    missing_countries: string[];
  }>> {
    const stats = await this.getMicStatistics(config);
    
    if (!stats.data) {
      throw new Error('Unable to retrieve MIC statistics');
    }

    // This would be calculated from the coverage data
    const coverage = {
      total_countries: Object.keys(stats.data.coverage_by_country).length,
      countries_with_mics: Object.keys(stats.data.coverage_by_country).length,
      coverage_percentage: 85.2, // Placeholder
      top_countries: Object.entries(stats.data.coverage_by_country)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 10)
        .map(([country, count]) => ({ country, mic_count: count })),
      missing_countries: [], // Would be calculated
    };

    return {
      status: 'success',
      data: coverage,
    };
  }

  // ===== UTILITY METHODS =====

  /**
   * Validate MIC code format
   */
  static validateMicFormat(micCode: string): boolean {
    // MIC format: 4 character code
    const micPattern = /^[A-Z0-9]{4}$/;
    return micPattern.test(micCode.toUpperCase());
  }

  /**
   * Get MIC status color for UI
   */
  static getMicStatusColor(status: string): string {
    const colors: Record<string, string> = {
      'ACTIVE': 'green',
      'INACTIVE': 'red',
      'PENDING': 'yellow',
      'DELETED': 'gray',
    };
    return colors[status] || 'gray';
  }

  /**
   * Format MIC display name
   */
  static formatMicName(mic: MicCode): string {
    if (mic.acronym) {
      return `${mic.name} (${mic.acronym})`;
    }
    return mic.name;
  }
}