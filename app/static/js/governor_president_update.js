function fetchPresidentDetails() {
    var presidentNationalId = document.getElementById('presidentNationalId').value;

    if (!presidentNationalId) {
        alert('Please enter President National ID.');
        return;
    }

    // Make a request to fetch president details
    fetch('/fetch_president_details/' + presidentNationalId)
        .then(response => response.json())
        .then(data => {
            var presidentDetails = `
                <p>Name: ${data.name}</p>
                <p>Party Name: ${data.party_name}</p>
                <p>Party Color: ${data.party_color}</p>
                <input type="text" id="updatedPresidentName" placeholder="Enter Updated Name">
                <input type="text" id="updatedPresidentPartyName" placeholder="Enter Updated Party Name">
                <input type="text" id="updatedPresidentPartyColor" placeholder="Enter Updated Party Color">
                <button onclick="updatePresident('${data.national_id}')">Update President</button>
            `;
            document.getElementById('presidentDetails').innerHTML = presidentDetails;
        })
        .catch(error => {
            console.error('Error fetching president details:', error);
        });
}

function fetchGovernorDetails() {
    var governorNationalId = document.getElementById('governorNationalId').value;

    if (!governorNationalId) {
        alert('Please enter Governor National ID.');
        return;
    }

    // Make a request to fetch governor details
    fetch('/fetch_governor_details/' + governorNationalId)
        .then(response => response.json())
        .then(data => {
            var governorDetails = `
                <p>Name: ${data.name}</p>
                <p>Party Name: ${data.party_name}</p>
                <p>County: ${data.county}</p>
                <p>Party Color: ${data.party_color}</p>
                <input type="text" id="updatedGovernorName" placeholder="Enter Updated Name">
                <input type="text" id="updatedGovernorPartyName" placeholder="Enter Updated Party Name">
                <input type="text" id="updatedGovernorCounty" placeholder="Enter Updated County">
                <select id="updatedGovernorPartyColor">
                    <option value="red">Red</option>
                    <option value="blue">Blue</option>
                    <option value="green">Green</option>
                <!-- Add more color options as needed -->
                </select>
                <button onclick="updateGovernor('${data.national_id}')">Update Governor</button>
            `;
            document.getElementById('governorDetails').innerHTML = governorDetails;
        })
        .catch(error => {
            console.error('Error fetching governor details:', error);
        });
}

function updatePresident(nationalId) {
    var updatedName = document.getElementById('updatedPresidentName').value;
    var updatedPartyName = document.getElementById('updatedPresidentPartyName').value;
    var updatedPartyColor = document.getElementById('updatedPresidentPartyColor').value;

    var updatedPresident = {
        name: updatedName,
        party_name: updatedPartyName,
        party_color: updatedPartyColor
    };

    // Make a request to update president details
    fetch('/update_president/' + nationalId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedPresident)
    })
    .then(response => response.json())
    .then(data => {
        console.log('President updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating president:', error);
    });
}

function updateGovernor(nationalId) {
    var updatedName = document.getElementById('updatedGovernorName').value;
    var updatedPartyName = document.getElementById('updatedGovernorPartyName').value;
    var updatedCounty = document.getElementById('updatedGovernorCounty').value;
    var updatedPartyColor = document.getElementById('updatedGovernorPartyColor').value;

    var updatedGovernor = {
        name: updatedName,
        party_name: updatedPartyName,
        county: updatedCounty,
        party_color: updatedPartyColor
    };

    // Make a request to update governor details
    fetch('/update_governor/' + nationalId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedGovernor)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Governor updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating governor:', error);
    });
}