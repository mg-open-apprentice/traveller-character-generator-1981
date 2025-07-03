from flask import Flask, jsonify, send_from_directory
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
    # Delete current_character.json if it exists
    json_path = 'current_character.json'
    if os.path.exists(json_path):
        os.remove(json_path)

    # Create new character instance
    character = Character()
    character.name = character.get_random_name()
    character.age = 18

    # Save to JSON using __dict__
    def safe_dict(obj):
        # Only keep items that are basic types (str, int, float, bool, list, dict, None)
        return {k: v for k, v in obj.__dict__.items() if isinstance(v, (str, int, float, bool, list, dict, type(None)))}

    char_data = safe_dict(character)
    with open(json_path, 'w') as f:
        json.dump(char_data, f)

    return jsonify({
        'name': character.name,
        'age': character.age
    })

@app.route('/delete_character', methods=['POST'])
def delete_character():
    json_path = 'current_character.json'
    if os.path.exists(json_path):
        os.remove(json_path)
        deleted = True
    else:
        deleted = False
    return jsonify({'deleted': deleted})

if __name__ == '__main__':
    app.run(debug=True) 