async function getIsinByFigi(figi) {
    try {
        const response = await fetch(`/api/figi/${figi}`);
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
    const identifier = document.getElementById("identifier-input").value;
    const identifierType = document.getElementById("identifier-type").value;
    const schemaFile = document.getElementById("schema-file").files[0];

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
            schema_type: 'equity',  // Use the schema type from the uploaded file
            format: 'json'
        };

        document.getElementById("spinner").style.display = "block";

        const response = await fetch("/api/schema/search", {
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

    // Update results table with dynamic fields based on schema
    const table = document.getElementById("results-table");
    if (data.results && data.results.length > 0) {
        const result = data.results[0];
        const fields = Object.keys(result);
        
        // Create table headers based on fields
        table.innerHTML = `
            <thead>
                <tr>
                    ${fields.map(field => `<th>${field}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        // Add data rows
        const tbody = table.querySelector('tbody');
        data.results.forEach(result => {
            const row = `
                <tr>
                    ${fields.map(field => `<td>${result[field] || 'N/A'}</td>`).join('')}
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } else {
        table.innerHTML = `<tr><td>No results found</td></tr>`;
    }
}

// Add example schema loading
async function loadExampleSchema() {
    try {
        // Update path to match where we store our example schemas
        const response = await fetch('/api/schema/examples/frontend_equity.yaml');
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
    }
});