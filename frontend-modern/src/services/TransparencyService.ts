/**
 * Transparency API Service
 * Handles MiFID II transparency calculations and regime determinations
 */

import { BaseApiService } from './BaseApiService';
import {
  ApiResponse,
  TransparencyCalculation,
  RequestConfig
} from '../types/api';

export class TransparencyService extends BaseApiService {

  /**
   * Calculate transparency regime for an instrument
   */
  async calculateTransparencyRegime(
    isin: string,
    config?: RequestConfig
  ): Promise<ApiResponse<TransparencyCalculation>> {
    const { cache, timeout, headers, retries } = config || {};
    return this.request<TransparencyCalculation>(
      `/transparency/calculate/${isin}`,
      { method: 'POST' },
      { cache, timeout, headers, retries }
    );
  }

  /**
   * Get transparency calculation details
   */
  async getTransparencyCalculation(
    calculationId: string,
    config?: RequestConfig
  ): Promise<ApiResponse<TransparencyCalculation>> {
    const { cache, timeout, headers, retries } = config || {};
    return this.request<TransparencyCalculation>(
      `/transparency/${calculationId}`,
      { method: 'GET' },
      { cache, timeout, headers, retries }
    );
  }

  /**
   * Get all transparency calculations with pagination
   */
  async getTransparencyCalculations(params?: {
    page?: number;
    per_page?: number;
    isin?: string;
    file_type?: string;
    calculation_type?: string;
  }, config?: RequestConfig): Promise<ApiResponse<{
    calculations: TransparencyCalculation[];
    pagination: {
      page: number;
      limit: number;
      total: number;
      pages: number;
    };
  }>> {
    const queryParams = new URLSearchParams();
    
    if (params?.page !== undefined) queryParams.append('page', params.page.toString());
    if (params?.per_page !== undefined) queryParams.append('per_page', params.per_page.toString());
    if (params?.isin) queryParams.append('isin', params.isin);
    if (params?.file_type) queryParams.append('file_type', params.file_type);
    if (params?.calculation_type) queryParams.append('calculation_type', params.calculation_type);

    const url = `/transparency${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    const { cache, timeout = 60000, headers, retries } = config || {};
    
    // Make the raw API request
    const rawResponse = await this.request<TransparencyCalculation[]>(url, { method: 'GET' }, { cache, timeout, headers, retries });
    
    // Transform the response to match expected format
    if (rawResponse.status === 'success') {
      // The API returns {status: "success", data: [...], meta: {...}}
      const apiResponse = rawResponse as any;
      const calculations = Array.isArray(apiResponse.data) ? apiResponse.data : [];
      const meta = apiResponse.meta || {};
      
      return {
        status: 'success',
        data: {
          calculations,
          pagination: {
            page: meta.page || 1,
            limit: meta.per_page || 20,
            total: meta.total || 0,
            pages: Math.ceil((meta.total || 0) / (meta.per_page || 20))
          }
        }
      };
    }
    
    return rawResponse as any;
  }

  /**
   * Bulk calculate transparency for multiple ISINs
   */
  async bulkCalculateTransparency(
    isins: string[],
    config?: RequestConfig
  ): Promise<ApiResponse<{
    job_id: string;
    status: 'queued' | 'processing' | 'completed' | 'failed';
    created_at: string;
    total_isins: number;
  }>> {
    const { cache, timeout, headers, retries } = config || {};
    return this.request<{
      job_id: string;
      status: 'queued' | 'processing' | 'completed' | 'failed';
      created_at: string;
      total_isins: number;
    }>('/transparency/bulk-calculate', 
       { method: 'POST', body: JSON.stringify({ isins }) }, 
       { cache, timeout, headers, retries });
  }

  /**
   * Get bulk calculation job status
   */
  async getBulkCalculationStatus(
    jobId: string,
    config?: RequestConfig
  ): Promise<ApiResponse<{
    job_id: string;
    status: 'queued' | 'processing' | 'completed' | 'failed';
    progress: {
      completed: number;
      total: number;
      percentage: number;
    };
    results?: TransparencyCalculation[];
    errors?: Array<{
      isin: string;
      error: string;
    }>;
  }>> {
    const { cache, timeout, headers, retries } = config || {};
    return this.request<{
      job_id: string;
      status: 'queued' | 'processing' | 'completed' | 'failed';
      progress: {
        completed: number;
        total: number;
        percentage: number;
      };
      results?: TransparencyCalculation[];
      errors?: Array<{
        isin: string;
        error: string;
      }>;
    }>(`/transparency/bulk-calculate/${jobId}/status`, 
       { method: 'GET' }, 
       { cache, timeout, headers, retries });
  }

  /**
   * Get transparency regime statistics
   */
  async getTransparencyStats(config?: RequestConfig): Promise<ApiResponse<{
    total_calculations: number;
    regimes_distribution: Record<string, number>;
    recent_calculations: number;
    calculation_trends: Array<{
      month: string;
      count: number;
    }>;
    processing_stats: {
      avg_processing_time_ms: number;
      success_rate: number;
      error_rate: number;
    };
  }>> {
    const { cache = true, timeout, headers, retries } = config || {};
    return this.request<{
      total_calculations: number;
      regimes_distribution: Record<string, number>;
      recent_calculations: number;
      calculation_trends: Array<{
        month: string;
        count: number;
      }>;
      processing_stats: {
        avg_processing_time_ms: number;
        success_rate: number;
        error_rate: number;
      };
    }>('/transparency/stats', 
       { method: 'GET' }, 
       { cache, timeout, headers, retries });
  }

  /**
   * Get transparency regime definitions and explanations
   */
  async getRegimeDefinitions(config?: RequestConfig): Promise<ApiResponse<Array<{
    regime_code: string;
    regime_name: string;
    description: string;
    criteria: Array<{
      field: string;
      condition: string;
      value: any;
      explanation: string;
    }>;
    examples: string[];
  }>>> {
    return this.request<Array<{
      regime_code: string;
      regime_name: string;
      description: string;
      criteria: Array<{
        field: string;
        condition: string;
        value: any;
        explanation: string;
      }>;
      examples: string[];
    }>>('/transparency/regimes/definitions', 
        { method: 'GET' }, 
        { cache: true, ...config });
  }

  /**
   * Validate transparency calculation rules for an instrument
   */
  async validateTransparencyRules(
    isin: string,
    config?: RequestConfig
  ): Promise<ApiResponse<{
    isin: string;
    is_valid: boolean;
    validation_results: Array<{
      rule_name: string;
      passed: boolean;
      message: string;
      severity: 'info' | 'warning' | 'error';
    }>;
    recommended_regime?: string;
    confidence_score: number;
  }>> {
    return this.request<{
      isin: string;
      is_valid: boolean;
      validation_results: Array<{
        rule_name: string;
        passed: boolean;
        message: string;
        severity: 'info' | 'warning' | 'error';
      }>;
      recommended_regime?: string;
      confidence_score: number;
    }>(`/transparency/validate/${isin}`, 
       { method: 'POST' }, 
       config);
  }

  /**
   * Get transparency calculation history for an ISIN
   */
  async getCalculationHistory(
    isin: string,
    params?: {
      limit?: number;
      offset?: number;
    },
    config?: RequestConfig
  ): Promise<ApiResponse<{
    isin: string;
    calculations: Array<{
      calculation_id: string;
      regime: string;
      confidence_score: number;
      calculated_at: string;
      calculation_details: any;
    }>;
    total_calculations: number;
  }>> {
    const queryParams = new URLSearchParams();
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.offset !== undefined) queryParams.append('offset', params.offset.toString());

    const url = `/transparency/history/${isin}${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    
    return this.request<{
      isin: string;
      calculations: Array<{
        calculation_id: string;
        regime: string;
        confidence_score: number;
        calculated_at: string;
        calculation_details: any;
      }>;
      total_calculations: number;
    }>(url, { method: 'GET' }, config);
  }

  /**
   * Export transparency calculations to various formats
   */
  async exportCalculations(
    params: {
      format: 'csv' | 'excel' | 'json';
      filters?: {
        regime?: string;
        isin_list?: string[];
        date_from?: string;
        date_to?: string;
      };
    },
    config?: RequestConfig
  ): Promise<ApiResponse<{
    download_url: string;
    file_size: number;
    expires_at: string;
  }>> {
    return this.request<{
      download_url: string;
      file_size: number;
      expires_at: string;
    }>('/transparency/export', 
       { method: 'POST', body: JSON.stringify(params) }, 
       config);
  }

  /**
   * Search transparency calculations with advanced filters
   */
  async searchCalculations(params: {
    query?: string;
    regime?: string;
    confidence_min?: number;
    confidence_max?: number;
    date_from?: string;
    date_to?: string;
    page?: number;
    limit?: number;
  }, config?: RequestConfig): Promise<ApiResponse<{
    calculations: TransparencyCalculation[];
    pagination: {
      page: number;
      limit: number;
      total: number;
      pages: number;
    };
    filters_applied: Record<string, any>;
  }>> {
    return this.request<{
      calculations: TransparencyCalculation[];
      pagination: {
        page: number;
        limit: number;
        total: number;
        pages: number;
      };
      filters_applied: Record<string, any>;
    }>('/transparency/search', 
       { method: 'POST', body: JSON.stringify(params) }, 
       config);
  }

  /**
   * Calculate transparency for instruments without current data
   */
  async batchCalculateTransparency(isins?: string[], config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.post<any>('/transparency/batch', {
      isins
    }, {
      ...config,
      timeout: 300000, // 5 minutes for batch operations
    });
  }
}