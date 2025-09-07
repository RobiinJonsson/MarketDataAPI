import type { ApiResponse, InstrumentSearchResult, CreateInstrumentRequest, TransparencyCalculation } from '../types/api.js';

const API_BASE = '/api/v1';

// Generic API fetch wrapper
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
  try {
    // Add timeout support
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      signal: controller.signal,
      ...options,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }));
      return { status: 'error', error: errorData.error || `HTTP ${response.status}` };
    }

    const data = await response.json();
    return { status: 'success', data };
  } catch (error) {
    console.error('API request failed:', error);
    if (error instanceof Error && error.name === 'AbortError') {
      return { status: 'error', error: 'Request timed out. Please try again.' };
    }
    return { 
      status: 'error', 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}

// Instrument API functions
export const instrumentApi = {
  search: async (isin: string): Promise<ApiResponse<InstrumentSearchResult>> => {
    return apiRequest(`/instruments/${encodeURIComponent(isin)}`);
  },

  create: async (data: CreateInstrumentRequest): Promise<ApiResponse<any>> => {
    return apiRequest('/instruments', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getValidTypes: async (): Promise<ApiResponse<{ valid_types: string[], message: string }>> => {
    return apiRequest('/instruments/types');
  },

  validateCfi: async (cfi_code: string): Promise<ApiResponse<{ valid: boolean, cfi_code: string, instrument_type: string, error?: string }>> => {
    return apiRequest('/instruments/validate-cfi', {
      method: 'POST',
      body: JSON.stringify({ cfi_code }),
    });
  },

  getAll: async (): Promise<ApiResponse<any[]>> => {
    return apiRequest('/instruments');
  },

  delete: async (id: string): Promise<ApiResponse<void>> => {
    return apiRequest(`/instruments/${id}`, { method: 'DELETE' });
  },
};

// Transparency API functions
export const transparencyApi = {
  getByIsin: async (isin: string): Promise<ApiResponse<TransparencyCalculation[]>> => {
    return apiRequest(`/transparency/isin/${encodeURIComponent(isin)}`);
  },

  create: async (data: any): Promise<ApiResponse<any>> => {
    return apiRequest('/transparency', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  batch: async (data: any): Promise<ApiResponse<any>> => {
    return apiRequest('/transparency/batch', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

// FIGI API functions
export const figiApi = {
  search: async (query: string): Promise<ApiResponse<any[]>> => {
    return apiRequest(`/figi/search?q=${encodeURIComponent(query)}`);
  },
};

// File API functions
export const fileApi = {
  upload: async (file: File, type: string): Promise<ApiResponse<any>> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    return apiRequest('/files/upload', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
  },

  list: async (): Promise<ApiResponse<any[]>> => {
    return apiRequest('/files');
  },

  process: async (filename: string): Promise<ApiResponse<any>> => {
    return apiRequest('/files/process', {
      method: 'POST',
      body: JSON.stringify({ filename }),
    });
  },
};
