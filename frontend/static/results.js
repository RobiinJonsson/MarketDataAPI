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
    const isin = document.getElementById("isin-input").value;
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

        const sections = {
            instrumentDetails: {
                "ISIN": data.instrument?.isin || 'N/A',
                "Type": data.instrument?.type || 'N/A',
                "Full Name": data.instrument?.full_name || 'N/A',
                "Short Name": data.instrument?.short_name || 'N/A',
                "Symbol": data.instrument?.symbol || 'N/A',
                "CFI Code": data.instrument?.cfi_code || 'N/A',
                "Currency": data.instrument?.currency || 'N/A',
                "First Trade Date": formatDateResults(data.instrument?.first_trade_date) || 'N/A',
                "FIGI": data.figi?.figi || 'N/A',
                "Security Type": data.figi?.security_type || 'N/A',
                "Market Sector": data.figi?.market_sector || 'N/A'
            },
            issuerData: {
                "LEI": data.lei?.lei || 'N/A',
                "Name": data.lei?.name || 'N/A',
                "Jurisdiction": data.lei?.jurisdiction || 'N/A',
                "Legal Form": data.lei?.legal_form || 'N/A',
                "Status": data.lei?.status || 'N/A',
                "Creation Date": formatDateResults(data.lei?.creation_date) || 'N/A'
            },
            tradingVenue: {
                "Trading Venue": data.instrument?.trading_venue || 'N/A',
                "Relevant Venue": data.instrument?.relevant_venue || 'N/A',
                "Relevant Authority": data.instrument?.relevant_authority || 'N/A'
            },
            underlyingInstruments: {
                "Commodity Derivative": data.instrument?.commodity_derivative ? 'Yes' : 'No'
            }
        };

        Object.entries(sections).forEach(([sectionId, sectionData]) => {
            const elementId = sectionId.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
            const sectionContent = document.querySelector(`#${elementId} .section-content`);
            if (!sectionContent) {
                return;
            }
            const htmlContent = Object.entries(sectionData)
                .map(([label, value]) => `
                    <div class="field-row">
                        <div class="label">${label}:</div>
                        <div class="value">${value}</div>
                    </div>
                `).join('');
            sectionContent.innerHTML = htmlContent;
        });

        switchTab('overview');
    } catch (error) {
        showResultsError('An error occurred while fetching the data');
    } finally {
        document.getElementById("spinner").style.display = "none";
    }
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
    if (!dateString || dateString === 'None') return 'N/A';
    try {
        return new Date(dateString).toLocaleString();
    } catch (e) {
        return dateString;
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