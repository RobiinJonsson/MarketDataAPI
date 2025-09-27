// API Response Types
export interface ApiResponse<T> {
  status: string;
  data?: T;
  error?: string;
  message?: string;
}

// Comprehensive Instrument Data
export interface ComprehensiveInstrumentData {
  instrument: any;
  transparency: any[];
  venues: any[];
  lei_data?: any;
  relationships?: any;
}

// Instrument Types
export interface Instrument {
  id: string;
  isin: string;
  symbol?: string;
  name?: string;
  cfi?: string;
  instrument_type?: string;
  created_at: string;
  updated_at: string;
}

export interface InstrumentSearchResult {
  instrument: Instrument;
  transparency_data?: TransparencyCalculation[];
  figi_data?: FigiData[];
}

// FIGI Types
export interface FigiData {
  id: string;
  figi: string;
  name: string;
  ticker?: string;
  exch_code?: string;
  composite_figi?: string;
  share_class_figi?: string;
  security_type?: string;
  market_sector?: string;
  security_description?: string;
  created_at: string;
  updated_at: string;
}

// Transparency Types
export interface TransparencyCalculation {
  id: string;
  isin: string;
  tech_record_id: string;
  from_date: string;
  to_date: string;
  liquidity: boolean;
  total_transactions_executed: number;
  total_volume_executed: number;
  transparency_fields: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Search and Form Types
export interface SearchParams {
  isin?: string;
  symbol?: string;
  name?: string;
}

export interface CreateInstrumentRequest {
  isin: string;
  symbol?: string;
  name?: string;
  cfi?: string;
  instrument_type?: string;
}

// UI State Types
export type TabName = 'overview' | 'data' | 'admin';
export type AdminTabName = 'instruments' | 'transparency' | 'files' | 'batch';

export interface UIState {
  activeTab: TabName;
  activeAdminTab: AdminTabName;
  isLoading: boolean;
  error: string | null;
  searchResults: InstrumentSearchResult | null;
}
