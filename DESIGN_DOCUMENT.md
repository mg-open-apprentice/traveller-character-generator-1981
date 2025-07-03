Classic Traveller Character Generator - Specification

> **Note:**  
> This document now serves as a specification for the completed minimal MVP of the Classic Traveller Character Generator. The functionality described below has been implemented and verified as working.

## 1. Minimal MVP Functionality (Implemented)

- The web interface provides two buttons: **Create Character** and **Delete Character**.
- **Create Character**:
  - Deletes any existing `current_character.json` file.
  - Instantiates a new character using the backend (`Character` class from `character_generator.py`).
  - Sets the character's name using a random sci-fi name generator and sets age to 18.
  - Saves the character's data (name, age, and other serializable fields) to `current_character.json`.
  - Displays the character's name and age in the UI.
- **Delete Character**:
  - Deletes the `current_character.json` file if it exists.
  - Displays a confirmation message in the UI.
- The backend is implemented in Flask, with endpoints `/create_character` and `/delete_character`.
- The frontend consists of `index.html`, `script.js`, and `style.css` in the project root, communicating with the backend via fetch requests.

---

## Current Implementation Status (as of [latest milestone])

- The app is a single-page web application (SPA) with a left-hand sidebar and a main content area.
- The sidebar is divided into three sections:
  1. **Character Actions:** Create Character, Delete Character
  2. **Characteristics:** Six attribute buttons (progressive reveal)
  3. **Service Selection:** Six service buttons (Navy, Marines, Army, Scouts, Merchants, Others)
- The workflow is progressive:
  - Only the relevant section is visible at each stage.
  - After all characteristics are revealed, only service selection is shown.
  - After a service is assigned (enlisted or drafted), only Character Actions remain.
- All UI updates are dynamic; no page reloads.

### Implementation Details

- **Frontend:**
  - HTML/CSS for layout, section headers, and dividers.
  - JavaScript for dynamic show/hide of sidebar sections and for calling backend endpoints.
- **Backend:**
  - Flask endpoints for character creation, deletion, characteristic reveal, and service enlistment.
  - State is stored in `current_character.json`.
- **Progressive Workflow:**
  - Characteristics are revealed one at a time; after all are revealed, service selection is enabled.
  - Service selection attempts enlistment and may result in drafting.

### GUI Elements and Backend Mapping

| GUI Element (Button/Section) | Backend Endpoint         | character_generator.py Function(s)      | Description/Workflow Step                |
|------------------------------|-------------------------|-----------------------------------------|------------------------------------------|
| Create Character             | `/create_character`     | `Character.__init__`, `get_random_name` | Start new character, set name/age        |
| Delete Character             | `/delete_character`     | (none)                                  | Delete/reset character                   |
| Strength, Dexterity, ...     | `/reveal_characteristic`| `generate_characteristics`, `convert_characteristics_to_hex` | Reveal and display each attribute        |
| Navy, Marines, ...           | `/attempt_enlistment`   | `attempt_enlistment`, `get_draft_career`| Attempt to enlist, possibly draft        |

## Updated Button ↔ Endpoint Correspondence for Term Workflow

- **Commission and Promotion** are now separate buttons and endpoints for clarity and direct mapping to backend logic.
- **Term outcome buttons** (Survival, Commission, Promotion, Skills, Ageing, Re-enlistment) are visually grouped in the lower half of the interface.
- **Skills buttons** are dynamically generated: after commission/promotion, a button is shown for each skill table the character is eligible for (based on education, service, etc.). Each button resolves one skill roll and disappears once resolved.

| Button Name         | When Shown / Logic                                 | Backend Endpoint           | character_generator.py Function(s)         | Description/Workflow Step                |
|---------------------|----------------------------------------------------|----------------------------|--------------------------------------------|------------------------------------------|
| Survival            | Start of each term                                 | `/term_survival`           | `check_survival_detailed`                  | Survival check for the term              |
| Commission          | If eligible, after survival                        | `/term_commission`         | `check_commission_detailed`                | Attempt to gain commission               |
| Promotion           | If eligible, after commission                      | `/term_promotion`          | `check_promotion_detailed`                 | Attempt to gain promotion                |
| Skill Table X       | For each eligible skill table, after promotion     | `/term_skill`              | `roll_for_skills`, `add_skill`             | Resolve one skill roll for a table       |
| Ageing              | After all skills resolved, if age threshold passed | `/term_ageing`             | `check_ageing`, `apply_ageing_effects`, `apply_advanced_ageing_effects` | Apply ageing effects      |
| Re-enlistment       | End of term                                        | `/term_reenlistment`       | `attempt_reenlistment`, `reenlistment_roll`| Attempt to re-enlist or muster out       |

