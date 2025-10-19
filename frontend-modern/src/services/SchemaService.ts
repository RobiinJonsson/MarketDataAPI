/**
 * Schema API Service
 * Handles database schema information and system metadata
 */

import { BaseApiService } from './BaseApiService';
import {
  ApiResponse,
  RequestConfig
} from '../types/api';

export class SchemaService extends BaseApiService {

  /**
   * Get database schema information
   */
  async getSchemaInfo(config?: RequestConfig): Promise<ApiResponse<{
    tables: Array<{
      name: string;
      type: 'table' | 'view';
      row_count: number;
      columns: Array<{
        name: string;
        type: string;
        nullable: boolean;
        primary_key: boolean;
        foreign_key?: {
          table: string;
          column: string;
        };
      }>;
    }>;
    relationships: Array<{
      from_table: string;
      from_column: string;
      to_table: string;
      to_column: string;
    }>;
    indexes: Array<{
      table: string;
      name: string;
      columns: string[];
      unique: boolean;
    }>;
  }>> {
    const { cache = true, timeout, headers, retries } = config || {};
    return this.request<{
      tables: Array<{
        name: string;
        type: 'table' | 'view';
        row_count: number;
        columns: Array<{
          name: string;
          type: string;
          nullable: boolean;
          primary_key: boolean;
          foreign_key?: {
            table: string;
            column: string;
          };
        }>;
      }>;
      relationships: Array<{
        from_table: string;
        from_column: string;
        to_table: string;
        to_column: string;
      }>;
      indexes: Array<{
        table: string;
        name: string;
        columns: string[];
        unique: boolean;
      }>;
    }>('/schema/info', { method: 'GET' }, { cache, timeout, headers, retries });
  }

  /**
   * Get table information
   */
  async getTableInfo(
    tableName: string,
    config?: RequestConfig
  ): Promise<ApiResponse<{
    name: string;
    type: 'table' | 'view';
    row_count: number;
    size_mb: number;
    columns: Array<{
      name: string;
      type: string;
      nullable: boolean;
      primary_key: boolean;
      foreign_key?: {
        table: string;
        column: string;
      };
      sample_values?: any[];
    }>;
    indexes: Array<{
      name: string;
      columns: string[];
      unique: boolean;
    }>;
    foreign_keys: Array<{
      column: string;
      references_table: string;
      references_column: string;
    }>;
  }>> {
    const { cache = true, timeout, headers, retries } = config || {};
    return this.request<{
      name: string;
      type: 'table' | 'view';
      row_count: number;
      size_mb: number;
      columns: Array<{
        name: string;
        type: string;
        nullable: boolean;
        primary_key: boolean;
        foreign_key?: {
          table: string;
          column: string;
        };
        sample_values?: any[];
      }>;
      indexes: Array<{
        name: string;
        columns: string[];
        unique: boolean;
      }>;
      foreign_keys: Array<{
        column: string;
        references_table: string;
        references_column: string;
      }>;
    }>(`/schema/table/${tableName}`, { method: 'GET' }, { cache, timeout, headers, retries });
  }

  /**
   * Get database statistics
   */
  async getDatabaseStats(config?: RequestConfig): Promise<ApiResponse<{
    database_type: string;
    version: string;
    size_mb: number;
    table_count: number;
    total_rows: number;
    largest_tables: Array<{
      name: string;
      row_count: number;
      size_mb: number;
    }>;
    connection_info: {
      max_connections: number;
      active_connections: number;
      idle_connections: number;
    };
    performance_metrics: {
      queries_per_second: number;
      avg_query_time_ms: number;
      cache_hit_ratio: number;
    };
  }>> {
    return this.request<{
      database_type: string;
      version: string;
      size_mb: number;
      table_count: number;
      total_rows: number;
      largest_tables: Array<{
        name: string;
        row_count: number;
        size_mb: number;
      }>;
      connection_info: {
        max_connections: number;
        active_connections: number;
        idle_connections: number;
      };
      performance_metrics: {
        queries_per_second: number;
        avg_query_time_ms: number;
        cache_hit_ratio: number;
      };
    }>('/schema/stats', { method: 'GET' }, config);
  }

