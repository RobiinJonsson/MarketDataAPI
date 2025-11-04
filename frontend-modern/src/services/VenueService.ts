/**
 * Venue Service - API service for trading venue operations
 */

import { BaseApiService } from './BaseApiService';
import type { 
  ApiResponse, 
  PaginatedResponse, 
  RequestConfig,
  VenueListFilters,
  VenueListResponse,
  VenueSummary,
  VenueDetail,
  VenueInstrument,
  VenueStatistics,
  CountrySummary
} from '../types/api';

export class VenueService extends BaseApiService {
  
  /**
   * Get paginated list of venues with filtering
   */
  async getVenues(
    filters: VenueListFilters = {}, 
    page: number = 1, 
    perPage: number = 50,
    config?: RequestConfig
  ): Promise<VenueListResponse> {
    const params = {
      page: page.toString(),
      per_page: perPage.toString(),
      ...Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== undefined && value !== '')
      )
    };

    return this.get<VenueSummary[]>(
      'venues/',
      params,
      config
    ) as Promise<VenueListResponse>;
  }

  /**
   * Get detailed venue information
   */
  async getVenueDetail(
    micCode: string, 
    includeInstruments: boolean = false, 
    instrumentLimit: number = 50,
    config?: RequestConfig
  ): Promise<ApiResponse<VenueDetail>> {
    const params: Record<string, string> = {};
    if (includeInstruments) {
      params.include_instruments = 'true';
      params.instrument_limit = instrumentLimit.toString();
    }

    return this.get<VenueDetail>(`venues/${micCode}`, params, config);
  }

  /**
   * Get instruments traded on a venue
   */
  async getVenueInstruments(
    micCode: string, 
    instrumentType?: string,
    page: number = 1, 
    perPage: number = 50,
    config?: RequestConfig
  ): Promise<ApiResponse<PaginatedResponse<VenueInstrument>>> {
    const params: Record<string, string> = {
      page: page.toString(),
      per_page: perPage.toString(),
    };

    if (instrumentType) {
      params.instrument_type = instrumentType;
    }

    return this.get<PaginatedResponse<VenueInstrument>>(
      `venues/${micCode}/instruments`, 
      params,
      config
    );
  }

  /**
   * Search venues with fuzzy matching
   */
  async searchVenues(
    query: string, 
    filters: Partial<VenueListFilters> = {},
    limit: number = 20,
    config?: RequestConfig
  ): Promise<ApiResponse<VenueSummary[]>> {
    const params = {
      query,
      limit: limit.toString(),
      ...Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== undefined && value !== '')
      )
    };

    return this.get<VenueSummary[]>(
      'venues/search',
      params,
      config
    );
  }

  /**
   * Get venue statistics
   */
  async getVenueStatistics(config?: RequestConfig): Promise<ApiResponse<VenueStatistics>> {
    return this.get<VenueStatistics>('venues/statistics', undefined, config);
  }

  /**
   * Get countries with venue counts
   */
  async getVenueCountries(config?: RequestConfig): Promise<ApiResponse<CountrySummary[]>> {
    return this.get<CountrySummary[]>('venues/countries', undefined, config);
  }

  /**
   * Get MIC validation information
   */
  async validateMIC(micCode: string, config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.get<any>(`mic/${micCode}`, undefined, config);
  }
}