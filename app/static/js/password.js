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