  /**
   * Validate database integrity
   */
  async validateIntegrity(config?: RequestConfig): Promise<ApiResponse<{
    status: 'healthy' | 'warnings' | 'errors';
    checks: Array<{
      check_name: string;
      status: 'pass' | 'warning' | 'fail';
      message: string;
      details?: any;
    }>;
    summary: {
      total_checks: number;
      passed: number;
      warnings: number;
      errors: number;
    };
  }>> {
    return this.request<{
      status: 'healthy' | 'warnings' | 'errors';
      checks: Array<{
        check_name: string;
        status: 'pass' | 'warning' | 'fail';
        message: string;
        details?: any;
      }>;
      summary: {
        total_checks: number;
        passed: number;
        warnings: number;
        errors: number;
      };
    }>('/schema/validate', { method: 'POST' }, config);
  }

  /**
   * Get API endpoints documentation
   */
  async getApiDocumentation(config?: RequestConfig): Promise<ApiResponse<{
    openapi_version: string;
    info: {
      title: string;
      version: string;
      description: string;
    };
    servers: Array<{
      url: string;
      description: string;
    }>;
    paths: Record<string, {
      methods: string[];
      summary: string;
      description?: string;
      parameters?: Array<{
        name: string;
        in: 'path' | 'query' | 'header' | 'body';
        required: boolean;
        type: string;
        description?: string;
      }>;
    }>;
    components: {
      schemas: Record<string, any>;
    };
  }>> {
    const { cache = true, timeout, headers, retries } = config || {};
    return this.request<{
      openapi_version: string;
      info: {
        title: string;
        version: string;
        description: string;
      };
      servers: Array<{
        url: string;
        description: string;
      }>;
      paths: Record<string, {
        methods: string[];
        summary: string;
        description?: string;
        parameters?: Array<{
          name: string;
          in: 'path' | 'query' | 'header' | 'body';
          required: boolean;
          type: string;
          description?: string;
        }>;
      }>;
      components: {
        schemas: Record<string, any>;
      };
    }>('/schema/api/docs', { method: 'GET' }, { cache, timeout, headers, retries });
  }

  /**
   * Export database schema
   */
  async exportSchema(
    format: 'json' | 'sql' | 'yaml',
    config?: RequestConfig
  ): Promise<ApiResponse<{
    download_url: string;
    file_size: number;
    expires_at: string;
    format: string;
  }>> {
    return this.request<{
      download_url: string;
      file_size: number;
      expires_at: string;
      format: string;
    }>('/schema/export', 
       { method: 'POST', body: JSON.stringify({ format }) }, 
       config);
  }

  /**
   * Get migration history
   */
  async getMigrationHistory(config?: RequestConfig): Promise<ApiResponse<{
    current_version: string;
    migrations: Array<{
      version: string;
      filename: string;
      applied_at: string;
      execution_time_ms: number;
      success: boolean;
      error_message?: string;
    }>;
    pending_migrations: Array<{
      version: string;
      filename: string;
      description: string;
    }>;
  }>> {
    const { cache = true, timeout, headers, retries } = config || {};
    return this.request<{
      current_version: string;
      migrations: Array<{
        version: string;
        filename: string;
        applied_at: string;
        execution_time_ms: number;
        success: boolean;
        error_message?: string;
      }>;
      pending_migrations: Array<{
        version: string;
        filename: string;
        description: string;
      }>;
    }>('/schema/migrations', { method: 'GET' }, { cache, timeout, headers, retries });
  }

  /**
   * Get data dictionary
   */
  async getDataDictionary(config?: RequestConfig): Promise<ApiResponse<{
    tables: Record<string, {
      description: string;
      columns: Record<string, {
        type: string;
        description: string;
        constraints: string[];
        examples: any[];
      }>;
    }>;
    enums: Record<string, {
      description: string;
      values: Array<{
        value: string;
        description: string;
      }>;
    }>;
  }>> {
    const { cache = true, timeout, headers, retries } = config || {};
    return this.request<{
      tables: Record<string, {
        description: string;
        columns: Record<string, {
          type: string;
          description: string;
          constraints: string[];
          examples: any[];
        }>;
      }>;
      enums: Record<string, {
        description: string;
        values: Array<{
          value: string;
          description: string;
        }>;
      }>;
    }>('/schema/dictionary', { method: 'GET' }, { cache, timeout, headers, retries });
  }

  /**
   * Query database directly (for admin use)
   */
  async executeQuery(
    query: string,
    params?: Record<string, any>,
    config?: RequestConfig
  ): Promise<ApiResponse<{
    columns: string[];
    rows: any[][];
    execution_time_ms: number;
    row_count: number;
  }>> {
    return this.request<{
      columns: string[];
      rows: any[][];
      execution_time_ms: number;
      row_count: number;
    }>('/schema/query', 
       { 
         method: 'POST', 
         body: JSON.stringify({ query, params }) 
       }, 
       config);
  }
}