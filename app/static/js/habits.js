document.addEventListener('DOMContentLoaded', () => {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) {
        window.location.href = 'index.html';
        return;
    }
    
    // Display user info
    document.getElementById('user-name').textContent = currentUser.name;
    document.getElementById('user-email').textContent = currentUser.email;
    
    // Load habits
    loadHabits();
    
    // Add new habit
    document.getElementById('add-habit-btn').addEventListener('click', (e) => {
        e.preventDefault();
        const habitName = document.getElementById('new-habit-name').value.trim();
        const habitColor = document.getElementById('new-habit-color').value;
        
        if (!habitName) return;
        
        addHabit(habitName, habitColor);
        document.getElementById('new-habit-name').value = '';
    });
});

function loadHabits() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const habitsList = document.querySelector('.habits-list');
    habitsList.innerHTML = '';
    
    if (!currentUser.habits || currentUser.habits.length === 0) {
        const noHabits = document.createElement('div');
        noHabits.className = 'no-habits';
        noHabits.textContent = 'No habits to display. Add your first habit below.';
        habitsList.appendChild(noHabits);
        return;
    }
    
    currentUser.habits.forEach(habit => {
        const habitItem = document.createElement('div');
        habitItem.className = 'habit-item';
        
        const habitInfo = document.createElement('div');
        habitInfo.className = 'habit-info';
        
        const colorIndicator = document.createElement('span');
        colorIndicator.className = 'color-indicator';
        colorIndicator.style.backgroundColor = habit.color || '#4A90E2';
        
        const habitName = document.createElement('span');
        habitName.className = 'habit-name';
        habitName.textContent = habit.name;
        
        const habitCount = document.createElement('span');
        habitCount.className = 'habit-count';
        habitCount.textContent = `Completed ${habit.completions ? habit.completions.length : 0} times`;
        
        habitInfo.appendChild(colorIndicator);
        habitInfo.appendChild(habitName);
        habitInfo.appendChild(habitCount);
        
        const habitActions = document.createElement('div');
        habitActions.className = 'habit-actions';
        
        const colorPicker = document.createElement('input');
        colorPicker.type = 'color';
        colorPicker.value = habit.color || '#4A90E2';
        colorPicker.dataset.habitId = habit.id;
        colorPicker.className = 'color-picker';
        colorPicker.addEventListener('change', (e) => {
            updateHabitColor(habit.id, e.target.value);
        });
        
        const editBtn = document.createElement('button');
        editBtn.className = 'btn btn-secondary';
        editBtn.textContent = 'Edit';
        editBtn.addEventListener('click', () => editHabit(habit.id));
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger';
        deleteBtn.textContent = 'Delete';
        deleteBtn.addEventListener('click', () => deleteHabit(habit.id));
        
        habitActions.appendChild(colorPicker);
        habitActions.appendChild(editBtn);
        habitActions.appendChild(deleteBtn);
        
        habitItem.appendChild(habitInfo);
        habitItem.appendChild(habitActions);
        habitsList.appendChild(habitItem);
    });
}

function addHabit(name, color) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const users = JSON.parse(localStorage.getItem('users'));
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    // Initialize habits array if it doesn't exist
    if (!currentUser.habits) {
        currentUser.habits = [];
    }
    
    // Create new habit
    const newHabit = {
        id: `habit-${Date.now()}`,
        name,
        color,
        completions: []
    };
    
    // Add to user's habits
    currentUser.habits.push(newHabit);
    
    // Update localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    users[userIndex] = currentUser;
    localStorage.setItem('users', JSON.stringify(users));
    
    // Reload habits list
    loadHabits();
}

function updateHabitColor(habitId, color) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const users = JSON.parse(localStorage.getItem('users'));
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    const habitIndex = currentUser.habits.findIndex(h => h.id === habitId);
    if (habitIndex === -1) return;
    
    // Update habit color
    currentUser.habits[habitIndex].color = color;
    
    // Update localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    users[userIndex] = currentUser;
    localStorage.setItem('users', JSON.stringify(users));
    
    // Reload habits list
    loadHabits();
}

function editHabit(habitId) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const habit = currentUser.habits.find(h => h.id === habitId);
    
    if (!habit) return;
    
    const newName = prompt('Enter new habit name:', habit.name);
    if (!newName || newName.trim() === '') return;
    
    const users = JSON.parse(localStorage.getItem('users'));
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    // Update habit name
    habit.name = newName.trim();
    
    // Update localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    users[userIndex] = currentUser;
    localStorage.setItem('users', JSON.stringify(users));
    
    // Reload habits list
    loadHabits();
}

function deleteHabit(habitId) {
    if (!confirm('Are you sure you want to delete this habit? This cannot be undone.')) return;
    
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const users = JSON.parse(localStorage.getItem('users'));
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    // Remove habit from array
    currentUser.habits = currentUser.habits.filter(h => h.id !== habitId);
    
    // Update localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    users[userIndex] = currentUser;
    localStorage.setItem('users', JSON.stringify(users));
    
    // Reload habits list
    loadHabits();
}
