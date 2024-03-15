document.addEventListener("DOMContentLoaded", function() {
    // JavaScript to handle vote submission
    document.getElementById('voteForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Make an AJAX request to check if the voter has already voted
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/check_vote', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.alreadyVoted) {
                        // Show "You already voted" message
                        var voteMessage = document.createElement('p');
                        voteMessage.textContent = "You already voted";
                        document.getElementById('voteButton').insertAdjacentElement('afterend', voteMessage);
                        
                        // Redirect to home page after displaying the message
                        setTimeout(function() {
                            window.location.href = homePageUrl;
                        }, 1500); // Redirect after 1.5 seconds
                    } else {
                        // Show "Thanks for voting" message and submit the form
                        var voteMessage = document.createElement('p');
                        voteMessage.textContent = "Thanks for voting";
                        document.getElementById('voteButton').insertAdjacentElement('afterend', voteMessage);

                        // After displaying the message, submit the form
                        setTimeout(function() {
                            document.getElementById('voteForm').submit();
                        }, 2000); // Submit the form after 1.5 seconds
                    }
                } else {
                    console.error('Error: Unable to check vote status');
                }
            }
        };
        xhr.send();
    });
});