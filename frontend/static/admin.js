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
            
            // Initialize FileManager only when Files tab is clicked
            if (tabName === 'files' && window.fileManager) {
                window.fileManager.init();
            }
        });
    });
    
    // Initialize all modules
    AdminUtils.init();
    AdminInstruments.init();
    AdminLegalEntities.init();
    AdminBatch.init();
    AdminCFI.init();
    
    console.log('Admin modules initialized');
    // Note: FileManager is initialized separately in admin_files.js
});

// Shared utility functions across modules
const AdminUtils = {
    init() {
        // Set up confirmation modal only if elements exist
        const modalClose = document.querySelector('.modal-close');
        if (modalClose) {
            modalClose.addEventListener('click', () => {
                this.hideConfirmationModal();
            });
        }

        const modalCancel = document.getElementById('modal-cancel');
        if (modalCancel) {
            modalCancel.addEventListener('click', () => {
                this.hideConfirmationModal();
            });
        }
    },
    
    showSpinner() {
        document.getElementById('admin-spinner').style.display = 'block';
    },

    hideSpinner() {
        document.getElementById('admin-spinner').style.display = 'none';
    },

    showToast(message, type = 'info') {
        const toast = document.getElementById('admin-toast');
        if (!toast) {
            console.log(`Toast: ${message}`);
            return;
        }
        
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        // Auto hide after configured duration
        const duration = (typeof APP_CONFIG !== 'undefined' && APP_CONFIG.TOAST_DURATION) ? APP_CONFIG.TOAST_DURATION : 3000;
        setTimeout(() => {
            toast.className = 'toast';
        }, duration);
    },

    showConfirmationModal(title, message, confirmCallback) {
        const modal = document.getElementById('confirmation-modal');
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-message').textContent = message;
        
        // Remove any existing event listeners
        const confirmBtn = document.getElementById('modal-confirm');
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        // Add new event listener
        newConfirmBtn.addEventListener('click', confirmCallback);
        
        // Show modal
        modal.style.display = 'flex';
    },

    hideConfirmationModal() {
        document.getElementById('confirmation-modal').style.display = 'none';
    },

    formatDate(dateString) {
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
    },

    updatePaginationInfo(type, currentPage, pageSize, totalItems) {
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
};
