window.onload = function() {
    fetch("/admin/get_counties")
        .then(response => response.json())
        .then(data => {
            var countySelect = document.getElementById("countySelect");
            var uniqueCounties = [...new Set(data.counties)]; // Remove duplicates
            uniqueCounties.forEach(county => {
                var option = document.createElement("option");
                option.value = county;
                option.text = county;
                countySelect.appendChild(option);
            });
        });
};

function getGovernors() {
    var county = document.getElementById("countySelect").value;
    fetch("/admin/get_governors_by_county", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "county=" + encodeURIComponent(county)
    })
    .then(response => response.json())
    .then(data => {
        var governorsList = document.getElementById("governorsList");
        governorsList.innerHTML = "";
        data.governors.forEach(governor => {
            governorsList.innerHTML += `<button type="button" class="btn btn-primary" onclick="getGovernorDetails('${governor.national_id}')">${governor.name}</button>`;
        });
    });
}

function getGovernorDetails(nationalId) {
    var governorDetails = document.getElementById("governorDetails");
    governorDetails.style.display = "none"; // Hide the form initially

    fetch("/admin/get_governor_details/" + nationalId)
        .then(response => response.json())
        .then(data => {
            governorDetails.innerHTML = `
                <h2>Governor Details</h2>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="name" value="${data.candidate.name}">
                    <label for="name">Name:</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="partyName" value="${data.candidate.party_name}">
                    <label for="partyName">Party Name:</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="color" class="form-control" id="partyColor" name="partyColor" value="${data.candidate.party_color}">
                    <label for="partyColor">Party Color:</label>
                </div>
                <div class="form-floating mb-3">
                    <input class="form-control" id="county" name="county" value="${data.candidate.county}">
                    <label for="county">County</label>
                </div>
                <button type="button" class="btn btn-primary" onclick="updateGovernor('${nationalId}')">Update</button>
                <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteConfirmationModal" onclick="setDeleteGovernorId('${nationalId}')">Delete</button>
            `;
            governorDetails.style.display = "block"; // Show the form after fetching governor details
        });
}

function editGovernor(nationalId) {
    window.location.href = "/admin/update/governor/" + nationalId;
}

function updateGovernor(nationalId) {
    var name = document.getElementById("name").value;
    var partyName = document.getElementById("partyName").value;
    var partyColor = document.getElementById("partyColor").value;
    var county = document.getElementById("county").value;

    // Add nationalId to the form data
    var formData = new FormData();
    formData.append('national_id', nationalId);
    formData.append('name', name);
    formData.append('party_name', partyName);
    formData.append('party_color', partyColor);
    formData.append('county', county);

    fetch("/admin/update_governor", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
        } else {
            alert("Failed to update governor details: " + data.message);
        }
    });
}

function setDeleteGovernorId(nationalId) {
    window.currentGovernorId = nationalId;
}

function deleteGovernor() {
    var nationalId = window.currentGovernorId;
    var formData = new FormData();
    formData.append('national_id', nationalId);

    fetch("/admin/delete_governor", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Reload the governors list after deletion
            window.location.reload();
        } else {
            alert("Failed to delete governor: " + data.message);
        }
    });
}