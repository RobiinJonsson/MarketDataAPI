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
document.getElementById('firds-form').addEventListener('submit', function(event) {
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
  
  async function searchByIsin() {
    const isin = document.getElementById("isin-input").value;
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }

    try {
        console.log("Starting search for ISIN:", isin);  // Debug
        const response = await fetch(`/api/search/${isin}`);
        const data = await response.json();
        console.log("Received data:", data);  // Debug
        
        const table = document.getElementById("results-table");
        console.log("Table element:", table);  // Debug
        
        if (!table) {
            console.error("Table element not found!");  // Debug
            return;
        }
        
        // Clear existing table content
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Type</th>
                    <th>ISIN</th>
                    <th>Full Name</th>
                    <th>Short Name</th>
                    <th>CFI Code</th>
                    <th>Currency</th>
                    <th>Issuer LEI</th>
                    <th>Trading Venue</th>
                    <th>FIGI</th>
                    <th>Ticker</th>
                    <th>Security Type</th>
                    <th>Market Sector</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;
        
        if (data.message) {
            // No results found
            console.log("No results found, showing message:", data.message);  // Debug
            table.querySelector('tbody').innerHTML = `
                <tr><td colspan="12">${data.message}</td></tr>
            `;
        } else {
            // Format and display the data
            console.log("Formatting and displaying data:", data);  // Debug
            const tbody = table.querySelector('tbody');
            
            // Add equity data if present
            if (data.equity) {
                const row = `
                    <tr>
                        <td>Equity</td>
                        <td>${data.equity.ISIN || 'N/A'}</td>
                        <td>${data.equity.FullName || 'N/A'}</td>
                        <td>${data.equity.ShortName || 'N/A'}</td>
                        <td>${data.equity.CFICode || 'N/A'}</td>
                        <td>${data.equity.Currency || 'N/A'}</td>
                        <td>${data.equity.IssuerLEI || 'N/A'}</td>
                        <td>${data.equity.TradingVenueId || 'N/A'}</td>
                        <td>${data.figi?.FIGI || 'N/A'}</td>
                        <td>${data.figi?.Ticker || 'N/A'}</td>
                        <td>${data.figi?.SecurityType || 'N/A'}</td>
                        <td>${data.figi?.MarketSector || 'N/A'}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            }
            
            // Add debt data if present
            if (data.debt) {
                const row = `
                    <tr>
                        <td>Debt</td>
                        <td>${data.debt.ISIN || 'N/A'}</td>
                        <td>${data.debt.FullName || 'N/A'}</td>
                        <td>${data.debt.ShortName || 'N/A'}</td>
                        <td>${data.debt.CFICode || 'N/A'}</td>
                        <td>${data.debt.Currency || 'N/A'}</td>
                        <td>${data.debt.IssuerLEI || 'N/A'}</td>
                        <td>${data.debt.TradingVenueId || 'N/A'}</td>
                        <td>${data.figi?.FIGI || 'N/A'}</td>
                        <td>${data.figi?.Ticker || 'N/A'}</td>
                        <td>${data.figi?.SecurityType || 'N/A'}</td>
                        <td>${data.figi?.MarketSector || 'N/A'}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            }
        }
        
        // Make sure the table is visible
        table.style.display = 'table';
        console.log("Table should be visible now");  // Debug
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while searching for the ISIN');
    }
}
  
  async function addISIN() {
    const isin = document.getElementById("isinInput").value;
    const res = await fetch(`/api/add/${isin}`, { method: "POST" });
    const msg = await res.json();
    alert(msg.message);
  }
  
  async function listAll() {
    try {
        console.log('Starting listAll function'); // Debug
        const response = await fetch(`/api/list`);
        const data = await response.json();
        console.log("Received data:", data); // Debug
        
        const table = document.getElementById("results-table");
        console.log("Table element:", table); // Debug
        
        if (!table) {
            console.error("Table element not found!"); // Debug
            return;
        }
        
        // Clear existing table content
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Type</th>
                    <th>ISIN</th>
                    <th>Full Name</th>
                    <th>Short Name</th>
                    <th>CFI Code</th>
                    <th>Currency</th>
                    <th>Issuer LEI</th>
                    <th>Trading Venue</th>
                    <th>FIGI</th>
                    <th>Ticker</th>
                    <th>Security Type</th>
                    <th>Market Sector</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;
        
        if (data.message) {
            // No results found
            console.log("No results found, showing message:", data.message); // Debug
            table.querySelector('tbody').innerHTML = `
                <tr><td colspan="12">${data.message}</td></tr>
            `;
            return;
        }
        
        // Format and display the data
        console.log("Formatting and displaying data:", data); // Debug
        const tbody = table.querySelector('tbody');
        
        // Process equity entries
        if (data.equity) {
            data.equity.forEach(item => {
                const figiData = data.figi?.find(f => f.ISIN === item.ISIN) || {};
                const row = `
                    <tr>
                        <td>Equity</td>
                        <td>${item.ISIN || 'N/A'}</td>
                        <td>${item.FullName || 'N/A'}</td>
                        <td>${item.ShortName || 'N/A'}</td>
                        <td>${item.CFICode || 'N/A'}</td>
                        <td>${item.Currency || 'N/A'}</td>
                        <td>${item.IssuerLEI || 'N/A'}</td>
                        <td>${item.TradingVenueId || 'N/A'}</td>
                        <td>${figiData.FIGI || 'N/A'}</td>
                        <td>${figiData.Ticker || 'N/A'}</td>
                        <td>${figiData.SecurityType || 'N/A'}</td>
                        <td>${figiData.MarketSector || 'N/A'}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }
        
        // Process debt entries
        if (data.debt) {
            data.debt.forEach(item => {
                const figiData = data.figi?.find(f => f.ISIN === item.ISIN) || {};
                const row = `
                    <tr>
                        <td>Debt</td>
                        <td>${item.ISIN || 'N/A'}</td>
                        <td>${item.FullName || 'N/A'}</td>
                        <td>${item.ShortName || 'N/A'}</td>
                        <td>${item.CFICode || 'N/A'}</td>
                        <td>${item.Currency || 'N/A'}</td>
                        <td>${item.IssuerLEI || 'N/A'}</td>
                        <td>${item.TradingVenueId || 'N/A'}</td>
                        <td>${figiData.FIGI || 'N/A'}</td>
                        <td>${figiData.Ticker || 'N/A'}</td>
                        <td>${figiData.SecurityType || 'N/A'}</td>
                        <td>${figiData.MarketSector || 'N/A'}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        }
        
        // Make sure the table is visible
        table.style.display = 'table';
        console.log("Table update complete"); // Debug
        
    } catch (error) {
        console.error('Error in listAll:', error);
        alert('An error occurred while fetching the data');
    }
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
            listAll();
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