// Add at the beginning of the file
function switchTab(tabName) {
    // Update tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase() === tabName) {
            btn.classList.add('active');
        }
    });

    // Update tab panes
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
        if (pane.id === `${tabName}-tab`) {
            pane.classList.add('active');
        }
    });
}

function fetchMarketData() {
    let ticker = document.getElementById("ticker").value;
    fetch(`/marketdata/${ticker}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error("Error fetching market data:", error));
}

async function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Please upload a .txt file with ISINs.");
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("/batch_search", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    console.log("Batch search response:", data);

    let tableBody = document.getElementById("batchResultsBody");
    tableBody.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="4">No results found</td></tr>`;
        return;
    }

    data.forEach(entry => {
        if (!entry.data || entry.data.length === 0) {
            return;
        }

        let row = `<tr>
            <td>${entry.data[0]?.figi || "N/A"}</td>
            <td>${entry.data[0]?.ticker || "N/A"}</td>
            <td>${entry.data[0]?.name || "N/A"}</td>
            <td>${entry.data[0]?.exchCode || "N/A"}</td>
            <td>${entry.data[0]?.marketSector || "N/A"}</td>
            <td>${entry.data[0]?.securityType || "N/A"}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

async function searchSecurity() {
    let query = document.getElementById("searchInput").value;
    if (!query) {
        alert("Please enter an ISIN or security description.");
        return;
    }

    console.log("Sending request with:", query);  // ✅ Debugging output

    let response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    let data = await response.json();
    console.log("Received response:", data);  // ✅ Debugging output

    let tableBody = document.getElementById("resultsBody");
    tableBody.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="3">No results found</td></tr>`;
        return;
    }

    data.forEach(entry => {
        if (!entry.data || entry.data.length === 0) {
            return;
        }

        let row = `<tr>
            <td>${entry.data[0]?.input_isin}</td>  <!-- ✅ Show input ISIN -->
            <td>${entry.data[0]?.figi || "N/A"}</td>  <!-- ✅ Added FIGI column -->
            <td>${entry.data[0]?.ticker || "N/A"}</td>
            <td>${entry.data[0]?.name || "N/A"}</td>
            <td>${entry.data[0]?.exchCode || "N/A"}</td>
            <td>${entry.data[0]?.marketSector || "N/A"}</td>
            <td>${entry.data[0]?.securityType || "N/A"}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const firdsForm = document.getElementById('firds-form');
    if (firdsForm) {  // Only add listener if element exists
        firdsForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const date = document.getElementById('date').value;
            const filePrefix = document.getElementById('file_prefix').value;

            // Send the data via AJAX (POST request)
            fetch('/firds', {
                method: 'POST',
                body: new URLSearchParams({
                    'date': date,
                    'file_prefix': filePrefix
                }),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',  // Correct content type for form submission
                    'X-Requested-With': 'XMLHttpRequest'  // Marks the request as an AJAX request
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Received data:', data);
            
                // Clear the previous list
                const fileList = document.getElementById('file-list');
                fileList.innerHTML = '';
            
                // Display the file names in the list
                if (data.file_names && data.file_names.length > 0) {
                    data.file_names.forEach(file => {
                        const li = document.createElement('li');
                        li.textContent = file;
                        fileList.appendChild(li);
                    });
                } else {
                    fileList.innerHTML = '<li>No files found for the given criteria.</li>';
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
        });
    }
});

function renderTable(data) {
    const head = document.getElementById("tableHead");
    const body = document.getElementById("tableBody");
    head.innerHTML = "";
    body.innerHTML = "";
  
    if (!data || data.length === 0) {
      body.innerHTML = "<tr><td colspan='100%'>No data found</td></tr>";
      return;
    }
  
    const isArray = Array.isArray(data);
    const firstItem = isArray ? data[0] : data;
  
    const columns = Object.keys(firstItem);
    head.innerHTML = `<tr>${columns.map(col => `<th>${col}</th>`).join('')}</tr>`;
  
    const rows = isArray ? data : [data];
    rows.forEach(item => {
      const row = `<tr>${columns.map(col => `<td>${item[col] || ""}</td>`).join('')}</tr>`;
      body.innerHTML += row;
    });
  }
  
// Replace the searchByIsin function
async function searchAndDisplay() {
    const isin = document.getElementById("isin-input").value;
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }

    try {
        document.getElementById("spinner").style.display = "block";
        console.log("Fetching data for ISIN:", isin);
        
        const response = await fetch(`/api/search/${isin}`);
        const data = await response.json();
        console.log("Raw response data:", data);

        if (!response.ok) {
            showError(data.message || "Error fetching data");
            return;
        }

        if (!data || (!data.equity && !data.debt && !data.figi)) {
            showError("No data found for this ISIN");
            return;
        }

        // Debug log of section data
        console.log("Equity data:", data.equity);
        console.log("Debt data:", data.debt);
        console.log("FIGI data:", data.figi);

        // Organize data into sections
        const sections = {
            instrumentDetails: {
                "ISIN": data.equity?.ISIN || data.debt?.ISIN || 'N/A',
                "Type": data.equity ? 'Equity' : 'Debt',
                "Full Name": data.equity?.FullName || data.debt?.FullName || 'N/A',
                "Short Name": data.equity?.ShortName || data.debt?.ShortName || 'N/A',
                "CFI Code": data.equity?.CFICode || data.debt?.CFICode || 'N/A',
                "Currency": data.equity?.Currency || data.debt?.Currency || 'N/A',
                "First Trade Date": formatDate(data.equity?.FirstTradeDate || data.debt?.FirstTradeDate) || 'N/A',
                "FIGI": data.figi?.FIGI || 'N/A',
                "Security Type": data.figi?.SecurityType || 'N/A',
                "Market Sector": data.figi?.MarketSector || 'N/A'
            },
            issuerData: {
                "Issuer LEI": data.equity?.IssuerLEI || data.debt?.IssuerLEI || 'N/A',
                "Issuer Required": String(data.equity?.IssuerReq || data.debt?.IssuerReq) === 'true' ? 'Yes' : 'No',
                "Market Sector": data.figi?.MarketSector || 'N/A',
                "Security Description": data.figi?.SecurityDescription || 'N/A'
            },
            tradingVenue: {
                "Trading Venue": data.equity?.TradingVenueId || data.debt?.TradingVenueId || 'N/A',
                "Relevant Trading Venue": data.equity?.RelevantTradingVenue || data.debt?.RelevantTradingVenue || 'N/A',
                "Relevant Authority": data.equity?.RlvntCmptntAuthrty || data.debt?.RlvntCmptntAuthrty || 'N/A',
                "Ticker": data.figi?.Ticker || 'N/A'
            },
            underlyingInstruments: {
                "Underlying Instrument": data.equity?.UnderlyingInstrm === 'None' ? 'N/A' : (data.equity?.UnderlyingInstrm || 'N/A'),
                "Commodity Derivative": String(data.equity?.ComdtyDerInd || data.debt?.ComdtyDerInd) === 'true' ? 'Yes' : 'No'
            }
        };

        console.log("Organized sections:", sections);

        // Update each section
        Object.entries(sections).forEach(([sectionId, sectionData]) => {
            // Convert camelCase to kebab-case for IDs
            const elementId = sectionId.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
            const sectionContent = document.querySelector(`#${elementId} .section-content`);
            if (!sectionContent) {
                console.error(`Section content not found for ${elementId}`);
                return;
            }
            console.log(`Updating section ${elementId}:`, sectionData);
            
            const htmlContent = Object.entries(sectionData)
                .map(([label, value]) => `
                    <div class="field-row">
                        <div class="label">${label}:</div>
                        <div class="value">${value}</div>
                    </div>
                `).join('');
            
            sectionContent.innerHTML = htmlContent;
        });

        // Show overview tab
        switchTab('overview');
        
    } catch (error) {
        console.error('Error in searchAndDisplay:', error);
        showError('An error occurred while fetching the data');
    } finally {
        document.getElementById("spinner").style.display = "none";
    }
}

