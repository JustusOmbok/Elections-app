document.addEventListener('DOMContentLoaded', function () {
    const voteTypeDropdownItems = document.querySelectorAll('[data-vote-type]');
    const votingContent = document.getElementById('votingContent');
    const submitVoteBtn = document.getElementById('submitVoteBtn');

    voteTypeDropdownItems.forEach(function (item) {
        item.addEventListener('click', function (event) {
            event.preventDefault();
            const voteType = this.getAttribute('data-vote-type');

            // Fetch candidates based on vote type (president or governor)
            fetchCandidates(voteType);
        });
    });

    function fetchCandidates(voteType) {
        // You can implement fetching candidates from your backend here
        // For demonstration purposes, I'll simulate fetching candidates
        let candidates = [];
        if (voteType === 'president') {
            candidates = ['Candidate A', 'Candidate B', 'Candidate C'];
        } else if (voteType === 'governor') {
            // Fetch governor candidates based on the voter's registered county
            candidates = ['Candidate X', 'Candidate Y', 'Candidate Z'];
        }

        displayCandidates(candidates);
    }

    function displayCandidates(candidates) {
        let candidatesHTML = '<h4 class="text-center mb-3">Select Candidate:</h4>';
        candidates.forEach(function (candidate) {
            candidatesHTML += `
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="candidate" id="${candidate}" value="${candidate}">
                    <label class="form-check-label" for="${candidate}">
                        ${candidate}
                    </label>
                </div>
            `;
        });
        votingContent.innerHTML = candidatesHTML;
    }

    // Add event listener for submitting the vote
    submitVoteBtn.addEventListener('click', function () {
        // Get the selected candidate and submit the vote
        const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
        if (selectedCandidate) {
            const selectedCandidateName = selectedCandidate.value;
            // Implement code to submit the vote with the selected candidate
            alert(`You have voted for ${selectedCandidateName}`);
        } else {
            alert('Please select a candidate before submitting.');
        }
    });
});