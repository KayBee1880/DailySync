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
    
    document.addEventListener("DOMContentLoaded", function() {
      // Open and close modal functions
      function openModal() {
          document.getElementById('addHabitModal').style.display = 'block';  // Show the modal
      }
  
      function closeModal() {
          document.getElementById('addHabitModal').style.display = 'none';   // Hide the modal
      }
  
      // Add event listener to the open modal button
      const openModalBtn = document.querySelector('.add-habit-button');
      if (openModalBtn) {
          openModalBtn.addEventListener('click', openModal);
      }
  
      // Add event listener to the close modal button
      const closeModalBtn = document.getElementById('closeModalBtn');
      if (closeModalBtn) {
          closeModalBtn.addEventListener('click', closeModal);
      }
    });
    document.addEventListener("DOMContentLoaded", function () {
      const habitSelect = document.getElementById("habitSelect");
      const customHabitWrapper = document.getElementById("customHabitFields");
      const customHabitInput = document.getElementById("customHabitInput");
      const charCount = document.getElementById("customHabitCharCount");

      const goalTypeSelect = document.getElementById("goalTypeSelect");
      const goalFrequencyInput = document.getElementById("goalFrequency");
      const frequencyHint = document.getElementById("frequencyHint");

      // Show custom habit field if "Custom" is selected
      habitSelect.addEventListener("change", function () {
        if (habitSelect.value === "Custom") {
          customHabitWrapper.style.display = "block";
          customHabitInput.required = true;
        } else {
          customHabitWrapper.style.display = "none";
          customHabitInput.required = false;
        }
      });

      // Limit custom habit name to 15 characters
      customHabitInput.addEventListener("input", function () {
        const maxLength = 15;
        const currentLength = customHabitInput.value.length;

        if (currentLength > maxLength) {
          customHabitInput.value = customHabitInput.value.slice(0, maxLength);
        }

        charCount.textContent = `${customHabitInput.value.length}/${maxLength}`;
      });

      // Goal type logic
      goalTypeSelect.addEventListener("change", function () {
        const type = goalTypeSelect.value;

        if (type === "daily") {
          goalFrequencyInput.style.display = "none";
          goalFrequencyInput.required = false;
          frequencyHint.textContent = "No frequency needed for daily habits.";
        } else {
          goalFrequencyInput.style.display = "inline-block";
          goalFrequencyInput.required = true;

          if (type === "weekly") {
            goalFrequencyInput.min = 1;
            goalFrequencyInput.max = 7;
            frequencyHint.textContent = "Enter a number from 1 to 7 (times per week)";
          } else if (type === "monthly") {
            goalFrequencyInput.min = 1;
            goalFrequencyInput.max = 28;
            frequencyHint.textContent = "Enter a number from 1 to 28 (times per month)";
          }
        }
      });
    });
