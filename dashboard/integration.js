/*
  Guardian AI - Backend Integration
  Connects the Dashboard UI to the FastAPI Backend
*/

const API_BASE_URL = 'http://localhost:8000';

async function runMarketIntelligence() {
    const product = document.querySelector('input[placeholder*="AI Marketing Platform"]').value;
    const url = document.querySelector('input[placeholder*="yourwebsite.com"]').value;
    
    if (!product) {
        alert("Please enter a product or service name.");
        return;
    }

    const runBtn = document.querySelector('.btn-primary');
    const originalText = runBtn.innerText;
    runBtn.innerText = "Analyzing...";
    runBtn.disabled = true;

    try {
        // Call the Text Analysis endpoint
        const response = await fetch(`${API_BASE_URL}/analyze/text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: `Product: ${product}. Website: ${url}` })
        });

        const result = await response.json();
        
        // Update Brand Safety section with results
        updateBrandSafety(product, result);
        
        // Show success
        alert("Analysis complete! Brand safety scores updated.");
    } catch (error) {
        console.error("Backend integration error:", error);
        alert("Could not connect to backend. Please ensure the FastAPI server is running on port 8000.");
    } finally {
        runBtn.innerText = originalText;
        runBtn.disabled = false;
    }
}

function updateBrandSafety(title, result) {
    const safetyContainer = document.querySelector('.col-4 .card');
    if (!safetyContainer) return;

    // Create a new safety item based on backend result
    const newItem = document.createElement('div');
    newItem.className = 'safety-item animate-in';
    
    const isSafe = !result.is_fraud;
    const statusIcon = isSafe ? '✅' : '❌';
    const statusClass = isSafe ? 'status-approved' : 'status-violation';
    const riskLabel = isSafe ? 'Low Risk' : 'High Risk';
    const riskColor = isSafe ? 'var(--color-success)' : 'var(--color-danger)';
    const sentiment = Math.round(result.confidence * 100);

    newItem.innerHTML = `
        <div class="safety-status ${statusClass}">${statusIcon}</div>
        <div class="safety-content">
            <div class="safety-title">${title}</div>
            <div class="safety-meta">
                <span>🧠 ${sentiment}% Confidence</span>
                <span style="color: ${riskColor};">${riskLabel}</span>
            </div>
        </div>
    `;

    // Insert at the top of the list (after the header)
    const header = safetyContainer.querySelector('.card-header');
    header.insertAdjacentElement('afterend', newItem);
}

// Hook into the UI
document.addEventListener('DOMContentLoaded', () => {
    const runIntelligenceBtn = document.querySelector('.btn-primary');
    if (runIntelligenceBtn) {
        runIntelligenceBtn.onclick = runMarketIntelligence;
    }
});
