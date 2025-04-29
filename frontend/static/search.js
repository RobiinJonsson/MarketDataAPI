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

    console.log("Sending request with:", query);

    let response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    let data = await response.json();
    console.log("Received response:", data);

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
            <td>${entry.data[0]?.input_isin}</td>
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

async function fetchAndInsert() {
    const isin = document.getElementById("isin-input").value;
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }

    try {
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

        document.getElementById("spinner").style.display = "none";

        if (response.ok) {
            const instrumentType = result.instrument_type || 'equity';
            const toast = document.getElementById("toast");
            toast.textContent = `${result.message} (${instrumentType} instrument)`;
            toast.className = "toast success show";
            setTimeout(() => toast.className = "toast", 3000);

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

function formatDateSearch(dateString) {
    if (!dateString || dateString === 'None') return 'N/A';
    try {
        return new Date(dateString).toLocaleString();
    } catch (e) {
        console.warn('Date parsing error:', e);
        return dateString;
    }
}

function showSearchError(message) {
    const sections = ['instrument-details', 'issuer-data', 'trading-venue', 'underlying-instruments'];
    sections.forEach(section => {
        const sectionContent = document.querySelector(`#${section} .section-content`);
        if (sectionContent) {
            sectionContent.innerHTML = `<div class="error-message">${message}</div>`;
        }
    });
    document.getElementById("spinner").style.display = "none";
}