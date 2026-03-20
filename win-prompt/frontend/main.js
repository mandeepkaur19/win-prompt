document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const textInput = document.getElementById('textInput').value.trim();
    const fileInput = document.getElementById('fileInput').files[0];
    
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const resultState = document.getElementById('resultState');
    const analyzeBtn = document.getElementById('analyzeBtn');

    if (!textInput && !fileInput) {
        showError("Please provide either text or an image.");
        return;
    }

    errorState.classList.add('hidden');
    resultState.classList.add('hidden');
    loadingState.classList.remove('hidden');
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';

    const formData = new FormData();
    if (textInput) formData.append('text', textInput);
    if (fileInput) formData.append('file', fileInput);

    try {
        // Use a relative path, so it works seamlessly on local dev server and Cloud Run
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error: HTTP ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);
    } catch (err) {
        let msg = err.message;
        if (err.message === 'Failed to fetch') {
            msg = 'Server offline. Please ensure the Python API is running on localhost:8000.';
        }
        showError(msg);
    } finally {
        loadingState.classList.add('hidden');
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze Truth';
    }
});

function showError(message) {
    const errorState = document.getElementById('errorState');
    document.getElementById('errorMsg').textContent = message;
    errorState.classList.remove('hidden');
}

function renderResults(payload) {
    const resultState = document.getElementById('resultState');
    const container = document.getElementById('cardsContainer');
    container.innerHTML = '';
    
    if (!payload.data || !payload.data.results || payload.data.results.length === 0) {
        container.innerHTML = '<p style="color: #94a3b8">No verifiable claims found in the input.</p>';
        resultState.classList.remove('hidden');
        return;
    }

    payload.data.results.forEach((res, index) => {
        const card = document.createElement('div');
        card.className = `claim-card card-${res.verdict}`;
        // Staggered loading animation for each card
        card.style.animationDelay = `${index * 0.15}s`;
        
        let factChecksHtml = '';
        if (res.fact_checks && res.fact_checks.length > 0) {
            factChecksHtml = `<ul class="fact-checks">
                ${res.fact_checks.map(fc => `<li>${fc}</li>`).join('')}
            </ul>`;
        }

        let scoreColor = '#94a3b8'; 
        if (res.verdict === 'True') scoreColor = '#34d399';
        else if (res.verdict === 'False') scoreColor = '#f87171';
        else if (res.verdict === 'Misleading') scoreColor = '#fbbf24';

        card.innerHTML = `
            <span class="verdict-badge badge-${res.verdict}">${res.verdict}</span>
            <div class="claim-text">"${res.claim_text}"</div>
            
            <div class="score-row">
                <div class="score-number" style="color: ${scoreColor}">${res.truth_score}<span style="font-size: 16px; color: #64748b">/100</span></div>
                <div class="score-label">Truth Score<br><span style="color: rgba(255,255,255,0.4)">Confidence: ${res.confidence}</span></div>
            </div>
            
            <p class="explanation">${res.explanation}</p>
            ${factChecksHtml}
        `;
        container.appendChild(card);
    });

    resultState.classList.remove('hidden');
}
