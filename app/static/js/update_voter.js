// Fetch voter details when the page loads
document.addEventListener("DOMContentLoaded", function() {
    fetch("/update_voter")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("county").value = data.elector.county;
                document.getElementById("name").value = data.elector.name;
                document.getElementById("phone_number").value = data.elector.phone_number;
                document.getElementById("email").value = data.elector.email;
            } else {
                alert("Failed to fetch voter details.");
            }
        })
        .catch(error => console.error("Error:", error));
});