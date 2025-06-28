from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
import time
from character_generator import Character

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to something secure

# Characteristic names in order
CHARACTERISTICS = ['Strength', 'Dexterity', 'Endurance', 'Intelligence', 'Education', 'Social Standing']
CHAR_ABBREV = ['STR', 'DEX', 'END', 'INT', 'EDU', 'SOC']

@app.route('/')
def start():
    # Clear any existing session data
    session.clear()
    return render_template('start.html')

@app.route('/begin', methods=['POST'])
def begin_generation():
    seed = request.form.get('seed')
    if not seed:
        # Generate a random seed if none provided
        seed = str(random.randint(100000, 999999))
    
    session['seed'] = seed
    session['characteristics'] = {}
    session['current_char'] = 0
    
    # Set the random seed
    random.seed(int(seed))
    
    return redirect(url_for('roll_characteristics'))

@app.route('/characteristics')
def roll_characteristics():
    current_char = session.get('current_char', 0)
    
    if current_char >= len(CHARACTERISTICS):
        return redirect(url_for('choose_service'))
    
    return render_template('characteristics.html', 
                         current_char=current_char,
                         char_name=CHARACTERISTICS[current_char],
                         char_abbrev=CHAR_ABBREV[current_char],
                         characteristics=session.get('characteristics', {}))

@app.route('/roll_next', methods=['POST'])
def roll_next():
    current_char = session.get('current_char', 0)
    
    if current_char < len(CHARACTERISTICS):
        # Roll 2d6 for characteristic
        roll = random.randint(1, 6) + random.randint(1, 6)
        
        char_name = CHAR_ABBREV[current_char]
        session['characteristics'][char_name] = roll
        session['current_char'] = current_char + 1
    
    return redirect(url_for('roll_characteristics'))

@app.route('/service')
def choose_service():
    return render_template('service_choice.html', 
                         characteristics=session.get('characteristics', {}))

@app.route('/enlist', methods=['POST'])
def attempt_enlistment():
    service = request.form.get('service')
    session['service'] = service
    
    # Get characteristics from session and convert to lowercase for character generator
    characteristics = session.get('characteristics', {})
    characteristics_lower = {k.lower(): v for k, v in characteristics.items()}
    
    # Attempt enlistment using character generator
    career, enlistment_status, required_roll, enlistment_roll, modifier = Character.attempt_enlistment(characteristics_lower, service)
    
    # Create a character object and set up for basic training
    char = Character()
    char.characteristics = characteristics_lower
    char.career = career
    char.terms_served = 1  # Starting first term
    
    # Grant automatic enlistment skill
    char.grant_automatic_enlistment_skill(career)
    
    # Get the automatic skill that was granted
    auto_skill = list(char.skills.items())[0] if char.skills else None
    
    # Store character data in session for next steps
    session['character'] = {
        'career': career,
        'enlistment_status': enlistment_status,
        'terms_served': 1,
        'skills': char.skills,
        'characteristics': characteristics_lower
    }
    
    return render_template('enlistment_result.html', 
                         service=service,
                         characteristics=characteristics,
                         career=career,
                         enlistment_status=enlistment_status,
                         required_roll=required_roll,
                         enlistment_roll=enlistment_roll,
                         modifier=modifier,
                         auto_skill=auto_skill)

