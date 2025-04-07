// Save user to localStorage
function saveUser(username, email) {
    const user = {
        username: username,
        email: email,
        lastLogin: new Date().toISOString()
    };
    localStorage.setItem('habitTrackerUser', JSON.stringify(user));
    return user;
}

// Check for existing user
function checkAuth() {
    // Only run on dashboard page
    if (!window.location.pathname.includes('dashboard.html')) return;
    
    const user = JSON.parse(localStorage.getItem('habitTrackerUser'));
    if (!user) {
        window.location.href = 'index.html';
        return;
    }
    
    // Update welcome message
    document.getElementById('welcomeUser').textContent = user.username;
    document.getElementById('userEmail').textContent = user.email;
    
    // Update "Welcome back" message with last login if available
    const welcomeMsg = document.querySelector('.welcome-message h2');
    if (welcomeMsg) {
        const lastLogin = user.lastLogin ? new Date(user.lastLogin) : null;
        welcomeMsg.textContent = lastLogin ? 
            `Welcome back ${user.username}` : 
            `Welcome ${user.username}`;
    }
}

// Login form handler
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    
    if (username && email) {
        saveUser(username, email);
        window.location.href = 'dashboard.html';
    }
});

// Check authentication on page load
document.addEventListener('DOMContentLoaded', checkAuth);