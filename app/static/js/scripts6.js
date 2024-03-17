document.addEventListener('DOMContentLoaded', function() {
    // Fetch governor election results
    fetch('/calculate_results_governor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token() }}'
        },
        body: 'county=' + '{{ selected_county }}'
    })
    .then(response => response.json())
    .then(data => {
        const governorResults = data.governor_results;
        const totalVotes = data.total_votes;

        const ctx = document.getElementById('governorChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar', // Use 'bar' type instead of 'horizontalBar'
            data: {
                labels: governorResults.map(result => result[0]),
                datasets: [{
                    label: 'Votes',
                    data: governorResults.map(result => result[1]),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y', // Use 'y' index axis for horizontal bars
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        document.getElementById('total_votes').textContent = totalVotes;
    })
    .catch(error => console.error('Error:', error));
});