@app.route('/first_term')
def first_term():
    """Handle the first term: survival, commissioning, promotion, and skills"""
    char_data = session.get('character', {})
    if not char_data:
        return redirect(url_for('start'))
    
    # Recreate character object from session data
    char = Character()
    char.characteristics = char_data['characteristics']
    char.career = char_data['career']
    char.terms_served = char_data['terms_served']
    char.skills = char_data['skills']
    
    # Check survival with detailed information
    survival_result = Character.check_survival_detailed(char.career, char.characteristics)
    
    if survival_result['outcome'] == 'died':
        # Character died - end generation
        return render_template('character_death.html', career=char.career)
    elif survival_result['outcome'] == 'injured':
        # Character injured - partial term
        char.complete_term(partial_term=True)
        session['character']['terms_served'] = char.terms_served
        session['character']['age'] = char.age
        return render_template('injury_result.html', career=char.career, age=char.age)
    
    # Character survived - continue with term
    char.complete_term()
    
    # Check for commission with detailed information
    commission_result = Character.check_commission_detailed(char.career, char.characteristics)
    commissioned = False
    if commission_result['applicable'] and commission_result['success']:
        char.commissioned = True
        char.rank = 1
        char.grant_automatic_commission_skill(char.career)
        commissioned = True
    
    # Check for promotion with detailed information (if commissioned)
    promotion_result = None
    if char.commissioned:
        promotion_result = Character.check_promotion_detailed(char.career, char.characteristics, char.rank)
        if promotion_result['applicable'] and promotion_result['success']:
            char.rank = promotion_result['new_rank']
            char.grant_automatic_rank_skill(char.career, char.rank)
    
    # Update session with new character data
    session['character'].update({
        'terms_served': char.terms_served,
        'age': char.age,
        'commissioned': char.commissioned,
        'rank': char.rank,
        'skills': char.skills,
        'skill_acquisition_log': char.skill_acquisition_log,
        'term_log': char.term_log
    })
    
    return render_template('first_term_result.html',
                         career=char.career,
                         age=char.age,
                         commissioned=commissioned,
                         rank=char.rank,
                         skills=char.skills,
                         skill_log=char.skill_acquisition_log,
                         term_log=char.term_log,
                         survival_result=survival_result,
                         commission_result=commission_result,
                         promotion_result=promotion_result)

@app.route('/skill_tables')
def skill_tables():
    """Display available skill tables for player choice"""
    char_data = session.get('character', {})
    if not char_data:
        return redirect(url_for('start'))
    
    # Get available skill tables for the career
    career = char_data['career']
    characteristics = char_data['characteristics']
    tables = Character.get_skill_tables(career)
    
    # Determine which tables are available
    available_tables = ['personal', 'service', 'advanced']
    if characteristics.get('edu', 0) >= 8:
        available_tables.append('advanced_education')
    
    # Prepare table data for display
    table_data = {}
    for table_name in available_tables:
        table_data[table_name] = {
            'name': table_name.replace('_', ' ').title(),
            'contents': tables[table_name][career]
        }
    
    return render_template('skill_tables.html',
                         career=career,
                         tables=table_data,
                         edu=characteristics.get('edu', 0))

@app.route('/roll_skill', methods=['POST'])
def roll_skill():
    """Handle skill roll on chosen table"""
    char_data = session.get('character', {})
    if not char_data:
        return redirect(url_for('start'))
    
    # Get the chosen table
    chosen_table = request.form.get('table')
    roll_number = int(request.form.get('roll_number', 1))
    
    # Recreate character object
    char = Character()
    char.characteristics = char_data['characteristics']
    char.career = char_data['career']
    char.terms_served = char_data['terms_served']
    char.skills = char_data['skills']
    char.commissioned = char_data.get('commissioned', False)
    char.rank = char_data.get('rank', 0)
    
    # Get the skill tables
    tables = Character.get_skill_tables(char.career)
    table = tables[chosen_table][char.career]
    
    # Roll on the chosen table
    roll = random.randint(1, 6)
    result = table.get(roll, 'No skill')
    
    # Apply the result
    if result.startswith('+1'):
        # Characteristic increase
        stat = result.split()[1].lower()
        if stat in char.characteristics:
            char.characteristics[stat] += 1
            char.log_skill_acquisition('term', chosen_table, roll, f'+1 {stat.upper()}', 1, 'Characteristic boost')
    else:
        # Skill gain
        char.add_skill(result, 1, 'term', chosen_table, roll, 'Skill gain')
    
    # Update session
    session['character'].update({
        'skills': char.skills,
        'skill_acquisition_log': char.skill_acquisition_log
    })
    
    # Prepare roll result for display
    roll_result = {
        'table': chosen_table,
        'roll': roll,
        'result': result,
        'table_contents': table
    }
    
    return render_template('skill_roll_result.html',
                         career=char.career,
                         roll_result=roll_result,
                         skills=char.skills,
                         skill_log=char.skill_acquisition_log)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)