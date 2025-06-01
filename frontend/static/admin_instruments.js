const AdminInstruments = {
    // State management for instruments
    state: {
        currentPage: 1,
        pageSize: 10,
        totalItems: 0,
        filters: {
            type: '',
            currency: ''
        },
        currentInstrument: null,
        mode: 'create' // 'create' or 'edit'
    },
    
    init() {
        // List instruments
        document.getElementById('list-instruments-btn').addEventListener('click', () => {
            this.state.currentPage = 1;
            this.fetchInstruments();
        });

        // Apply instrument filters
        document.getElementById('apply-instrument-filters').addEventListener('click', () => {
            this.state.filters.type = document.getElementById('instrument-type-filter').value;
            this.state.filters.currency = document.getElementById('instrument-currency-filter').value;
            this.state.currentPage = 1;
            this.fetchInstruments();
        });

        // Pagination for instruments
        document.getElementById('prev-page').addEventListener('click', () => {
            if (this.state.currentPage > 1) {
                this.state.currentPage--;
                this.fetchInstruments();
            }
        });

        document.getElementById('next-page').addEventListener('click', () => {
            const totalPages = Math.ceil(this.state.totalItems / this.state.pageSize);
            if (this.state.currentPage < totalPages) {
                this.state.currentPage++;
                this.fetchInstruments();
            }
        });

        // Instrument search
        document.getElementById('instrument-search-btn').addEventListener('click', () => {
            const searchQuery = document.getElementById('instrument-search').value.trim();
            if (searchQuery) {
                this.fetchInstrumentById(searchQuery);
            } else {
                AdminUtils.showToast('Please enter an ISIN or ID to search', 'error');
            }
        });

        // Create new instrument
        document.getElementById('create-instrument-btn').addEventListener('click', () => {
            this.state.mode = 'create';
            document.getElementById('instrument-form-title').textContent = 'New Instrument';
            document.getElementById('instrument-form-container').style.display = 'block';
            document.getElementById('instrument-form').reset();
            document.getElementById('instrument-isin').disabled = false;
            
            // Check if fetch-and-enrich checkbox exists
            const fetchEnrichCheckbox = document.getElementById('fetch-and-enrich');
            if (fetchEnrichCheckbox) {
                fetchEnrichCheckbox.checked = true;
                this.toggleManualFields(true);
                
                // Add event listener for the checkbox if it doesn't have one
                if (!fetchEnrichCheckbox._hasListener) {
                    fetchEnrichCheckbox.addEventListener('change', (e) => {
                        this.toggleManualFields(e.target.checked);
                    });
                    fetchEnrichCheckbox._hasListener = true;
                }
            }
            
            this.updateTypeSpecificFields(document.getElementById('instrument-type').value);
        });

        // Handle instrument type change in form
        document.getElementById('instrument-type').addEventListener('change', (e) => {
            this.updateTypeSpecificFields(e.target.value);
        });

        // Close form buttons
        document.querySelectorAll('.close-form, .cancel-form').forEach(elem => {
            elem.addEventListener('click', () => {
                document.getElementById('instrument-form-container').style.display = 'none';
            });
        });

        // Submit instrument form
        document.getElementById('instrument-form').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const fetchAndEnrich = document.getElementById('fetch-and-enrich')?.checked;
            
            // If using fetch and enrich, use that process instead of the manual form submission
            if (fetchAndEnrich) {
                const isin = document.getElementById('instrument-isin').value;
                const type = document.getElementById('instrument-type').value;
                this.fetchAndInsert(isin, type);
                return;
            }
            
            // Otherwise use the normal manual form submission
            const formData = new FormData(e.target);
            const instrumentData = Object.fromEntries(formData.entries());
            
            // Remove the fetch_and_enrich field
            delete instrumentData.fetch_and_enrich;
            
            if (this.state.mode === 'create') {
                this.createInstrument(instrumentData);
            } else {
                this.updateInstrument(this.state.currentInstrument.id, instrumentData);
            }
        });

        // Close detail view
        document.querySelector('#instrument-detail-view .close-detail').addEventListener('click', () => {
            document.getElementById('instrument-detail-view').style.display = 'none';
        });

        // Instrument detail actions
        document.getElementById('edit-instrument-btn').addEventListener('click', () => {
            this.prepareEditForm(this.state.currentInstrument);
        });

        document.getElementById('enrich-instrument-btn').addEventListener('click', () => {
            this.enrichInstrument(this.state.currentInstrument.id);
        });

        document.getElementById('delete-instrument-btn').addEventListener('click', () => {
            AdminUtils.showConfirmationModal(
                'Delete Instrument', 
                `Are you sure you want to delete instrument ${this.state.currentInstrument.isin}?`,
                () => this.deleteInstrument(this.state.currentInstrument.id)
            );
        });
        
        // Load initial data
        this.fetchInstruments();
    },
    
    // Toggle visibility of manual fields based on checkbox
    toggleManualFields(fetchAndEnrich) {
        const manualFields = document.getElementById('manual-fields');
        if (manualFields) {
            manualFields.style.display = fetchAndEnrich ? 'none' : 'block';
        }
    },
    
    // New fetchAndInsert function moved from search.js
    async fetchAndInsert(isin, category) {
        AdminUtils.showSpinner();
        try {
            const payload = {
                Id: isin,
                Category: category  // This matches the database polymorphic identity
            };

            const response = await fetch('/api/fetch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            
            if (response.ok) {
                const enrichmentStatus = [];
                if (result.figi) enrichmentStatus.push('FIGI');
                if (result.lei) enrichmentStatus.push('LEI');
                
                const enrichmentText = enrichmentStatus.length ? 
                    ` (enriched with ${enrichmentStatus.join(', ')})` : '';
                    
                AdminUtils.showToast(`Successfully processed ${isin}${enrichmentText}`, 'success');
                document.getElementById('instrument-form-container').style.display = 'none';
                
                // Fetch and show the newly created instrument
                this.fetchInstrumentById(isin);
                
                // Refresh the instruments list
                this.fetchInstruments();
            } else {
                throw new Error(result.error || 'Failed to process request');
            }
        } catch (error) {
            console.error('Error:', error);
            AdminUtils.showToast(error.message, 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },
    
    // API Functions for Instruments
    async fetchInstruments() {
        AdminUtils.showSpinner();
        try {
            let url = `/api/v1/instruments?limit=${this.state.pageSize}&offset=${(this.state.currentPage - 1) * this.state.pageSize}`;
            
            if (this.state.filters.type) {
                url += `&type=${this.state.filters.type}`;
            }
            
            if (this.state.filters.currency) {
                url += `&currency=${this.state.filters.currency}`;
            }
              const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                // Handle both the new API format (with status/data/meta) and the old format (with instruments/count) 
                const instruments = data.data || data.instruments || [];
                const count = data.meta?.total || data.count || 0;
                
                this.renderInstrumentsTable(instruments);
                this.state.totalItems = count;
                AdminUtils.updatePaginationInfo('instruments', this.state.currentPage, this.state.pageSize, this.state.totalItems);
            } else {
                AdminUtils.showToast(data.error || 'Failed to fetch instruments', 'error');
            }
        } catch (error) {
            console.error('Error fetching instruments:', error);
            AdminUtils.showToast('An error occurred while fetching instruments', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async fetchInstrumentById(identifier) {
        AdminUtils.showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${identifier}`);
            const data = await response.json();
            
            if (response.ok) {
                this.showInstrumentDetail(data);
            } else {
                AdminUtils.showToast(data.error || 'Instrument not found', 'error');
            }
        } catch (error) {
            console.error('Error fetching instrument:', error);
            AdminUtils.showToast('An error occurred while fetching the instrument', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async fetchInstrumentForEdit(id) {
        AdminUtils.showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${id}`);
            const data = await response.json();
            
            if (response.ok) {
                this.prepareEditForm(data);
            } else {
                AdminUtils.showToast(data.error || 'Instrument not found', 'error');
            }
        } catch (error) {
            console.error('Error fetching instrument for edit:', error);
            AdminUtils.showToast('An error occurred while fetching the instrument', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async createInstrument(instrumentData) {
        AdminUtils.showSpinner();
        try {
            const response = await fetch('/api/v1/instruments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(instrumentData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast('Instrument created successfully', 'success');
                document.getElementById('instrument-form-container').style.display = 'none';
                this.fetchInstrumentById(data.id);
            } else {
                AdminUtils.showToast(data.error || 'Failed to create instrument', 'error');
            }
        } catch (error) {
            console.error('Error creating instrument:', error);
            AdminUtils.showToast('An error occurred while creating the instrument', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async updateInstrument(id, instrumentData) {
        AdminUtils.showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(instrumentData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast('Instrument updated successfully', 'success');
                document.getElementById('instrument-form-container').style.display = 'none';
                this.fetchInstrumentById(id);
            } else {
                AdminUtils.showToast(data.error || 'Failed to update instrument', 'error');
            }
        } catch (error) {
            console.error('Error updating instrument:', error);
            AdminUtils.showToast('An error occurred while updating the instrument', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async deleteInstrument(id) {
        AdminUtils.showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${id}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                AdminUtils.showToast('Instrument deleted successfully', 'success');
                document.getElementById('instrument-detail-view').style.display = 'none';
                this.fetchInstruments();
            } else {
                AdminUtils.showToast(data.error || 'Failed to delete instrument', 'error');
            }
        } catch (error) {
            console.error('Error deleting instrument:', error);
            AdminUtils.showToast('An error occurred while deleting the instrument', 'error');
        } finally {
            AdminUtils.hideSpinner();
            AdminUtils.hideConfirmationModal();
        }
    },

    async enrichInstrument(id) {
        AdminUtils.showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${id}/enrich`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                let message = 'Instrument enriched successfully';
                if (data.enrichment_results) {
                    const figiChanged = data.enrichment_results.figi.changed;
                    const leiChanged = data.enrichment_results.lei.changed;
                    
                    if (figiChanged && leiChanged) {
                        message += ' (FIGI and LEI added)';
                    } else if (figiChanged) {
                        message += ' (FIGI added)';
                    } else if (leiChanged) {
                        message += ' (LEI added)';
                    } else {
                        message += ' (no changes)';
                    }
                }
                
                AdminUtils.showToast(message, 'success');
                this.fetchInstrumentById(id);
            } else {
                AdminUtils.showToast(data.error || 'Failed to enrich instrument', 'error');
            }
        } catch (error) {
            console.error('Error enriching instrument:', error);
            AdminUtils.showToast('An error occurred while enriching the instrument', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },
    
    // Helper function for type-specific fields
    updateTypeSpecificFields(type) {
        const container = document.getElementById('type-specific-fields');
        container.innerHTML = '';
        
        switch (type) {
            case 'equity':
                container.innerHTML = `
                    <div class="form-group">
                        <label for="instrument-shares">Shares Outstanding:</label>
                        <input type="number" id="instrument-shares" name="shares_outstanding" step="any">
                    </div>
                    <div class="form-group">
                        <label for="instrument-market-cap">Market Cap:</label>
                        <input type="number" id="instrument-market-cap" name="market_cap" step="any">
                    </div>
                    <div class="form-group">
                        <label for="instrument-sector">Sector:</label>
                        <input type="text" id="instrument-sector" name="sector">
                    </div>
                    <div class="form-group">
                        <label for="instrument-industry">Industry:</label>
                        <input type="text" id="instrument-industry" name="industry">
                    </div>
                `;
                break;
                
            case 'debt':
                container.innerHTML = `
                    <div class="form-group">
                        <label for="instrument-maturity">Maturity Date:</label>
                        <input type="date" id="instrument-maturity" name="maturity_date">
                    </div>
                    <div class="form-group">
                        <label for="instrument-nominal">Nominal Value:</label>
                        <input type="number" id="instrument-nominal" name="nominal_value_per_unit" step="any">
                    </div>
                    <div class="form-group">
                        <label for="instrument-total-nominal">Total Issued Nominal:</label>
                        <input type="number" id="instrument-total-nominal" name="total_issued_nominal" step="any">
                    </div>
                    <div class="form-group">
                        <label for="instrument-debt-seniority">Seniority:</label>
                        <input type="text" id="instrument-debt-seniority" name="debt_seniority">
                    </div>
                `;
                break;
                
            case 'future':
                container.innerHTML = `
                    <div class="form-group">
                        <label for="instrument-expiration">Expiration Date:</label>
                        <input type="date" id="instrument-expiration" name="expiration_date">
                    </div>
                    <div class="form-group">
                        <label for="instrument-price-multiplier">Price Multiplier:</label>
                        <input type="number" id="instrument-price-multiplier" name="price_multiplier" step="any">
                    </div>
                    <div class="form-group">
                        <label for="instrument-delivery-type">Delivery Type:</label>
                        <select id="instrument-delivery-type" name="delivery_type">
                            <option value="PHYS">Physical</option>
                            <option value="CASH">Cash</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="instrument-underlying-isin">Underlying ISIN:</label>
                        <input type="text" id="instrument-underlying-isin" name="underlying_single_isin">
                    </div>
                `;
                break;
        }
    },

    // Helper function for edit form
    prepareEditForm(instrument) {
        this.state.mode = 'edit';
        document.getElementById('instrument-form-title').textContent = `Edit Instrument: ${instrument.isin}`;
        document.getElementById('instrument-form-container').style.display = 'block';
        
        // Set base form fields
        document.getElementById('instrument-isin').value = instrument.isin;
        document.getElementById('instrument-isin').disabled = true; // Can't edit ISIN
        document.getElementById('instrument-type').value = instrument.type;
        document.getElementById('instrument-type').disabled = true; // Can't edit type
        document.getElementById('instrument-symbol').value = instrument.symbol || '';
        document.getElementById('instrument-full-name').value = instrument.full_name || '';
        document.getElementById('instrument-cfi').value = instrument.cfi_code || '';
        document.getElementById('instrument-currency').value = instrument.currency || '';
        
        // Add type-specific fields
        this.updateTypeSpecificFields(instrument.type);
        
        // Set type-specific field values
        switch (instrument.type) {
            case 'equity':
                if (instrument.equity_attributes) {
                    document.getElementById('instrument-shares').value = instrument.equity_attributes.shares_outstanding || '';
                    document.getElementById('instrument-market-cap').value = instrument.equity_attributes.market_cap || '';
                    document.getElementById('instrument-sector').value = instrument.equity_attributes.sector || '';
                    document.getElementById('instrument-industry').value = instrument.equity_attributes.industry || '';
                }
                break;
                
            case 'debt':
                if (instrument.debt_attributes) {
                    const maturityDate = instrument.debt_attributes.maturity_date ? 
                        new Date(instrument.debt_attributes.maturity_date).toISOString().split('T')[0] : '';
                    document.getElementById('instrument-maturity').value = maturityDate;
                    document.getElementById('instrument-nominal').value = instrument.debt_attributes.nominal_value_per_unit || '';
                    document.getElementById('instrument-total-nominal').value = instrument.debt_attributes.total_issued_nominal || '';
                    document.getElementById('instrument-debt-seniority').value = instrument.debt_attributes.debt_seniority || '';
                }
                break;
                
            case 'future':
                if (instrument.future_attributes) {
                    const expirationDate = instrument.future_attributes.expiration_date ? 
                        new Date(instrument.future_attributes.expiration_date).toISOString().split('T')[0] : '';
                    document.getElementById('instrument-expiration').value = expirationDate;
                    document.getElementById('instrument-price-multiplier').value = instrument.future_attributes.price_multiplier || '';
                    document.getElementById('instrument-delivery-type').value = instrument.future_attributes.delivery_type || '';
                    document.getElementById('instrument-underlying-isin').value = instrument.future_attributes.underlying_isin || '';
                }
                break;
        }
    },
    
    // UI Rendering Functions
    renderInstrumentsTable(instruments) {
        const tbody = document.getElementById('instruments-tbody');
        tbody.innerHTML = '';
        
        if (instruments.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" class="text-center">No instruments found</td>';
            tbody.appendChild(row);
            return;
        }
        
        instruments.forEach(instrument => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${instrument.isin || '-'}</td>
                <td>${instrument.type || '-'}</td>
                <td>${instrument.symbol || '-'}</td>
                <td>${instrument.full_name || '-'}</td>
                <td>
                    <button class="table-action-btn view" data-id="${instrument.id}">View</button>
                    <button class="table-action-btn edit" data-id="${instrument.id}">Edit</button>
                    <button class="table-action-btn delete" data-id="${instrument.id}">Delete</button>
                </td>
            `;
            
            // Add event listeners to action buttons
            row.querySelector('.view').addEventListener('click', () => this.fetchInstrumentById(instrument.id));
            row.querySelector('.edit').addEventListener('click', () => this.fetchInstrumentForEdit(instrument.id));
            row.querySelector('.delete').addEventListener('click', () => {
                AdminUtils.showConfirmationModal(
                    'Delete Instrument', 
                    `Are you sure you want to delete instrument ${instrument.isin}?`,
                    () => this.deleteInstrument(instrument.id)
                );
            });
            
            tbody.appendChild(row);
        });
    },

    showInstrumentDetail(instrument) {
        this.state.currentInstrument = instrument;
        
        const detailContent = document.getElementById('instrument-detail-content');
        detailContent.innerHTML = '';
        
        // Create sections for the instrument details
        const sections = [];
        
        // Basic info section
        sections.push({
            title: 'Basic Information',
            fields: {
                'ID': instrument.id,
                'ISIN': instrument.isin || '-',
                'Type': instrument.type || '-',
                'Symbol': instrument.symbol || '-',
                'Full Name': instrument.full_name || '-',
                'CFI Code': instrument.cfi_code || '-',
                'Currency': instrument.currency || '-',
                'First Trade Date': instrument.first_trade_date ? AdminUtils.formatDate(instrument.first_trade_date) : '-'
            }
        });
        
        // Venue section
        sections.push({
            title: 'Trading Venue',
            fields: {
                'Trading Venue': instrument.trading_venue || '-',
                'Relevant Venue': instrument.relevant_venue || '-',
                'Relevant Authority': instrument.relevant_authority || '-'
            }
        });
        
        // Type-specific attributes
        if (instrument.type === 'equity' && instrument.equity_attributes) {
            sections.push({
                title: 'Equity Specific Attributes',
                fields: {
                    'Shares Outstanding': instrument.equity_attributes.shares_outstanding || '-',
                    'Market Cap': instrument.equity_attributes.market_cap || '-',
                    'Sector': instrument.equity_attributes.sector || '-',
                    'Industry': instrument.equity_attributes.industry || '-'
                }
            });
        } else if (instrument.type === 'debt' && instrument.debt_attributes) {
            sections.push({
                title: 'Debt Specific Attributes',
                fields: {
                    'Maturity Date': AdminUtils.formatDate(instrument.debt_attributes.maturity_date),
                    'Nominal Value': instrument.debt_attributes.nominal_value_per_unit || '-',
                    'Total Issued Nominal': instrument.debt_attributes.total_issued_nominal || '-',
                    'Debt Seniority': instrument.debt_attributes.debt_seniority || '-'
                }
            });
        } else if (instrument.type === 'future' && instrument.future_attributes) {
            sections.push({
                title: 'Future Specific Attributes',
                fields: {
                    'Expiration Date': AdminUtils.formatDate(instrument.future_attributes.expiration_date),
                    'Price Multiplier': instrument.future_attributes.price_multiplier || '-',
                    'Delivery Type': instrument.future_attributes.delivery_type || '-',
                    'Underlying ISIN': instrument.future_attributes.underlying_isin || '-'
                }
            });
        }
        
        // CFI decoded section
        if (instrument.cfi_decoded) {
            const cfiSection = {
                title: 'CFI Classification',
                fields: {
                    'Category': `${instrument.cfi_decoded.category} - ${instrument.cfi_decoded.category_description}`,
                    'Group': `${instrument.cfi_decoded.group} - ${instrument.cfi_decoded.group_description}`
                }
            };
            
            // Add attributes if available
            if (instrument.cfi_decoded.attributes && typeof instrument.cfi_decoded.attributes === 'object') {
                Object.entries(instrument.cfi_decoded.attributes).forEach(([key, value]) => {
                    const formattedKey = key.replace(/_/g, ' ')
                        .replace(/\b\w/g, l => l.toUpperCase());
                    cfiSection.fields[formattedKey] = value;
                });
            }
            
            sections.push(cfiSection);
        }
        
        // Legal entity section
        if (instrument.legal_entity) {
            sections.push({
                title: 'Legal Entity',
                fields: {
                    'LEI': instrument.legal_entity.lei,
                    'Name': instrument.legal_entity.name,
                    'Jurisdiction': instrument.legal_entity.jurisdiction,
                    'Status': instrument.legal_entity.status
                }
            });
        }
        
        // FIGI section
        if (instrument.figi) {
            sections.push({
                title: 'FIGI Data',
                fields: {
                    'FIGI': instrument.figi.figi,
                    'Composite FIGI': instrument.figi.composite_figi || '-',
                    'Share Class FIGI': instrument.figi.share_class_figi || '-',
                    'Security Type': instrument.figi.security_type || '-',
                    'Market Sector': instrument.figi.market_sector || '-'
                }
            });
        }
        
        // Render all sections
        sections.forEach(section => {
            const sectionElem = document.createElement('div');
            sectionElem.classList.add('detail-section');
            
            sectionElem.innerHTML = `<h4>${section.title}</h4>`;
            
            Object.entries(section.fields).forEach(([label, value]) => {
                const row = document.createElement('div');
                row.classList.add('detail-row');
                
                row.innerHTML = `
                    <span class="detail-label">${label}:</span>
                    <span>${value}</span>
                `;
                
                sectionElem.appendChild(row);
            });
            
            detailContent.appendChild(sectionElem);
        });
        
        // Show the detail view
        document.getElementById('instrument-detail-view').style.display = 'block';
    }
};
