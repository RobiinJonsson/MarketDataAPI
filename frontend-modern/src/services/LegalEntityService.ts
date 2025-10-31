/**
 * Legal Entity API Service
 * Handles all legal entity and relationship operations
 */

import { BaseApiService } from './BaseApiService';
import {
  ApiResponse,
  LegalEntity,
  EntityRelationship,
  EntityHierarchy,
  PaginationParams,
  RequestConfig
} from '../types/api';

export class LegalEntityService extends BaseApiService {
  
  /**
   * List legal entities with pagination
   */
  async listEntities(
    filters: {
      search?: string;
      country?: string;
      status?: string;
    } = {},
    pagination: PaginationParams = {},
    config?: RequestConfig
  ): Promise<ApiResponse<LegalEntity[]>> {
    const params = {
      ...filters,
      ...pagination,
    };
    
    return this.get<LegalEntity[]>('/legal-entities/', params, config);
  }

  /**
   * Get legal entity details by LEI
   */
  async getEntity(lei: string, config?: RequestConfig): Promise<ApiResponse<LegalEntity>> {
    return this.get<LegalEntity>(`/legal-entities/${encodeURIComponent(lei)}`, {}, config);
  }

  /**
   * Get entity relationships
   */
  async getEntityRelationships(lei: string, config?: RequestConfig): Promise<ApiResponse<EntityRelationship[]>> {
    return this.get<EntityRelationship[]>(`/relationships/${encodeURIComponent(lei)}`, {}, config);
  }

  /**
   * Get entity hierarchy
   */
  async getEntityHierarchy(lei: string, config?: RequestConfig): Promise<ApiResponse<EntityHierarchy>> {
    return this.get<EntityHierarchy>(`/relationships/hierarchy/${encodeURIComponent(lei)}`, {}, config);
  }

  /**
   * Search entities by name or LEI
   */
  async searchEntities(
    query: string,
    options: {
      limit?: number;
      country?: string;
      status?: string;
    } = {},
    config?: RequestConfig
  ): Promise<ApiResponse<LegalEntity[]>> {
    return this.listEntities(
      {
        search: query,
        country: options.country,
        status: options.status,
      },
      {
        limit: options.limit || 20,
      },
      { ...config, cache: false }
    );
  }

  /**
   * Get entities by country
   */
  async getEntitiesByCountry(
    countryCode: string,
    pagination: PaginationParams = {},
    config?: RequestConfig
  ): Promise<ApiResponse<LegalEntity[]>> {
    return this.listEntities(
      { country: countryCode },
      pagination,
      config
    );
  }

  /**
   * Get entity statistics
   */
  async getEntityStats(config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.get<any>('/legal-entities/stats', {}, { ...config, cache: true });
  }

  /**
   * Check if entity exists
   */
  async entityExists(lei: string, config?: RequestConfig): Promise<boolean> {
    try {
      await this.getEntity(lei, { ...config, cache: true });
      return true;
    } catch (error: any) {
      if (error.status === 404) {
        return false;
      }
      throw error;
    }
  }

  /**
   * Get entity with all related data (relationships + instruments)
   */
  async getEntityComplete(lei: string, config?: RequestConfig): Promise<ApiResponse<{
    entity: LegalEntity;
    relationships: EntityRelationship[];
    hierarchy: EntityHierarchy;
  }>> {
    // Make parallel requests for efficiency
    const [entityResponse, relationshipsResponse, hierarchyResponse] = await Promise.all([
      this.getEntity(lei, config),
      this.getEntityRelationships(lei, config),
      this.getEntityHierarchy(lei, config),
    ]);

    return {
      status: 'success',
      data: {
        entity: entityResponse.data!,
        relationships: relationshipsResponse.data || [],
        hierarchy: hierarchyResponse.data!,
      },
    };
  }

  /**
   * Get parent entities
   */
  async getParentEntities(lei: string, config?: RequestConfig): Promise<ApiResponse<LegalEntity[]>> {
    const relationships = await this.getEntityRelationships(lei, config);
    
    if (!relationships.data) {
      return { status: 'success', data: [] };
    }

    // Filter for parent relationships and get parent entities
    const parentLeis = relationships.data
      .filter(rel => rel.child_lei === lei)
      .map(rel => rel.parent_lei);

    if (parentLeis.length === 0) {
      return { status: 'success', data: [] };
    }

    // Get parent entity details
    const parentEntities = await Promise.all(
      parentLeis.map(parentLei => this.getEntity(parentLei, config))
    );

    return {
      status: 'success',
      data: parentEntities.map(response => response.data!),
    };
  }

  /**
   * Get child entities
   */
  async getChildEntities(lei: string, config?: RequestConfig): Promise<ApiResponse<LegalEntity[]>> {
    const relationships = await this.getEntityRelationships(lei, config);
    
    if (!relationships.data) {
      return { status: 'success', data: [] };
    }

    // Filter for child relationships and get child entities
    const childLeis = relationships.data
      .filter(rel => rel.parent_lei === lei)
      .map(rel => rel.child_lei);

    if (childLeis.length === 0) {
      return { status: 'success', data: [] };
    }

    // Get child entity details
    const childEntities = await Promise.all(
      childLeis.map(childLei => this.getEntity(childLei, config))
    );

    return {
      status: 'success',
      data: childEntities.map(response => response.data!),
    };
  }

  /**
   * Get relationship network (entities within N degrees)
   */
  async getRelationshipNetwork(
    lei: string,
    degrees: number = 2,
    config?: RequestConfig
  ): Promise<ApiResponse<{
    entities: LegalEntity[];
    relationships: EntityRelationship[];
  }>> {
    // This would require recursive relationship traversal
    // Starting with immediate relationships
    const directRelationships = await this.getEntityRelationships(lei, config);
    
    if (!directRelationships.data || degrees === 1) {
      return {
        status: 'success',
        data: {
          entities: [],
          relationships: directRelationships.data || [],
        },
      };
    }

    // For now, return direct relationships
    // In a full implementation, this would recursively traverse the network
    return {
      status: 'success',
      data: {
        entities: [],
        relationships: directRelationships.data,
      },
    };
  }

  /**
   * Validate LEI format
   */
  static validateLEI(lei: string): boolean {
    // LEI format: 20 character alphanumeric code
    const leiPattern = /^[A-Z0-9]{18}[0-9]{2}$/;
    return leiPattern.test(lei.toUpperCase());
  }

  /**
   * Get recent entities
   */
  async getRecentEntities(
    limit: number = 10,
    config?: RequestConfig
  ): Promise<ApiResponse<LegalEntity[]>> {
    return this.get<LegalEntity[]>('/legal-entities', {
      sort: 'created_at',
      order: 'desc',
      limit,
    }, config);
  }

  /**
   * Fill missing entity data from GLEIF registry
   */
  async batchFillEntityData(config?: RequestConfig): Promise<ApiResponse<any>> {
    return this.post<any>('/legal-entities/batch/fill', {}, {
      ...config,
      timeout: 300000, // 5 minutes for batch operations
    });
  }
}