function switchTab(tabName) {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.toLowerCase() === tabName) {
            btn.classList.add('active');
        }
    });

    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
        if (pane.id === `${tabName}-tab`) {
            pane.classList.add('active');
        }
    });
}

async function searchAndDisplay() {
    const isin = document.getElementById("search-isin-input").value;
    if (!isin) return;
    
    try {
        // Use the new API endpoint
        const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.SEARCH}/${isin}`);
        console.log('Searching with URL:', url); // Debug log
        
        const response = await fetch(url);
        const responseData = await response.json();
        
        console.log('Raw API response:', responseData); // Debug log
        console.log('Response type:', typeof responseData);
        console.log('Response keys:', Object.keys(responseData || {}));
        
        if (response.ok && responseData) {
            // Handle the new API response structure that wraps data in {status, data}
            let data;
            if (responseData.status === 'success' && responseData.data) {
                data = responseData.data;
            } else if (responseData.type && responseData.isin) {
                // Direct data response (fallback)
                data = responseData;
            } else {
                console.error('Invalid data structure:', responseData);
                showResultsError('Invalid response from server');
                return;
            }
            
            console.log('Extracted data:', data);
            
            // Check if data has the expected structure
            if (!data.type || !data.isin) {
                console.error('Invalid data structure after extraction:', data);
                showResultsError('Invalid response from server');
                return;
            }
            
            // Transform the API response to match the legacy structure
            const transformedData = {
                instrument: {
                    id: data.id,
                    type: data.type,
                    isin: data.isin,
                    full_name: data.full_name,
                    short_name: data.short_name,
                    symbol: data.symbol,
                    cfi_code: data.cfi_code,
                    currency: data.currency,
                    trading_venue: data.trading_venue,
                    relevant_authority: data.relevant_authority,
                    relevant_venue: data.relevant_venue,
                    commodity_derivative: data.commodity_derivative,
                    first_trade_date: data.first_trade_date,
                    termination_date: data.termination_date,
                    cfi_decoded: data.cfi_decoded
                },
                // Map the new API structure to legacy structure
                figi: data.figi || {},
                lei: data.legal_entity || {},
                derivatives: data.derivatives || [],
                underlying_instrument: data.underlying_instrument || { full_name: null }
            };
            
            // Add type-specific attributes from the new API structure
            if (data.type === "future" && data.future_attributes) {
                // Map future_attributes to instrument level for legacy compatibility
                transformedData.instrument.expiration_date = data.future_attributes.expiration_date;
                transformedData.instrument.price_multiplier = data.future_attributes.price_multiplier;
                transformedData.instrument.delivery_type = data.future_attributes.delivery_type;
                transformedData.instrument.underlying_single_isin = data.future_attributes.underlying_single_isin;
                transformedData.instrument.basket_isin = data.future_attributes.basket_isin;
                transformedData.instrument.underlying_index_isin = data.future_attributes.underlying_index_isin;
                transformedData.instrument.underlying_single_index_name = data.future_attributes.underlying_single_index_name;
            }
            
            if (data.type === "debt" && data.debt_attributes) {
                // Map debt_attributes to instrument level for legacy compatibility
                transformedData.instrument.maturity_date = data.debt_attributes.maturity_date;
                transformedData.instrument.total_issued_nominal = data.debt_attributes.total_issued_nominal;
                transformedData.instrument.nominal_value_per_unit = data.debt_attributes.nominal_value_per_unit;
                transformedData.instrument.debt_seniority = data.debt_attributes.debt_seniority;
                transformedData.instrument.floating_rate_term_unit = data.debt_attributes.floating_rate_term_unit;
                transformedData.instrument.floating_rate_term_value = data.debt_attributes.floating_rate_term_value;
                transformedData.instrument.floating_rate_basis_points_spread = data.debt_attributes.floating_rate_basis_points_spread;
                transformedData.instrument.interest_rate_floating_reference_index = data.debt_attributes.interest_rate_floating_reference_index;
            }
            
            if (data.type === "equity" && data.equity_attributes) {
                // Map equity_attributes to instrument level for legacy compatibility
                transformedData.instrument.asset_class = data.equity_attributes.asset_class;
                transformedData.instrument.shares_outstanding = data.equity_attributes.shares_outstanding;
                transformedData.instrument.market_cap = data.equity_attributes.market_cap;
                transformedData.instrument.sector = data.equity_attributes.sector;
                transformedData.instrument.industry = data.equity_attributes.industry;
            }
            
            console.log('Transformed data:', transformedData);
            console.log('Instrument type:', transformedData.instrument?.type);
            
            // Hide all instrument views first
            document.querySelectorAll('.instrument-view').forEach(view => {
                view.style.display = 'none';
            });
            
            // Show appropriate view based on instrument type
            const instrumentType = transformedData.instrument?.type;
            
            if (!instrumentType) {
                console.error('No instrument type found in transformed data');
                showResultsError('Invalid instrument data - missing type');
                return;
            }
            
            const viewElement = document.getElementById(`${instrumentType}-view`);
            console.log(`Looking for view element: ${instrumentType}-view`, viewElement);
            
            if (viewElement) {
                viewElement.style.display = 'grid';
                updateInstrumentView(instrumentType, transformedData);
                displayRawData(data);
            } else {
                console.error(`No view element found for type: ${instrumentType}`);
                showResultsError(`Unsupported instrument type: ${instrumentType}`);
            }
        } else {
            console.error('Search failed:', responseData);
            showResultsError(responseData?.error || responseData?.message || 'Instrument not found');
        }
    } catch (error) {
        console.error('Search error:', error);
        showResultsError('An error occurred while searching');
    }
}

function updateInstrumentView(type, data) {
    const sections = {
        equity: {
            [`${type}-instrument-details`]: {
                "ISIN": data.instrument?.isin || 'N/A',
                "Type": data.instrument?.type || 'N/A',
                "Symbol": data.instrument?.symbol || 'N/A',
                "Full Name": data.instrument?.full_name || 'N/A',
                "CFI Code": data.instrument?.cfi_code || 'N/A'
            },
            [`${type}-issuer-data`]: {
                "LEI": data.lei?.lei || 'N/A',
                "Name": data.lei?.name || 'N/A',
                "Jurisdiction": data.lei?.jurisdiction || 'N/A',
                "Legal Form": data.lei?.legal_form || 'N/A',
                "Status": data.lei?.status || 'N/A'
            },
            [`${type}-trading-venue`]: {
                "Relevant Venue": data.instrument?.relevant_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A',
                "Currency": data.instrument?.currency || 'N/A',
                "First Trade Date": data.instrument?.first_trade_date ? formatDateResults(data.instrument.first_trade_date) : 'N/A',
                "Termination Date": data.instrument?.termination_date ? formatDateResults(data.instrument.termination_date) : 'N/A'
            },
            [`${type}-cfi-decoded`]: (() => {
                const decoded = data.instrument?.cfi_decoded;
                if (!decoded || typeof decoded !== 'object') return { "CFI Decoding": "N/A" };
                
                // Create a more complete CFI classification display
                const result = {
                    "CFI Code": decoded.cfi_code || 'N/A',
                    "Category": `${decoded.category} - ${decoded.category_description}` || 'N/A',
                    "Group": `${decoded.group} - ${decoded.group_description}` || 'N/A'
                };
                
                // Add attributes if available
                if (decoded.attributes && typeof decoded.attributes === 'object') {
                    Object.entries(decoded.attributes).forEach(([key, value]) => {
                        // Capitalize and format keys for display
                        const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        result[displayKey] = value;
                    });
                }
                
                return result;
            })(),
            [`${type}-derivatives`]: (() => {
                const list = data.derivatives;
                if (!list || !Array.isArray(list) || list.length === 0) return { "Related Futures": "None" };
                // Show each as ISIN (Symbol) or just ISIN if symbol is missing
                return {
                    "Related Futures": list.map(f => f.symbol ? `${f.isin} (${f.symbol})` : f.isin).join(", ")
                };
            })()
        },
        future: {
            // Status bar section (handled separately below)
            [`${type}-instrument-details`]: {
                "ISIN": data.instrument?.isin || 'N/A',
                "Type": data.instrument?.type || 'N/A',
                "Symbol": data.instrument?.symbol || 'N/A',
                "Full Name": data.instrument?.full_name || 'N/A',
                "CFI Code": data.instrument?.cfi_code || 'N/A'
            },
            [`${type}-contract-data`]: {
                "Expiration Date": data.instrument?.expiration_date ? formatDateResults(data.instrument.expiration_date) : 'N/A',
                "Price Multiplier": data.instrument?.price_multiplier || 'N/A',
                "Delivery Type": data.instrument?.delivery_type || 'N/A'
            },
            [`${type}-trading-venue`]: {
                "Relevant Venue": data.instrument?.relevant_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A',
                "Currency": data.instrument?.currency || 'N/A',
                "First Trade Date": data.instrument?.first_trade_date ? formatDateResults(data.instrument.first_trade_date) : 'N/A',
                "Termination Date": data.instrument?.termination_date ? formatDateResults(data.instrument.termination_date) : 'N/A'
            },
            [`${type}-cfi-decoded`]: (() => {
                const decoded = data.instrument?.cfi_decoded;
                if (!decoded || typeof decoded !== 'object') return { "CFI Decoding": "N/A" };
                
                // Create a more complete CFI classification display
                const result = {
                    "CFI Code": decoded.cfi_code || 'N/A',
                    "Category": `${decoded.category} - ${decoded.category_description}` || 'N/A',
                    "Group": `${decoded.group} - ${decoded.group_description}` || 'N/A'
                };
                
                // Add attributes if available
                if (decoded.attributes && typeof decoded.attributes === 'object') {
                    Object.entries(decoded.attributes).forEach(([key, value]) => {
                        // Capitalize and format keys for display
                        const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        result[displayKey] = value;
                    });
                }
                
                return result;
            })(),
            [`${type}-underlying-instrument`]: {
                "Underlying ISIN": data.instrument?.underlying_single_isin || data.instrument?.basket_isin || data.instrument?.underlying_index_isin || 'N/A',
                "Underlying Name": data.underlying_instrument?.full_name || 'N/A'
            }
        },
        debt: {
            [`${type}-instrument-details`]: {
                "ISIN": data.instrument?.isin || 'N/A',
                "Type": data.instrument?.type || 'N/A',
                "Symbol": data.instrument?.symbol || 'N/A',
                "Full Name": data.instrument?.full_name || 'N/A',
                "CFI Code": data.instrument?.cfi_code || 'N/A'
            },
            [`${type}-issuer-data`]: {
                "LEI": data.lei?.lei || 'N/A',
                "Name": data.lei?.name || 'N/A',
                "Jurisdiction": data.lei?.jurisdiction || 'N/A',
                "Legal Form": data.lei?.legal_form || 'N/A',
                "Status": data.lei?.status || 'N/A'
            },
            [`${type}-payment-info`]: {
                "Maturity Date": data.instrument?.maturity_date ? formatDateResults(data.instrument.maturity_date) : 'N/A',
                "Total Nominal Value": data.instrument?.total_issued_nominal ? `${data.instrument.total_issued_nominal.toLocaleString()} ${data.instrument?.currency || ''}` : 'N/A',
                "Nominal Per Unit": data.instrument?.nominal_value_per_unit ? `${data.instrument.nominal_value_per_unit.toLocaleString()} ${data.instrument?.currency || ''}` : 'N/A',
                "Floating Rate Index": data.instrument?.interest_rate_floating_reference_index || 'N/A',
                "Rate Term": data.instrument?.floating_rate_term_value ? `${data.instrument.floating_rate_term_value} ${data.instrument.floating_rate_term_unit || ''}` : 'N/A',
                "Basis Points Spread": data.instrument?.floating_rate_basis_points_spread ? `${data.instrument.floating_rate_basis_points_spread} bp` : 'N/A',
                "Seniority": data.instrument?.debt_seniority || 'N/A'
            },
            [`${type}-trading-venue`]: {
                "Relevant Venue": data.instrument?.relevant_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A',
                "Currency": data.instrument?.currency || 'N/A',
                "First Trade Date": data.instrument?.first_trade_date ? formatDateResults(data.instrument.first_trade_date) : 'N/A'
            },
            [`${type}-cfi-decoded`]: (() => {
                const decoded = data.instrument?.cfi_decoded;
                if (!decoded || typeof decoded !== 'object') return { "CFI Decoding": "N/A" };
                
                // Create a more complete CFI classification display
                const result = {
                    "CFI Code": decoded.cfi_code || 'N/A',
                    "Category": `${decoded.category} - ${decoded.category_description}` || 'N/A',
                    "Group": `${decoded.group} - ${decoded.group_description}` || 'N/A'
                };
                
                // Add attributes if available
                if (decoded.attributes && typeof decoded.attributes === 'object') {
                    Object.entries(decoded.attributes).forEach(([key, value]) => {
                        // Capitalize and format keys for display
                        const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        result[displayKey] = value;
                    });
                }
                
                return result;
            })()
        }
    };

    const viewSections = sections[type];
    if (!viewSections) return;

    // Render status bar for futures and debt instruments
    if (type === "future") {
        renderFutureStatusBar(data.instrument?.first_trade_date, data.instrument?.expiration_date);
    } else if (type === "debt") {
        // Use maturity_date instead of falling back to termination_date
        renderDebtStatusBar(data.instrument?.first_trade_date, data.instrument?.maturity_date);
    }

    Object.entries(viewSections).forEach(([sectionId, sectionData]) => {
        const sectionContent = document.querySelector(`#${sectionId} .section-content`);
        if (!sectionContent) return;

        const htmlContent = Object.entries(sectionData)
            .map(([label, value]) => `
                <div class="field-row">
                    <div class="label">${label}:</div>
                    <div class="value">${value}</div>
                </div>
            `).join('');
        sectionContent.innerHTML = htmlContent;
    });
}

