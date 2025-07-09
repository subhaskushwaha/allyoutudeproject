document.addEventListener('DOMContentLoaded', function() {
            // DOM Elements
            const container = document.getElementById('container');
            const signUpButton = document.getElementById('signUpOverlay');
            const signInButton = document.getElementById('signInOverlay');
            const signInFormButton = document.getElementById('signInButton');
            const signUpFormButton = document.getElementById('signUpButton');
            const forgotPasswordLink = document.getElementById('forgotPasswordLink');
            const backToLogin = document.getElementById('backToLogin');
            const resetPasswordButton = document.getElementById('resetPasswordButton');
            const successMessage = document.getElementById('successMessage');

            // Toggle between sign up and sign in
            signUpButton.addEventListener('click', () => {
                container.classList.add('right-panel-active');
                container.classList.remove('forgot-password-active');
            });
            signInButton.addEventListener('click', () => {
                container.classList.remove('right-panel-active');
                container.classList.remove('forgot-password-active');
            });
            // Show forgot password form
            forgotPasswordLink.addEventListener('click', (e) => {
                e.preventDefault();
                container.classList.add('forgot-password-active');
            });
            // Back to login from forgot password
            backToLogin.addEventListener('click', (e) => {
                e.preventDefault();
                container.classList.remove('forgot-password-active');
            });
            // Login success simulation
            signInFormButton.addEventListener('click', (e) => {
                e.preventDefault();
                // Validate inputs (simple validation)
                const email = document.getElementById('login-email').value;
                const password = document.getElementById('login-password').value;  
                if(email && password) {
                    // Show success message
                    successMessage.classList.add('show');
                    
                    // Hide after 3 seconds
                    setTimeout(() => {
                        successMessage.classList.remove('show');
                    }, 3000);
                    
                    // Here you would typically submit the form to your server
                    // For demo, we're just showing the success message
                } else {
                    alert('Please enter both email and password');
                }
            });
            // Sign up button handler
            signUpFormButton.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Validate inputs
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                if(name && email && password) {
                    alert('Account created successfully! Please login.');
                    container.classList.remove('right-panel-active');
                } else {
                    alert('Please fill in all fields');
                }
            });

            // Reset password handler
            resetPasswordButton.addEventListener('click', (e) => {
                e.preventDefault();
                
                const email = document.getElementById('forgot-email').value;
                
                if(email) {
                    alert('Password reset link sent to your email!');
                    container.classList.remove('forgot-password-active');
                } else {
                    alert('Please enter your email address');
                }
            });

            // Floating label effect
            const inputs = document.querySelectorAll('input');
            
            inputs.forEach(input => {
                input.addEventListener('focus', function() {
                    this.parentNode.querySelector('label').classList.add('active');
                });
                
                input.addEventListener('blur', function() {
                    if(this.value === "") {
                        this.parentNode.querySelector('label').classList.remove('active');
                    }
                });
            });

            // Button ripple effect
            const buttons = document.querySelectorAll('button:not(.ghost)');
            
            buttons.forEach(button => {
                button.addEventListener('click', function(e) {
                    const rect = this.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    const ripple = document.createElement('span');
                    ripple.classList.add('ripple-effect');
                    ripple.style.left = `${x}px`;
                    ripple.style.top = `${y}px`;
                    
                    this.appendChild(ripple);
                    
                    setTimeout(() => {
                        ripple.remove();
                    }, 1000);
                });
            });
        });
