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

        if (!data || (!data.equity && !data.debt && !data.figi)) {
            showResultsError("No data found for this ISIN");
            return;
        }

        const sections = {
            instrumentDetails: {
                "ISIN": data.equity?.ISIN || data.debt?.ISIN || 'N/A',
                "Type": data.equity ? 'Equity' : 'Debt',
                "Full Name": data.equity?.FullName || data.debt?.FullName || 'N/A',
                "Short Name": data.equity?.ShortName || data.debt?.ShortName || 'N/A',
                "CFI Code": data.equity?.CFICode || data.debt?.CFICode || 'N/A',
                "Currency": data.equity?.Currency || data.debt?.Currency || 'N/A',
                "First Trade Date": formatDateResults(data.equity?.FirstTradeDate || data.debt?.FirstTradeDate) || 'N/A',
                "FIGI": data.figi?.FIGI || 'N/A',
                "Security Type": data.figi?.SecurityType || 'N/A',
                "Market Sector": data.figi?.MarketSector || 'N/A',
                "Security Description": data.figi?.SecurityDescription || 'N/A'
            },
            issuerData: {
                "LEI": data.lei?.lei || 'N/A',
                "Legal Name": data.lei?.legalName || 'N/A',
                "Legal Jurisdiction": data.lei?.legalJurisdiction || 'N/A',
                "Registered As": data.lei?.registeredAs || 'N/A',
                "Category": data.lei?.category || 'N/A',
                "Subcategory": data.lei?.subCategory || 'N/A',
                "Conformity Flag": data.lei?.conformityFlag || 'N/A',
                "Creation Date": formatDateResults(data.lei?.creationDate) || 'N/A'
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