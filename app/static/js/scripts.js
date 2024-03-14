document.addEventListener("DOMContentLoaded", function() {
    // JavaScript to handle vote submission
    document.getElementById('voteButton').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Show "Thanks for voting" message
        var voteMessage = document.createElement('p');
        voteMessage.textContent = "Thanks for voting";
        document.getElementById('voteButton').insertAdjacentElement('afterend', voteMessage);
    });
});