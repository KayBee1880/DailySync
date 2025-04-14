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
    document.getElementById('welcome-text').textContent = `Welcome back, ${currentUser.name}`;
    
    // Initialize time period
    let currentPeriod = 'week';
    updateTimeDisplay(currentPeriod);
    
    // Time period selector event listeners
    document.querySelectorAll('.time-period-btn').forEach(button => {
        button.addEventListener('click', () => {
            currentPeriod = button.dataset.period;
            document.querySelectorAll('.time-period-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            updateTimeDisplay(currentPeriod);
            updateHabitGrid(currentPeriod);
            updateChart(currentPeriod);
        });
    });
    
    // Initialize view
    updateHabitGrid(currentPeriod);
    updateTodayHabits();
    updateChart(currentPeriod);
    checkStreak();
});

function updateTimeDisplay(period) {
    const today = new Date();
    let displayText = '';
    
    switch(period) {
        case 'week':
            const startOfWeek = new Date(today);
            startOfWeek.setDate(today.getDate() - today.getDay());
            displayText = `${formatDate(startOfWeek)} - ${formatDate(today)}`;
            break;
        case 'month':
            const monthName = today.toLocaleString('default', { month: 'long' });
            displayText = `${monthName} ${today.getFullYear()}`;
            break;
        case 'year':
            displayText = today.getFullYear().toString();
            break;
        case 'all':
            displayText = 'All Time';
            break;
    }
    
    document.getElementById('current-period-range').textContent = displayText;
}

function formatDate(date) {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function updateHabitGrid(period) {
    const habitGrid = document.querySelector('.habit-grid');
    habitGrid.innerHTML = '';
    
    // Add header row
    const headerRow = document.createElement('div');
    headerRow.className = 'habit-grid-header';
    headerRow.textContent = 'Habit';
    habitGrid.appendChild(headerRow);
    
    // Add day headers
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    days.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'habit-grid-header';
        dayHeader.textContent = day;
        habitGrid.appendChild(dayHeader);
    });
    
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser.habits || currentUser.habits.length === 0) {
        const noHabits = document.createElement('div');
        noHabits.className = 'no-habits';
        noHabits.textContent = 'No habits to display. Add some habits first.';
        noHabits.style.gridColumn = '1 / -1';
        noHabits.style.textAlign = 'center';
        noHabits.style.padding = '20px';
        habitGrid.appendChild(noHabits);
        return;
    }
    
    // Add habit rows
    currentUser.habits.forEach(habit => {
        // Habit name cell with color indicator
        const habitNameCell = document.createElement('div');
        habitNameCell.className = 'habit-name-cell';
        
        const colorIndicator = document.createElement('span');
        colorIndicator.className = 'color-indicator';
        colorIndicator.style.backgroundColor = habit.color || '#4A90E2';
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = habit.name;
        
        habitNameCell.appendChild(colorIndicator);
        habitNameCell.appendChild(nameSpan);
        habitGrid.appendChild(habitNameCell);
        
        // Day cells
        for (let i = 0; i < 7; i++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'habit-day-cell';
            
            const dayDate = new Date();
            dayDate.setDate(dayDate.getDate() - (dayDate.getDay() - i));
            const dateStr = dayDate.toISOString().split('T')[0];
            
            if (habit.completions && habit.completions.includes(dateStr)) {
                dayCell.classList.add('habit-completed');
                dayCell.style.backgroundColor = habit.color || '#4A90E2';
                dayCell.textContent = '✓';
            }
            
            dayCell.addEventListener('click', () => toggleHabitCompletion(habit.id, dateStr));
            habitGrid.appendChild(dayCell);
        }
    });
}

