// Main JavaScript for Event Management System

document.addEventListener('DOMContentLoaded', function() {
    // Search functionality for event lists
    const searchInput = document.getElementById('eventSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const eventCards = document.querySelectorAll('.event-card');
            
            eventCards.forEach(function(card) {
                const eventTitle = card.querySelector('.event-title').textContent.toLowerCase();
                const eventType = card.querySelector('.event-type').textContent.toLowerCase();
                
                if (eventTitle.includes(searchTerm) || eventType.includes(searchTerm)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Form validation
    const registrationForm = document.querySelector('.registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }
});