// Add this function at the end of the file
function renderFutureStatusBar(firstTradeDate, expiryDate) {
    const container = document.getElementById("future-status-bar-container");
    if (!container) return;

    if (!firstTradeDate || !expiryDate) {
        container.innerHTML = "<div class='status-bar-error'>No date data available</div>";
        return;
    }

    const start = new Date(firstTradeDate);
    const end = new Date(expiryDate);
    const now = new Date();

    if (isNaN(start.getTime()) || isNaN(end.getTime())) {
        container.innerHTML = "<div class='status-bar-error'>Invalid date data</div>";
        return;
    }

    const total = end - start;
    const elapsed = Math.min(Math.max(now - start, 0), total);
    const percent = total > 0 ? (elapsed / total) * 100 : 0;
    const expired = now > end;
    const statusText = expired ? "Expired" : "Active";

    container.innerHTML = `
        <div class="status-bar-outer">
            <div class="status-bar-inner${expired ? " expired" : ""}" style="width:${percent}%;"></div>
            <div class="status-bar-labels">
                <span>${formatDateResults(firstTradeDate)}</span>
                <span class="status-bar-status ${expired ? "expired" : "active"}">${statusText}</span>
                <span>${formatDateResults(expiryDate)}</span>
            </div>
        </div>
    `;
}

