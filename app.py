from flask import Flask, jsonify, send_from_directory, request
import os
import json
from character_generator import Character

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def serve_script():
    return send_from_directory('.', 'script.js')

@app.route('/style.css')
def serve_style():
    return send_from_directory('.', 'style.css')

@app.route('/create_character', methods=['POST'])
def create_character():
    json_path = 'current_character.json'
    if os.path.exists(json_path):
        os.remove(json_path)
    character = Character()
    character.name = character.get_random_name()
    character.age = 18
    char_data = safe_dict(character)
    # Add empty characteristics and revealed list
    char_data['characteristics'] = {}
    char_data['revealed'] = []
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify({
        'name': character.name,
        'age': character.age
    })

def safe_dict(obj):
    return {k: v for k, v in obj.__dict__.items() if isinstance(v, (str, int, float, bool, list, dict, type(None)))}

@app.route('/delete_character', methods=['POST'])
def delete_character():
    json_path = 'current_character.json'
    if os.path.exists(json_path):
        os.remove(json_path)
        deleted = True
    else:
        deleted = False
    return jsonify({'deleted': deleted})

@app.route('/reveal_characteristic', methods=['POST'])
def reveal_characteristic():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    data = request.get_json()
    char_name = data.get('characteristic')
    valid_chars = ['strength', 'dexterity', 'endurance', 'intelligence', 'education', 'social']
    char_map = {
        'strength': 'str',
        'dexterity': 'dex',
        'endurance': 'end',
        'intelligence': 'int',
        'education': 'edu',
        'social': 'soc'
    }
    if char_name not in valid_chars:
        return jsonify({'error': 'Invalid characteristic'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    # Generate characteristics if not present
    if not char_data.get('characteristics'):
        all_chars = Character.generate_characteristics()
        char_data['characteristics'] = {
            'strength': all_chars['str'],
            'dexterity': all_chars['dex'],
            'endurance': all_chars['end'],
            'intelligence': all_chars['int'],
            'education': all_chars['edu'],
            'social': all_chars['soc'],
        }
        char_data['revealed'] = []
    # Reveal the requested characteristic
    if char_name not in char_data['revealed']:
        char_data['revealed'].append(char_name)
    # Build UPP string in pseudo-hex
    upp_order = ['strength', 'dexterity', 'endurance', 'intelligence', 'education', 'social']
    # Prepare a dict for hex conversion, using None for unrevealed
    revealed_chars = {}
    for c in upp_order:
        if c in char_data['revealed']:
            revealed_chars[char_map[c]] = char_data['characteristics'][c]
        else:
            revealed_chars[char_map[c]] = None
    # Convert to hex, using '-' for unrevealed
    hex_values = Character.convert_characteristics_to_hex({k: v if v is not None else 0 for k, v in revealed_chars.items()})
    upp = ''
    for c in ['str', 'dex', 'end', 'int', 'edu', 'soc']:
        if revealed_chars[c] is not None:
            upp += hex_values[c]
        else:
            upp += '-'
    # Save updated state
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify({'upp': upp, 'revealed': char_data['revealed']})

if __name__ == '__main__':
    app.run(debug=True) 