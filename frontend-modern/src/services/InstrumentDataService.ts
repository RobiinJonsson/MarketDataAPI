import { ComprehensiveInstrumentData } from '../types/api';

export class InstrumentDataService {
  private static instance: InstrumentDataService;
  
  static getInstance(): InstrumentDataService {
    if (!InstrumentDataService.instance) {
      InstrumentDataService.instance = new InstrumentDataService();
    }
    return InstrumentDataService.instance;
  }

  /**
   * Fetch comprehensive instrument data including all related information
   */
  async fetchComprehensiveInstrumentData(isin: string): Promise<ComprehensiveInstrumentData> {
    console.log(`Fetching comprehensive data for ISIN: ${isin}`);
    
    try {
      // Fetch all data in parallel for better performance
      const [instrument, transparency, venues] = await Promise.allSettled([
        this.fetchInstrumentData(isin),
        this.fetchTransparencyData(isin),
        this.fetchVenuesData(isin)
      ]);

      // Extract successful results, use empty arrays/null for failures
      const instrumentData = instrument.status === 'fulfilled' ? instrument.value : null;
      const transparencyData = transparency.status === 'fulfilled' ? transparency.value : [];
      const venuesData = venues.status === 'fulfilled' ? venues.value : [];

      if (!instrumentData) {
        throw new Error('Instrument not found');
      }

      // Fetch LEI and relationship data if available - check multiple possible LEI field names
      let leiData = null;
      let relationshipData = null;
      const leiId = instrumentData.lei_id || instrumentData.lei || instrumentData.legal_entity_identifier;
            console.log(`Looking for LEI data with identifier: ${leiId}`);
      console.log('Using updated legal-entities endpoint');
      
      if (leiId) {
        try {
          // Fetch both LEI entity data and relationship data in parallel
          const [leiResult, relationshipResult] = await Promise.allSettled([
            this.fetchLeiData(leiId),
            this.fetchRelationshipData(leiId)
          ]);
          
          leiData = leiResult.status === 'fulfilled' ? leiResult.value : null;
          relationshipData = relationshipResult.status === 'fulfilled' ? relationshipResult.value : null;
          
          console.log('LEI data fetched:', leiData);
          console.log('Relationship data fetched:', relationshipData);
          
          // Debug the relationship result in detail
          if (relationshipResult.status === 'rejected') {
            console.log('Relationship fetch failed:', relationshipResult.reason);
          } else if (relationshipResult.value) {
            console.log('Relationship data structure:', Object.keys(relationshipResult.value));
          }
        } catch (error) {
          console.warn('Failed to fetch LEI/relationship data:', error);
        }
      } else {
        console.log('No LEI identifier found in instrument data. Available fields:', Object.keys(instrumentData));
      }

      return {
        instrument: instrumentData,
        transparency: transparencyData,
        venues: venuesData,
        lei_data: leiData,
        relationships: relationshipData
      };
    } catch (error) {
      console.error('Error fetching comprehensive instrument data:', error);
      throw error;
    }
  }

  /**
   * Fetch basic instrument data by ISIN
   */
  async fetchInstrumentData(isin: string): Promise<any> {
    const response = await fetch(`/api/v1/instruments/${isin}`);
    if (!response.ok) {
      throw new Error(`Instrument not found: ${response.status} ${response.statusText}`);
    }
    const apiResponse = await response.json();
    
    // Extract data from API response structure
    if (apiResponse.status === 'success' && apiResponse.data) {
      return apiResponse.data;
    }
    return apiResponse;
  }

  /**
   * Fetch transparency data for an ISIN
   */
  async fetchTransparencyData(isin: string): Promise<any[]> {
    try {
      const response = await fetch(`/api/v1/transparency/isin/${isin}`);
      if (!response.ok) {
        console.warn(`Transparency data not available for ${isin}: ${response.status}`);
        return [];
      }
      const apiResponse = await response.json();
      
      // Extract data from API response structure
      if (apiResponse.status === 'success' && apiResponse.data) {
        return Array.isArray(apiResponse.data) ? apiResponse.data : [];
      }
      return Array.isArray(apiResponse) ? apiResponse : [];
    } catch (error) {
      console.warn('Error fetching transparency data:', error);
      return [];
    }
  }

  /**
   * Fetch trading venues data for an ISIN
   */
  async fetchVenuesData(isin: string): Promise<any[]> {
    try {
      console.log(`Fetching venues data for ISIN: ${isin}`);
      const url = `/api/v1/instruments/${isin}/venues`;
      
      const response = await fetch(url);
      console.log(`Venues response status: ${response.status}`);
      
      if (!response.ok) {
        console.warn(`Venues request failed with status: ${response.status}`);
        return [];
      }
      
      // Handle potential JSON issues (like NaN values)
      const responseText = await response.text();
      
      try {
        // Fix invalid JSON by replacing NaN with null
        const cleanedResponseText = responseText.replace(/:\s*NaN\s*([,}])/g, ': null$1');
        const apiResponse = JSON.parse(cleanedResponseText);
        console.log('Venues response data:', apiResponse);
        
        // Extract data from API response structure
        if (apiResponse.status === 'success' && apiResponse.data && apiResponse.data.venues) {
          return Array.isArray(apiResponse.data.venues) ? apiResponse.data.venues : [];
        }
        return Array.isArray(apiResponse) ? apiResponse : [];
      } catch (jsonError) {
        console.error('JSON parsing error for venues response:', jsonError);
        console.log('Response text (first 1000 chars):', responseText.substring(0, 1000));
        return [];
      }
    } catch (error) {
      console.error('Error fetching venues data:', error);
      return [];
    }
  }

  /**
   * Fetch LEI (Legal Entity Identifier) data
   */
  async fetchLeiData(lei: string): Promise<any | null> {
    try {
      const response = await fetch(`/api/v1/legal-entities/${lei}`);
      if (!response.ok) {
        console.warn(`LEI data not available for ${lei}: ${response.status}`);
        return null;
      }
      const apiResponse = await response.json();
      
      // Extract data from API response structure
      if (apiResponse.status === 'success' && apiResponse.data) {
        return apiResponse.data;
      }
      return apiResponse;
    } catch (error) {
      console.warn('Error fetching LEI data:', error);
      return null;
    }
  }

  /**
   * Fetch relationship data for a legal entity
   */
  async fetchRelationshipData(lei: string): Promise<any | null> {
    try {
      const response = await fetch(`/api/v1/relationships/${lei}`);
      if (!response.ok) {
        console.warn(`Relationship data not available for ${lei}: ${response.status}`);
        return null;
      }
      const apiResponse = await response.json();
      
      // Extract data from API response structure
      if (apiResponse.status === 'success' && apiResponse.data) {
        return apiResponse.data;
      }
      return apiResponse;
    } catch (error) {
      console.warn('Error fetching relationship data:', error);
      return null;
    }
  }

  /**
   * Search for instruments by various criteria
   */
  async searchInstruments(query: string, filters?: any): Promise<any[]> {
    try {
      const url = new URL('/api/v1/instruments/search', window.location.origin);
      url.searchParams.set('q', query);
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== '') {
            url.searchParams.set(key, String(value));
          }
        });
      }

      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Search failed: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (error) {
      console.error('Error searching instruments:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const instrumentDataService = InstrumentDataService.getInstance();
