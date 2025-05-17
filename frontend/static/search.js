async function searchAndDisplay() {
    const isin = document.getElementById("search-isin-input").value;
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }
    // ...existing search code...
}

async function fetchAndInsert() {
    const isin = document.getElementById("insert-isin-input").value;
    const category = document.getElementById("cfi-category").value;
    
    if (!isin) {
        alert("Please enter an ISIN");
        return;
    }
    
    if (!category) {
        alert("Please select an instrument category");
        return;
    }

    try {
        document.getElementById("spinner").style.display = "block";

        const payload = {
            Id: isin,
            Category: category  // This matches the database polymorphic identity
        };

        const response = await fetch('/api/fetch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        
        if (response.ok) {
            const toast = document.getElementById("toast");
            const enrichmentStatus = [];
            if (result.figi) enrichmentStatus.push('FIGI');
            if (result.lei) enrichmentStatus.push('LEI');
            
            const enrichmentText = enrichmentStatus.length ? 
                ` (enriched with ${enrichmentStatus.join(', ')})` : '';
                
            toast.textContent = `Successfully processed ${isin}${enrichmentText}`;
            toast.className = "toast success show";
            setTimeout(() => toast.className = "toast", 3000);

            await searchAndDisplay();
        } else {
            throw new Error(result.error || 'Failed to process request');
        }
    } catch (error) {
        console.error('Error:', error);
        const toast = document.getElementById("toast");
        toast.textContent = error.message;
        toast.className = "toast error show";
        setTimeout(() => toast.className = "toast", 3000);
    } finally {
        document.getElementById("spinner").style.display = "none";
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