// Add this function for debt status bar
function renderDebtStatusBar(issueDate, maturityDate) {
    const container = document.getElementById("debt-status-bar-container");
    if (!container) return;

    if (!issueDate || !maturityDate) {
        container.innerHTML = "<div class='status-bar-error'>No date data available</div>";
        return;
    }

    const start = new Date(issueDate);
    const end = new Date(maturityDate);
    const now = new Date();

    if (isNaN(start.getTime()) || isNaN(end.getTime())) {
        container.innerHTML = "<div class='status-bar-error'>Invalid date data</div>";
        return;
    }

    const total = end - start;
    const elapsed = Math.min(Math.max(now - start, 0), total);
    const percent = total > 0 ? (elapsed / total) * 100 : 0;
    const matured = now > end;
    const statusText = matured ? "Matured" : "Active";

    container.innerHTML = `
        <div class="status-bar-outer">
            <div class="status-bar-inner${matured ? " expired" : ""}" style="width:${percent}%;"></div>
            <div class="status-bar-labels">
                <span>${formatDateResults(issueDate)}</span>
                <span class="status-bar-status ${matured ? "expired" : "active"}">${statusText}</span>
                <span>${formatDateResults(maturityDate)}</span>
            </div>
        </div>
    `;
}

// Add this function to display raw JSON data
function displayRawData(data) {
    const dataTab = document.getElementById('data-tab');
    if (!dataTab) return;
    
    const jsonStr = JSON.stringify(data, null, 2);
    dataTab.innerHTML = `
        <div class="raw-data-container">
            <h3>Raw Instrument Data</h3>
            <pre class="raw-json">${jsonStr}</pre>
        </div>
    `;
}

