// dashboard.js - Handles Dashboard UI and data fetching

// Check Auth State
auth.onAuthStateChanged((user) => {
    if (!user) {
        // Not logged in, redirect to login page
        window.location.href = "index.html";
    } else {
        // Update User Profile UI
        document.getElementById('user-name').innerText = user.displayName || user.email;
        if (user.photoURL) {
            document.getElementById('user-pfp').src = user.photoURL;
        }
        
        // Initialize dashboard data
        loadDashboardStats();
    }
});

// Logout
document.getElementById('logout-btn').addEventListener('click', () => {
    auth.signOut().then(() => {
        window.location.href = "index.html";
    });
});

// Clock
function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleString();
}
setInterval(updateClock, 1000);
updateClock();

// Mock Data Loader (Since Firestore is empty initially)
function loadDashboardStats() {
    // In a real app, you would query db.collection('cars'), etc.
    // Example:
    // db.collection('rentals').get().then(snap => { ... });
    
    // For demonstration, setting dummy values:
    document.getElementById('stat-available').innerText = "12";
    document.getElementById('stat-rented').innerText = "5";
    document.getElementById('stat-customers').innerText = "24";
    document.getElementById('stat-revenue').innerText = "₹45,200";
    
    const tbody = document.getElementById('recent-rentals-body');
    tbody.innerHTML = `
        <tr>
            <td>#RNT-001</td>
            <td>John Doe</td>
            <td>Toyota Camry</td>
            <td><span style="color: #2ECC71;">Active</span></td>
            <td>₹2,500</td>
        </tr>
        <tr>
            <td>#RNT-002</td>
            <td>Jane Smith</td>
            <td>Honda Civic</td>
            <td><span style="color: #F39C12;">Pending</span></td>
            <td>₹1,800</td>
        </tr>
    `;
}