- **Skill Table Buttons:** The number and type of skill buttons depend on the character’s eligibility (e.g., education, service, term events). Each button triggers a roll for a specific skill table and disappears once resolved.
- **Button Visibility:** Only show buttons relevant to the current step in the term workflow. Disable or hide buttons that are not currently actionable.

## 1. Project Overview

The Traveller Character Generator is a web-based application designed to guide users through the process of creating a character for the 1981 'Classic Traveller' science fiction role-playing game. The generator supports users through the initial character creation, career progression, and mustering out, culminating in a downloadable character sheet.

## 2. Goals and Scope

- Provide an interactive, browser-based character generation experience for Classic Traveller (1981 rules).
- Guide users step-by-step through character creation, career terms, and mustering out.
- Store character progress in a JSON file during the process.
- Allow users to download a completed character sheet at the end.
- Leverage existing backend logic for character generation to avoid unnecessary duplication.

## 3. User Experience Flow

- Single-page web application (SPA) interface.
- User begins character creation and is guided through each decision point (attributes, career choices, events, etc.).
- Progress is saved semi-persistently in a JSON file.
- Upon completion, the user can download a summary character sheet.

## 4. Interface Details

The interface is based on a wireframe with the following key elements:

- **Sidebar/Menu:**
  - Options to create character, muster out, or delete character.
  - List of attributes: strength, dexterity, endurance, intelligence, education, social.
  - List of services: navy, marines, army, scouts, merchants, others.
  - Career phase actions: survival, commission, promotion, skills, ageing, re-enlistment.

- **Main Display Area:**
  - Character summary: title, name, service, rank, UPP (Universal Personality Profile), age, terms.
  - Terms and skills breakdown.
  - Cash, retirement pay, starship, weapon, and TAS (Traveller's Aid Society) status.
  - Detailed breakdown for each term: survival, commission, promotion, skills, ageing, term completion, re-enlistment, with outcomes and skill details.

- **User Actions:**
  - Stepwise progression through character creation phases.
  - Buttons or controls for each phase (e.g., roll characteristics, choose service, resolve survival, etc.).

## 5. State Model and Routing

The application state and routing are governed by a state model, which ensures the correct interface and options are presented at each stage. Key state domains include:

- **Character Generation Status:**
  - `new (blank)`: No character started.
  - `in-progress`: Character creation underway.
  - `completed`: Character generation finished.

- **Enlistment Status:**
  - `pre-enlisted`, `enlisted`, `commissioned`, `drafted`, `post-service`.

- **Survival Status:**
  - `pre-survival-check`, `survived`, `injured`, `fatal-injury`.

- **Promotion Status:**
  - `ineligible-for-commission`, `eligible-for-commission`, `ineligible-for-promotion`, `eligible-for-promotion`.

- **Re-enlistment Status:**
  - `applied_for_discharge`, `applied_for_retirement`, `applied_for_reenlistment`.

- **Post-Service Status:**
  - `serving`, `discharged`, `retired`, `military-discharged`, `medical-discharged`, `military-retirement`, `dead`.

**Routing Logic:**
- The UI presents only the actions and information relevant to the current state.
- State transitions (e.g., from 'pre-enlisted' to 'enlisted') trigger updates to the available UI controls and displayed information.
- The state model ensures users cannot skip required steps or access actions out of sequence.
- Debug and error states (e.g., incomplete UPP, missing career) are tracked for troubleshooting and user feedback.

## 6. Technical Architecture

- **Frontend:**
  - Structure: HTML
  - Styling: CSS
  - Dynamic behavior: JavaScript
- **Backend:**
  - Logic: Python (existing character_generator.py)
  - Routing and API: Python (Flask or similar framework)
- **Persistence:**
  - Semi-persistent storage using JSON files for in-progress characters

## 7. Data Storage and Persistence

- Character state is stored in a JSON file throughout the generation process.
- The JSON file is updated as the user makes choices and progresses.
- Final character data is compiled into a downloadable character sheet (format TBD: PDF, JSON, or HTML).

## 8. Integration with Existing Logic

- The backend logic for character generation already exists in `character_generator.py`.
- The web app will interface with this module to process user inputs and compute intermediate and final results.
- The app will focus on UI, routing, and state management, delegating all game logic to the backend module.

## 9. Deliverables and Next Steps

- [x] Complete design document (this file)
- [x] Define API endpoints for frontend-backend communication
- [x] Implement frontend SPA (HTML/CSS/JS)
- [x] Integrate backend logic and routing
- [x] Implement JSON-based state persistence
- [ ] Enable character sheet download functionality
- [ ] Testing and user feedback 