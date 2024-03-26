function checkEnter(event) {
    if (event.keyCode === 13) { // Check if the pressed key is "Enter"
        event.preventDefault(); // Prevent form submission
        var nationalId = document.getElementById("national_id_input").value.trim(); // Get the entered national ID
        if (nationalId === "") {
            alert("Please enter your ID!");
            return;
        }
        var loggedInNationalId = "{{ session.get('national_id') }}"; // Get the national ID from the session
        if (!loggedInNationalId) {
            alert("Please log in first!");
            return;
        }
        if (loggedInNationalId !== nationalId) {
            alert("Please enter your own ID!");
            return;
        }
        fetchElectorDetails(nationalId); // Call function to fetch voter details
    }
}

function fetchElectorDetails(nationalId) {
    fetch("/get_voter_details/" + nationalId)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("county").value = data.elector.county;
                document.getElementById("name").value = data.elector.name;
                document.getElementById("phone_number").value = data.elector.phone_number;
                document.getElementById("email").value = data.elector.email;
                // Update the hidden input field with the entered national ID
                document.getElementById("hidden_national_id").value = nationalId;
                // Update the form action with the entered national ID
                var formAction = "/update/voter/" + nationalId;
                document.getElementById("updateForm").setAttribute("action", formAction);
            } else {
                alert("No voter found with the provided national ID.");
            }
        })
        .catch(error => console.error("Error:", error));
}