function toggleHabitCompletion(habitId, dateStr) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const users = JSON.parse(localStorage.getItem('users'));
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    const habitIndex = currentUser.habits.findIndex(h => h.id === habitId);
    if (habitIndex === -1) return;
    
    // Initialize completions array if it doesn't exist
    if (!currentUser.habits[habitIndex].completions) {
        currentUser.habits[habitIndex].completions = [];
    }
    
    // Toggle completion status
    const completions = currentUser.habits[habitIndex].completions;
    const completionIndex = completions.indexOf(dateStr);
    
    if (completionIndex === -1) {
        completions.push(dateStr);
    } else {
        completions.splice(completionIndex, 1);
    }
    
    // Update localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    users[userIndex] = currentUser;
    localStorage.setItem('users', JSON.stringify(users));
    
    // Update UI
    const currentPeriod = document.querySelector('.time-period-btn.active').dataset.period;
    updateHabitGrid(currentPeriod);
    updateTodayHabits();
    updateChart(currentPeriod);
    checkStreak();
}

function updateTodayHabits() {
    const todayList = document.querySelector('.today-list');
    todayList.innerHTML = '';
    
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const today = new Date().toISOString().split('T')[0];
    
    if (!currentUser.habits || currentUser.habits.length === 0) {
        const noHabits = document.createElement('div');
        noHabits.className = 'no-habits';
        noHabits.textContent = 'No habits to display for today.';
        todayList.appendChild(noHabits);
        return;
    }
    
    currentUser.habits.forEach(habit => {
        const habitItem = document.createElement('div');
        habitItem.className = 'today-habit-item';
        
        const habitName = document.createElement('div');
        habitName.className = 'today-habit-name';
        
        const colorIndicator = document.createElement('span');
        colorIndicator.className = 'color-indicator';
        colorIndicator.style.backgroundColor = habit.color || '#4A90E2';
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = habit.name;
        
        habitName.appendChild(colorIndicator);
        habitName.appendChild(nameSpan);
        
        const habitAction = document.createElement('div');
        habitAction.className = 'today-habit-action';
        
        // Check if habit is already completed today
        const isCompleted = habit.completions && habit.completions.includes(today);
        
        if (isCompleted) {
            habitItem.classList.add('completed');
            const completedBtn = document.createElement('button');
            completedBtn.className = 'btn btn-secondary';
            completedBtn.textContent = 'Completed';
            completedBtn.addEventListener('click', () => toggleHabitCompletion(habit.id, today));
            habitAction.appendChild(completedBtn);
        } else {
            const completeBtn = document.createElement('button');
            completeBtn.className = 'btn btn-primary';
            completeBtn.textContent = 'Mark Complete';
            completeBtn.addEventListener('click', () => toggleHabitCompletion(habit.id, today));
            habitAction.appendChild(completeBtn);
        }
        
        habitItem.appendChild(habitName);
        habitItem.appendChild(habitAction);
        todayList.appendChild(habitItem);
    });
}

function checkStreak() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const users = JSON.parse(localStorage.getItem('users'));
    const userIndex = users.findIndex(u => u.id === currentUser.id);
    
    // Get all completion dates from all habits
    let allCompletions = [];
    currentUser.habits.forEach(habit => {
        if (habit.completions) {
            allCompletions = allCompletions.concat(habit.completions);
        }
    });
    
    // Remove duplicates and sort
    const uniqueDates = [...new Set(allCompletions)].sort();
    
    // Calculate current streak
    let currentStreak = 0;
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    const todayStr = today.toISOString().split('T')[0];
    const yesterdayStr = yesterday.toISOString().split('T')[0];
    
    if (uniqueDates.includes(todayStr)) {
        currentStreak = 1;
        
        // Check previous days
        let checkDate = new Date(today);
        let previousDate = new Date(checkDate);
        previousDate.setDate(previousDate.getDate() - 1);
        let previousDateStr = previousDate.toISOString().split('T')[0];
        
        while (uniqueDates.includes(previousDateStr)) {
            currentStreak++;
            checkDate = new Date(previousDate);
            previousDate.setDate(previousDate.getDate() - 1);
            previousDateStr = previousDate.toISOString().split('T')[0];
        }
    } else if (uniqueDates.includes(yesterdayStr)) {
        currentStreak = 1;
        
        // Check previous days
        let checkDate = new Date(yesterday);
        let previousDate = new Date(checkDate);
        previousDate.setDate(previousDate.getDate() - 1);
        let previousDateStr = previousDate.toISOString().split('T')[0];
        
        while (uniqueDates.includes(previousDateStr)) {
            currentStreak++;
            checkDate = new Date(previousDate);
            previousDate.setDate(previousDate.getDate() - 1);
            previousDateStr = previousDate.toISOString().split('T')[0];
        }
    }
    
    // Update user streak if it's higher than before
    if (currentStreak > currentUser.streaks) {
        currentUser.streaks = currentStreak;
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        users[userIndex] = currentUser;
        localStorage.setItem('users', JSON.stringify(users));
    }
    
    // Update streak display
    const streakDisplay = document.getElementById('current-streak');
    if (streakDisplay) {
        streakDisplay.textContent = `${currentStreak} day${currentStreak !== 1 ? 's' : ''}`;
    }
}

