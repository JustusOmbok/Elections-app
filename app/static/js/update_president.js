function checkEnter(event) {
    if (event.keyCode === 13) { // Check if the pressed key is "Enter"
        event.preventDefault(); // Prevent form submission
        var nationalId = document.getElementById("national_id_input").value; // Get the entered national ID
        fetchCandidateDetails(nationalId); // Call function to fetch candidate details
    }
}

function fetchCandidateDetails(nationalId) {
    fetch("/admin/get_president_details/" + nationalId)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("name").value = data.candidate.name;
                document.getElementById("party_name").value = data.candidate.party_name;
                document.getElementById("party_color").value = data.candidate.party_color;
                // Update the hidden input field with the entered national ID
                document.getElementById("hidden_national_id").value = nationalId;
                // Update the form action with the entered national ID
                var formAction = "/admin/update/president/" + nationalId;
                document.getElementById("updateForm").setAttribute("action", formAction);
            } else {
                alert("No president found with the provided national ID.");
            }
        })
        .catch(error => console.error("Error:", error));
}