/**
 * Instrument API Service
 * Handles all instrument-related API operations including search, details, venues, and CFI operations
 */

import { BaseApiService } from './BaseApiService';
import {
  ApiResponse,
  Instrument,
  InstrumentDetail,
  InstrumentFilter,
  VenueData,
  PaginationParams,
  RequestConfig
} from '../types/api';

export class InstrumentService extends BaseApiService {
  
  /**
   * List instruments with filtering and pagination
   */
  async listInstruments(
    filters: InstrumentFilter = {},
    pagination: PaginationParams = {},
    config?: RequestConfig
  ): Promise<ApiResponse<Instrument[]>> {
    const params = {
      ...filters,
      ...pagination,
    };
    
    return this.get<Instrument[]>('/instruments/', params, config);
  }

  /**
   * Get instrument details by ISIN
   */
  async getInstrument(isin: string, config?: RequestConfig): Promise<ApiResponse<InstrumentDetail>> {
    return this.get<InstrumentDetail>(`/instruments/${encodeURIComponent(isin)}`, {}, config);
  }

  /**
   * Get raw instrument model data for comparison
   */
  async getInstrumentRaw(isin: string, config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.get<any>(`/instruments/${encodeURIComponent(isin)}/raw`, {}, config);
  }

  /**
   * Get venues for an instrument
   */
  async getInstrumentVenues(identifier: string, config?: RequestConfig): Promise<ApiResponse<VenueData[]>> {
    return this.get<VenueData[]>(`/instruments/${encodeURIComponent(identifier)}/venues`, {}, config);
  }

  /**
   * Get available instrument types
   */
  async getInstrumentTypes(config?: RequestConfig): Promise<ApiResponse<{ instrument_types: string[] }>> {
    return this.get<{ instrument_types: string[] }>('/instruments/types', {}, { ...config, cache: true });
  }

  /**
   * Search instruments by CFI code
   */
  async searchByCfi(cfiCode: string, config?: RequestConfig): Promise<ApiResponse<Instrument[]>> {
    return this.get<Instrument[]>(`/instruments/cfi/${encodeURIComponent(cfiCode)}`, {}, config);
  }

  /**
   * Search instruments with comprehensive filters
   */
  async searchInstruments(query: {
    search?: string;
    type?: string;
    currency?: string;
    country?: string;
    cfi?: string;
    limit?: number;
    offset?: number;
  }, config?: RequestConfig): Promise<ApiResponse<Instrument[]>> {
    return this.get<Instrument[]>('/instruments', query, config);
  }

  /**
   * Get instrument statistics
   */
  async getInstrumentStats(config?: RequestConfig): Promise<ApiResponse<any>> {
    // This would be a custom endpoint for statistics
    return this.get<any>('/instruments/stats', {}, { ...config, cache: true });
  }

  /**
   * Batch get instruments by ISINs
   */
  async getInstrumentsBatch(isins: string[], config?: RequestConfig): Promise<ApiResponse<Instrument[]>> {
    return this.post<Instrument[]>('/instruments/batch', { isins }, config);
  }

  /**
   * Get instruments with type-specific attributes
   */
  async getInstrumentsWithAttributes(
    filters: InstrumentFilter & { include_attributes?: boolean } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<InstrumentDetail[]>> {
    const params = {
      include_attributes: true,
      ...filters,
    };
    
    return this.get<InstrumentDetail[]>('/instruments', params, config);
  }

  /**
   * Decode CFI code
   */
  async decodeCfi(cfiCode: string, config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.get<any>(`/instruments/cfi/${encodeURIComponent(cfiCode)}/decode`, {}, config);
  }

  // ===== CONVENIENCE METHODS =====

  /**
   * Get instruments by type with common filters
   */
  async getInstrumentsByType(
    instrumentType: string, 
    options: {
      currency?: string;
      country?: string;
      limit?: number;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<Instrument[]>> {
    return this.listInstruments(
      {
        type: instrumentType,
        currency: options.currency,
        country: options.country,
      },
      {
        limit: options.limit || 50,
      },
      config
    );
  }

  /**
   * Search instruments by name or ISIN
   */
  async quickSearch(
    searchTerm: string,
    limit: number = 10,
    config?: RequestConfig
  ): Promise<ApiResponse<Instrument[]>> {
    return this.listInstruments(
      { search: searchTerm },
      { limit },
      { ...config, cache: false } // Don't cache search results
    );
  }

  /**
   * Get recently added instruments
   */
  async getRecentInstruments(
    limit: number = 10,
    config?: RequestConfig
  ): Promise<ApiResponse<Instrument[]>> {
    // Assuming the API supports sorting by created_at
    return this.get<Instrument[]>('/instruments', {
      sort: 'created_at',
      order: 'desc',
      limit,
    }, config);
  }

  /**
   * Check if instrument exists
   */
  async instrumentExists(isin: string, config?: RequestConfig): Promise<boolean> {
    try {
      await this.getInstrument(isin, { ...config, cache: true });
      return true;
    } catch (error: any) {
      if (error.status === 404) {
        return false;
      }
      throw error;
    }
  }

  /**
   * Get instrument summary (lightweight version)
   */
  async getInstrumentSummary(isin: string, config?: RequestConfig): Promise<ApiResponse<Partial<Instrument>>> {
    // This could be a specific endpoint that returns only essential fields
    const response = await this.getInstrument(isin, config);
    
    // Extract only summary fields
    if (response.data) {
      const summary = {
        id: response.data.id,
        isin: response.data.isin,
        name: response.data.name,
        instrument_type: response.data.instrument_type,
        currency: response.data.currency,
        cfi: response.data.cfi,
      };
      
      return {
        ...response,
        data: summary,
      };
    }
    
    return response;
  }
}