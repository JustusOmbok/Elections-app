function displayPresidentCandidates() {
    // This function should fetch president candidates' information from the backend and dynamically update the voting section
    // For demonstration purposes, let's assume you have an array of candidate objects containing their party, name, etc.
    var candidates = [
        { party: "Example Party", name: "John Doe" },
        { party: "Sample Party", name: "Jane Smith" }
    ];

    // Construct HTML for displaying candidates and voting box
    var html = "<h2 class='fw-bolder'>President Candidates</h2>";
    candidates.forEach(function(candidate, index) {
        html += "<div class='card mb-3'>";
        html += "<div class='card-body'>";
        html += "<h5 class='card-title'>" + candidate.name + " - " + candidate.party + "</h5>";
        html += "<input type='radio' id='presidentCandidate" + index + "' name='presidentCandidate' value='" + candidate.name + "'>";
        html += "<label for='presidentCandidate" + index + "'>Vote for " + candidate.name + "</label>";
        html += "</div>";
        html += "</div>";
    });

    // Display the HTML in the voting section
    document.getElementById("votingSection").innerHTML = html;
}

function displayGovernorCandidates() {
    // This function should fetch governor candidates' information from the backend and dynamically update the voting section
    // For demonstration purposes, let's assume you have an array of candidate objects containing their county, name, etc.
    var candidates = [
        { county: "Example County", name: "Jane Smith" },
        { county: "Sample County", name: "John Doe" }
    ];

    // Construct HTML for displaying candidates and voting box
    var html = "<h2 class='fw-bolder'>Governor Candidates</h2>";
    candidates.forEach(function(candidate, index) {
        html += "<div class='card mb-3'>";
        html += "<div class='card-body'>";
        html += "<h5 class='card-title'>" + candidate.name + " - " + candidate.county + "</h5>";
        html += "<input type='radio' id='governorCandidate" + index + "' name='governorCandidate' value='" + candidate.name + "'>";
        html += "<label for='governorCandidate" + index + "'>Vote for " + candidate.name + "</label>";
        html += "</div>";
        html += "</div>";
    });

    // Display the HTML in the voting section
    document.getElementById("votingSection").innerHTML = html;
}