// Helper function for formatting dates
function formatDate(dateString) {
    if (!dateString || dateString === 'None') return 'N/A';
    try {
        return new Date(dateString).toLocaleString();
    } catch (e) {
        console.warn('Date parsing error:', e);
        return dateString;
    }
}

function showError(message) {
    const sections = ['instrument-details', 'issuer-data', 'trading-venue', 'underlying-instruments'];
    sections.forEach(section => {
        const sectionContent = document.querySelector(`#${section} .section-content`);
        if (sectionContent) {
            sectionContent.innerHTML = `<div class="error-message">${message}</div>`;
        }
    });
    document.getElementById("spinner").style.display = "none";
}

async function addISIN() {
    const isin = document.getElementById("isinInput").value;
    const res = await fetch(`/api/add/${isin}`, { method: "POST" });
    const msg = await res.json();
    alert(msg.message);
}

async function fetchAndInsert() {
    const isin = document.getElementById("isin-input").value;
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }

    try {
        // Show loading spinner
        document.getElementById("spinner").style.display = "block";

        const response = await fetch('/api/fetch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                identifier: isin,
                identifier_type: 'ISIN'
            })
        });

        const result = await response.json();
        
        // Hide loading spinner
        document.getElementById("spinner").style.display = "none";
        
        if (response.ok) {
            // Show success message with instrument type
            const instrumentType = result.instrument_type || 'equity';
            const toast = document.getElementById("toast");
            toast.textContent = `${result.message} (${instrumentType} instrument)`;
            toast.className = "toast success show";
            setTimeout(() => toast.className = "toast", 3000);
            
            // Refresh the table to show the new data
            searchAndDisplay();
        } else {
            const toast = document.getElementById("toast");
            toast.textContent = result.error || 'Failed to fetch and insert data';
            toast.className = "toast error show";
            setTimeout(() => toast.className = "toast", 3000);
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("spinner").style.display = "none";
        const toast = document.getElementById("toast");
        toast.textContent = 'An error occurred while processing your request';
        toast.className = "toast error show";
        setTimeout(() => toast.className = "toast", 3000);
    }
}

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

// Add this at the end of the file
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener for schema file input
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