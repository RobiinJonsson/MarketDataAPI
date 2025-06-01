const AdminCFI = {
    init() {
        // CFI decoder
        document.getElementById('decode-cfi-btn').addEventListener('click', () => {
            const cfiCode = document.getElementById('cfi-code-input').value.trim().toUpperCase();
            if (cfiCode.length !== 6) {
                AdminUtils.showToast('CFI code must be 6 characters', 'error');
                return;
            }
            
            this.decodeCFI(cfiCode);
        });
    },
    
    // API Function for CFI Decoding
    async decodeCFI(cfiCode) {
        AdminUtils.showSpinner();        try {
            const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.CFI}/${cfiCode}`);
            const response = await fetch(url);
            const data = await response.json();
            
            if (response.ok) {
                this.renderCFIResults(data);
            } else {
                AdminUtils.showToast(data.error || 'Failed to decode CFI code', 'error');
            }
        } catch (error) {
            console.error('Error decoding CFI:', error);
            AdminUtils.showToast('An error occurred while decoding the CFI code', 'error');
        } finally {
            AdminUtils.hideSpinner();
        }
    },
    
    // UI Rendering Function
    renderCFIResults(data) {
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
};
