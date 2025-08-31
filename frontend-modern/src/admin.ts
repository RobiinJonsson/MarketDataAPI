import './styles/main.css';
import { instrumentApi, transparencyApi, fileApi } from './utils/api.js';
import { showToast, showLoading, showError, formatDate } from './utils/helpers.js';
import type { CreateInstrumentRequest } from './types/api.js';

// Initialize the admin application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  console.log('MarketData Admin initialized');
  
  initializeTabs();
  initializeInstrumentForm();
  initializeTransparencyForm();
  initializeFileUpload();
  initializeButtons();
});

function initializeTabs(): void {
  const tabButtons = document.querySelectorAll('[data-tab]');
  const tabPanes = document.querySelectorAll('[data-tab-pane]');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabName = button.getAttribute('data-tab');
      
      // Update active tab button
      tabButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      
      // Update active tab pane
      tabPanes.forEach(pane => {
        pane.classList.remove('active');
        pane.classList.add('hidden');
        if (pane.getAttribute('data-tab-pane') === tabName) {
          pane.classList.add('active');
          pane.classList.remove('hidden');
        }
      });
    });
  });
}

function initializeInstrumentForm(): void {
  const form = document.getElementById('create-instrument-form') as HTMLFormElement;
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const isin = formData.get('isin') as string;
    const type = formData.get('instrument_type') as string;
    const fetchAndEnrich = formData.get('fetch_and_enrich');

    // Build payload as in old frontend
    const payload: any = {
      isin,
      type
    };
    if (fetchAndEnrich) {
      payload.fetch_and_enrich = true;
    }

    const submitButton = form.querySelector('button[type="submit"]') as HTMLButtonElement;
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Creating...';
    submitButton.disabled = true;

    try {
      const response = await instrumentApi.create(payload);
      if (response.status === 'success') {
        showToast('Instrument created and enriched successfully!', 'success');
        form.reset();
        loadInstruments();
      } else {
        showToast(response.error || 'Failed to create instrument', 'error');
      }
    } catch (error) {
      showToast('Network error occurred', 'error');
    } finally {
      submitButton.textContent = originalText;
      submitButton.disabled = false;
    }
  });

  // Enrichment logic
  async function enrichInstrument(isin: string) {
    try {
      const res = await fetch(`/api/v1/instruments/${encodeURIComponent(isin)}/enrich`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        return { status: 'error', error: err.error || `HTTP ${res.status}` };
      }
      const data = await res.json();
      return { status: 'success', data };
    } catch (error) {
      return { status: 'error', error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }
}

function initializeTransparencyForm(): void {
  const form = document.getElementById('batch-transparency-form') as HTMLFormElement;
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    const data = {
      calculation_type: formData.get('calculation_type'),
      isin_prefix: formData.get('isin_prefix') || undefined,
      limit: parseInt(formData.get('limit') as string) || 10,
    };

    const submitButton = form.querySelector('button[type="submit"]') as HTMLButtonElement;
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Processing...';
    submitButton.disabled = true;

    try {
      const response = await transparencyApi.batch(data);
      
      if (response.status === 'success') {
        showToast(`Successfully created ${response.data?.created_count || 0} transparency calculations`, 'success');
        form.reset();
      } else {
        showToast(response.error || 'Failed to create transparency batch', 'error');
      }
    } catch (error) {
      showToast('Network error occurred', 'error');
    } finally {
      submitButton.textContent = originalText;
      submitButton.disabled = false;
    }
  });
}

function initializeFileUpload(): void {
  const fileInput = document.getElementById('file-upload') as HTMLInputElement;
  const dropZone = fileInput?.closest('.border-dashed');
  
  if (!fileInput || !dropZone) return;

  // Handle file selection
  fileInput.addEventListener('change', handleFileUpload);
  
  // Handle drag and drop
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-primary-400', 'bg-primary-50');
  });
  
  dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-primary-400', 'bg-primary-50');
  });
  
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-primary-400', 'bg-primary-50');
    
    const dragEvent = e as DragEvent;
    const files = dragEvent.dataTransfer?.files;
    if (files) {
      fileInput.files = files;
      handleFileUpload();
    }
  });
}

