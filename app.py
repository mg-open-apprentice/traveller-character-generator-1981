from flask import Flask, jsonify, send_from_directory, request
import os
import json
from character_generator import Character

app = Flask(__name__)

def ordinal(n):
    # Dictionary mapping numbers to written ordinal forms
    ordinal_dict = {
        1: "First",
        2: "Second",
        3: "Third",
        4: "Fourth",
        5: "Fifth",
        6: "Sixth",
        7: "Seventh",
        8: "Eighth",
        9: "Ninth",
        10: "Tenth",
        11: "Eleventh",
        12: "Twelfth",
        13: "Thirteenth",
        14: "Fourteenth",
        15: "Fifteenth",
        16: "Sixteenth",
        17: "Seventeenth",
        18: "Eighteenth",
        19: "Nineteenth",
        20: "Twentieth"
    }
    return ordinal_dict.get(n, f"{n}th") if n > 0 else "Zero"

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
    char_data['terms_served'] = 0
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

@app.route('/attempt_enlistment', methods=['POST'])
def attempt_enlistment():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    data = request.get_json()
    service = data.get('service')
    valid_services = ['Navy', 'Marines', 'Army', 'Scouts', 'Merchants', 'Others']
    if service not in valid_services:
        return jsonify({'error': 'Invalid service'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    characteristics = char_data.get('characteristics', {})
    # Map to short keys for attempt_enlistment
    char_map = {
        'strength': 'str',
        'dexterity': 'dex',
        'endurance': 'end',
        'intelligence': 'int',
        'education': 'edu',
        'social': 'soc'
    }
    char_for_enlist = {char_map[k]: v for k, v in characteristics.items()}
    career, enlistment_status, required_roll, enlistment_roll, modifier = Character.attempt_enlistment(char_for_enlist, service)
    # Save outcome to character data
    char_data['service'] = career
    char_data['enlistment_status'] = enlistment_status
    char_data['enlistment_roll'] = enlistment_roll
    char_data['enlistment_required'] = required_roll
    char_data['enlistment_modifier'] = modifier
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify({
        'service': career,
        'enlistment_status': enlistment_status,
        'required_roll': required_roll,
        'enlistment_roll': enlistment_roll,
        'modifier': modifier
    })

@app.route('/term_info', methods=['GET'])
def term_info():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    term_number = char_data.get('terms_served', 0) + 1
    return jsonify({
        'term_number': term_number,
        'term_ordinal': ordinal(term_number)
    })

@app.route('/term_survival', methods=['POST'])
def term_survival():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    service = char_data.get('service')
    characteristics = char_data.get('characteristics', {})
    # Map to short keys for check_survival_detailed
    char_map = {
        'strength': 'str',
        'dexterity': 'dex',
        'endurance': 'end',
        'intelligence': 'int',
        'education': 'edu',
        'social': 'soc'
    }
    char_for_survival = {char_map[k]: v for k, v in characteristics.items()}
    result = Character.check_survival_detailed(service, char_for_survival)
    # Save outcome to character data and mark survival as completed
    char_data['last_survival'] = result
    char_data['survival_completed'] = True
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify(result)

@app.route('/term_survival', methods=['GET'])
def get_term_survival():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    return jsonify(char_data.get('last_survival', {}))

@app.route('/term_commission', methods=['POST'])
def term_commission():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    service = char_data.get('service')
    characteristics = char_data.get('characteristics', {})
    # Map to short keys for check_commission_detailed
    char_map = {
        'strength': 'str',
        'dexterity': 'dex',
        'endurance': 'end',
        'intelligence': 'int',
        'education': 'edu',
        'social': 'soc'
    }
    char_for_commission = {char_map[k]: v for k, v in characteristics.items()}
    result = Character.check_commission_detailed(service, char_for_commission)
    # Save outcome to character data and mark commission as completed
    char_data['last_commission'] = result
    char_data['commission_completed'] = True
    char_data['commission_succeeded'] = result.get('success', False)
    # If commission succeeded, mark character as commissioned permanently
    if result.get('success', False):
        char_data['is_commissioned'] = True
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify(result)

@app.route('/term_commission', methods=['GET'])
def get_term_commission():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    return jsonify(char_data.get('last_commission', {}))

@app.route('/term_promotion', methods=['POST'])
def term_promotion():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    service = char_data.get('service')
    characteristics = char_data.get('characteristics', {})
    current_rank = char_data.get('current_rank', 0)  # Default to 0 if no rank
    # Map to short keys for check_promotion_detailed
    char_map = {
        'strength': 'str',
        'dexterity': 'dex',
        'endurance': 'end',
        'intelligence': 'int',
        'education': 'edu',
        'social': 'soc'
    }
    char_for_promotion = {char_map[k]: v for k, v in characteristics.items()}
    result = Character.check_promotion_detailed(service, char_for_promotion, current_rank)
    # Save outcome to character data and mark promotion as completed
    char_data['last_promotion'] = result
    char_data['promotion_completed'] = True
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify(result)

@app.route('/term_promotion', methods=['GET'])
def get_term_promotion():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    return jsonify(char_data.get('last_promotion', {}))

@app.route('/term_button_status', methods=['GET'])
def term_button_status():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    return jsonify({
        'survival_completed': char_data.get('survival_completed', False),
        'commission_completed': char_data.get('commission_completed', False),
        'commission_succeeded': char_data.get('commission_succeeded', False),
        'is_commissioned': char_data.get('is_commissioned', False),
        'promotion_completed': char_data.get('promotion_completed', False),
        'reenlistment_completed': char_data.get('reenlistment_completed', False)
    })

@app.route('/term_reenlistment', methods=['POST'])
def term_reenlistment():
    json_path = 'current_character.json'
    if not os.path.exists(json_path):
        return jsonify({'error': 'No character found'}), 400
    with open(json_path, 'r') as f:
        char_data = json.load(f)
    service = char_data.get('service')
    age = char_data.get('age', 18)
    # For now, assume character wants to re-enlist
    result = Character.attempt_reenlistment(service, age, preference='reenlist')
    # Save outcome to character data and mark re-enlistment as completed
    char_data['last_reenlistment'] = result
    char_data['reenlistment_completed'] = True
    char_data['reenlistment_succeeded'] = result in ['approved', 'mandatory']
    # If re-enlistment succeeded, increment terms served and age
    if result in ['approved', 'mandatory']:
        char_data['terms_served'] = char_data.get('terms_served', 0) + 1
        char_data['age'] = age + 4
        # Reset term completion flags for next term
        char_data['survival_completed'] = False
        char_data['commission_completed'] = False
        char_data['promotion_completed'] = False
        char_data['last_survival'] = {}
        char_data['last_commission'] = {}
        char_data['last_promotion'] = {}
    with open(json_path, 'w') as f:
        json.dump(char_data, f)
    return jsonify({
        'result': result,
        'succeeded': result in ['approved', 'mandatory'],
        'terms_served': char_data.get('terms_served', 0),
        'age': char_data.get('age', 18)
    })

if __name__ == '__main__':
    app.run(debug=True) 