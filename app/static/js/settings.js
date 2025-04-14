document.addEventListener('DOMContentLoaded', () => {
    // Get current user from localStorage
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    if (!currentUser) {
        window.location.href = 'index.html';
        return;
    }
    
    // Display user info
    document.getElementById('user-name').textContent = currentUser.name;
    document.getElementById('user-email').textContent = currentUser.email;
    
    // Populate account form
    document.getElementById('settings-name').value = currentUser.name;
    document.getElementById('settings-email').value = currentUser.email;
    
    // Update account info
    document.getElementById('account-form').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const newName = document.getElementById('settings-name').value.trim();
        const newEmail = document.getElementById('settings-email').value.trim();
        
        if (!newName || !newEmail) {
            alert('Please fill in all fields');
            return;
        }
        
        const users = JSON.parse(localStorage.getItem('users'));
        const userIndex = users.findIndex(u => u.id === currentUser.id);
        
        // Check if email is already taken by another user
        if (newEmail !== currentUser.email && users.some(u => u.email === newEmail && u.id !== currentUser.id)) {
            alert('This email is already in use by another account');
            return;
        }
        
        // Update user info
        currentUser.name = newName;
        currentUser.email = newEmail;
        
        // Update localStorage
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        users[userIndex] = currentUser;
        localStorage.setItem('users', JSON.stringify(users));
        
        // Update displayed info
        document.getElementById('user-name').textContent = newName;
        document.getElementById('user-email').textContent = newEmail;
        
        alert('Account information updated successfully');
    });
    
    // Change password
    document.getElementById('password-form').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        if (currentUser.password !== currentPassword) {
            alert('Current password is incorrect');
            return;
        }
        
        if (newPassword !== confirmPassword) {
            alert('New passwords do not match');
            return;
        }
        
        if (newPassword.length < 6) {
            alert('Password must be at least 6 characters long');
            return;
        }
        
        const users = JSON.parse(localStorage.getItem('users'));
        const userIndex = users.findIndex(u => u.id === currentUser.id);
        
        // Update password
        currentUser.password = newPassword;
        
        // Update localStorage
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        users[userIndex] = currentUser;
        localStorage.setItem('users', JSON.stringify(users));
        
        // Clear form
        document.getElementById('password-form').reset();
        
        alert('Password changed successfully');
    });
    
    // Reset progress
    document.getElementById('reset-progress-btn').addEventListener('click', () => {
        if (!confirm('Are you sure you want to reset all your progress? This cannot be undone.')) return;
        
        const users = JSON.parse(localStorage.getItem('users'));
        const userIndex = users.findIndex(u => u.id === currentUser.id);
        
        // Reset habits and streaks
        currentUser.habits.forEach(habit => {
            habit.completions = [];
        });
        currentUser.streaks = 0;
        
        // Update localStorage
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        users[userIndex] = currentUser;
        localStorage.setItem('users', JSON.stringify(users));
        
        alert('All progress has been reset');
    });
    
    // Delete account
    document.getElementById('delete-account-btn').addEventListener('click', () => {
        if (!confirm('Are you sure you want to delete your account? All your data will be permanently lost.')) return;
        
        const users = JSON.parse(localStorage.getItem('users'));
        const updatedUsers = users.filter(u => u.id !== currentUser.id);
        
        // Update localStorage
        localStorage.setItem('users', JSON.stringify(updatedUsers));
        localStorage.removeItem('currentUser');
        
        // Redirect to login page
        window.location.href = 'index.html';
    });
});

function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'index.html';
}
