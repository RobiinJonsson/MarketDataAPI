async function getIsinByFigi(figi) {
    try {
        const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.FIGI}/${figi}`);
        const response = await fetch(url);
        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        return data.ISIN;
    } catch (error) {
        console.error('Error looking up ISIN by FIGI:', error);
        throw error;
    }
}

async function searchBySchema() {
    console.log('searchBySchema function called'); // Debug log
    const identifier = document.getElementById("identifier-input").value;
    const identifierType = document.getElementById("identifier-type").value;
    const schemaFile = document.getElementById("schema-file").files[0];
    
    // Fix: Check if schema-type element exists before trying to read its value
    let schemaType = 'base';
    const schemaTypeElement = document.getElementById("schema-type");
    if (schemaTypeElement) {
        schemaType = schemaTypeElement.value || 'base';
    }

    console.log('Form values:', { identifier, identifierType, schemaType, hasFile: !!schemaFile }); // Debug log

    if (!identifier || !identifierType || !schemaFile) {
        alert("Please fill in all fields and upload a schema file");
        return;
    }

    try {
        const schemaText = await schemaFile.text();
        let searchIdentifier = identifier;
        
        if (identifierType === 'FIGI') {
            try {
                searchIdentifier = await getIsinByFigi(identifier);
            } catch (error) {
                alert(`Error looking up ISIN for FIGI ${identifier}: ${error.message}`);
                return;
            }
        }

        const payload = {
            filters: {
                identifier: searchIdentifier
            },
            schema_type: schemaType,  // Use the selected schema type
            format: 'json'
        };        document.getElementById("spinner").style.display = "block";

        const url = `/api/schema/search`;
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        document.getElementById("spinner").style.display = "none";

        if (data.error) {
            throw new Error(data.error);
        }

        // Display results
        displaySchemaResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error performing schema search: ' + error.message);
        document.getElementById("spinner").style.display = "none";
    }
}

function displaySchemaResults(data) {
    const schemaOutput = document.getElementById("schema-output");
    schemaOutput.textContent = JSON.stringify(data.results, null, 2);

    // Update unmapped fields display if available
    const unmappedFieldsOutput = document.getElementById("unmapped-fields");
    if (data.unmapped_fields && data.unmapped_fields.length > 0) {
        unmappedFieldsOutput.textContent = JSON.stringify({
            unmapped_fields: data.unmapped_fields,
            count: data.unmapped_fields.length
        }, null, 2);
    } else {
        unmappedFieldsOutput.textContent = '';
    }
}

// Add example schema loading
async function loadExampleSchema() {
    try {        // Update path to match where we store our example schemas
        const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.SCHEMAS}/examples/frontend_equity.yaml`);
        const response = await fetch(url);
        const schemaText = await response.text();
        
        // Create a file object from the schema text
        const file = new File([schemaText], 'frontend_equity.yaml', {
            type: 'application/x-yaml'
        });
        
        // Set the file in the file input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.getElementById('schema-file').files = dataTransfer.files;
        
        // Trigger the change event
        document.getElementById('schema-file').dispatchEvent(new Event('change'));
        
        // Show success message
        const fileNameDisplay = document.querySelector('.file-name-display');
        fileNameDisplay.textContent = 'Example schema loaded: frontend_equity.yaml';
        fileNameDisplay.style.display = 'block';
    } catch (error) {
        console.error('Error loading example schema:', error);
        alert('Failed to load example schema. Please try uploading manually.');
    }
}

// Copy of formatDate for schema functionality
function formatDateSchema(dateString) {
    if (!dateString || dateString === 'None') return 'N/A';
    try {
        return new Date(dateString).toLocaleString();
    } catch (e) {
        console.warn('Date parsing error:', e);
        return dateString;
    }
}

// Add a function to populate the schema type dropdown
async function populateSchemaTypes() {    try {
        const url = buildApiUrl(APP_CONFIG.ENDPOINTS.SCHEMAS);
        const response = await fetch(url);
        const data = await response.json();
        
        const schemaTypeSelect = document.getElementById("schema-type");
        if (!schemaTypeSelect) return;
        
        // Add base option
        const baseOption = document.createElement("option");
        baseOption.value = "base";
        baseOption.textContent = "Base";
        schemaTypeSelect.appendChild(baseOption);
        
        // Add available schemas
        if (data && Array.isArray(data)) {
            data.forEach(schema => {
                const option = document.createElement("option");
                option.value = schema.name;
                option.textContent = schema.name;
                schemaTypeSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Error loading schema types:", error);
    }
}

// Schema-specific initialization
document.addEventListener('DOMContentLoaded', function() {
    const schemaFileInput = document.getElementById('schema-file');
    const searchButton = document.querySelector('.schema-search-form button[type="submit"]');
    
    if (schemaFileInput && searchButton) {
        schemaFileInput.addEventListener('change', function() {
            // Create or update the filename display
            let fileNameDisplay = document.querySelector('.file-name-display');
            if (!fileNameDisplay) {
                fileNameDisplay = document.createElement('div');
                fileNameDisplay.className = 'file-name-display';
                this.parentNode.appendChild(fileNameDisplay);
            }
            
            if (this.files.length) {
                fileNameDisplay.textContent = `Selected file: ${this.files[0].name}`;
                fileNameDisplay.style.display = 'block';
                searchButton.disabled = false;
            } else {
                fileNameDisplay.style.display = 'none';
                searchButton.disabled = true;
            }
        });
        
        // Add direct click handler to search button
        searchButton.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent form submission
            console.log('Search button clicked'); // Debug log
            searchBySchema();
        });
    }
    
    // Add event listener for the form submission
    const searchForm = document.querySelector('.schema-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent default form submission
            console.log('Schema search form submitted'); // Debug log
            searchBySchema();
        });
    } else {
        console.error('Schema search form not found');
    }
    
    // Only try to populate schema types if the dropdown exists
    const schemaTypeElement = document.getElementById("schema-type");
    if (schemaTypeElement) {
        populateSchemaTypes();
    } else {
        console.warn("Schema type dropdown not found, using default 'base' schema");
        // If the dropdown doesn't exist in the HTML, we might need to create it
        // or we can just use the default 'base' schema
    }
});