function decodeCFIPosition(char, mapping) {
    return mapping[char] || "Unknown";
}

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

function formatDateResults(dateString) {
    console.log("Formatting date:", dateString);
    if (!dateString || dateString === 'None' || dateString === null) {
        console.log("Date is null/None/empty");
        return 'N/A';
    }
    try {
        const date = new Date(dateString);
        console.log("Parsed date object:", date);
        
        if (isNaN(date.getTime())) {
            console.log("Invalid date - NaN");
            return 'N/A';
        }
        
        const formatted = date.toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        console.log("Formatted date:", formatted);
        return formatted;
    } catch (e) {
        console.error('Error formatting date:', dateString, e);
        return 'N/A';
    }
}

function showResultsError(message) {
    // Find any available section content containers to show the error
    const possibleSections = [
        'equity-instrument-details', 'future-instrument-details', 'debt-instrument-details',
        'instrument-details', 'issuer-data', 'trading-venue', 'underlying-instruments'
    ];
    
    let errorShown = false;
    possibleSections.forEach(section => {
        const sectionContent = document.querySelector(`#${section} .section-content`);
        if (sectionContent && !errorShown) {
            sectionContent.innerHTML = `<div class="error-message">${message}</div>`;
            errorShown = true;
        }
    });
    
    // If no section found, try to show in results area
    if (!errorShown) {
        const resultsSection = document.querySelector('.results-section');
        if (resultsSection) {
            resultsSection.innerHTML = `<div class="error-message">${message}</div>`;
        } else {
            // Fallback to alert if no suitable container found
            alert(message);
        }
    }
    
    // Hide spinner if it exists
    const spinner = document.getElementById("spinner");
    if (spinner) {
        spinner.style.display = "none";
    }
}

// Add a special logging function for debugging debt fields
function logDebugInfo(data) {
    console.log("Debt Instrument Data:", {
        maturity_date: data.instrument?.maturity_date,
        total_issued_nominal: data.instrument?.total_issued_nominal,
        nominal_value_per_unit: data.instrument?.nominal_value_per_unit,
        debt_seniority: data.instrument?.debt_seniority,
        floating_rate_term_unit: data.instrument?.floating_rate_term_unit,
        floating_rate_term_value: data.instrument?.floating_rate_term_value,
        floating_rate_basis_points_spread: data.instrument?.floating_rate_basis_points_spread,
        interest_rate_floating_reference_index: data.instrument?.interest_rate_floating_reference_index
    });
}