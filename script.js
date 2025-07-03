document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('create-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const resultDiv = document.getElementById('result');

    btn.addEventListener('click', async function() {
        resultDiv.textContent = 'Creating character...';
        try {
            const response = await fetch('/create_character', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            resultDiv.textContent = `Character created! Name: ${data.name}, Age: ${data.age}`;
        } catch (err) {
            resultDiv.textContent = 'Error creating character.';
        }
    });

    deleteBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Deleting character...';
        try {
            const response = await fetch('/delete_character', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            if (data.deleted) {
                resultDiv.textContent = 'Character deleted.';
            } else {
                resultDiv.textContent = 'No character to delete.';
            }
        } catch (err) {
            resultDiv.textContent = 'Error deleting character.';
        }
    });
}); 