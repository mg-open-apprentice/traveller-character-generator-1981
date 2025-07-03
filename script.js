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
    const commissionBtn = document.getElementById('commission-btn');
    const promotionBtn = document.getElementById('promotion-btn');
    const reenlistmentBtn = document.getElementById('reenlistment-btn');

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

    function updateTermButtonVisibility() {
        fetch('/term_button_status')
            .then(res => res.json())
            .then(data => {
                // Hide survival button if completed
                if (data.survival_completed) {
                    survivalBtn.style.display = 'none';
                } else {
                    survivalBtn.style.display = 'block';
                }
                
                // Hide commission button if completed OR if character is already commissioned
                if (data.commission_completed || data.is_commissioned) {
                    commissionBtn.style.display = 'none';
                } else {
                    commissionBtn.style.display = 'block';
                }
                
                // Hide promotion button if commission failed OR if promotion completed
                if ((data.commission_completed && !data.commission_succeeded) || data.promotion_completed) {
                    promotionBtn.style.display = 'none';
                } else {
                    promotionBtn.style.display = 'block';
                }
                
                // Hide skills button (not implemented yet)
                document.getElementById('skills-btn').style.display = 'none';
                
                // Hide ageing button until 4th term
                fetch('/term_info')
                    .then(res => res.json())
                    .then(termData => {
                        if (termData.term_number >= 4) {
                            document.getElementById('ageing-btn').style.display = 'block';
                        } else {
                            document.getElementById('ageing-btn').style.display = 'none';
                        }
                    });
            });
    }

    function displayTermOutcomes() {
        fetch('/term_button_status')
            .then(res => res.json())
            .then(data => {
                let outcomes = [];
                let promises = [];
                
                // Add survival outcome if completed (1st)
                if (data.survival_completed) {
                    promises.push(
                        fetch('/term_survival', { method: 'GET' })
                            .then(res => res.json())
                            .then(survivalData => {
                                return `Survival: ${survivalData.outcome || (survivalData.survived ? 'Survived' : 'Injured')} (Roll: ${survivalData.roll}, Bonus: ${survivalData.bonus}, Total: ${survivalData.total}, Required: ${survivalData.required})`;
                            })
                    );
                }
                
                // Add commission outcome if completed (2nd)
                if (data.commission_completed) {
                    promises.push(
                        fetch('/term_commission', { method: 'GET' })
                            .then(res => res.json())
                            .then(commissionData => {
                                return `Commission: ${commissionData.success ? 'Commissioned' : 'Not Commissioned'} (Roll: ${commissionData.roll}, Bonus: ${commissionData.modifier}, Total: ${commissionData.total}, Required: ${commissionData.target})`;
                            })
                    );
                }
                
                // Add promotion outcome if completed (3rd)
                if (data.promotion_completed) {
                    promises.push(
                        fetch('/term_promotion', { method: 'GET' })
                            .then(res => res.json())
                            .then(promotionData => {
                                return `Promotion: ${promotionData.success ? 'Promoted' : 'Not Promoted'} (Roll: ${promotionData.roll}, Bonus: ${promotionData.modifier}, Total: ${promotionData.total}, Required: ${promotionData.target})`;
                            })
                    );
                }
                
                // Wait for all promises to resolve and display in order
                Promise.all(promises).then(results => {
                    if (results.length > 0) {
                        resultDiv.innerHTML = results.join('<br>');
                    } else {
                        resultDiv.textContent = '';
                    }
                });
            });
    }

    function updateOutcomesDisplay(outcomes) {
        if (outcomes.length > 0) {
            resultDiv.innerHTML = outcomes.join('<br>');
        }
    }

    // Update survival button logic
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
            updateTermButtonVisibility(); // Update button visibility after survival
            setTimeout(displayTermOutcomes, 100); // Update display after a short delay
        } catch (err) {
            resultDiv.textContent = 'Error checking survival.';
        }
    });

    // Commission button logic
    commissionBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Checking commission...';
        try {
            const response = await fetch('/term_commission', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            let msg = `Commission Outcome: ${data.success ? 'commissioned' : 'not commissioned'}` +
                      `\nRoll: ${data.roll}, Bonus: ${data.modifier}, Total: ${data.total}, Required: ${data.target}`;
            resultDiv.textContent = msg;
            updateTermButtonVisibility(); // Update button visibility after commission
            setTimeout(displayTermOutcomes, 100); // Update display after a short delay
        } catch (err) {
            resultDiv.textContent = 'Error checking commission.';
        }
    });

    // Promotion button logic
    promotionBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Checking promotion...';
        try {
            const response = await fetch('/term_promotion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            let msg = `Promotion Outcome: ${data.success ? 'promoted' : 'not promoted'}` +
                      `\nRoll: ${data.roll}, Bonus: ${data.modifier}, Total: ${data.total}, Required: ${data.target}`;
            resultDiv.textContent = msg;
            updateTermButtonVisibility(); // Update button visibility after promotion
            setTimeout(displayTermOutcomes, 100); // Update display after a short delay
        } catch (err) {
            resultDiv.textContent = 'Error checking promotion.';
        }
    });

    // Update showTermSection to also update button visibility and display outcomes
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
                updateTermButtonVisibility(); // Update button visibility when showing term section
                displayTermOutcomes(); // Display any existing outcomes
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

    // Re-enlistment button logic
    reenlistmentBtn.addEventListener('click', async function() {
        resultDiv.textContent = 'Checking re-enlistment...';
        try {
            const response = await fetch('/term_reenlistment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            let msg = `Re-enlistment Outcome: ${data.result}` +
                      `\nSucceeded: ${data.succeeded ? 'Yes' : 'No'}` +
                      `\nTerms Served: ${data.terms_served}` +
                      `\nAge: ${data.age}`;
            resultDiv.textContent = msg;
            if (data.succeeded) {
                // Update character summary
                summaryDiv.textContent = `Name: ${characterName} | Age: ${data.age}`;
                // Update term section for new term
                setTimeout(() => {
                    showTermSection();
                }, 1000);
            }
        } catch (err) {
            resultDiv.textContent = 'Error checking re-enlistment.';
        }
    });

    // Initial state
    updateButtonVisibility();
}); 