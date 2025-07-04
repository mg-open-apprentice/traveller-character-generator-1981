document.addEventListener('DOMContentLoaded', function() {
    // Sidebar and workflow controls
    const btn = document.getElementById('create-btn');
    const deleteBtn = document.getElementById('delete-btn');
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

    // Permanent record fields
    const charTitle = document.getElementById('character-title');
    const charName = document.getElementById('character-name');
    const charService = document.getElementById('character-service');
    const charRank = document.getElementById('character-rank');
    const charUPP = document.getElementById('character-upp');
    const charAge = document.getElementById('character-age');
    const charTerms = document.getElementById('character-terms');
    const charCash = document.getElementById('character-cash');
    const charStarship = document.getElementById('character-starship');
    const charWeapons = document.getElementById('character-weapons');
    const charTAS = document.getElementById('character-tas');

    // Term info fields
    const currentTerm = document.getElementById('current-term');
    const survivalOutcome = document.getElementById('survival-outcome');
    const commissioningOutcome = document.getElementById('commissioning-outcome');
    const promotionOutcome = document.getElementById('promotion-outcome');
    const termSkillsEligibility = document.getElementById('term-skills-eligibility');
    const commissionSkillsEligibility = document.getElementById('commission-skills-eligibility');
    const promotionSkillsEligibility = document.getElementById('promotion-skills-eligibility');
    const ageingEffects = document.getElementById('ageing-effects');
    const reenlistmentOutcome = document.getElementById('reenlistment-outcome');

    // Utility: Safely set text content
    function safeSetText(element, text) {
        if (element) element.textContent = text;
    }

    // Utility: Show a message to the user
    function showUserMessage(msg) {
        // Remove the user message functionality entirely
    }

    function clearUserMessage() {
        // Remove the user message functionality entirely
    }

    // --- UI Update Functions ---

    function updatePermanentRecord(data) {
        // Title only if social >= 11
        safeSetText(charTitle, (data.social && data.social >= 11) ? (data.title || "Noble") : "");
        safeSetText(charName, data.name ? `Name: ${data.name}` : "");
        safeSetText(charService, data.service ? `Service: ${data.service}` : "");
        safeSetText(charRank, data.rank !== undefined && data.rank !== null ? `Rank: ${data.rank}` : "");
        // Only show UPP if all characteristics are revealed
        if (data.revealed && data.revealed.length === 6 && data.upp) {
            safeSetText(charUPP, `UPP: ${data.upp}`);
        } else {
            safeSetText(charUPP, "UPP: ------");
        }
        safeSetText(charAge, data.age !== undefined && data.age !== null ? `Age: ${data.age}` : "");
        safeSetText(charTerms, data.terms !== undefined && data.terms !== null ? `Terms Served: ${data.terms}` : "");
        safeSetText(charCash, data.cash !== undefined && data.cash !== null ? `Cash: ${data.cash}` : "");
        safeSetText(charStarship, data.starship ? `Starship: ${data.starship}` : "");
        safeSetText(charWeapons, data.weapons ? `Weapons: ${data.weapons}` : "");
        safeSetText(charTAS, data.tas ? `TAS: ${data.tas}` : "");
    }

    function updateTermInfo(termData) {
        safeSetText(currentTerm, termData.term ? `Current Term: ${termData.term}` : "");
        safeSetText(survivalOutcome, termData.survival ? `Survival: ${termData.survival}` : "");
        safeSetText(commissioningOutcome, termData.commission ? `Commission: ${termData.commission}` : "");
        safeSetText(promotionOutcome, termData.promotion ? `Promotion: ${termData.promotion}` : "");
        safeSetText(termSkillsEligibility, termData.termSkills ? `Term Skills: ${termData.termSkills}` : "");
        safeSetText(commissionSkillsEligibility, termData.commissionSkills ? `Commission Skills: ${termData.commissionSkills}` : "");
        safeSetText(promotionSkillsEligibility, termData.promotionSkills ? `Promotion Skills: ${termData.promotionSkills}` : "");
        safeSetText(ageingEffects, termData.ageing ? `Ageing: ${termData.ageing}` : "");
        safeSetText(reenlistmentOutcome, termData.reenlistment ? `Re-enlistment: ${termData.reenlistment}` : "");

        // Display a log of the most recent survival, commission, and promotion rolls/results
        const logDiv = document.getElementById('term-outcome-log');
        if (logDiv && window.lastStatusData) {
            const { last_survival, last_commission, last_promotion } = window.lastStatusData;
            let logHtml = '';
            if (last_survival && Object.keys(last_survival).length > 0) {
                logHtml += `<div>Survival: Roll ${last_survival.roll} + Bonus ${last_survival.bonus} = Total ${last_survival.total} (Need ${last_survival.required}) → ${last_survival.outcome ? last_survival.outcome.toUpperCase() : ''}</div>`;
            }
            if (last_commission && Object.keys(last_commission).length > 0 && last_commission.applicable !== false) {
                logHtml += `<div>Commission: Roll ${last_commission.roll} + Modifier ${last_commission.modifier} = Total ${last_commission.total} (Need ${last_commission.target}) → ${last_commission.success ? 'COMMISSIONED' : 'FAILED'}</div>`;
            }
            if (last_promotion && Object.keys(last_promotion).length > 0 && last_promotion.applicable !== false) {
                logHtml += `<div>Promotion: Roll ${last_promotion.roll} + Modifier ${last_promotion.modifier} = Total ${last_promotion.total} (Need ${last_promotion.target}) → ${last_promotion.success ? 'PROMOTED' : 'FAILED'}</div>`;
            }
            
            // Add skill breakdown if available
            if (window.skillBreakdown && Object.keys(window.skillBreakdown).length > 0) {
                logHtml += `<div style="margin-top: 10px; font-weight: bold;">Skills Available:</div>`;
                const total = Object.values(window.skillBreakdown).reduce((sum, val) => sum + val, 0);
                logHtml += `<div>Total: ${total} skills</div>`;
                if (window.skillBreakdown.survival !== undefined) {
                    logHtml += `<div>Survival: ${window.skillBreakdown.survival} skills</div>`;
                }
                if (window.skillBreakdown.commission !== undefined) {
                    logHtml += `<div>Commission: ${window.skillBreakdown.commission} skills</div>`;
                }
                if (window.skillBreakdown.promotion !== undefined) {
                    logHtml += `<div>Promotion: ${window.skillBreakdown.promotion} skills</div>`;
                }
            }
            
            logDiv.innerHTML = logHtml;
        }
    }

    function updateCharacteristicButtons(revealedList, characterExists) {
        for (const [key, btn] of Object.entries(attrButtons)) {
            if (btn) {
                if (!characterExists) {
                    btn.style.display = 'none';
                } else if (revealedList && revealedList.includes(key)) {
                    btn.style.display = 'none';
                } else {
                    btn.style.display = 'block';
                }
            }
        }
    }

    function updateTermButtons(buttonStatus) {
        // Hide survival button if survival is completed
        if (survivalBtn) {
            survivalBtn.style.display = buttonStatus.survival_completed ? 'none' : 'block';
        }
        
        // Hide commission button if commission is completed
        if (commissionBtn) {
            commissionBtn.style.display = buttonStatus.commission_completed ? 'none' : 'block';
        }
        
        // Hide promotion button if promotion is completed
        if (promotionBtn) {
            promotionBtn.style.display = buttonStatus.promotion_completed ? 'none' : 'block';
        }
    }

    function showCreatePrompt() {
        const charPanel = document.querySelector('.permanent-record');
        if (charPanel) {
            charPanel.innerHTML = '<div style="color:#b00; font-weight:bold;">No character found. Please create a character.</div>';
        }
    }

    // Fetch and update all UI after any state change
    function refreshAllUI() {
        fetch('/character_status')
            .then(res => {
                if (!res.ok) {
                    updateCharacteristicButtons([], false); // Hide all
                    // No message shown
                    window.lastStatusData = null;
                    return {};
                }
                // No message shown
                return res.json();
            })
            .then(data => {
                if (data && data.name) {
                    updatePermanentRecord(data);
                    updateCharacteristicButtons(data.revealed || [], true);
                    window.lastStatusData = data;
                }
            });
        fetch('/term_info')
            .then(res => {
                if (!res.ok) return {};
                return res.json();
            })
            .then(termData => updateTermInfo(termData));
        
        // Fetch button status and update button visibility
        fetch('/term_button_status')
            .then(res => {
                if (!res.ok) return {};
                return res.json();
            })
            .then(buttonStatus => {
                if (buttonStatus && Object.keys(buttonStatus).length > 0) {
                    updateTermButtons(buttonStatus);
                }
            });
        
        // Calculate skills if term checks are completed
        calculateTermSkills();
    }

    // Calculate skills based on term outcomes
    function calculateTermSkills() {
        fetch('/calculate_term_skills', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => {
            if (!res.ok) return {};
            return res.json();
        })
        .then(skillData => {
            if (skillData && skillData.skill_breakdown) {
                window.skillBreakdown = skillData.skill_breakdown;
                // Update the term info display to show skill breakdown
                updateTermInfo({});
            }
        });
    }

    // --- Workflow State ---

    let revealed = [];
    let serviceAssigned = false;

    // --- Button Visibility Logic (unchanged, but can be refactored for clarity) ---

    // Update updateButtonVisibility to hide/disable buttons if no character
    function updateButtonVisibility() {
        if (!window.lastStatusData || !window.lastStatusData.name) {
            updateCharacteristicButtons([], false);
            if (attributeDiv) attributeDiv.style.display = 'none';
            if (serviceDiv) serviceDiv.style.display = 'none';
            if (termSection) termSection.style.display = 'none';
            return;
        }
        if (serviceAssigned) {
            if (attributeDiv) attributeDiv.style.display = 'none';
            if (serviceDiv) serviceDiv.style.display = 'none';
            if (termSection) termSection.style.display = 'block';
        } else if (revealed.length === 6) {
            if (attributeDiv) attributeDiv.style.display = 'none';
            if (serviceDiv) serviceDiv.style.display = 'block';
            if (termSection) termSection.style.display = 'none';
        } else {
            if (attributeDiv) attributeDiv.style.display = 'block';
            if (serviceDiv) serviceDiv.style.display = 'none';
            if (termSection) termSection.style.display = 'none';
        }
    }

    // --- Event Handlers ---

    if (btn) btn.addEventListener('click', async function() {
        revealed = [];
        serviceAssigned = false;
        try {
            const response = await fetch('/create_character', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            // Disable create button after successful character creation
            btn.disabled = true;
            btn.style.opacity = '0.5';
            // Reset term button visibility for new character
            if (survivalBtn) survivalBtn.style.display = 'block';
            if (commissionBtn) commissionBtn.style.display = 'block';
            if (promotionBtn) promotionBtn.style.display = 'block';
            // Refresh UI first to get character data
            await refreshAllUI();
            // Force show characteristic buttons after character creation
            if (attributeDiv) attributeDiv.style.display = 'block';
            updateCharacteristicButtons([], true);
        } catch (err) {
            alert('Error creating character.');
        }
    });

    if (deleteBtn) deleteBtn.addEventListener('click', async function() {
        revealed = [];
        serviceAssigned = false;
        try {
            const response = await fetch('/delete_character', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            // Re-enable create button after character deletion
            if (btn) {
                btn.disabled = false;
                btn.style.opacity = '1';
            }
            // Clear all UI fields
            [charTitle, charName, charService, charRank, charUPP, charAge, charTerms, charCash, charStarship, charWeapons, charTAS].forEach(el => { if (el) el.textContent = ''; });
            [currentTerm, survivalOutcome, commissioningOutcome, promotionOutcome, termSkillsEligibility, commissionSkillsEligibility, promotionSkillsEligibility, ageingEffects, reenlistmentOutcome].forEach(el => { if (el) el.textContent = ''; });
            const logDiv = document.getElementById('term-outcome-log');
            if (logDiv) logDiv.innerHTML = '';
            updateCharacteristicButtons([], false);
            window.lastStatusData = null;
            window.skillBreakdown = null;
            // Reset term button visibility
            if (survivalBtn) survivalBtn.style.display = 'block';
            if (commissionBtn) commissionBtn.style.display = 'block';
            if (promotionBtn) promotionBtn.style.display = 'block';
            // Hide attribute, service, and term sections
            if (attributeDiv) attributeDiv.style.display = 'none';
            if (serviceDiv) serviceDiv.style.display = 'none';
            if (termSection) termSection.style.display = 'none';
        } catch (err) {
            // No message shown
        }
    });

    for (const [key, btn] of Object.entries(attrButtons)) {
        if (btn) btn.addEventListener('click', function() {
            revealCharacteristic(key);
        });
    }

    // In revealCharacteristic, handle 400 error gracefully
    async function revealCharacteristic(characteristic) {
        try {
            const response = await fetch('/reveal_characteristic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ characteristic })
            });
            if (!response.ok) {
                if (response.status === 400) {
                    // No message shown
                    return;
                }
                throw new Error('Network response was not ok');
            }
            // No message shown
            const data = await response.json();
            revealed = data.revealed;
            updateButtonVisibility();
            updateCharacteristicButtons(revealed, true);
            refreshAllUI();
        } catch (err) {
            // No message shown
        }
    }

    for (const [key, btn] of Object.entries(serviceButtons)) {
        if (btn) btn.addEventListener('click', async function() {
            try {
                const response = await fetch('/attempt_enlistment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service: serviceMap[key] })
                });
                if (!response.ok) throw new Error('Network response was not ok');
                serviceAssigned = true;
                updateButtonVisibility();
                refreshAllUI();
            } catch (err) {
                alert('Error attempting enlistment.');
            }
        });
    }

    if (survivalBtn) survivalBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/term_survival', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            // Hide the survival button immediately after successful check
            if (survivalBtn) survivalBtn.style.display = 'none';
            updateButtonVisibility();
            refreshAllUI();
        } catch (err) {
            alert('Error checking survival.');
        }
    });

    if (commissionBtn) commissionBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/term_commission', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            // Hide the commission button immediately after successful check
            if (commissionBtn) commissionBtn.style.display = 'none';
            updateButtonVisibility();
            refreshAllUI();
        } catch (err) {
            alert('Error checking commission.');
        }
    });

    if (promotionBtn) promotionBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/term_promotion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            // Hide the promotion button immediately after successful check
            if (promotionBtn) promotionBtn.style.display = 'none';
            updateButtonVisibility();
            refreshAllUI();
        } catch (err) {
            alert('Error checking promotion.');
        }
    });

    if (reenlistmentBtn) reenlistmentBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/term_reenlistment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            updateButtonVisibility();
            refreshAllUI();
        } catch (err) {
            alert('Error checking re-enlistment.');
        }
    });

    // Initial UI state
    updateButtonVisibility();
    refreshAllUI();
}); 