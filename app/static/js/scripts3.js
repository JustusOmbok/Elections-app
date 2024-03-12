// Sample data for demonstration
const nationalData = {{ national_data|tojson }};
const totalVotes = {{ total_votes }};

const nationalChart = new Chart(document.getElementById('nationalChart'), {
    type: 'horizontalBar',
    data: nationalData,
    options: {
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

// Display total votes
document.getElementById('totalVotes').innerText = totalVotes.toLocaleString();

// Function to populate county specific results
function populateCountyResults(countyName, countyData) {
    const countyChart = new Chart(document.createElement('canvas'), {
        type: 'horizontalBar',
        data: countyData,
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    const countyResultDiv = document.createElement('div');
    countyResultDiv.classList.add('mb-3');
    countyResultDiv.innerHTML = `<h3>${countyName}</h3>`;
    countyResultDiv.appendChild(countyChart.canvas);
    document.getElementById('countyResults').appendChild(countyResultDiv);
}

// Sample event listener for demonstration
document.addEventListener('DOMContentLoaded', function () {
    // Sample county results data for demonstration
    const countyResultsData = {
        'County A': {
            labels: ['Candidate A', 'Candidate B', 'Candidate C'],
            datasets: [{
                label: 'Percentage of Votes',
                data: [40, 30, 30], // Sample percentages for County A
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1
            }]
        },
        'County B': {
            labels: ['Candidate A', 'Candidate B', 'Candidate C'],
            datasets: [{
                label: 'Percentage of Votes',
                data: [50, 20, 30], // Sample percentages for County B
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1
            }]
        },
        'County C': {
            labels: ['Candidate A', 'Candidate B', 'Candidate C'],
            datasets: [{
                label: 'Percentage of Votes',
                data: [30, 40, 30], // Sample percentages for County C
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1
            }]
        }
    };

    // Populate county results on county click (sample event listener)
    document.getElementById('countyResults').addEventListener('click', function (event) {
        if (event.target.tagName === 'H3') {
            const countyName = event.target.innerText;
            populateCountyResults(countyName, countyResultsData[countyName]);
        }
    });
});