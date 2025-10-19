/**
 * File Management API Service
 * Handles all file operations including ESMA downloads, storage analytics, and batch operations
 */

import { BaseApiService } from './BaseApiService';
import {
  ApiResponse,
  FileInfo,
  FileStats,
  DetailedFileStats,
  DownloadCriteria,
  RequestConfig
} from '../types/api';

export class FileService extends BaseApiService {
  
  /**
   * List files with filtering
   */
  async listFiles(
    filters: {
      type?: 'FIRDS' | 'FITRS' | 'OTHER';
      dataset?: string;
      status?: 'active' | 'outdated' | 'processing';
      date_from?: string;
      date_to?: string;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<FileInfo[]>> {
    return this.get<FileInfo[]>('/files', filters, config);
  }

  /**
   * Get ESMA files
   */
  async getEsmaFiles(config?: RequestConfig): Promise<ApiResponse<FileInfo[]>> {
    return this.get<FileInfo[]>('/files/esma', {}, config);
  }

  /**
   * Download files by criteria
   */
  async downloadFiles(criteria: DownloadCriteria, config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.post<any>('/files/download', criteria, {
      ...config,
      timeout: 120000, // 2 minutes for downloads
    });
  }

  /**
   * Download files by specific criteria
   */
  async downloadByCriteria(criteria: DownloadCriteria, config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.post<any>('/files/download-by-criteria', criteria, {
      ...config,
      timeout: 300000, // 5 minutes for batch downloads
    });
  }

  /**
   * Get file statistics
   */
  async getFileStats(config?: RequestConfig): Promise<ApiResponse<FileStats>> {
    return this.get<FileStats>('/files/stats', {}, { ...config, cache: true });
  }

  /**
   * Get detailed file statistics
   */
  async getDetailedFileStats(
    filters: {
      type?: string;
      date_range?: { start: string; end: string };
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<DetailedFileStats>> {
    return this.get<DetailedFileStats>('/files/stats/detailed', filters, { ...config, cache: true });
  }

  /**
   * Get file summary
   */
  async getFileSummary(config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.get<any>('/files/summary', {}, { ...config, cache: true });
  }

  /**
   * Trigger auto-cleanup
   */
  async autoCleanup(
    options: {
      dry_run?: boolean;
      max_age_days?: number;
      keep_latest?: number;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<any>> {
    return this.post<any>('/files/auto-cleanup', options, {
      ...config,
      timeout: 60000, // 1 minute for cleanup operations
    });
  }

  /**
   * Delete specific file
   */
  async deleteFile(fileName: string, config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.delete<any>(`/files/${encodeURIComponent(fileName)}`, config);
  }

  /**
   * Get file download URL
   */
  getFileDownloadUrl(fileName: string): string {
    return `${this.getBaseURL()}/files/download/${encodeURIComponent(fileName)}`;
  }

  // ===== ESMA SPECIFIC OPERATIONS =====

  /**
   * Get latest FIRDS files
   */
  async getLatestFirdsFiles(
    instrumentTypes: string[] = [],
    config?: RequestConfig
  ): Promise<ApiResponse<FileInfo[]>> {
    const filters: any = { type: 'FIRDS' };
    if (instrumentTypes.length > 0) {
      filters.instrument_types = instrumentTypes.join(',');
    }
    
    return this.listFiles(filters, config);
  }

  /**
   * Get latest FITRS files
   */
  async getLatestFitrsFiles(config?: RequestConfig): Promise<ApiResponse<FileInfo[]>> {
    return this.listFiles({ type: 'FITRS' }, config);
  }

  /**
   * Download latest ESMA data
   */
  async downloadLatestEsmaData(
    options: {
      include_firds?: boolean;
      include_fitrs?: boolean;
      instrument_types?: string[];
      force_update?: boolean;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<any>> {
    const criteria: DownloadCriteria = {
      file_types: [],
      force_update: options.force_update,
    };

    if (options.include_firds !== false) {
      criteria.file_types.push('FIRDS');
    }
    if (options.include_fitrs !== false) {
      criteria.file_types.push('FITRS');
    }

    return this.downloadByCriteria(criteria, {
      ...config,
      timeout: 600000, // 10 minutes for ESMA downloads
    });
  }

  // ===== ANALYTICS AND MONITORING =====

  /**
   * Get storage analytics
   */
  async getStorageAnalytics(config?: RequestConfig): Promise<ApiResponse<{
    usage_by_type: Record<string, number>;
    usage_by_month: Record<string, number>;
    growth_trend: Array<{ date: string; size: number }>;
    oldest_files: FileInfo[];
    largest_files: FileInfo[];
  }>> {
    return this.get<any>('/files/analytics/storage', {}, { ...config, cache: true });
  }

  /**
   * Get download activity
   */
  async getDownloadActivity(
    period: 'day' | 'week' | 'month' = 'week',
    config?: RequestConfig
  ): Promise<ApiResponse<Array<{ date: string; downloads: number; size: number }>>> {
    return this.get<any>('/files/analytics/downloads', { period }, { ...config, cache: true });
  }

  /**
   * Get file processing status
   */
  async getProcessingStatus(config?: RequestConfig): Promise<ApiResponse<{
    processing: FileInfo[];
    failed: FileInfo[];
    completed_recently: FileInfo[];
  }>> {
    return this.get<any>('/files/status', {}, config);
  }

  // ===== BATCH OPERATIONS =====

  /**
   * Batch delete files
   */
  async batchDeleteFiles(
    fileNames: string[],
    config?: RequestConfig
  ): Promise<ApiResponse<{ deleted: string[]; failed: string[] }>> {
    return this.post<any>('/files/batch/delete', { files: fileNames }, config);
  }

  /**
   * Batch validate files
   */
  async batchValidateFiles(
    fileNames: string[] = [],
    config?: RequestConfig
  ): Promise<ApiResponse<Array<{ file: string; valid: boolean; errors: string[] }>>> {
    return this.post<any>('/files/batch/validate', { files: fileNames }, {
      ...config,
      timeout: 180000, // 3 minutes for validation
    });
  }

  /**
   * Get file health check
   */
  async getFileHealthCheck(config?: RequestConfig): Promise<ApiResponse<{
    total_files: number;
    corrupted_files: number;
    missing_files: number;
    outdated_files: number;
    health_score: number;
  }>> {
    return this.get<any>('/files/health', {}, { ...config, cache: true });
  }

  // ===== UTILITY METHODS =====

  /**
   * Format file size for display
   */
  static formatFileSize(bytes: number): string {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }
    
    return `${size.toFixed(1)} ${units[unitIndex]}`;
  }

  /**
   * Get file type color for UI
   */
  static getFileTypeColor(type: string): string {
    const colors: Record<string, string> = {
      'FIRDS': 'blue',
      'FITRS': 'green',
      'OTHER': 'gray',
    };
    return colors[type] || 'gray';
  }

  /**
   * Check if file is recent (within last 24 hours)
   */
  static isRecentFile(modifiedDate: string): boolean {
    const fileDate = new Date(modifiedDate);
    const dayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    return fileDate > dayAgo;
  }
}