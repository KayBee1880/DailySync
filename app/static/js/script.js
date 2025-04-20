document.addEventListener('DOMContentLoaded', function() {
    // Navigation between views
    const navItems = document.querySelectorAll('.main-nav li');
    const views = document.querySelectorAll('.view');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all nav items and views
            navItems.forEach(navItem => navItem.classList.remove('active'));
            views.forEach(view => view.classList.remove('active-view'));
            
            // Add active class to clicked nav item
            this.classList.add('active');
            
            // Show corresponding view
            const viewName = this.getAttribute('data-view');
            document.querySelector(`.${viewName}-view`).classList.add('active-view');
        });
    });
    
    // Time period selector functionality
    const timePeriodButtons = document.querySelectorAll('.time-period-selector button');
    
    timePeriodButtons.forEach(button => {
        button.addEventListener('click', function() {
            const parent = this.parentElement;
            parent.querySelector('.active').classList.remove('active');
            this.classList.add('active');
        });
    });
    
    // Mark complete button functionality
    const markCompleteButtons = document.querySelectorAll('.mark-complete-btn');
    
    markCompleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.textContent = 'Completed';
            this.classList.remove('mark-complete-btn');
            this.classList.add('completed-btn');
            this.style.backgroundColor = '#4CAF50';
        });
    });
    
    // Edit button functionality (placeholder)
    const editButtons = document.querySelectorAll('.edit-btn');
    
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Edit functionality would be implemented here');
        });
    });
    
    // Add habit button functionality (placeholder)
    document.addEventListener("DOMContentLoaded", function() {
        // Function to open the modal
        function openModal() {
          document.getElementById('addHabitModal').style.display = 'block';
        }
    
        // Function to close the modal
        function closeModal() {
          document.getElementById('addHabitModal').style.display = 'none';
        }
    
        // Add event listeners to all "Add Habit" buttons to open the modal
        const addHabitButtons = document.querySelectorAll('.add-habit-button, .add-habit-btn');
        addHabitButtons.forEach(button => {
          button.addEventListener('click', openModal);
        });
    
        // Close modal when close button is clicked
        const closeModalBtn = document.getElementById('closeModalBtn');
        if (closeModalBtn) {
          closeModalBtn.addEventListener('click', closeModal);
        }
    
        // Optional: Close modal when clicking outside the modal content
        window.addEventListener('click', function(event) {
          const modal = document.getElementById('addHabitModal');
          if (event.target === modal) {
            closeModal();
          }
        });
    
        // Simulate loading the dashboard view by default
        document.querySelector('.dashboard-view')?.classList.add('active-view');
      });
