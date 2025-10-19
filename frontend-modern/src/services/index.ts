/**
 * API Services - Centralized exports for all service classes
 */

// Base service
export { BaseApiService } from './BaseApiService';

// Domain-specific services
export { InstrumentService } from './InstrumentService';
export { LegalEntityService } from './LegalEntityService';
export { FileService } from './FileService';
export { MicService } from './MicService';
export { AnalyticsService } from './AnalyticsService';
export { TransparencyService } from './TransparencyService';
export { SchemaService } from './SchemaService';

// Legacy service (to be migrated)
export { InstrumentDataService, instrumentDataService } from './InstrumentDataService';

// Service factory for easy instantiation
import { InstrumentService } from './InstrumentService';
import { LegalEntityService } from './LegalEntityService';
import { FileService } from './FileService';
import { MicService } from './MicService';
import { AnalyticsService } from './AnalyticsService';
import { TransparencyService } from './TransparencyService';
import { SchemaService } from './SchemaService';
import type { RequestConfig } from '../types/api';

export class ApiServiceFactory {
  private static instance: ApiServiceFactory;
  private baseURL: string;
  private defaultConfig: RequestConfig;

  private constructor(baseURL = 'http://localhost:5000/api/v1', config: RequestConfig = {}) {
    this.baseURL = baseURL;
    this.defaultConfig = config;
  }

  static getInstance(baseURL?: string, config?: RequestConfig): ApiServiceFactory {
    if (!ApiServiceFactory.instance) {
      ApiServiceFactory.instance = new ApiServiceFactory(baseURL, config);
    }
    return ApiServiceFactory.instance;
  }

  static configure(baseURL: string, config?: RequestConfig): void {
    ApiServiceFactory.instance = new ApiServiceFactory(baseURL, config);
  }

  // Service getters
  get instruments(): InstrumentService {
    return new InstrumentService(this.baseURL, this.defaultConfig);
  }

  get entities(): LegalEntityService {
    return new LegalEntityService(this.baseURL, this.defaultConfig);
  }

  get files(): FileService {
    return new FileService(this.baseURL, this.defaultConfig);
  }

  get mics(): MicService {
    return new MicService(this.baseURL, this.defaultConfig);
  }

  get analytics(): AnalyticsService {
    return new AnalyticsService(this.baseURL, this.defaultConfig);
  }

  get transparency(): TransparencyService {
    return new TransparencyService(this.baseURL, this.defaultConfig);
  }

  get schema(): SchemaService {
    return new SchemaService(this.baseURL, this.defaultConfig);
  }

  // Convenience method to get all services
  getAllServices() {
    return {
      instruments: this.instruments,
      entities: this.entities,
      files: this.files,
      mics: this.mics,
      analytics: this.analytics,
      transparency: this.transparency,
      schema: this.schema,
    };
  }

  // Health check for all services
  async healthCheck(): Promise<{
    baseURL: string;
    timestamp: string;
    services: {
      name: string;
      available: boolean;
      responseTime?: number;
      error?: string;
    }[];
  }> {
    const services: { name: string; available: boolean; responseTime?: number; error?: string }[] = [];

    // Test each service with a simple call
    const testPromises = [
      this.testService('instruments', () => this.instruments.listInstruments({})),
      this.testService('entities', () => this.entities.listEntities({})),
      this.testService('files', () => this.files.listFiles({})),
      this.testService('mics', () => this.mics.listMics({})),
      this.testService('analytics', () => this.analytics.getSystemAnalytics()),
      this.testService('transparency', () => this.transparency.getTransparencyStats()),
      this.testService('schema', () => this.schema.getDatabaseStats()),
    ];

    const results = await Promise.allSettled(testPromises);
    
    results.forEach((result, index) => {
      const serviceName = ['instruments', 'entities', 'files', 'mics', 'analytics', 'transparency', 'schema'][index];
      if (result.status === 'fulfilled') {
        services.push(result.value);
      } else {
        services.push({
          name: serviceName,
          available: false,
          error: result.reason?.message,
        });
      }
    });

    return {
      baseURL: this.baseURL,
      timestamp: new Date().toISOString(),
      services,
    };
  }

  private async testService(
    name: string, 
    testFn: () => Promise<any>
  ): Promise<{ name: string; available: boolean; responseTime?: number }> {
    const start = Date.now();
    try {
      await testFn();
      return {
        name,
        available: true,
        responseTime: Date.now() - start,
      };
    } catch (error) {
      return {
        name,
        available: false,
        responseTime: Date.now() - start,
      };
    }
  }
}

// Force reconfiguration to ensure correct port
ApiServiceFactory.configure('http://localhost:5000/api/v1');

// Default instance for convenience
export const apiServices = ApiServiceFactory.getInstance();
