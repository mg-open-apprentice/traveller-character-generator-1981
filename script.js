document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('create-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const resultDiv = document.getElementById('result');
    const revealDiv = document.getElementById('reveal-buttons');
    const summaryDiv = document.getElementById('summary');
    const uppDisplay = document.getElementById('upp-display');

    const attrButtons = {
        strength: document.getElementById('strength-btn'),
        dexterity: document.getElementById('dexterity-btn'),
        endurance: document.getElementById('endurance-btn'),
        intelligence: document.getElementById('intelligence-btn'),
        education: document.getElementById('education-btn'),
        social: document.getElementById('social-btn')
    };

    let characterName = '';
    let characterAge = '';

    btn.addEventListener('click', async function() {
        resultDiv.textContent = 'Creating character...';
        uppDisplay.textContent = '';
        summaryDiv.textContent = '';
        revealDiv.style.display = 'none';
        try {
            const response = await fetch('/create_character', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            characterName = data.name;
            characterAge = data.age;
            summaryDiv.textContent = `Name: ${characterName} | Age: ${characterAge}`;
            resultDiv.textContent = `Character created!`;
            uppDisplay.textContent = '';
            revealDiv.style.display = 'block';
        } catch (err) {
            resultDiv.textContent = 'Error creating character.';
        }
    });

    deleteBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Deleting character...';
        uppDisplay.textContent = '';
        summaryDiv.textContent = '';
        revealDiv.style.display = 'none';
        try {
            const response = await fetch('/delete_character', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
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

    async function revealCharacteristic(characteristic) {
        resultDiv.textContent = '';
        try {
            const response = await fetch('/reveal_characteristic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ characteristic })
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            uppDisplay.textContent = `UPP: ${data.upp}`;
        } catch (err) {
            resultDiv.textContent = 'Error revealing characteristic.';
        }
    }

    for (const [key, btn] of Object.entries(attrButtons)) {
        btn.addEventListener('click', function() {
            revealCharacteristic(key);
        });
    }
}); 