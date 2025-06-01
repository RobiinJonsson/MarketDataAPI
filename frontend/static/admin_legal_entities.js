const AdminLegalEntities = {
    // State management for legal entities
    state: {
        currentPage: 1,
        pageSize: APP_CONFIG.DEFAULT_PAGE_SIZE,
        totalItems: 0,
        filters: {
            status: '',
            jurisdiction: ''
        },
        currentEntity: null
    },
    
    init() {
        // List entities
        document.getElementById('list-entities-btn').addEventListener('click', () => {
            this.state.currentPage = 1;
            this.fetchEntities();
        });

        // Apply entity filters
        document.getElementById('apply-entity-filters').addEventListener('click', () => {
            this.state.filters.status = document.getElementById('entity-status-filter').value;
            this.state.filters.jurisdiction = document.getElementById('entity-jurisdiction-filter').value;
            this.state.currentPage = 1;
            this.fetchEntities();
        });

        // Fetch entity from GLEIF
        document.getElementById('fetch-entity-btn').addEventListener('click', () => {
            const lei = prompt('Enter LEI code to fetch from GLEIF:');
            if (lei && lei.trim()) {
                this.fetchEntityFromGLEIF(lei.trim());
            }
        });

        // Entity search
        document.getElementById('entity-search-btn').addEventListener('click', () => {
            const searchQuery = document.getElementById('entity-search').value.trim();
            if (searchQuery) {
                this.fetchEntityById(searchQuery);
            } else {
                AdminUtils.showToast('Please enter an LEI to search', 'error');
            }
        });

        // Pagination for entities
        document.getElementById('entity-prev-page').addEventListener('click', () => {
            if (this.state.currentPage > 1) {
                this.state.currentPage--;
                this.fetchEntities();
            }
        });

        document.getElementById('entity-next-page').addEventListener('click', () => {
            const totalPages = Math.ceil(this.state.totalItems / this.state.pageSize);
            if (this.state.currentPage < totalPages) {
                this.state.currentPage++;
                this.fetchEntities();
            }
        });

        // Close entity detail view
        document.querySelector('#entity-detail-view .close-detail').addEventListener('click', () => {
            document.getElementById('entity-detail-view').style.display = 'none';
        });

        // Entity detail actions
        document.getElementById('refresh-entity-btn').addEventListener('click', () => {
            this.refreshEntityFromGLEIF(this.state.currentEntity.lei);
        });

        document.getElementById('delete-entity-btn').addEventListener('click', () => {
            AdminUtils.showConfirmationModal(
                'Delete Legal Entity', 
                `Are you sure you want to delete legal entity ${this.state.currentEntity.lei}?`,
                () => this.deleteEntity(this.state.currentEntity.lei)
            );
        });
        
        // Load initial entities
        this.fetchEntities();
    },
    
    // API Functions for Legal Entities
    async fetchEntities() {
        AdminUtils.showSpinner();        try {
            const params = {
                limit: this.state.pageSize,
                offset: (this.state.currentPage - 1) * this.state.pageSize
            };
            
            if (this.state.filters.status) {
                params.status = this.state.filters.status;
            }
            
            if (this.state.filters.jurisdiction) {
                params.jurisdiction = this.state.filters.jurisdiction;
            }
            
            const url = buildApiUrl(APP_CONFIG.ENDPOINTS.ENTITIES, params);
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                // Handle both the new API format (with status/data/meta) and the old format (with entities/count) 
                const entities = data.data || data.entities || [];
                const count = data.meta?.total || data.count || 0;
                
                this.renderEntitiesTable(entities);
                this.state.totalItems = count;
                AdminUtils.updatePaginationInfo('entities', this.state.currentPage, this.state.pageSize, this.state.totalItems);
                
                // Fetch all available jurisdictions for the filter
                if (!this.state.filters.jurisdiction) {
                    this.fetchAllAvailableJurisdictions();
                }
            } else {
                AdminUtils.showToast(data.error || 'Failed to fetch entities', 'error');
            }
        } catch (error) {
            console.error('Error fetching entities:', error);
            AdminUtils.showToast('An error occurred while fetching entities', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async fetchEntityById(lei) {
        AdminUtils.showSpinner();
        try {
            const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.ENTITIES}/${lei}`);
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                this.showEntityDetail(data);
            } else {
                AdminUtils.showToast(data.error || 'Legal entity not found', 'error');
            }
        } catch (error) {
            console.error('Error fetching entity:', error);
            AdminUtils.showToast('An error occurred while fetching the legal entity', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async fetchEntityFromGLEIF(lei) {
        AdminUtils.showSpinner();        try {
            const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.ENTITIES}/${lei}`);
            const response = await fetch(url, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast('Legal entity fetched successfully from GLEIF', 'success');
                this.fetchEntityById(lei);
            } else {
                AdminUtils.showToast(data.error || 'Failed to fetch legal entity', 'error');
            }
        } catch (error) {
            console.error('Error fetching entity from GLEIF:', error);
            AdminUtils.showToast('An error occurred while fetching the legal entity', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async refreshEntityFromGLEIF(lei) {
        AdminUtils.showSpinner();        try {
            const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.ENTITIES}/${lei}`);
            const response = await fetch(url, {
                method: 'PUT'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast('Legal entity refreshed successfully from GLEIF', 'success');
                this.fetchEntityById(lei);
            } else {
                AdminUtils.showToast(data.error || 'Failed to refresh legal entity', 'error');
            }
        } catch (error) {
            console.error('Error refreshing entity from GLEIF:', error);
            AdminUtils.showToast('An error occurred while refreshing the legal entity', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async deleteEntity(lei) {
        AdminUtils.showSpinner();        try {
            const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.ENTITIES}/${lei}`);
            const response = await fetch(url, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast('Legal entity deleted successfully', 'success');
                document.getElementById('entity-detail-view').style.display = 'none';
                this.fetchEntities();
            } else {
                AdminUtils.showToast(data.error || 'Failed to delete legal entity', 'error');
            }
        } catch (error) {
            console.error('Error deleting entity:', error);
            AdminUtils.showToast('An error occurred while deleting the legal entity', 'error');
        } finally {
            AdminUtils.hideSpinner();
            AdminUtils.hideConfirmationModal();
        }
    },    async fetchAllAvailableJurisdictions() {        try {
            // Use a larger limit to get as many different jurisdictions as possible
            const url = buildApiUrl(APP_CONFIG.ENDPOINTS.ENTITIES, { limit: 1000 });
            const response = await fetch(url);
            const data = await response.json();
            
            // Handle both old and new API response formats
            const entities = data.data || data.entities || [];
            
            if (response.ok && entities.length > 0) {
                this.updateJurisdictionFilter(entities);
            }
        } catch (error) {
            console.error('Error fetching jurisdictions:', error);
            // Don't show an error toast as this is a background operation
        }
    },

    updateJurisdictionFilter(entities) {
        // Get unique jurisdictions
        const jurisdictions = [...new Set(
            entities
                .map(entity => entity.jurisdiction)
                .filter(jurisdiction => jurisdiction) // Filter out null/undefined
        )].sort();
        
        // Update the jurisdiction filter dropdown
        const selectElement = document.getElementById('entity-jurisdiction-filter');
        
        // Store current value to preserve it
        const currentValue = selectElement.value;
        
        // Keep the first empty option
        const emptyOption = selectElement.querySelector('option:first-child');
        selectElement.innerHTML = '';
        selectElement.appendChild(emptyOption);
        
        // Add options for each jurisdiction
        jurisdictions.forEach(jurisdiction => {
            const option = document.createElement('option');
            option.value = jurisdiction;
            option.textContent = jurisdiction;
            selectElement.appendChild(option);
        });
        
        // Restore selected value if it exists
        if (currentValue) {
            selectElement.value = currentValue;
        }
    },
    
    // UI Rendering Functions
    renderEntitiesTable(entities) {
        const tbody = document.getElementById('entities-tbody');
        tbody.innerHTML = '';
        
        if (entities.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" class="text-center">No legal entities found</td>';
            tbody.appendChild(row);
            return;
        }
        
        entities.forEach(entity => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${entity.lei || '-'}</td>
                <td>${entity.name || '-'}</td>
                <td>${entity.jurisdiction || '-'}</td>
                <td>${entity.status || '-'}</td>
                <td>
                    <button class="table-action-btn view" data-lei="${entity.lei}">View</button>
                    <button class="table-action-btn refresh" data-lei="${entity.lei}">Refresh</button>
                    <button class="table-action-btn delete" data-lei="${entity.lei}">Delete</button>
                </td>
            `;
            
            // Add event listeners to action buttons
            row.querySelector('.view').addEventListener('click', () => this.fetchEntityById(entity.lei));
            row.querySelector('.refresh').addEventListener('click', () => this.refreshEntityFromGLEIF(entity.lei));
            row.querySelector('.delete').addEventListener('click', () => {
                AdminUtils.showConfirmationModal(
                    'Delete Legal Entity', 
                    `Are you sure you want to delete legal entity ${entity.lei}?`,
                    () => this.deleteEntity(entity.lei)
                );
            });
            
            tbody.appendChild(row);
        });
    },

    showEntityDetail(entity) {
        this.state.currentEntity = entity;
        
        const detailContent = document.getElementById('entity-detail-content');
        detailContent.innerHTML = '';
        
        // Basic info section
        const basicSection = document.createElement('div');
        basicSection.classList.add('detail-section');
        basicSection.innerHTML = `
            <h4>Basic Information</h4>
            <div class="detail-row">
                <span class="detail-label">LEI:</span>
                <span>${entity.lei}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Name:</span>
                <span>${entity.name || '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Jurisdiction:</span>
                <span>${entity.jurisdiction || '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Legal Form:</span>
                <span>${entity.legal_form || '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Registered As:</span>
                <span>${entity.registered_as || '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Status:</span>
                <span>${entity.status || '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Creation Date:</span>
                <span>${entity.creation_date ? AdminUtils.formatDate(entity.creation_date) : '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Next Renewal:</span>
                <span>${entity.next_renewal_date ? AdminUtils.formatDate(entity.next_renewal_date) : '-'}</span>
            </div>
        `;
        detailContent.appendChild(basicSection);
        
        // Add addresses if available
        if (entity.addresses && entity.addresses.length > 0) {
            const addressSection = document.createElement('div');
            addressSection.classList.add('detail-section');
            addressSection.innerHTML = '<h4>Addresses</h4>';
            
            entity.addresses.forEach(addr => {
                const addressBox = document.createElement('div');
                addressBox.classList.add('address-box');
                addressBox.innerHTML = `
                    <div class="detail-row">
                        <span class="detail-label">Type:</span>
                        <span>${addr.type || '-'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Address:</span>
                        <span>${addr.address_lines || '-'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">City:</span>
                        <span>${addr.city || '-'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Region:</span>
                        <span>${addr.region || '-'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Postal Code:</span>
                        <span>${addr.postal_code || '-'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Country:</span>
                        <span>${addr.country || '-'}</span>
                    </div>
                `;
                addressSection.appendChild(addressBox);
            });
            
            detailContent.appendChild(addressSection);
        }
        
        // Add registration details if available
        if (entity.registration) {
            const regSection = document.createElement('div');
            regSection.classList.add('detail-section');
            regSection.innerHTML = `
                <h4>Registration Details</h4>
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    <span>${entity.registration.status || '-'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Last Update:</span>
                    <span>${entity.registration.last_update ? AdminUtils.formatDate(entity.registration.last_update) : '-'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Next Renewal:</span>
                    <span>${entity.registration.next_renewal ? AdminUtils.formatDate(entity.registration.next_renewal) : '-'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Managing LOU:</span>
                    <span>${entity.registration.managing_lou || '-'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Validation Sources:</span>
                    <span>${entity.registration.validation_sources || '-'}</span>
                </div>
            `;
            detailContent.appendChild(regSection);
        }
        
        // Show the entity detail view
        document.getElementById('entity-detail-view').style.display = 'block';
    }
};
