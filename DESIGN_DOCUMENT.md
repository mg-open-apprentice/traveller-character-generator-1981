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