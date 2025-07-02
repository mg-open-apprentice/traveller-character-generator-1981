// character.js - Main JavaScript file for Traveller Character Generator SPA

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

// Initialize the application
function initApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Check for any flash messages or errors
    checkMessages();
}

// Set up all event listeners
function setupEventListeners() {
    // Create Character button
    const createButton = document.getElementById('create-character-btn');
    if (createButton) {
        createButton.addEventListener('click', createCharacter);
    }
    
    // Delete Character button
    const deleteButton = document.getElementById('delete-character-btn');
    if (deleteButton) {
        deleteButton.addEventListener('click', deleteCharacter);
    }
    
    // Career selection buttons
    const careerButtons = document.querySelectorAll('.career-btn');
    careerButtons.forEach(button => {
        button.addEventListener('click', function() {
            selectCareer(this.getAttribute('data-career'));
        });
    });
}

// Create a new character
function createCharacter(event) {
    if (event) event.preventDefault();
    
    // Show loading state
    toggleLoadingState(true, 'Creating character...');
    
    // Make API call to create character
    fetch('/api/character/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Character created:', data);
        
        // Refresh the page to show the new character
        // In a full SPA, you would update the DOM instead
        window.location.reload();
    })
    .catch(error => {
        console.error('Error creating character:', error);
        showMessage('error', 'Failed to create character: ' + error.message);
        toggleLoadingState(false);
    });
}

// Delete the current character
function deleteCharacter(event) {
    if (event) event.preventDefault();
    
    // Confirm deletion
    if (!confirm('Are you sure you want to delete this character?')) {
        return;
    }
    
    // Show loading state
    toggleLoadingState(true, 'Deleting character...');
    
    // Make API call to delete character
    fetch('/api/character/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Delete response:', data);
        
        // Check if we got a successful response
        if (data.success) {
            showMessage('success', 'Character deleted successfully!');
            
            // Refresh the page to show updated state
            window.location.reload();
        } else {
            showMessage('error', 'Failed to delete character: ' + (data.message || 'Unknown error'));
            toggleLoadingState(false);
        }
    })
    .catch(error => {
        console.error('Error deleting character:', error);
        showMessage('error', 'Failed to delete character: ' + error.message);
        toggleLoadingState(false);
    });
}

// Select a career for the character
function selectCareer(career) {
    console.log('Career selected:', career);
    
    // Show loading state
    toggleLoadingState(true, `Selecting career: ${career}...`);
    
    // Make API call to select career
    fetch('/api/character/career', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ career: career })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Career selection response:', data);
        
        // Refresh the page to show updated character
        // In a full SPA, you would update the DOM instead
        window.location.reload();
    })
    .catch(error => {
        console.error('Error selecting career:', error);
        showMessage('error', 'Failed to select career: ' + error.message);
        toggleLoadingState(false);
    });
}

// Helper Functions

// Toggle loading state
function toggleLoadingState(isLoading, message = 'Loading...') {
    // Create or get loading overlay
    let loadingOverlay = document.getElementById('loading-overlay');
    
    if (isLoading) {
        if (!loadingOverlay) {
            loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-spinner"></div>
                <div class="loading-message">${message}</div>
            `;
            document.body.appendChild(loadingOverlay);
        } else {
            const loadingMessage = loadingOverlay.querySelector('.loading-message');
            if (loadingMessage) {
                loadingMessage.textContent = message;
            }
            loadingOverlay.style.display = 'flex';
        }
    } else if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

// Show a message to the user
function showMessage(type, message, duration = 5000) {
    const messageContainer = document.getElementById('message-container');
    
    if (messageContainer) {
        const alertClass = type === 'error' ? 'alert-danger' : 
                          type === 'warning' ? 'alert-warning' : 
                          type === 'success' ? 'alert-success' : 'alert-info';
        
        const alertElement = document.createElement('div');
        alertElement.className = `alert ${alertClass} alert-dismissible fade show`;
        alertElement.role = 'alert';
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        messageContainer.appendChild(alertElement);
        
        // Auto-dismiss after duration (if positive)
        if (duration > 0) {
            setTimeout(() => {
                alertElement.classList.remove('show');
                setTimeout(() => {
                    messageContainer.removeChild(alertElement);
                }, 150);
            }, duration);
        }
    } else {
        // Fallback to alert if message container doesn't exist
        if (type === 'error') {
            alert('Error: ' + message);
        } else {
            alert(message);
        }
    }
}

// Check for flash messages or errors (from server-side redirects)
function checkMessages() {
    // Implementation depends on how server sends flash messages
    // This is just a placeholder - you might have query parameters or cookies
    const urlParams = new URLSearchParams(window.location.search);
    const flashMessage = urlParams.get('flash');
    const flashType = urlParams.get('type') || 'info';
    
    if (flashMessage) {
        showMessage(flashType, decodeURIComponent(flashMessage));
    }
}