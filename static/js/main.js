document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const questionForm = document.getElementById('question-form');
    const questionInput = document.getElementById('question-input');
    const submitBtn = document.getElementById('submit-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const sourceAnswer = document.getElementById('source-answer');
    const generalAnswer = document.getElementById('general-answer');
    const sourceList = document.getElementById('source-list');
    const metricsData = document.getElementById('metrics-data');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Check system status
    checkStatus();
    // Check status every 5 seconds until ready
    const statusInterval = setInterval(checkStatus, 5000);

    // Handle tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show corresponding tab content
            tabPanes.forEach(pane => pane.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
        });
    });

    // Handle form submission
    questionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question) return;
        
        // Show loading, hide results
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        submitBtn.disabled = true;
        
        // Send question to server
        askQuestion(question);
    });

    // Check system status
    function checkStatus() {
        fetch('/status')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ready') {
                    statusDot.classList.add('ready');
                    statusText.textContent = `Ready (${data.document_count} documents indexed)`;
                    submitBtn.disabled = false;
                    clearInterval(statusInterval);
                } else {
                    statusText.textContent = 'System initializing...';
                    submitBtn.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error checking status:', error);
                statusDot.classList.add('error');
                statusText.textContent = 'Error connecting to server';
                submitBtn.disabled = true;
            });
    }

    // Ask a question
    function askQuestion(question) {
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error');
            }
            return response.json();
        })
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your question. Please try again.');
        })
        .finally(() => {
            loadingDiv.classList.add('hidden');
            submitBtn.disabled = false;
        });
    }

    // Display results
    function displayResults(data) {
        // Display answers
        sourceAnswer.textContent = data.source_based_summary;
        generalAnswer.textContent = data.general_answer;
        
        // Display sources
        sourceList.innerHTML = '';
        data.sources.forEach(source => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            
            const sourceHeader = document.createElement('div');
            sourceHeader.className = 'source-header';
            
            const fileInfo = document.createElement('div');
            const fileName = source.file.split('/').pop();
            fileInfo.innerHTML = `<span class="source-file">${fileName}</span> <span class="source-page">Page ${source.page}</span>`;
            
            const scoreSpan = document.createElement('span');
            scoreSpan.className = 'source-score';
            scoreSpan.textContent = `Score: ${source.score.toFixed(2)}`;
            
            sourceHeader.appendChild(fileInfo);
            sourceHeader.appendChild(scoreSpan);
            
            const sourceText = document.createElement('div');
            sourceText.className = 'source-text';
            sourceText.textContent = source.text;
            
            sourceItem.appendChild(sourceHeader);
            sourceItem.appendChild(sourceText);
            sourceList.appendChild(sourceItem);
        });
        
        // Display metrics
        metricsData.innerHTML = '';
        
        const metrics = [
            { label: 'Total Documents', value: data.metrics.total_documents },
            { label: 'Documents with Matches', value: data.metrics.documents_with_matches },
            { label: 'Relevant Passages', value: data.metrics.relevant_passages },
            { label: 'Average Score', value: data.metrics.avg_score.toFixed(2) },
            { label: 'Search Duration', value: data.metrics.search_duration.toFixed(2), unit: 's' },
            { label: 'Total Duration', value: data.metrics.total_duration.toFixed(2), unit: 's' }
        ];
        
        metrics.forEach(metric => {
            const metricCard = document.createElement('div');
            metricCard.className = 'metric-card';
            
            const metricLabel = document.createElement('div');
            metricLabel.className = 'metric-label';
            metricLabel.textContent = metric.label;
            
            const metricValue = document.createElement('div');
            metricValue.className = 'metric-value';
            metricValue.textContent = metric.value;
            
            if (metric.unit) {
                const metricUnit = document.createElement('span');
                metricUnit.className = 'metric-unit';
                metricUnit.textContent = metric.unit;
                metricValue.appendChild(metricUnit);
            }
            
            metricCard.appendChild(metricLabel);
            metricCard.appendChild(metricValue);
            metricsData.appendChild(metricCard);
        });
        
        // Show results
        resultsDiv.classList.remove('hidden');
        
        // Reset to first tab
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabButtons[0].classList.add('active');
        
        tabPanes.forEach(pane => pane.classList.remove('active'));
        tabPanes[0].classList.add('active');
    }
});