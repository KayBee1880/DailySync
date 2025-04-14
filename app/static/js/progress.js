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
    
    // Set up time period selector
    const timePeriodButtons = document.querySelectorAll('.time-period-btn');
    timePeriodButtons.forEach(button => {
        button.addEventListener('click', () => {
            timePeriodButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            updateProgressData();
        });
    });
    
    // Initialize progress data
    updateProgressData();
});

function updateProgressData() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    // Update streak counter
    document.getElementById('current-streak').textContent = `${currentUser.streaks || 0} days`;
    
    // Update days completed
    const daysCompletedGrid = document.querySelector('.days-completed-grid');
    daysCompletedGrid.innerHTML = '';
    
    if (!currentUser.habits || currentUser.habits.length === 0) {
        const noHabits = document.createElement('div');
        noHabits.textContent = 'No habits to display';
        noHabits.style.gridColumn = '1 / -1';
        noHabits.style.textAlign = 'center';
        daysCompletedGrid.appendChild(noHabits);
        return;
    }
    
    currentUser.habits.forEach(habit => {
        const completionItem = document.createElement('div');
        completionItem.className = 'day-completed-item';
        
        const habitName = document.createElement('div');
        habitName.textContent = habit.name;
        
        const completionCount = document.createElement('div');
        completionCount.textContent = habit.completions ? habit.completions.length : 0;
        
        completionItem.appendChild(habitName);
        completionItem.appendChild(completionCount);
        daysCompletedGrid.appendChild(completionItem);
    });
    
    // Update progress chart
    updateProgressChart();
    
    // Generate feedback
    generateFeedback();
}

function updateProgressChart() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const ctx = document.getElementById('habit-chart').getContext('2d');
    
    if (window.habitChart) {
        window.habitChart.destroy();
    }
    
    if (!currentUser.habits || currentUser.habits.length === 0) {
        return;
    }
    
    const habitNames = currentUser.habits.map(habit => habit.name);
    const habitCompletions = currentUser.habits.map(habit => habit.completions ? habit.completions.length : 0);
    
    window.habitChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: habitNames,
            datasets: [{
                label: 'Completions',
                data: habitCompletions,
                backgroundColor: '#4a6fa5',
                borderColor: '#3a5a8a',
                borderWidth: 1
            }]
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
                        text: 'Habits'
                    }
                }
            }
        }
    });
}

function generateFeedback() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    const feedbackContainer = document.getElementById('feedback-messages');
    feedbackContainer.innerHTML = '';
    
    if (!currentUser.habits || currentUser.habits.length === 0) {
        const noFeedback = document.createElement('div');
        noFeedback.className = 'feedback-message';
        noFeedback.textContent = 'No habits to provide feedback on. Add some habits first.';
        feedbackContainer.appendChild(noFeedback);
        return;
    }
    
    // Check for streaks
    if (currentUser.streaks >= 7) {
        const streakFeedback = document.createElement('div');
        streakFeedback.className = 'feedback-message';
        streakFeedback.textContent = `Great job! You're on a ${currentUser.streaks}-day streak. Keep it up!`;
        feedbackContainer.appendChild(streakFeedback);
    }
    
    // Check for habit progress
    currentUser.habits.forEach(habit => {
        const completionCount = habit.completions ? habit.completions.length : 0;
        
        if (completionCount === 0) {
            const noCompletions = document.createElement('div');
            noCompletions.className = 'feedback-message';
            noCompletions.textContent = `You haven't logged any completions for ${habit.name} yet. Try to get started today!`;
            feedbackContainer.appendChild(noCompletions);
        } else if (completionCount >= 5) {
            const goodProgress = document.createElement('div');
            goodProgress.className = 'feedback-message';
            goodProgress.textContent = `You're doing great with ${habit.name}! You've completed it ${completionCount} times.`;
            feedbackContainer.appendChild(goodProgress);
        }
    });
    
    // If no specific feedback, show general encouragement
    if (feedbackContainer.children.length === 0) {
        const generalFeedback = document.createElement('div');
        generalFeedback.className = 'feedback-message';
        generalFeedback.textContent = 'Keep up the good work! Consistency is key to building lasting habits.';
        feedbackContainer.appendChild(generalFeedback);
    }
}
