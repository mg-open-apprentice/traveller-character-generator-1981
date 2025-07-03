document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('create-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const resultDiv = document.getElementById('result');
    const summaryDiv = document.getElementById('summary');
    const uppDisplay = document.getElementById('upp-display');
    const attributeDiv = document.getElementById('attribute-buttons');
    const serviceDiv = document.getElementById('service-buttons');
    const termSection = document.getElementById('term-section');
    const termTitle = document.getElementById('term-title');
    const survivalBtn = document.getElementById('survival-btn');

    const attrButtons = {
        strength: document.getElementById('strength-btn'),
        dexterity: document.getElementById('dexterity-btn'),
        endurance: document.getElementById('endurance-btn'),
        intelligence: document.getElementById('intelligence-btn'),
        education: document.getElementById('education-btn'),
        social: document.getElementById('social-btn')
    };

    const serviceButtons = {
        navy: document.getElementById('navy-btn'),
        marines: document.getElementById('marines-btn'),
        army: document.getElementById('army-btn'),
        scouts: document.getElementById('scouts-btn'),
        merchants: document.getElementById('merchants-btn'),
        others: document.getElementById('others-btn')
    };

    const serviceMap = {
        navy: 'Navy',
        marines: 'Marines',
        army: 'Army',
        scouts: 'Scouts',
        merchants: 'Merchants',
        others: 'Others'
    };

    let characterName = '';
    let characterAge = '';
    let revealed = [];
    let serviceAssigned = false;

    function showTermSection() {
        fetch('/term_info')
            .then(res => res.json())
            .then(data => {
                if (data.term_ordinal) {
                    termTitle.textContent = `${data.term_ordinal.charAt(0).toUpperCase() + data.term_ordinal.slice(1)} Term`;
                } else {
                    termTitle.textContent = 'Term';
                }
                termSection.style.display = 'block';
            });
    }

    function hideTermSection() {
        termSection.style.display = 'none';
    }

    function updateButtonVisibility() {
        if (serviceAssigned) {
            attributeDiv.style.display = 'none';
            serviceDiv.style.display = 'none';
            showTermSection();
        } else if (revealed.length === 6) {
            attributeDiv.style.display = 'none';
            serviceDiv.style.display = 'block';
            hideTermSection();
        } else {
            attributeDiv.style.display = 'block';
            serviceDiv.style.display = 'none';
            hideTermSection();
        }
    }

    btn.addEventListener('click', async function() {
        resultDiv.textContent = 'Creating character...';
        uppDisplay.textContent = '';
        summaryDiv.textContent = '';
        attributeDiv.style.display = 'block';
        serviceDiv.style.display = 'none';
        revealed = [];
        serviceAssigned = false;
        hideTermSection();
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
            updateButtonVisibility();
        } catch (err) {
            resultDiv.textContent = 'Error creating character.';
        }
    });

    deleteBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Deleting character...';
        uppDisplay.textContent = '';
        summaryDiv.textContent = '';
        attributeDiv.style.display = 'block';
        serviceDiv.style.display = 'none';
        revealed = [];
        serviceAssigned = false;
        hideTermSection();
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
            revealed = data.revealed;
            updateButtonVisibility();
        } catch (err) {
            resultDiv.textContent = 'Error revealing characteristic.';
        }
    }

    for (const [key, btn] of Object.entries(attrButtons)) {
        btn.addEventListener('click', function() {
            revealCharacteristic(key);
        });
    }

    // Service selection logic: call backend and display outcome
    for (const [key, btn] of Object.entries(serviceButtons)) {
        btn.addEventListener('click', async function() {
            resultDiv.textContent = 'Attempting enlistment...';
            try {
                const response = await fetch('/attempt_enlistment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service: serviceMap[key] })
                });
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                let msg = `Service selected: ${data.service}\nStatus: ${data.enlistment_status}\n` +
                          `Required Roll: ${data.required_roll}, Actual Roll: ${data.enlistment_roll}, Modifier: ${data.modifier}`;
                if (data.enlistment_status === 'drafted') {
                    msg += `\nDrafted to: ${data.service}`;
                }
                resultDiv.textContent = msg;
                serviceAssigned = true;
                updateButtonVisibility();
            } catch (err) {
                resultDiv.textContent = 'Error attempting enlistment.';
            }
        });
    }

    // Survival button logic
    survivalBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Checking survival...';
        try {
            const response = await fetch('/term_survival', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            let msg = `Survival Outcome: ${data.outcome || (data.survived ? 'survived' : 'injured')}` +
                      `\nRoll: ${data.roll}, Bonus: ${data.bonus}, Total: ${data.total}, Required: ${data.required}`;
            resultDiv.textContent = msg;
        } catch (err) {
            resultDiv.textContent = 'Error checking survival.';
        }
    });

    // Initial state
    updateButtonVisibility();
}); 