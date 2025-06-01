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
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }

    try {
        document.getElementById("spinner").style.display = "block";
        const url = buildApiUrl(`${APP_CONFIG.ENDPOINTS.SEARCH}/${isin}`);
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            showResultsError(data.message || "Error fetching data");
            return;
        }

        if (!data || (!data.instrument && !data.figi && !data.lei)) {
            showResultsError("No data found for this ISIN");
            return;
        }

        // Hide all instrument views first
        document.querySelectorAll('.instrument-view').forEach(view => {
            view.style.display = 'none';
        });

        // Show the appropriate view based on instrument type
        const instrumentType = data.instrument?.type?.toLowerCase() || '';
        if (instrumentType === 'debt') {
            logDebugInfo(data);
        }
        const viewElement = document.getElementById(`${instrumentType}-view`);
        if (viewElement) {
            viewElement.style.display = 'grid';
        } else {
            showResultsError("Unsupported instrument type");
            return;
        }

        // Update the sections based on instrument type
        updateInstrumentView(instrumentType, data);
        
        // Add raw JSON data to the Data tab
        displayRawData(data);
        
        switchTab('overview');
    } catch (error) {
        showResultsError('An error occurred while fetching the data');
    } finally {
        document.getElementById("spinner").style.display = "none";
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

function decodeCFIAttributes(cfiCode) {
    if (!cfiCode || cfiCode.length !== 6) return { "Error": "Invalid or missing CFI Code" };

    const attributes = {
        "Voting Rights": decodeCFIPosition(cfiCode[2], {
            'V': "Voting",
            'N': "Non-voting",
            'R': "Restricted voting",
            'X': "Not applicable"
        }),
        "Ownership Transfer": decodeCFIPosition(cfiCode[3], {
            'R': "Registered",
            'B': "Bearer",
            'X': "Not applicable"
        }),
        "Dividend Status": decodeCFIPosition(cfiCode[4], {
            'F': "Full dividend",
            'P': "Partial dividend",
            'N': "No dividend",
            'X': "Not applicable"
        }),
        "Payment Status": decodeCFIPosition(cfiCode[5], {
            'P': "Paid",
            'N': "Partly paid",
            'O': "Nil paid",
            'X': "Not applicable"
        })
    };

    return attributes;
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
    const sections = ['instrument-details', 'issuer-data', 'trading-venue', 'underlying-instruments'];
    sections.forEach(section => {
        const sectionContent = document.querySelector(`#${section} .section-content`);
        if (sectionContent) {
            sectionContent.innerHTML = `<div class="error-message">${message}</div>`;
        }
    });
    document.getElementById("spinner").style.display = "none";
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