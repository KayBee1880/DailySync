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
    
    // Add custom habit
    document.getElementById('add-custom-habit').addEventListener('click', (e) => {
        e.preventDefault();
        const customHabitInput = document.getElementById('custom-habit-input');
        const habitName = customHabitInput.value.trim();
        
        if (!habitName) return;
        
        // Create checkbox for the custom habit
        const habitId = `habit-${habitName.toLowerCase().replace(/\s+/g, '-')}`;
        const habitOption = document.createElement('div');
        habitOption.className = 'habit-option';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = habitId;
        checkbox.value = habitName;
        
        const label = document.createElement('label');
        label.htmlFor = habitId;
        label.textContent = habitName;
        
        habitOption.appendChild(checkbox);
        habitOption.appendChild(label);
        
        // Insert before the custom-habit div
        const habitSelection = document.querySelector('.habit-selection');
        habitSelection.insertBefore(habitOption, document.querySelector('.custom-habit'));
        
        // Clear input
        customHabitInput.value = '';
    });
    
    // Complete setup
    document.getElementById('complete-setup').addEventListener('click', (e) => {
        e.preventDefault();
        
        // Get selected habits
        const selectedHabits = [];
        document.querySelectorAll('.habit-option input[type="checkbox"]:checked').forEach(checkbox => {
            selectedHabits.push(checkbox.value);
        });
        
        if (selectedHabits.length === 0) {
            alert('Please select at least one habit to track');
            return;
        }
        
        // Get tracking frequency
        const trackingFrequency = document.getElementById('tracking-frequency').value;
        
        // Update current user with habits
        const users = JSON.parse(localStorage.getItem('users'));
        const userIndex = users.findIndex(u => u.id === currentUser.id);
        
        currentUser.habits = selectedHabits.map(habitName => ({
            id: `habit-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
            name: habitName,
            frequency: trackingFrequency,
            completions: []
        }));
        
        // Update localStorage
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        users[userIndex] = currentUser;
        localStorage.setItem('users', JSON.stringify(users));
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    });
});
