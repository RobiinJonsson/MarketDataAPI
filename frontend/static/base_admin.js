// Base Admin Module - Consolidates common functionality
class BaseAdminModule {
    constructor(entityType, config = {}) {
        this.entityType = entityType;
        this.config = {
            pageSize: APP_CONFIG.DEFAULT_PAGE_SIZE,
            apiEndpoint: APP_CONFIG.ENDPOINTS[entityType.toUpperCase()],
            ...config
        };
        
        this.state = {
            currentPage: 1,
            pageSize: this.config.pageSize,
            totalItems: 0,
            filters: {},
            currentItem: null,
            mode: 'create'
        };
    }
    
    // Common API methods
    async fetchItems(filters = {}) {
        AdminUtils.showSpinner();
        try {
            const params = {
                limit: this.state.pageSize,
                offset: (this.state.currentPage - 1) * this.state.pageSize,
                ...this.state.filters,
                ...filters
            };
            
            const url = buildApiUrl(this.config.apiEndpoint, params);
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                const items = data.data || data[this.entityType + 's'] || [];
                const count = data.meta?.total || data.count || 0;
                
                this.renderItemsTable(items);
                this.state.totalItems = count;
                AdminUtils.updatePaginationInfo(this.entityType, this.state.currentPage, this.state.pageSize, this.state.totalItems);
            } else {
                AdminUtils.showToast(data.error || `Failed to fetch ${this.entityType}s`, 'error');
            }
        } catch (error) {
            console.error(`Error fetching ${this.entityType}s:`, error);
            AdminUtils.showToast(`An error occurred while fetching ${this.entityType}s`, 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    }
    
    async fetchItemById(id) {
        AdminUtils.showSpinner();
        try {
            const url = buildApiUrl(`${this.config.apiEndpoint}/${id}`);
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                this.showItemDetail(data);
            } else {
                AdminUtils.showToast(data.error || `${this.entityType} not found`, 'error');
            }
        } catch (error) {
            console.error(`Error fetching ${this.entityType}:`, error);
            AdminUtils.showToast(`An error occurred while fetching the ${this.entityType}`, 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    }
    
    async deleteItem(id) {
        AdminUtils.showSpinner();
        try {
            const url = buildApiUrl(`${this.config.apiEndpoint}/${id}`);
            const response = await fetch(url, { method: 'DELETE' });
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast(`${this.entityType} deleted successfully`, 'success');
                this.hideDetailView();
                this.fetchItems();
            } else {
                AdminUtils.showToast(data.error || `Failed to delete ${this.entityType}`, 'error');
            }
        } catch (error) {
            console.error(`Error deleting ${this.entityType}:`, error);
            AdminUtils.showToast(`An error occurred while deleting the ${this.entityType}`, 'error');
        } finally {
            AdminUtils.hideSpinner();
            AdminUtils.hideConfirmationModal();
        }
    }
    
    // Common pagination methods
    initPagination() {
        document.getElementById(`${this.entityType}-prev-page`).addEventListener('click', () => {
            if (this.state.currentPage > 1) {
                this.state.currentPage--;
                this.fetchItems();
            }
        });

        document.getElementById(`${this.entityType}-next-page`).addEventListener('click', () => {
            const totalPages = Math.ceil(this.state.totalItems / this.state.pageSize);
            if (this.state.currentPage < totalPages) {
                this.state.currentPage++;
                this.fetchItems();
            }
        });
    }
    
    // Common filter methods
    applyFilters() {
        this.state.currentPage = 1;
        this.fetchItems();
    }
    
    // Abstract methods that subclasses should implement
    renderItemsTable(items) {
        throw new Error('renderItemsTable must be implemented by subclass');
    }
    
    showItemDetail(item) {
        throw new Error('showItemDetail must be implemented by subclass');
    }
    
    hideDetailView() {
        document.getElementById(`${this.entityType}-detail-view`).style.display = 'none';
    }
}
