// Function to display success message and redirect
const urlParams = new URLSearchParams(window.location.search);
const successMessage = urlParams.get('success');
// If success message exists, display it and then redirect
if (successMessage === 'true') {
    alert("President registered successfully");
    window.location.replace("/admin_dashboard");
}