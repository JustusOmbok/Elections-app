window.onload = function() {
    // Fetch and populate county select dropdown
    fetch("/admin/get_presidents")
        .then(response => response.json())
        .then(data => {
            var presidentSelect = document.getElementById("presidentSelect");
            data.presidents.forEach(president => {
                var option = document.createElement("option");
                option.value = president.national_id;
                option.text = president.name;
                option.setAttribute("national_id", president.national_id); // Add this line
                presidentSelect.appendChild(option);
            });
        });
};

function getPresidentDetails(nationalId) {
    var updateButton = document.getElementById("updateButton");
    if (updateButton) {
        updateButton.onclick = function() {
            updatePresident(nationalId); // Pass nationalId to updatePresident function
        };
    } else {
        console.error("Update button not found.");
    }
    var presidentDetails = document.getElementById("presidentDetails");
    presidentDetails.style.display = "none"; // Hide the form initially

    fetch("/admin/get_president_details/" + nationalId)
        .then(response => response.json())
        .then(data => {
            var nameInput = document.getElementById("name");
            var partyNameInput = document.getElementById("partyName");
            var partyColorInput = document.getElementById("partyColor");

            nameInput.value = data.president.name;
            partyNameInput.value = data.president.party_name;
            partyColorInput.value = data.president.party_color;

            presidentDetails.style.display = "block"; // Show the form after fetching president details
        });
}

function updatePresident(nationalId) {
    var name = document.getElementById("name").value;
    var partyName = document.getElementById("partyName").value;
    var partyColor = document.getElementById("partyColor").value;

    // Add nationalId to the form data
    var formData = new FormData();
    formData.append('national_id', nationalId);
    formData.append('name', name);
    formData.append('party_name', partyName);
    formData.append('party_color', partyColor);

    fetch("/admin/update_president", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
        } else {
            alert("Failed to update president details: " + data.message);
        }
    });
}

function setDeletePresidentId(nationalId) {
    window.currentPresidentId = nationalId;
}

function deletePresident() {
    var nationalId = document.getElementById("presidentSelect").value;
    var formData = new FormData();
    formData.append('national_id', nationalId);

    fetch("/admin/delete_president", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Reload the presidents list after deletion
            window.location.reload();
        } else {
            alert("Failed to delete president: " + data.message);
        }
    });
}