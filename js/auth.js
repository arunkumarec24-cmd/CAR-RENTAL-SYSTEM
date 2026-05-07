// auth.js - Handles Login Operations

// Listen for auth state changes
auth.onAuthStateChanged((user) => {
    if (user) {
        // User is signed in, redirect to dashboard
        window.location.href = "dashboard.html";
    }
});

// Google Login
document.getElementById('google-login-btn').addEventListener('click', () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider)
        .then((result) => {
            console.log("Logged in with Google", result.user);
        })
        .catch((error) => {
            alert("Google Login Error: " + error.message);
        });
});

// Email Login
document.getElementById('email-login-btn').addEventListener('click', () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    auth.signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            console.log("Logged in with Email", userCredential.user);
        })
        .catch((error) => {
            alert("Login Error: " + error.message);
        });
});
