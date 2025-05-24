document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.admin-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active tab pane
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === `${tabName}-tab`) {
                    pane.classList.add('active');
                }
            });
        });
    });

    // Instruments management
    const instrumentState = {
        currentPage: 1,
        pageSize: 10,
        totalItems: 0,
        filters: {
            type: '',
            currency: ''
        },
        currentInstrument: null,
        mode: 'create' // 'create' or 'edit'
    };

    // List instruments
    document.getElementById('list-instruments-btn').addEventListener('click', () => {
        instrumentState.currentPage = 1;
        fetchInstruments();
    });

    // Apply instrument filters
    document.getElementById('apply-instrument-filters').addEventListener('click', () => {
        instrumentState.filters.type = document.getElementById('instrument-type-filter').value;
        instrumentState.filters.currency = document.getElementById('instrument-currency-filter').value;
        instrumentState.currentPage = 1;
        fetchInstruments();
    });

    // Pagination for instruments
    document.getElementById('prev-page').addEventListener('click', () => {
        if (instrumentState.currentPage > 1) {
            instrumentState.currentPage--;
            fetchInstruments();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        const totalPages = Math.ceil(instrumentState.totalItems / instrumentState.pageSize);
        if (instrumentState.currentPage < totalPages) {
            instrumentState.currentPage++;
            fetchInstruments();
        }
    });

    // Instrument search
    document.getElementById('instrument-search-btn').addEventListener('click', () => {
        const searchQuery = document.getElementById('instrument-search').value.trim();
        if (searchQuery) {
            fetchInstrumentById(searchQuery);
        } else {
            showToast('Please enter an ISIN or ID to search', 'error');
        }
    });

    // Create new instrument
    document.getElementById('create-instrument-btn').addEventListener('click', () => {
        instrumentState.mode = 'create';
        document.getElementById('instrument-form-title').textContent = 'New Instrument';
        document.getElementById('instrument-form-container').style.display = 'block';
        document.getElementById('instrument-form').reset();
        document.getElementById('instrument-isin').disabled = false;
        updateTypeSpecificFields(document.getElementById('instrument-type').value);
    });

    // Handle instrument type change in form
    document.getElementById('instrument-type').addEventListener('change', (e) => {
        updateTypeSpecificFields(e.target.value);
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
        const formData = new FormData(e.target);
        const instrumentData = Object.fromEntries(formData.entries());
        
        if (instrumentState.mode === 'create') {
            createInstrument(instrumentData);
        } else {
            updateInstrument(instrumentState.currentInstrument.id, instrumentData);
        }
    });

    // Close detail view
    document.querySelector('#instrument-detail-view .close-detail').addEventListener('click', () => {
        document.getElementById('instrument-detail-view').style.display = 'none';
    });

    // Instrument detail actions
    document.getElementById('edit-instrument-btn').addEventListener('click', () => {
        prepareEditForm(instrumentState.currentInstrument);
    });

    document.getElementById('enrich-instrument-btn').addEventListener('click', () => {
        enrichInstrument(instrumentState.currentInstrument.id);
    });

    document.getElementById('delete-instrument-btn').addEventListener('click', () => {
        showConfirmationModal(
            'Delete Instrument', 
            `Are you sure you want to delete instrument ${instrumentState.currentInstrument.isin}?`,
            () => deleteInstrument(instrumentState.currentInstrument.id)
        );
    });

    // Legal Entities management
    const entityState = {
        currentPage: 1,
        pageSize: 10,
        totalItems: 0,
        filters: {
            status: '',
            jurisdiction: ''
        },
        currentEntity: null
    };

    // List entities
    document.getElementById('list-entities-btn').addEventListener('click', () => {
        entityState.currentPage = 1;
        fetchEntities();
    });

    // Apply entity filters
    document.getElementById('apply-entity-filters').addEventListener('click', () => {
        entityState.filters.status = document.getElementById('entity-status-filter').value;
        entityState.filters.jurisdiction = document.getElementById('entity-jurisdiction-filter').value;
        entityState.currentPage = 1;
        fetchEntities();
    });

    // Fetch entity from GLEIF
    document.getElementById('fetch-entity-btn').addEventListener('click', () => {
        const lei = prompt('Enter LEI code to fetch from GLEIF:');
        if (lei && lei.trim()) {
            fetchEntityFromGLEIF(lei.trim());
        }
    });

    // Entity search
    document.getElementById('entity-search-btn').addEventListener('click', () => {
        const searchQuery = document.getElementById('entity-search').value.trim();
        if (searchQuery) {
            fetchEntityById(searchQuery);
        } else {
            showToast('Please enter an LEI to search', 'error');
        }
    });

    // Pagination for entities
    document.getElementById('entity-prev-page').addEventListener('click', () => {
        if (entityState.currentPage > 1) {
            entityState.currentPage--;
            fetchEntities();
        }
    });

    document.getElementById('entity-next-page').addEventListener('click', () => {
        const totalPages = Math.ceil(entityState.totalItems / entityState.pageSize);
        if (entityState.currentPage < totalPages) {
            entityState.currentPage++;
            fetchEntities();
        }
    });

    // Close entity detail view
    document.querySelector('#entity-detail-view .close-detail').addEventListener('click', () => {
        document.getElementById('entity-detail-view').style.display = 'none';
    });

    // Entity detail actions
    document.getElementById('refresh-entity-btn').addEventListener('click', () => {
        refreshEntityFromGLEIF(entityState.currentEntity.lei);
    });

    document.getElementById('delete-entity-btn').addEventListener('click', () => {
        showConfirmationModal(
            'Delete Legal Entity', 
            `Are you sure you want to delete legal entity ${entityState.currentEntity.lei}?`,
            () => deleteEntity(entityState.currentEntity.lei)
        );
    });

    // Batch operations
    document.getElementById('batch-create-btn').addEventListener('click', () => {
        const type = document.getElementById('batch-type').value;
        const isins = document.getElementById('batch-isins').value.trim().split(/\r?\n/).filter(Boolean);
        
        if (isins.length === 0) {
            showToast('Please enter at least one ISIN', 'error');
            return;
        }
        
        batchCreateInstruments(type, isins);
    });

    document.getElementById('batch-enrich-btn').addEventListener('click', () => {
        const isins = document.getElementById('batch-enrich-isins').value.trim().split(/\r?\n/).filter(Boolean);
        
        if (isins.length === 0) {
            showToast('Please enter at least one ISIN', 'error');
            return;
        }
        
        batchEnrichInstruments(isins);
    });

    // CFI decoder
    document.getElementById('decode-cfi-btn').addEventListener('click', () => {
        const cfiCode = document.getElementById('cfi-code-input').value.trim().toUpperCase();
        if (cfiCode.length !== 6) {
            showToast('CFI code must be 6 characters', 'error');
            return;
        }
        
        decodeCFI(cfiCode);
    });

    // Confirmation modal
    document.querySelector('.modal-close').addEventListener('click', () => {
        hideConfirmationModal();
    });

    document.getElementById('modal-cancel').addEventListener('click', () => {
        hideConfirmationModal();
    });

    // API Functions for Instruments
    async function fetchInstruments() {
        showSpinner();
        try {
            let url = `/api/v1/instruments?limit=${instrumentState.pageSize}&offset=${(instrumentState.currentPage - 1) * instrumentState.pageSize}`;
            
            if (instrumentState.filters.type) {
                url += `&type=${instrumentState.filters.type}`;
            }
            
            if (instrumentState.filters.currency) {
                url += `&currency=${instrumentState.filters.currency}`;
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                renderInstrumentsTable(data.instruments);
                instrumentState.totalItems = data.count;
                updatePaginationInfo('instruments', instrumentState.currentPage, instrumentState.pageSize, instrumentState.totalItems);
            } else {
                showToast(data.error || 'Failed to fetch instruments', 'error');
            }
        } catch (error) {
            console.error('Error fetching instruments:', error);
            showToast('An error occurred while fetching instruments', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function fetchInstrumentById(identifier) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${identifier}`);
            const data = await response.json();
            
            if (response.ok) {
                showInstrumentDetail(data);
            } else {
                showToast(data.error || 'Instrument not found', 'error');
            }
        } catch (error) {
            console.error('Error fetching instrument:', error);
            showToast('An error occurred while fetching the instrument', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function createInstrument(instrumentData) {
        showSpinner();
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
                showToast('Instrument created successfully', 'success');
                document.getElementById('instrument-form-container').style.display = 'none';
                fetchInstrumentById(data.id);
            } else {
                showToast(data.error || 'Failed to create instrument', 'error');
            }
        } catch (error) {
            console.error('Error creating instrument:', error);
            showToast('An error occurred while creating the instrument', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function updateInstrument(id, instrumentData) {
        showSpinner();
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
                showToast('Instrument updated successfully', 'success');
                document.getElementById('instrument-form-container').style.display = 'none';
                fetchInstrumentById(id);
            } else {
                showToast(data.error || 'Failed to update instrument', 'error');
            }
        } catch (error) {
            console.error('Error updating instrument:', error);
            showToast('An error occurred while updating the instrument', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function deleteInstrument(id) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${id}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Instrument deleted successfully', 'success');
                document.getElementById('instrument-detail-view').style.display = 'none';
                fetchInstruments();
            } else {
                showToast(data.error || 'Failed to delete instrument', 'error');
            }
        } catch (error) {
            console.error('Error deleting instrument:', error);
            showToast('An error occurred while deleting the instrument', 'error');
        } finally {
            hideSpinner();
            hideConfirmationModal();
        }
    }

    async function enrichInstrument(id) {
        showSpinner();
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
                
                showToast(message, 'success');
                fetchInstrumentById(id);
            } else {
                showToast(data.error || 'Failed to enrich instrument', 'error');
            }
        } catch (error) {
            console.error('Error enriching instrument:', error);
            showToast('An error occurred while enriching the instrument', 'error');
        } finally {
            hideSpinner();
        }
    }

    // API Functions for Legal Entities
    async function fetchEntities() {
        showSpinner();
        try {
            let url = `/api/v1/entities?limit=${entityState.pageSize}&offset=${(entityState.currentPage - 1) * entityState.pageSize}`;
            
            if (entityState.filters.status) {
                url += `&status=${entityState.filters.status}`;
            }
            
            if (entityState.filters.jurisdiction) {
                url += `&jurisdiction=${entityState.filters.jurisdiction}`;
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                renderEntitiesTable(data.entities);
                entityState.totalItems = data.count;
                updatePaginationInfo('entities', entityState.currentPage, entityState.pageSize, entityState.totalItems);
            } else {
                showToast(data.error || 'Failed to fetch entities', 'error');
            }
        } catch (error) {
            console.error('Error fetching entities:', error);
            showToast('An error occurred while fetching entities', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function fetchEntityById(lei) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/entities/${lei}`);
            const data = await response.json();
            
            if (response.ok) {
                showEntityDetail(data);
            } else {
                showToast(data.error || 'Legal entity not found', 'error');
            }
        } catch (error) {
            console.error('Error fetching entity:', error);
            showToast('An error occurred while fetching the legal entity', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function fetchEntityFromGLEIF(lei) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/entities/${lei}`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Legal entity fetched successfully from GLEIF', 'success');
                fetchEntityById(lei);
            } else {
                showToast(data.error || 'Failed to fetch legal entity', 'error');
            }
        } catch (error) {
            console.error('Error fetching entity from GLEIF:', error);
            showToast('An error occurred while fetching the legal entity', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function refreshEntityFromGLEIF(lei) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/entities/${lei}`, {
                method: 'PUT'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Legal entity refreshed successfully from GLEIF', 'success');
                fetchEntityById(lei);
            } else {
                showToast(data.error || 'Failed to refresh legal entity', 'error');
            }
        } catch (error) {
            console.error('Error refreshing entity from GLEIF:', error);
            showToast('An error occurred while refreshing the legal entity', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function deleteEntity(lei) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/entities/${lei}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showToast('Legal entity deleted successfully', 'success');
                document.getElementById('entity-detail-view').style.display = 'none';
                fetchEntities();
            } else {
                showToast(data.error || 'Failed to delete legal entity', 'error');
            }
        } catch (error) {
            console.error('Error deleting entity:', error);
            showToast('An error occurred while deleting the legal entity', 'error');
        } finally {
            hideSpinner();
            hideConfirmationModal();
        }
    }

    // API Functions for Batch Operations
    async function batchCreateInstruments(type, identifiers) {
        showSpinner();
        try {
            const response = await fetch('/api/v1/batch/instruments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    operation: 'create',
                    type: type,
                    identifiers: identifiers
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                renderBatchResults(data);
            } else {
                showToast(data.error || 'Batch operation failed', 'error');
            }
        } catch (error) {
            console.error('Error in batch operation:', error);
            showToast('An error occurred during the batch operation', 'error');
        } finally {
            hideSpinner();
        }
    }

    async function batchEnrichInstruments(identifiers) {
        showSpinner();
        try {
            const response = await fetch('/api/v1/batch/instruments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    operation: 'enrich',
                    identifiers: identifiers
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                renderBatchResults(data);
            } else {
                showToast(data.error || 'Batch operation failed', 'error');
            }
        } catch (error) {
            console.error('Error in batch operation:', error);
            showToast('An error occurred during the batch operation', 'error');
        } finally {
            hideSpinner();
        }
    }

    // API Function for CFI Decoding
    async function decodeCFI(cfiCode) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/cfi/${cfiCode}`);
            const data = await response.json();
            
            if (response.ok) {
                renderCFIResults(data);
            } else {
                showToast(data.error || 'Failed to decode CFI code', 'error');
            }
        } catch (error) {
            console.error('Error decoding CFI:', error);
            showToast('An error occurred while decoding the CFI code', 'error');
        } finally {
            hideSpinner();
        }
    }

    // Helper Function to update pagination info
    function updatePaginationInfo(type, currentPage, pageSize, totalItems) {
        const totalPages = Math.ceil(totalItems / pageSize);
        const startItem = ((currentPage - 1) * pageSize) + 1;
        const endItem = Math.min(currentPage * pageSize, totalItems);
        
        let pageInfoElem;
        if (type === 'instruments') {
            pageInfoElem = document.getElementById('page-info');
        } else {
            pageInfoElem = document.getElementById('entity-page-info');
        }
        
        if (pageInfoElem) {
            pageInfoElem.textContent = `Page ${currentPage} of ${totalPages} (${startItem}-${endItem} of ${totalItems})`;
        }
    }

    // Helper function for type-specific fields
    function updateTypeSpecificFields(type) {
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
    }

    // Helper function for edit form
    function prepareEditForm(instrument) {
        instrumentState.mode = 'edit';
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
        updateTypeSpecificFields(instrument.type);
        
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
    }

    // UI Rendering Functions
    function renderInstrumentsTable(instruments) {
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
            row.querySelector('.view').addEventListener('click', () => fetchInstrumentById(instrument.id));
            row.querySelector('.edit').addEventListener('click', () => fetchInstrumentForEdit(instrument.id));
            row.querySelector('.delete').addEventListener('click', () => {
                showConfirmationModal(
                    'Delete Instrument', 
                    `Are you sure you want to delete instrument ${instrument.isin}?`,
                    () => deleteInstrument(instrument.id)
                );
            });
            
            tbody.appendChild(row);
        });
    }

    async function fetchInstrumentForEdit(id) {
        showSpinner();
        try {
            const response = await fetch(`/api/v1/instruments/${id}`);
            const data = await response.json();
            
            if (response.ok) {
                prepareEditForm(data);
            } else {
                showToast(data.error || 'Instrument not found', 'error');
            }
        } catch (error) {
            console.error('Error fetching instrument for edit:', error);
            showToast('An error occurred while fetching the instrument', 'error');
        } finally {
            hideSpinner();
        }
    }

    function renderEntitiesTable(entities) {
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
            row.querySelector('.view').addEventListener('click', () => fetchEntityById(entity.lei));
            row.querySelector('.refresh').addEventListener('click', () => refreshEntityFromGLEIF(entity.lei));
            row.querySelector('.delete').addEventListener('click', () => {
                showConfirmationModal(
                    'Delete Legal Entity', 
                    `Are you sure you want to delete legal entity ${entity.lei}?`,
                    () => deleteEntity(entity.lei)
                );
            });
            
            tbody.appendChild(row);
        });
    }

    function renderBatchResults(data) {
        const batchResults = document.getElementById('batch-results');
        batchResults.style.display = 'block';
        
        document.getElementById('batch-total').textContent = data.total;
        document.getElementById('batch-success').textContent = data.successful;
        document.getElementById('batch-failed').textContent = data.failed;
        
        const successList = document.getElementById('batch-success-list');
        const failList = document.getElementById('batch-fail-list');
        
        successList.innerHTML = '';
        failList.innerHTML = '';
        
        data.results.successful.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.isin} - ${item.type}${item.figi ? ' (FIGI: ' + item.figi + ')' : ''}${item.lei ? ' (LEI: ' + item.lei + ')' : ''}`;
            successList.appendChild(li);
        });
        
        data.results.failed.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.isin} - ${item.error}`;
            failList.appendChild(li);
        });
    }

    function renderCFIResults(data) {
        const cfiResults = document.getElementById('cfi-results');
        cfiResults.style.display = 'block';
        
        const cfiDetail = document.getElementById('cfi-detail');
        cfiDetail.innerHTML = '';
        
        // Main classification
        const mainSection = document.createElement('div');
        mainSection.classList.add('cfi-section');
        mainSection.innerHTML = `
            <h4>Basic Classification</h4>
            <div class="detail-row">
                <span class="detail-label">CFI Code:</span>
                <span>${data.cfi_code}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Category:</span>
                <span>${data.category} - ${data.category_description}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Group:</span>
                <span>${data.group} - ${data.group_description}</span>
            </div>
        `;
        cfiDetail.appendChild(mainSection);
        
        // Attributes
        if (data.attributes && typeof data.attributes === 'object') {
            const attrSection = document.createElement('div');
            attrSection.classList.add('cfi-section');
            attrSection.innerHTML = '<h4>Attributes</h4>';
            
            for (const [key, value] of Object.entries(data.attributes)) {
                const row = document.createElement('div');
                row.classList.add('detail-row');
                
                const formattedKey = key.replace(/_/g, ' ')
                    .replace(/\b\w/g, l => l.toUpperCase());
                
                row.innerHTML = `
                    <span class="detail-label">${formattedKey}:</span>
                    <span>${value}</span>
                `;
                attrSection.appendChild(row);
            }
            
            cfiDetail.appendChild(attrSection);
        }
    }

    function showInstrumentDetail(instrument) {
        instrumentState.currentInstrument = instrument;
        
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
                'First Trade Date': instrument.first_trade_date ? formatDate(instrument.first_trade_date) : '-'
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
                    'Maturity Date': formatDate(instrument.debt_attributes.maturity_date),
                    'Nominal Value': instrument.debt_attributes.nominal_value_per_unit || '-',
                    'Total Issued Nominal': instrument.debt_attributes.total_issued_nominal || '-',
                    'Debt Seniority': instrument.debt_attributes.debt_seniority || '-'
                }
            });
        } else if (instrument.type === 'future' && instrument.future_attributes) {
            sections.push({
                title: 'Future Specific Attributes',
                fields: {
                    'Expiration Date': formatDate(instrument.future_attributes.expiration_date),
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

    function showEntityDetail(entity) {
        entityState.currentEntity = entity;
        
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
                <span>${entity.creation_date ? formatDate(entity.creation_date) : '-'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Next Renewal:</span>
                <span>${entity.next_renewal_date ? formatDate(entity.next_renewal_date) : '-'}</span>
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
                    <span>${entity.registration.last_update ? formatDate(entity.registration.last_update) : '-'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Next Renewal:</span>
                    <span>${entity.registration.next_renewal ? formatDate(entity.registration.next_renewal) : '-'}</span>
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

    // Utility Functions
    function formatDate(dateString) {
        if (!dateString) return '-';
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString(undefined, {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch (error) {
            console.error('Error formatting date:', dateString, error);
            return dateString;
        }
    }

    function showSpinner() {
        document.getElementById('admin-spinner').style.display = 'block';
    }

    function hideSpinner() {
        document.getElementById('admin-spinner').style.display = 'none';
    }

    function showToast(message, type = 'info') {
        const toast = document.getElementById('admin-toast');
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            toast.className = 'toast';
        }, 3000);
    }

    function showConfirmationModal(title, message, confirmCallback) {
        const modal = document.getElementById('confirmation-modal');
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-message').textContent = message;
        
        // Set up confirm button action
        const confirmBtn = document.getElementById('modal-confirm');
        
        // Remove any existing event listeners
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        // Add new event listener
        newConfirmBtn.addEventListener('click', confirmCallback);
        
        // Show modal
        modal.style.display = 'flex';
    }

    function hideConfirmationModal() {
        document.getElementById('confirmation-modal').style.display = 'none';
    }

    // Initialize page
    function init() {
        // Set default active tab
        document.querySelector('.admin-tab[data-tab="instruments"]').click();
        
        // Load initial data
        fetchInstruments();
    }
    
    // Start the application
    init();
});
