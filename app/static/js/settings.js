document.addEventListener('DOMContentLoaded', () => {
   
    // Display user info
    document.getElementById('user-name').textContent = currentUser.name;
    document.getElementById('user-email').textContent = currentUser.email;
    
    // Populate account form
    document.getElementById('settings-name').value = currentUser.name;
    document.getElementById('settings-email').value = currentUser.email;
        
    // Update form listener
    document.getElementById('account-form').addEventListener('submit', (e) => {
        e.preventDefault();

        const newName = document.getElementById('settings-name').value.trim();
        const newEmail = document.getElementById('settings-email').value.trim();

        if (!newName || !newEmail) {
            alert('Please fill in all fields');
            return;
        }

        fetch('/update-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: newName, email: newEmail })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert('User updated!');
                document.getElementById('user-name').textContent = data.user.name;
                document.getElementById('user-email').textContent = data.user.email;
            }
        })
        .catch(err => {
            console.error(err);
            alert('Something went wrong.');
        });
    });
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
        
        
        // Clear form
        document.getElementById('password-form').reset();
        
        alert('Password changed successfully');
    });
    
    // Reset progress
    document.getElementById('reset-progress-btn').addEventListener('click', () => {
        if (!confirm('Are you sure you want to reset all your progress? This cannot be undone.')) return;
        
        
        // Reset habits and streaks
        currentUser.habits.forEach(habit => {
            habit.completions = [];
        });
        currentUser.streaks = 0;
        
    });
    
    // Delete account
    document.getElementById('delete-account-btn').addEventListener('click', () => {
        if (!confirm('Are you sure you want to delete your account? All your data will be permanently lost.')) return;
    }