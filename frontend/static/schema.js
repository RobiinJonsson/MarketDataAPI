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
        // Read the schema file
        const schemaText = await schemaFile.text();
        
        let searchIdentifier = identifier;
        
        // If identifier type is FIGI, look up the corresponding ISIN
        if (identifierType === 'FIGI') {
            try {
                searchIdentifier = await getIsinByFigi(identifier);
                console.log(`Found ISIN ${searchIdentifier} for FIGI ${identifier}`);
            } catch (error) {
                alert(`Error looking up ISIN for FIGI ${identifier}: ${error.message}`);
                return;
            }
        }
        
        // Create the request payload
        const payload = {
            filters: {
                identifier: searchIdentifier,
                identifier_type: 'ISIN'  // Always use ISIN for the actual search
            },
            schema: schemaText
        };

        // Show loading spinner
        document.getElementById("spinner").style.display = "block";

        // Make the API request
        const response = await fetch("/api/schema/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Hide loading spinner
        document.getElementById("spinner").style.display = "none";

        // Display results
        const schemaOutput = document.getElementById("schema-output");
        schemaOutput.textContent = JSON.stringify(data.results, null, 2);

        // Display unmapped fields
        const unmappedFieldsOutput = document.getElementById("unmapped-fields");
        if (data.unmapped_fields && data.unmapped_fields.length > 0) {
            unmappedFieldsOutput.textContent = JSON.stringify({
                unmapped_fields: data.unmapped_fields,
                count: data.unmapped_fields.length
            }, null, 2);
        } else {
            unmappedFieldsOutput.textContent = JSON.stringify({
                unmapped_fields: [],
                count: 0
            }, null, 2);
        }

        // Also update the main results table
        const table = document.getElementById("results-table");
        table.innerHTML = `
            <thead>
                <tr>
                    <th>ISIN</th>
                    <th>Full Name</th>
                    <th>Short Name</th>
                    <th>CFI Code</th>
                    <th>Currency</th>
                    <th>Issuer LEI</th>
                    <th>Trading Venue</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;

        if (data.results && data.results.length > 0) {
            const tbody = table.querySelector('tbody');
            data.results.forEach(result => {
                const row = `
                    <tr>
                        <td>${result.identifier || 'N/A'}</td>
                        <td>${result.full_name || 'N/A'}</td>
                        <td>${result.short_name || 'N/A'}</td>
                        <td>${result.classification_type || 'N/A'}</td>
                        <td>${result.currency || 'N/A'}</td>
                        <td>${result.issuer_lei || 'N/A'}</td>
                        <td>${result.trading_venue_id || 'N/A'}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        } else {
            table.querySelector('tbody').innerHTML = `
                <tr><td colspan="7">No results found</td></tr>
            `;
        }

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while performing the schema search');
        document.getElementById("spinner").style.display = "none";
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