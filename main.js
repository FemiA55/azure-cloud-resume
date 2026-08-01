window.addEventListener('DOMContentLoaded', () => {
    getVisitorCount();
});

const functionApiUrl = 'https://fe1resumefunction.azurewebsites.net/api/GetResumeCounter';

function getVisitorCount() {
    fetch(functionApiUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('counter').innerText = data.count;
        })
        .catch(error => {
            console.error('Error fetching visitor count:', error);
            document.getElementById('counter').innerText = 'Error loading count';
        });
}