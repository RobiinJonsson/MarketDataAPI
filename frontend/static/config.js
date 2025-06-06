// Frontend Configuration Constants
const APP_CONFIG = {
    // API Configuration
    API_BASE_URL: '/api/v1',
    
    // Pagination Settings
    DEFAULT_PAGE_SIZE: 10,
    MAX_PAGE_SIZE: 100,
    
    // UI Settings
    TOAST_DURATION: 3000,
    SEARCH_DEBOUNCE_DELAY: 300,
    
    // Validation Rules
    CFI_CODE_LENGTH: 6,
    MAX_BATCH_SIZE: 100,
    
    // File Upload Limits
    MAX_FILE_SIZE: 500 * 1024 * 1024, // 500MB
    ALLOWED_FILE_TYPES: ['.yaml', '.yml'],    // API Endpoints
    ENDPOINTS: {
        INSTRUMENTS: '/instruments',
        ENTITIES: '/entities',
        CFI: '/cfi',
        BATCH: '/batch',
        FIGI: '/figi',
        SCHEMAS: '/schemas',
        SEARCH: '/instruments'  // Updated to use new instruments endpoint
    }
};

// Helper function to build API URLs
function buildApiUrl(endpoint, params = {}) {
    let url = `${APP_CONFIG.API_BASE_URL}${endpoint}`;
    
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
            queryParams.append(key, value);
        }
    });
    
    const queryString = queryParams.toString();
    return queryString ? `${url}?${queryString}` : url;
}

// Export for use in other modules
window.APP_CONFIG = APP_CONFIG;
window.buildApiUrl = buildApiUrl;
