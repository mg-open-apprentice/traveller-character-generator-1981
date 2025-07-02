from flask import Flask, render_template, jsonify, request
from character_generator import Character
import json
import os
import traceback

app = Flask(__name__)

def load_character():
    if os.path.exists('current_character.json'):
        with open('current_character.json', 'r') as f:
            return json.load(f)
    return None

def get_character_state():
    """Determine what state the character creation is in"""
    character = load_character()
    if not character:
        return 'start'  # No character - ready to create
    elif character.get('creation_complete', False):
        return 'complete'  # Character finished
    else:
        return 'in_progress'  # Character exists but not finished

@app.route('/')
def index():
    character = load_character()
    state = get_character_state()
    return render_template('simple.html', character=character, state=state)

@app.route('/template-test')
def template_test():
    character = load_character()
    state = get_character_state()
    return render_template('simple.html', character=character, state=state)

@app.route('/api/character/create', methods=['POST'])
def create_character():
    print("=== CREATING CHARACTER ===")
    
    # Check if character already exists and is in progress
    existing_state = get_character_state()
    if existing_state == 'in_progress':
        return jsonify({"error": "Character creation already in progress"}), 400
    
    try:
        # Create new character
        character = Character()
        character.characteristics = character.generate_characteristics()
        
        character_data = {
            "name": character.name,
            "characteristics": character.characteristics,
            "creation_complete": False,  # Mark as in progress
            "creation_phase": "characteristics"  # Track what phase we're in
        }
        
        print(f"Character created: {character_data}")
        
        # Save character to file
        with open('current_character.json', 'w') as f:
            json.dump(character_data, f)
        
        return jsonify(character_data)
        
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500

@app.route('/api/character/delete', methods=['POST'])
def delete_character():
    print("=== DELETE CHARACTER ROUTE CALLED ===")
    
    try:
        if os.path.exists('current_character.json'):
            os.remove('current_character.json')
            print("Character file deleted - resetting to start state")
            return jsonify({
                "success": True, 
                "message": "Character deleted successfully", 
                "new_state": "start"
            })
        else:
            print("No character file found to delete")
            return jsonify({
                "success": True, 
                "message": "No character to delete", 
                "new_state": "start"
            })
            
    except Exception as e:
        print(f"ERROR in delete_character: {e}")
        traceback.print_exc()  # Print the full stack trace
        return jsonify({
            "success": False, 
            "message": f"Error deleting character: {str(e)}"
        }), 500

@app.route('/api/character/career', methods=['POST'])
def select_career():
    print("=== CAREER SELECTION ROUTE CALLED ===")
    
    # Check if character exists
    if get_character_state() != 'in_progress':
        return jsonify({"error": "No character in progress"}), 400
    
    try:
        # Get the career from request data
        data = request.get_json()
        if not data or 'career' not in data:
            return jsonify({"error": "No career specified"}), 400
        
        career = data['career']
        print(f"Selected career: {career}")
        
        # Load current character data
        character_data = load_character()
        if not character_data:
            return jsonify({"error": "Character not found"}), 404
        
        # Update character with selected career
        character_data['career'] = career
        character_data['creation_phase'] = 'enlistment'  # Move to next phase
        
        # Save updated character
        with open('current_character.json', 'w') as f:
            json.dump(character_data, f)
        
        return jsonify({
            "success": True,
            "message": f"Career selected: {career}",
            "character": character_data
        })
        
    except Exception as e:
        print(f"ERROR in select_career: {e}")
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500

@app.route('/test-character')
def test_character():
    try:
        character = Character()
        character.characteristics = character.generate_characteristics()
        
        html = f"""
        <h1>Character Test</h1>
        <p>Name: {character.name}</p>
        <p>STR: {character.characteristics['str']}</p>
        <a href='/template-test'>Back to Template Test</a>
        """
        return html
        
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, port=5000)