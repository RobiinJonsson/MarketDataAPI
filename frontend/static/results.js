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
        const response = await fetch(`/api/search/${isin}`);
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
        const viewElement = document.getElementById(`${instrumentType}-view`);
        if (viewElement) {
            viewElement.style.display = 'grid';
        } else {
            showResultsError("Unsupported instrument type");
            return;
        }

        // Update the sections based on instrument type
        updateInstrumentView(instrumentType, data);
        
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
                "CFI Code": data.instrument?.cfi_code || 'N/A',
                "Currency": data.instrument?.currency || 'N/A'
            },
            [`${type}-issuer-data`]: {
                "LEI": data.lei?.lei || 'N/A',
                "Name": data.lei?.name || 'N/A',
                "Status": data.lei?.status || 'N/A'
            },
            [`${type}-trading-venue`]: {
                "Trading Venue": data.instrument?.trading_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A'
            },
            [`${type}-price-data`]: {
                "First Trade Date": data.instrument?.first_trade_date ? 
                    formatDateResults(data.instrument.first_trade_date) : 'N/A'
            }
        },
        future: {
            [`${type}-instrument-details`]: {
                "ISIN": data.instrument?.isin || 'N/A',
                "Type": data.instrument?.type || 'N/A',
                "Symbol": data.instrument?.symbol || 'N/A',
                "CFI Code": data.instrument?.cfi_code || 'N/A'
            },
            [`${type}-contract-data`]: {
                "Currency": data.instrument?.currency || 'N/A',
                "First Trade Date": data.instrument?.first_trade_date ? 
                    formatDateResults(data.instrument.first_trade_date) : 'N/A'
            },
            [`${type}-trading-venue`]: {
                "Trading Venue": data.instrument?.trading_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A'
            },
            [`${type}-underlying`]: {
                "Commodity Derivative": data.instrument?.commodity_derivative ? 'Yes' : 'No'
            }
        },
        debt: {
            [`${type}-instrument-details`]: {
                "ISIN": data.instrument?.isin || 'N/A',
                "Type": data.instrument?.type || 'N/A',
                "CFI Code": data.instrument?.cfi_code || 'N/A',
                "Currency": data.instrument?.currency || 'N/A'
            },
            [`${type}-issuer-data`]: {
                "LEI": data.lei?.lei || 'N/A',
                "Name": data.lei?.name || 'N/A',
                "Status": data.lei?.status || 'N/A'
            },
            [`${type}-payment-info`]: {
                "First Trade Date": data.instrument?.first_trade_date ? 
                    formatDateResults(data.instrument.first_trade_date) : 'N/A'
            },
            [`${type}-trading-venue`]: {
                "Trading Venue": data.instrument?.trading_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A'
            }
        }
    };

    const viewSections = sections[type];
    if (!viewSections) return;

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