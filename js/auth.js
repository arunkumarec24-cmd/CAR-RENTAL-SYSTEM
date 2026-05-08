// ==========================================
// AUTH.JS - Enhanced Authentication Logic
// ==========================================

// Tab Switching
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Remove active class from all tabs
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

// Toast Notification Function
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = toast.querySelector('.toast-message');
    
    // Remove all type classes
    toast.classList.remove('success', 'error', 'warning', 'info');
    
    // Add appropriate type class
    toast.classList.add(type);
    
    // Set message
    toastMessage.textContent = message;
    
    // Show toast
    toast.classList.add('show');
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Show/Hide Loading Overlay
function showLoading(show = true) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

// Listen for auth state changes
auth.onAuthStateChanged((user) => {
    if (user) {
        // User is signed in, redirect to dashboard
        console.log('User logged in:', user.email);
        window.location.href = "dashboard.html";
    }
});

// ==========================================
// SIGN IN HANDLERS
// ==========================================

// Email Sign In
document.getElementById('email-login-btn').addEventListener('click', () => {
    const email = document.getElementById('signin-email').value.trim();
    const password = document.getElementById('signin-password').value;
    
    // Validation
    if (!email || !password) {
        showToast('Please enter both email and password.', 'warning');
        return;
    }

    if (!validateEmail(email)) {
        showToast('Please enter a valid email address.', 'error');
        return;
    }

    showLoading(true);

    auth.signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log("Logged in with Email:", userCredential.user.email);
            showToast('Login successful! Redirecting...', 'success');
            // Redirect happens automatically via onAuthStateChanged
        })
        .catch((error) => {
            showLoading(false);
            console.error('Login Error:', error);
            
            let errorMessage = 'Login failed. Please try again.';
            
            switch(error.code) {
                case 'auth/user-not-found':
                    errorMessage = 'No account found with this email.';
                    break;
                case 'auth/wrong-password':
                    errorMessage = 'Incorrect password. Please try again.';
                    break;
                case 'auth/invalid-email':
                    errorMessage = 'Invalid email address format.';
                    break;
                case 'auth/user-disabled':
                    errorMessage = 'This account has been disabled.';
                    break;
                case 'auth/too-many-requests':
                    errorMessage = 'Too many failed attempts. Please try again later.';
                    break;
                default:
                    errorMessage = error.message;
            }
            
            showToast(errorMessage, 'error');
        });
});

// Google Sign In
document.getElementById('google-login-btn').addEventListener('click', () => {
    showLoading(true);
    const provider = new firebase.auth.GoogleAuthProvider();
    
    auth.signInWithPopup(provider)
        .then((result) => {
            console.log("Logged in with Google:", result.user.email);
            showToast('Google login successful!', 'success');
            // Redirect happens automatically via onAuthStateChanged
        })
        .catch((error) => {
            showLoading(false);
            console.error('Google Login Error:', error);
            
            let errorMessage = 'Google login failed. Please try again.';
            
            if (error.code === 'auth/popup-closed-by-user') {
                errorMessage = 'Login cancelled.';
            } else if (error.code === 'auth/popup-blocked') {
                errorMessage = 'Popup blocked. Please allow popups for this site.';
            }
            
            showToast(errorMessage, 'error');
        });
});

// ==========================================
// SIGN UP HANDLERS
// ==========================================

// Email Sign Up
document.getElementById('email-signup-btn').addEventListener('click', () => {
    const name = document.getElementById('signup-name').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    const agreedToTerms = document.getElementById('agree-terms').checked;
    
    // Validation
    if (!name || !email || !password) {
        showToast('Please fill in all fields.', 'warning');
        return;
    }

    if (!validateEmail(email)) {
        showToast('Please enter a valid email address.', 'error');
        return;
    }

    if (password.length < 6) {
        showToast('Password must be at least 6 characters long.', 'error');
        return;
    }

    if (!agreedToTerms) {
        showToast('Please agree to the Terms & Conditions.', 'warning');
        return;
    }

    showLoading(true);

    auth.createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            // Update user profile with name
            return userCredential.user.updateProfile({
                displayName: name
            }).then(() => {
                // Create user document in Firestore
                return db.collection('users').doc(userCredential.user.uid).set({
                    name: name,
                    email: email,
                    role: 'customer',
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    photoURL: userCredential.user.photoURL || null
                });
            }).then(() => {
                console.log("Account created:", userCredential.user.email);
                showToast('Account created successfully!', 'success');
                // Redirect happens automatically via onAuthStateChanged
            });
        })
        .catch((error) => {
            showLoading(false);
            console.error('Signup Error:', error);
            
            let errorMessage = 'Sign up failed. Please try again.';
            
            switch(error.code) {
                case 'auth/email-already-in-use':
                    errorMessage = 'This email is already registered. Please sign in.';
                    break;
                case 'auth/invalid-email':
                    errorMessage = 'Invalid email address format.';
                    break;
                case 'auth/weak-password':
                    errorMessage = 'Password is too weak. Use at least 6 characters.';
                    break;
                case 'auth/operation-not-allowed':
                    errorMessage = 'Email/password accounts are not enabled.';
                    break;
                default:
                    errorMessage = error.message;
            }
            
            showToast(errorMessage, 'error');
        });
});

// Google Sign Up
document.getElementById('google-signup-btn').addEventListener('click', () => {
    showLoading(true);
    const provider = new firebase.auth.GoogleAuthProvider();
    
    auth.signInWithPopup(provider)
        .then((result) => {
            const user = result.user;
            
            // Check if this is a new user
            if (result.additionalUserInfo.isNewUser) {
                // Create user document in Firestore
                return db.collection('users').doc(user.uid).set({
                    name: user.displayName,
                    email: user.email,
                    role: 'customer',
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    photoURL: user.photoURL
                }).then(() => {
                    console.log("Google account created:", user.email);
                    showToast('Account created with Google!', 'success');
                });
            } else {
                console.log("Logged in with Google:", user.email);
                showToast('Google login successful!', 'success');
            }
            // Redirect happens automatically via onAuthStateChanged
        })
        .catch((error) => {
            showLoading(false);
            console.error('Google Signup Error:', error);
            
            let errorMessage = 'Google sign up failed. Please try again.';
            
            if (error.code === 'auth/popup-closed-by-user') {
                errorMessage = 'Sign up cancelled.';
            } else if (error.code === 'auth/popup-blocked') {
                errorMessage = 'Popup blocked. Please allow popups for this site.';
            }
            
            showToast(errorMessage, 'error');
        });
});

// ==========================================
// HELPER FUNCTIONS
// ==========================================

// Email Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Enter key support for login
document.getElementById('signin-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('email-login-btn').click();
    }
});

document.getElementById('signup-password').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('email-signup-btn').click();
    }
});
