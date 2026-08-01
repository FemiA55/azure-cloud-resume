window.addEventListener('DOMContentLoaded', () => {
    getVisitorCount();
});

const functionApiUrl = 'https://fe1resumefunction.azurewebsites.net/api/GetResumeCount';

function getVisitorCount() {
    fetch(functionApiUrl)
        .then(response => response.text()) // Use text() to safely handle raw numbers/text
        .then(data => {
            // Try parsing as JSON first; fall back to plain text/number
            try {
                const parsed = JSON.parse(data);
                document.getElementById('counter').innerText = parsed.count ?? parsed;
            } catch {
                document.getElementById('counter').innerText = data;
            }
        })
        .catch(error => {
            console.error('Error fetching visitor count:', error);
            document.getElementById('counter').innerText = 'Error loading count';
        });
}