// Get current week and display it
function updateWeekDisplay() {
    const now = new Date();
    const currentWeek = getWeekDates(now);
    const weekDisplay = `${currentWeek.start} - ${currentWeek.end}`;
    document.getElementById('current-week').textContent = weekDisplay;
}

// Calculate week dates (Sunday to Saturday)
function getWeekDates(date) {
    const start = new Date(date);
    const day = start.getDay();
    const diff = start.getDate() - day;
    start.setDate(diff);
    
    const end = new Date(start);
    end.setDate(start.getDate() + 6);
    
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    
    return {
        start: start.toLocaleDateString('en-US', options),
        end: end.toLocaleDateString('en-US', options)
    };
}

// Modal functions
function openNewTaskModal() {
    document.getElementById('newTaskModal').style.display = 'block';
    // Set today's date as default for due date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('due_date').value = today;
}

function closeNewTaskModal() {
    document.getElementById('newTaskModal').style.display = 'none';
    document.getElementById('newTaskForm').reset();
}

// Search functionality
function setupSearch() {
    const searchInput = document.getElementById('search-tasks');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const taskCards = document.querySelectorAll('.task-card');
        
        taskCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const description = card.querySelector('p').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('newTaskModal');
    if (event.target === modal) {
        closeNewTaskModal();
    }
}
// Status dropdown functionality
function updateStatus(selectElement) {
    const taskId = selectElement.getAttribute('data-task-id');
    const newStatus = selectElement.value;
    
    // Update the task status via the API
    fetch(`/update/${taskId}/${newStatus}`)
        .then(response => {
            if (response.ok) {
                // Success - you could add visual feedback here
                console.log(`Task ${taskId} status updated to ${newStatus}`);
                
                // Update the task card class to reflect new status
                const taskCard = selectElement.closest('.task-card');
                taskCard.className = 'task-card ' + newStatus.toLowerCase().replace(' ', '-');
            } else {
                // Revert the dropdown if update failed
                console.error('Failed to update task status');
            }
        })
        .catch(error => {
            console.error('Error updating task status:', error);
        });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    updateWeekDisplay();
    setupSearch();
});