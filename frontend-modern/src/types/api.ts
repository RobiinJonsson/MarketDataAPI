// ===== CORE API TYPES =====

export interface ApiResponse<T> {
  status: string;
  data?: T;
  error?: string;
  message?: string;
  meta?: {
    page: number;
    per_page: number;
    total: number;
  };
}

export interface PaginationParams {
  limit?: number;
  offset?: number;
  page?: number;
  per_page?: number;
}

export interface FilterParams {
  [key: string]: string | number | boolean | undefined;
}

// ===== INSTRUMENT TYPES =====

export interface Instrument {
  id: string;
  isin: string;
  symbol?: string;
  name?: string;
  full_name?: string;
  short_name?: string;
  cfi?: string;
  cfi_code?: string;
  instrument_type?: string;
  currency?: string;
  country?: string;
  market?: string;
  issuer?: string;
  maturity_date?: string;
  issue_date?: string;
  firds_data?: Record<string, any>;
  processed_attributes?: Record<string, any>;
  created_at: string;
  updated_at: string;
  // Additional fields from actual API response
  lei_id?: string;
  commodity_derivative_indicator?: boolean;
  competent_authority?: string | null;
  relevant_trading_venue?: string | null;
  publication_from_date?: string | null;
  status_indicators?: string[];
  trading_venues?: VenueData[];
  figi_mappings?: FigiData[];
  trading_venues_count?: number;
  legal_entity?: {
    lei: string;
    name: string;
    jurisdiction: string;
    legal_form: string;
    status: string;
    creation_date: string;
  };
  cfi_decoded?: {
    cfi_code: string;
    category: string;
    category_description: string;
    group: string;
    group_description: string;
    attributes: string;
    decoded_attributes: Record<string, string>;
  };
}

export interface InstrumentDetail extends Instrument {
  transparency_data?: TransparencyCalculation[];
  venues?: VenueData[];
  entity_relationships?: EntityRelationship[];
  type_specific_attributes?: Record<string, any>;
}

export interface InstrumentSearchResult {
  instrument: Instrument;
  transparency_data?: TransparencyCalculation[];
  figi_data?: FigiData[];
}

export interface InstrumentFilter {
  type?: string;
  currency?: string;
  country?: string;
  cfi?: string;
  search?: string;
}

export interface VenueData {
  mic: string;
  name?: string;
  country?: string;
  segment?: string;
  trading_hours?: string;
}

// ===== LEGAL ENTITY TYPES =====

export interface LegalEntity {
  id: string;
  lei: string;
  name: string;
  country?: string;
  city?: string;
  legal_form?: string;
  status?: string;
  registration_date?: string;
  last_update?: string;
  parent_entity?: string;
  created_at: string;
  updated_at: string;
}

export interface EntityRelationship {
  parent_lei: string;
  child_lei: string;
  relationship_type: string;
  start_date?: string;
  end_date?: string;
  ownership_percentage?: number;
}

export interface EntityHierarchy {
  entity: LegalEntity;
  children: EntityHierarchy[];
  parent?: LegalEntity;
  depth: number;
}

// ===== TRANSPARENCY TYPES =====

export interface TransparencyCalculation {
  id: string;
  isin: string;
  calculation_date: string;
  total_turnover: number;
  average_daily_turnover: number;
  number_of_transactions: number;
  large_in_scale_threshold?: number;
  size_specific_to_instrument_threshold?: number;
  transparency_regime: string;
  created_at: string;
  updated_at: string;
}

// ===== MIC TYPES =====

export interface MicCode {
  mic: string;
  name: string;
  country: string;
  city?: string;
  website?: string;
  status: string;
  creation_date?: string;
  last_update_date?: string;
  segment?: string;
  acronym?: string;
  comments?: string;
}

export interface MicStatistics {
  total_mics: number;
  active_mics: number;
  countries_covered: number;
  segments_available: number;
  recent_updates: number;
  coverage_by_country: Record<string, number>;
  coverage_by_status: Record<string, number>;
}

export interface CountryMicData {
  country_code: string;
  country_name: string;
  mic_count: number;
  active_count: number;
  mics: MicCode[];
}

// ===== FILE MANAGEMENT TYPES =====

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  modified: string;
  type: 'FIRDS' | 'FITRS' | 'OTHER';
  dataset?: string;
  status: 'active' | 'outdated' | 'processing';
}

export interface FileStats {
  firds_files: number;
  fitrs_files: number;
  total_files: number;
  total_size: number;
  firds_size: number;
  fitrs_size: number;
  last_updated: string;
}

export interface DetailedFileStats extends FileStats {
  files_by_type: Record<string, number>;
  files_by_date: Record<string, number>;
  size_by_type: Record<string, number>;
  recent_downloads: number;
}

export interface DownloadCriteria {
  file_types: string[];
  date_range?: {
    start: string;
    end: string;
  };
  force_update?: boolean;
}

// ===== SCHEMA TYPES =====

export interface SchemaDefinition {
  name: string;
  version: string;
  description?: string;
  schema: Record<string, any>;
  examples?: Record<string, any>[];
  created_at: string;
  updated_at: string;
}

export interface SchemaValidation {
  valid: boolean;
  errors: string[];
  warnings: string[];
  data_path?: string;
}

// ===== FIGI TYPES =====

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

// ===== ANALYTICS TYPES =====

export interface SystemAnalytics {
  instrument_stats: {
    total: number;
    by_type: Record<string, number>;
    by_country: Record<string, number>;
    by_currency: Record<string, number>;
  };
  entity_stats: {
    total: number;
    by_country: Record<string, number>;
    with_relationships: number;
  };
  data_quality: {
    completeness_percentage: number;
    recent_updates_percentage: number;
    validation_pass_percentage: number;
  };
  system_health: {
    uptime_percentage: number;
    avg_response_time: number;
    database_size: number;
    api_calls_per_hour: number;
  };
}

// ===== HTTP TYPES =====

export interface HttpError {
  status: number;
  message: string;
  details?: string;
  timestamp: string;
}

export interface RequestConfig {
  timeout?: number;
  headers?: Record<string, string>;
  retries?: number;
  cache?: boolean;
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
