/**
 * Base API Service Class
 * Provides common functionality for all API services including error handling, caching, and request management
 */

import { ApiResponse, HttpError, RequestConfig } from '../types/api';

export class BaseApiService {
  protected baseURL: string;
  private cache: Map<string, { data: any; timestamp: number; ttl: number }> = new Map();
  private defaultConfig: RequestConfig;

  constructor(baseURL: string = 'http://127.0.0.1:5000/api/v1', config: RequestConfig = {}) {
    this.baseURL = baseURL.replace(/\/+$/, ''); // Remove trailing slashes
    this.defaultConfig = {
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      retries: 3,
      cache: true,
      ...config,
    };
  }

  /**
   * Make HTTP request with error handling and caching
   */
  protected async request<T>(
    endpoint: string,
    options: RequestInit = {},
    config: RequestConfig = {}
  ): Promise<ApiResponse<T>> {
    const finalConfig = { ...this.defaultConfig, ...config };
    const url = `${this.baseURL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    
    // Check cache for GET requests
    const cacheKey = `${options.method || 'GET'}:${url}:${JSON.stringify(options.body || {})}`;
    if (finalConfig.cache && (!options.method || options.method === 'GET')) {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }
    }

    // Setup request options
    const requestOptions: RequestInit = {
      method: 'GET',
      ...options,
      headers: {
        ...finalConfig.headers,
        ...options.headers,
      },
    };

    // Add timeout using AbortController
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), finalConfig.timeout);
    requestOptions.signal = controller.signal;

    try {
      const response = await this.fetchWithRetries(url, requestOptions, finalConfig.retries || 0);
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw await this.createHttpError(response);
      }

      const rawData = await response.json();
      
      // Wrap raw Flask responses in ApiResponse format
      const data: ApiResponse<T> = this.isApiResponse(rawData) 
        ? rawData 
        : {
            status: 'success',
            data: rawData as T
          };
      
      // Cache successful GET requests
      if (finalConfig.cache && (!options.method || options.method === 'GET')) {
        this.setCache(cacheKey, data, 300000); // 5 minutes default TTL
      }

      return data;
      
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error && error.name === 'AbortError') {
        throw this.createTimeoutError(finalConfig.timeout!);
      }
      
      if (error instanceof Error && 'status' in error) {
        throw error; // Re-throw HTTP errors
      }
      
      throw this.createNetworkError(error);
    }
  }

  /**
   * GET request
   */
  protected async get<T>(endpoint: string, params?: Record<string, any>, config?: RequestConfig): Promise<ApiResponse<T>> {
    if (!params) {
      return this.request<T>(endpoint, { method: 'GET' }, config);
    }
    
    const sanitizedParams = this.sanitizeParams(params);
    const queryString = new URLSearchParams(sanitizedParams).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request<T>(url, { method: 'GET' }, config);
  }

  /**
   * POST request
   */
  protected async post<T>(endpoint: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }, config);
  }

  /**
   * PUT request
   */
  protected async put<T>(endpoint: string, data?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    }, config);
  }

  /**
   * DELETE request
   */
  protected async delete<T>(endpoint: string, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' }, config);
  }

  /**
   * Fetch with exponential backoff retries
   */
  private async fetchWithRetries(url: string, options: RequestInit, retries: number): Promise<Response> {
    let lastError: Error;
    
    for (let i = 0; i <= retries; i++) {
      try {
        const response = await fetch(url, options);
        
        // Don't retry on client errors (4xx), only server errors (5xx) and network issues
        if (response.ok || (response.status >= 400 && response.status < 500)) {
          return response;
        }
        
        if (i === retries) {
          return response;
        }
        
        // Exponential backoff: 1s, 2s, 4s...
        await this.sleep(Math.pow(2, i) * 1000);
        
      } catch (error) {
        lastError = error as Error;
        
        if (i === retries) {
          throw error;
        }
        
        // Wait before retry
        await this.sleep(Math.pow(2, i) * 1000);
      }
    }
    
    throw lastError!;
  }

  /**
   * Create HTTP error from response
   */
  private async createHttpError(response: Response): Promise<HttpError> {
    let message = `HTTP ${response.status}: ${response.statusText}`;
    let details: string | undefined;
    
    try {
      const errorData = await response.json();
      if (errorData.message) {
        message = errorData.message;
      }
      if (errorData.error) {
        details = errorData.error;
      }
    } catch {
      // Ignore JSON parsing errors
    }
    
    const error = new Error(message) as unknown as HttpError;
    error.status = response.status;
    error.message = message;
    error.details = details;
    error.timestamp = new Date().toISOString();
    
    return error;
  }

  /**
   * Create timeout error
   */
  private createTimeoutError(timeout: number): HttpError {
    const error = new Error(`Request timeout after ${timeout}ms`) as unknown as HttpError;
    error.status = 408;
    error.message = `Request timeout after ${timeout}ms`;
    error.timestamp = new Date().toISOString();
    
    return error;
  }

  /**
   * Create network error
   */
  private createNetworkError(originalError: any): HttpError {
    const error = new Error('Network error occurred') as unknown as HttpError;
    error.status = 0;
    error.message = 'Network error occurred';
    error.details = originalError?.message || 'Unknown network error';
    error.timestamp = new Date().toISOString();
    
    return error;
  }

  /**
   * Cache management
   */
  private getFromCache(key: string): any | null {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < cached.ttl) {
      return cached.data;
    }
    
    if (cached) {
      this.cache.delete(key);
    }
    
    return null;
  }

  private setCache(key: string, data: any, ttl: number): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  /**
   * Clear cache
   */
  public clearCache(pattern?: string): void {
    if (!pattern) {
      this.cache.clear();
      return;
    }
    
    const regex = new RegExp(pattern);
    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Sanitize URL parameters
   */
  private sanitizeParams(params: Record<string, any>): Record<string, string> {
    const sanitized: Record<string, string> = {};
    
    for (const [key, value] of Object.entries(params)) {
      if (value !== null && value !== undefined && value !== '') {
        sanitized[key] = String(value);
      }
    }
    
    return sanitized;
  }

  /**
   * Sleep utility for retries
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Check if response is already in ApiResponse format
   */
  private isApiResponse(data: any): data is ApiResponse<any> {
    return data && typeof data === 'object' && ('status' in data || 'data' in data || 'error' in data);
  }

  /**
   * Get base URL
   */
  public getBaseURL(): string {
    return this.baseURL;
  }

  /**
   * Update base URL (useful for environment switching)
   */
  public setBaseURL(url: string): void {
    this.baseURL = url.replace(/\/+$/, '');
    this.clearCache(); // Clear cache when URL changes
  }

  /**
   * Health check
   */
  public async healthCheck(): Promise<boolean> {
    try {
      const response = await this.get('/', {}, { cache: false, timeout: 5000 });
      return response.status === 'success' || response.status === 'ok';
    } catch {
      return false;
    }
  }
}