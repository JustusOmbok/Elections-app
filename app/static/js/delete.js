$(document).ready(function () {
    // President delete form submission
    $('#delete_president_form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        // Submit the form using AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                // Display the message below the delete button
                $('#delete_president_message').html(response);

                // Wait for 3 seconds
                setTimeout(function () {
                    // Redirect to admin dashboard after displaying the message
                    window.location.href = homePageUrl;
                }, 3000);
            }
        });
    });

    // Governor delete form submission
    $('#delete_governor_form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        // Submit the form using AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                // Display the message below the delete button
                $('#delete_governor_message').html(response);

                // Wait for 3 seconds
                setTimeout(function () {
                    // Redirect to admin dashboard after displaying the message
                    window.location.href = homePageUrl;
                }, 3000);
            }
        });
    });

    // Voter delete form submission
    $('#delete_voter_form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        // Submit the form using AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                // Display the message below the delete button
                $('#delete_voter_message').html(response);

                // Wait for 3 seconds
                setTimeout(function () {
                    // Redirect to admin dashboard after displaying the message
                    window.location.href = homePageUrl;
                }, 3000);
            }
        });
    });
});