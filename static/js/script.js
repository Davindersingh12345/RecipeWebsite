// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Signup form validation
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate username
            const username = document.getElementById('username');
            const usernameError = document.getElementById('username-error');
            if (username.value.length < 3) {
                usernameError.textContent = 'Username must be at least 3 characters';
                usernameError.style.display = 'block';
                isValid = false;
            } else {
                usernameError.style.display = 'none';
            }
            
            // Validate email
            const email = document.getElementById('email');
            const emailError = document.getElementById('email-error');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value)) {
                emailError.textContent = 'Please enter a valid email address';
                emailError.style.display = 'block';
                isValid = false;
            } else {
                emailError.style.display = 'none';
            }
            
            // Validate password
            const password = document.getElementById('password');
            const passwordError = document.getElementById('password-error');
            if (password.value.length < 6) {
                passwordError.textContent = 'Password must be at least 6 characters';
                passwordError.style.display = 'block';
                isValid = false;
            } else {
                passwordError.style.display = 'none';
            }
            
            // Validate confirm password
            const confirmPassword = document.getElementById('confirm_password');
            const confirmPasswordError = document.getElementById('confirm-password-error');
            if (password.value !== confirmPassword.value) {
                confirmPasswordError.textContent = 'Passwords do not match';
                confirmPasswordError.style.display = 'block';
                isValid = false;
            } else {
                confirmPasswordError.style.display = 'none';
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Login form validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate username
            const username = document.getElementById('username');
            const usernameError = document.getElementById('username-error');
            if (username.value.trim() === '') {
                usernameError.textContent = 'Username is required';
                usernameError.style.display = 'block';
                isValid = false;
            } else {
                usernameError.style.display = 'none';
            }
            
            // Validate password
            const password = document.getElementById('password');
            const passwordError = document.getElementById('password-error');
            if (password.value.trim() === '') {
                passwordError.textContent = 'Password is required';
                passwordError.style.display = 'block';
                isValid = false;
            } else {
                passwordError.style.display = 'none';
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});