<span style="font-variant: small-caps; font-size: 2em;">traveller character generator design document</span>

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

## 4. Technical Architecture

- **Frontend:**
  - Structure: HTML
  - Styling: CSS
  - Dynamic behavior: JavaScript
- **Backend:**
  - Logic: Python (existing character_generator.py)
  - Routing and API: Python (Flask or similar framework)
- **Persistence:**
  - Semi-persistent storage using JSON files for in-progress characters

## 5. Data Storage and Persistence

- Character state is stored in a JSON file throughout the generation process.
- The JSON file is updated as the user makes choices and progresses.
- Final character data is compiled into a downloadable character sheet (format TBD: PDF, JSON, or HTML).

## 6. Integration with Existing Logic

- The backend logic for character generation already exists in `character_generator.py`.
- The web app will interface with this module to process user inputs and compute intermediate and final results.
- The app will focus on UI, routing, and state management, delegating all game logic to the backend module.

## 7. Deliverables and Next Steps

- [ ] Complete design document (this file)
- [ ] Define API endpoints for frontend-backend communication
- [ ] Implement frontend SPA (HTML/CSS/JS)
- [ ] Integrate backend logic and routing
- [ ] Implement JSON-based state persistence
- [ ] Enable character sheet download functionality
- [ ] Testing and user feedback 