async function handleFileUpload(): Promise<void> {
  const fileInput = document.getElementById('file-upload') as HTMLInputElement;
  const files = fileInput.files;
  
  if (!files || files.length === 0) return;

  for (const file of files) {
    try {
      showToast(`Uploading ${file.name}...`, 'info');
      
      // Determine file type based on extension
      const extension = file.name.split('.').pop()?.toLowerCase();
      let fileType = 'unknown';
      
      if (extension === 'csv') fileType = 'csv';
      else if (extension === 'xml') fileType = 'xml';
      else if (extension === 'zip') fileType = 'zip';
      
      const response = await fileApi.upload(file, fileType);
      
      if (response.status === 'success') {
        showToast(`${file.name} uploaded successfully`, 'success');
      } else {
        showToast(`Failed to upload ${file.name}: ${response.error}`, 'error');
      }
    } catch (error) {
      showToast(`Error uploading ${file.name}`, 'error');
    }
  }
  
  // Clear the input
  fileInput.value = '';
  loadFiles(); // Refresh file list
}

function initializeButtons(): void {
  // Refresh instruments button
  const refreshInstrumentsBtn = document.getElementById('refresh-instruments');
  refreshInstrumentsBtn?.addEventListener('click', loadInstruments);
  
  // Refresh files button
  const refreshFilesBtn = document.getElementById('refresh-files');
  refreshFilesBtn?.addEventListener('click', loadFiles);
}

async function loadInstruments(): Promise<void> {
  const container = document.getElementById('instruments-list');
  if (!container) return;

  showLoading(container, 'Loading instruments...');
  
  const response = await instrumentApi.getAll();
  
  if (response.status === 'error') {
    showError(container, response.error || 'Failed to load instruments');
    return;
  }

  const instruments = response.data || [];
  
  if (instruments.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center text-gray-500">
        No instruments found. Create your first instrument using the form above.
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISIN</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          ${instruments.map(instrument => `
            <tr>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">${instrument.isin}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.symbol || '-'}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.name || '-'}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${instrument.instrument_type || '-'}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${formatDate(instrument.created_at)}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button onclick="deleteInstrument('${instrument.id}')" class="text-red-600 hover:text-red-900">Delete</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

async function loadFiles(): Promise<void> {
  const container = document.getElementById('files-list');
  if (!container) return;

  showLoading(container, 'Loading files...');
  
  const response = await fileApi.list();
  
  if (response.status === 'error') {
    showError(container, response.error || 'Failed to load files');
    return;
  }

  const files = response.data || [];
  
  if (files.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center text-gray-500">
        No files found. Upload files using the form above.
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="space-y-3">
      ${files.map(file => `
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-900">${file.filename || file.name}</p>
              <p class="text-sm text-gray-500">${formatDate(file.created_at || new Date().toISOString())}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button onclick="processFile('${file.filename || file.name}')" class="btn btn-primary btn-sm">Process</button>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// Global functions for button handlers
(window as any).deleteInstrument = async (id: string) => {
  if (!confirm('Are you sure you want to delete this instrument?')) return;
  
  const response = await instrumentApi.delete(id);
  
  if (response.status === 'success') {
    showToast('Instrument deleted successfully', 'success');
    loadInstruments();
  } else {
    showToast(response.error || 'Failed to delete instrument', 'error');
  }
};

(window as any).processFile = async (filename: string) => {
  const response = await fileApi.process(filename);
  
  if (response.status === 'success') {
    showToast(`File ${filename} processed successfully`, 'success');
  } else {
    showToast(`Failed to process ${filename}: ${response.error}`, 'error');
  }
};
