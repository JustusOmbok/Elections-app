$(document).ready(function () {
    // President delete form submission
    $('#register_voter_form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        // Submit the form using AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                // Display the message below the button
                $('#register_voter_message').html(response);

                // Check response message and redirect accordingly
                if (response.includes("Passwords do not match. Please try again.") || response.includes("Voter already exists.")) {
                    // Redirect to homePageUrl
                    setTimeout(function () {
                        window.location.href = homePageUrl;
                    }, 3000);
                } else if (response.includes("Voter registered successfully.")) {
                    // Redirect to homePageUrl1
                    setTimeout(function () {
                        window.location.href = homePageUrl1;
                    }, 3000);
                }
            }
        });
    });
});

// JavaScript to toggle password visibility
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelectorAll('.toggle-password');

    togglePassword.forEach(function(icon) {
        icon.addEventListener('click', function() {
            const target = document.querySelector(this.getAttribute('toggle'));
            const type = target.getAttribute('type') === 'password' ? 'text' : 'password';
            target.setAttribute('type', type);
            this.classList.toggle('bi-eye');
            this.classList.toggle('bi-eye-slash');
        });
    });
});