const AdminBatch = {
    init() {
        // Batch operations
        document.getElementById('batch-create-btn').addEventListener('click', () => {
            const type = document.getElementById('batch-type').value;
            const isins = document.getElementById('batch-isins').value.trim().split(/\r?\n/).filter(Boolean);
            
            if (isins.length === 0) {
                AdminUtils.showToast('Please enter at least one ISIN', 'error');
                return;
            }
            
            this.batchCreateInstruments(type, isins);
        });

        document.getElementById('batch-enrich-btn').addEventListener('click', () => {
            const isins = document.getElementById('batch-enrich-isins').value.trim().split(/\r?\n/).filter(Boolean);
            
            if (isins.length === 0) {
                AdminUtils.showToast('Please enter at least one ISIN', 'error');
                return;
            }
            
            this.batchEnrichInstruments(isins);
        });
    },
    
    // API Functions for Batch Operations
    async batchCreateInstruments(type, identifiers) {
        AdminUtils.showSpinner();
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
                this.renderBatchResults(data);
            } else {
                AdminUtils.showToast(data.error || 'Batch operation failed', 'error');
            }
        } catch (error) {
            console.error('Error in batch operation:', error);
            AdminUtils.showToast('An error occurred during the batch operation', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },

    async batchEnrichInstruments(identifiers) {
        AdminUtils.showSpinner();
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
                this.renderBatchResults(data);
            } else {
                AdminUtils.showToast(data.error || 'Batch operation failed', 'error');
            }
        } catch (error) {
            console.error('Error in batch operation:', error);
            AdminUtils.showToast('An error occurred during the batch operation', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },
    
    // UI Rendering Functions
    renderBatchResults(data) {
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
};
