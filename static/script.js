document.addEventListener('DOMContentLoaded', function() {
    console.log("Real script loaded!");
    
    // Create Character Function
    document.getElementById('create-btn').onclick = async function() {
        console.log("Create button clicked - making API call!");
        
        // Show loading state
        this.disabled = true;
        this.querySelector('.btn-text').textContent = '⏳ Creating...';
        
        const messageDisplay = document.getElementById('message-display');
        messageDisplay.textContent = '▶ Creating character...';
        
        try {
            console.log("Making fetch request to /api/character/create");
            
            const response = await fetch('/api/character/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            console.log("Response status:", response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const character = await response.json();
            console.log("Character created:", character);
            
            messageDisplay.textContent = `▶ Created character: ${character.name}`;
            
            // Reload page after 2 seconds
            setTimeout(() => {
                window.location.reload();
            }, 2000);
            
        } catch (error) {
            console.error("Error creating character:", error);
            messageDisplay.textContent = `▶ Error: ${error.message}`;
            
            // Re-enable button
            this.disabled = false;
            this.querySelector('.btn-text').textContent = '🎯 CREATE CHARACTER';
        }
    };
});