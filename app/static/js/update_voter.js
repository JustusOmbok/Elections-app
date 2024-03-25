function checkEnter(event) {
    if (event.keyCode === 13) { // Check if the pressed key is "Enter"
        event.preventDefault(); // Prevent form submission
        var nationalId = document.getElementById("national_id_input").value; // Get the entered national ID
        fetchCandidateDetails(nationalId); // Call function to fetch candidate details
    }
}

function fetchCandidateDetails(nationalId) {
    // Make a request to the server to fetch candidate details based on the national ID
    fetch("/admin/get_voter_details/" + nationalId)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If candidate details are found, populate the form fields with the retrieved data
                document.getElementById("name").value = data.candidate.name;
                document.getElementById("county_name").value = data.voter.county;
                document.getElementById("phone_number").value = data.voter.phone_number;
                document.getElementById("email").value = data.voter.email;
            } else {
                // If no candidate is found with the provided national ID, show an alert or handle accordingly
                alert("No voter found with the provided national ID.");
            }
        })
        .catch(error => console.error("Error:", error));
}