function updateChart(period) {
    const ctx = document.getElementById('habit-chart').getContext('2d');
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    if (window.habitChart) {
        window.habitChart.destroy();
    }
    
    if (!currentUser.habits || currentUser.habits.length === 0) {
        return;
    }
    
    // Prepare data based on time period
    let labels = [];
    let datasets = [];
    
    switch(period) {
        case 'week':
            labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            datasets = currentUser.habits.map(habit => {
                const weeklyCompletions = Array(7).fill(0);
                if (habit.completions) {
                    habit.completions.forEach(dateStr => {
                        const date = new Date(dateStr);
                        const dayOfWeek = date.getDay();
                        weeklyCompletions[dayOfWeek]++;
                    });
                }
                return {
                    label: habit.name,
                    data: weeklyCompletions,
                    backgroundColor: habit.color || '#4A90E2',
                    borderColor: habit.color ? `${habit.color}80` : '#4A90E280',
                    borderWidth: 1
                };
            });
            break;
            
        case 'month':
            const daysInMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate();
            labels = Array.from({length: daysInMonth}, (_, i) => (i + 1).toString());
            datasets = currentUser.habits.map(habit => {
                const monthlyCompletions = Array(daysInMonth).fill(0);
                if (habit.completions) {
                    habit.completions.forEach(dateStr => {
                        const date = new Date(dateStr);
                        if (date.getMonth() === new Date().getMonth()) {
                            const dayOfMonth = date.getDate() - 1;
                            monthlyCompletions[dayOfMonth]++;
                        }
                    });
                }
                return {
                    label: habit.name,
                    data: monthlyCompletions,
                    backgroundColor: habit.color || '#4A90E2',
                    borderColor: habit.color ? `${habit.color}80` : '#4A90E280',
                    borderWidth: 1
                };
            });
            break;
            
        case 'year':
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            datasets = currentUser.habits.map(habit => {
                const yearlyCompletions = Array(12).fill(0);
                if (habit.completions) {
                    habit.completions.forEach(dateStr => {
                        const date = new Date(dateStr);
                        if (date.getFullYear() === new Date().getFullYear()) {
                            const month = date.getMonth();
                            yearlyCompletions[month]++;
                        }
                    });
                }
                return {
                    label: habit.name,
                    data: yearlyCompletions,
                    backgroundColor: habit.color || '#4A90E2',
                    borderColor: habit.color ? `${habit.color}80` : '#4A90E280',
                    borderWidth: 1
                };
            });
            break;
            
        case 'all':
            // Group by month/year for all time
            const allCompletions = {};
            currentUser.habits.forEach(habit => {
                if (habit.completions) {
                    habit.completions.forEach(dateStr => {
                        const date = new Date(dateStr);
                        const monthYear = `${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`;
                        if (!allCompletions[monthYear]) {
                            allCompletions[monthYear] = 0;
                        }
                        allCompletions[monthYear]++;
                    });
                }
            });
            
            labels = Object.keys(allCompletions);
            datasets = [{
                label: 'Total Completions',
                data: Object.values(allCompletions),
                backgroundColor: '#4A90E2',
                borderColor: '#4A90E280',
                borderWidth: 1
            }];
            break;
    }
    
    window.habitChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Completions'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: period === 'week' ? 'Day of Week' : 
                              period === 'month' ? 'Day of Month' :
                              period === 'year' ? 'Month' : 'Time Period'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}
