import random

class Character:
    def __init__(self):
        self.age = 18  # Starting age (Traveller standard)
        self.terms_served = 0
        self.characteristics = {}
        self.career = None
        self.name = self.get_random_name()
        self.career_history = []
        self.skills = {}  # Dict of skill_name: level
        self.mustering_out_benefits = {'cash': 0, 'items': []}

    def complete_term(self):
        """Complete a 4-year term of service"""
        self.age += 4
        self.terms_served += 1

    def get_age(self):
        return self.age

    def get_terms_served(self):
        return self.terms_served

    @staticmethod
    def roll_2d6():
        """Roll 2d6 (standard Traveller dice mechanic)"""
        return random.randint(1, 6) + random.randint(1, 6)

    @staticmethod
    def generate_characteristics():
        """Generate the six basic characteristics"""
        characteristics_order = ['str', 'dex', 'end', 'int', 'edu', 'soc']
        return {attr: Character.roll_2d6() for attr in characteristics_order}

    @staticmethod
    def convert_characteristics_to_hex(characteristics):
        """Convert characteristics to hexadecimal notation (10-15 become A-F)"""
        return {
            k: hex(v)[2:].upper() if 10 <= v <= 15 else str(v)
            for k, v in characteristics.items()
        }

    @staticmethod
    def create_hex_string(hex_values):
        """Create UPP (Universal Personality Profile) string"""
        return ''.join(hex_values.values())

    # --- CAREER LOGIC ---

    @staticmethod
    def get_available_careers():
        """Return list of available careers"""
        return ['Navy', 'Marines', 'Army', 'Scouts', 'Merchants', 'Others']

    @staticmethod
    def get_random_career():
        """Get a random career for testing"""
        return random.choice(Character.get_available_careers())

    @staticmethod
    def enlistment_roll(chosen_career):
        """Get the target number for enlistment in a career"""
        career_dict = {
            'Navy': 8,
            'Marines': 9,
            'Army': 5,
            'Scouts': 7,
            'Merchants': 7,
            'Others': 3
        }
        return career_dict.get(chosen_career, 5)

    @staticmethod
    def get_career_bonuses(chosen_career):
        """Get characteristic requirements and bonuses for enlistment"""
        career_choice_bonuses = {
            'Navy': {'int': (8, 1), 'edu': (9, 2)},
            'Marines': {'int': (8, 1), 'str': (8, 2)},
            'Army': {'dex': (6, 1), 'end': (5, 2)},
            'Scouts': {'int': (6, 1), 'str': (8, 2)},
            'Merchants': {'str': (7, 1), 'int': (6, 2)},
            'Others': {}
        }
        return career_choice_bonuses.get(chosen_career, {})

    @staticmethod
    def get_career_choice_modifiers(characteristics, chosen_career):
        """Calculate enlistment modifiers based on characteristics"""
        bonuses = Character.get_career_bonuses(chosen_career)
        return sum(
            bonus for attr, (req, bonus) in bonuses.items()
            if characteristics.get(attr, 0) >= req
        )

    @staticmethod
    def attempt_enlistment(characteristics, chosen_career):
        """Attempt to enlist in chosen career"""
        required_roll = Character.enlistment_roll(chosen_career)
        enlistment_roll = Character.roll_2d6()
        modifier = Character.get_career_choice_modifiers(characteristics, chosen_career)
        successful = enlistment_roll + modifier >= required_roll

        if successful:
            enlistment_status = 'enlisted'
            final_career = chosen_career
        else:
            enlistment_status = 'drafted'
            final_career = Character.get_draft_career()

        return final_career, enlistment_status, required_roll, enlistment_roll, modifier

    @staticmethod
    def get_draft_career():
        """Get randomly assigned career when enlistment fails"""
        return random.choice(Character.get_available_careers())

    # --- SURVIVAL LOGIC ---

    @staticmethod
    def survival_roll(career):
        """Get the target number for survival in a career"""
        survival_dict = {
            'Navy': 5,
            'Marines': 6,
            'Army': 5,
            'Scouts': 7,
            'Merchants': 5,
            'Others': 5
        }
        return survival_dict.get(career, 5)

    @staticmethod
    def survival_bonuses(career):
        """Get characteristic requirements and bonuses for survival"""
        survival_bonuses = {
            'Navy': {'int': (7, 1)},
            'Marines': {'end': (8, 1)},
            'Army': {'edu': (6, 1)},
            'Scouts': {'end': (9, 1)},
            'Merchants': {'int': (7, 1)},
            'Others': {}
        }
        return survival_bonuses.get(career, {})

    @staticmethod
    def check_survival(career, characteristics):
        """Check if character survives the term"""
        required_roll = Character.survival_roll(career)
        roll = Character.roll_2d6()
        bonus = 0

        bonuses = Character.survival_bonuses(career)
        for attr, (req, bns) in bonuses.items():
            if characteristics.get(attr, 0) >= req:
                bonus += bns

        total = roll + bonus
        survived = total >= required_roll

        print(f"[Survival Check] Career: {career} | Roll: {roll} + Bonus: {bonus} = {total} (Need {required_roll}) → {'SURVIVED' if survived else 'DIED'}")
        return survived

    @staticmethod
    def reenlistment_roll(career):
        """Get the target number for reenlistment"""
        reenlistment_targets = {
            'Navy': 6,
            'Marines': 6,
            'Army': 7,
            'Scouts': 6,
            'Merchants': 4,
            'Others': 5
        }
        return reenlistment_targets.get(career, 5)

    @staticmethod
    def attempt_reenlistment(career):
        """Attempt to reenlist for another term"""
        target = Character.reenlistment_roll(career)
        roll = Character.roll_2d6()
        success = roll >= target
        print(f"[Reenlistment Check] Career: {career} | Roll: {roll} (Need {target}) → {'APPROVED' if success else 'DENIED'}")
        return success

    @staticmethod
    def get_random_name():
        """Generate a random sci-fi name"""
        sci_fi_names = [
            "Zara Xylo", "Orion Pax", "Nova Kin", "Elexis Vortex",
            "Jaxon Starfire", "Lyra Nebulae", "Nyx Solaris", "Ryker Quantum",
            "Elara Galaxy", "Caelum Void", "Vega Stardust", "Draco Cosmos",
            "Aurora Hyperdrive", "Cassius Meteor", "Astra Comet", "Kaius Eclipse",
            "Seren Andromeda", "Altair Nebular", "Selene Astraeus", "Maximus Ion"
        ]
        return random.choice(sci_fi_names)

    def add_career_term(self, career, term_number):
        """Add a career term to history"""
        self.career_history.append({
            'career': career,
            'term': term_number,
            'age_start': self.age - 4,
            'age_end': self.age
        })

    def add_skill(self, skill_name, levels=1):
        """Add or increase a skill"""
        if skill_name in self.skills:
            self.skills[skill_name] += levels
        else:
            self.skills[skill_name] = levels
        print(f"  → Gained {skill_name} +{levels} (now level {self.skills[skill_name]})")

    # --- SKILL TABLES ---
    
    @staticmethod
    def get_skill_tables(career):
        """Get all skill tables for a career"""
        # Personal Development tables (same structure for all careers, values differ)
        personal_development = {
            'Navy': {1: '+1 STR', 2: '+1 DEX', 3: '+1 END', 4: '+1 INT', 5: '+1 EDU', 6: '+1 SOC'},
            'Marines': {1: '+1 STR', 2: '+1 DEX', 3: '+1 END', 4: 'Gambling', 5: 'Brawling', 6: 'Blade Combat'},
            'Army': {1: '+1 STR', 2: '+1 DEX', 3: '+1 END', 4: 'Gambling', 5: '+1 EDU', 6: 'Brawling'},
            'Scouts': {1: '+1 STR', 2: '+1 DEX', 3: '+1 END', 4: '+1 INT', 5: '+1 EDU', 6: 'Gun Combat'},
            'Merchants': {1: '+1 STR', 2: '+1 DEX', 3: '+1 END', 4: 'Blade Combat', 5: 'Bribery', 6: '+1 INT'},
            'Others': {1: '+1 STR', 2: '+1 DEX', 3: '+1 END', 4: 'Blade Combat', 5: 'Brawling', 6: '+1 SOC'}
        }
        
        # Service Skills
        service_skills = {
            'Navy': {1: 'Ship\'s Boat', 2: 'Vacc Suit', 3: 'Forward Observer', 4: 'Gunnery', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Marines': {1: 'Vehicle', 2: 'Vacc Suit', 3: 'Blade Combat', 4: 'Gun Combat', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Army': {1: 'Vehicle', 2: 'Air/Raft', 3: 'Gun Combat', 4: 'Forward Observer', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Scouts': {1: 'Vehicle', 2: 'Vacc Suit', 3: 'Mechanical', 4: 'Navigation', 5: 'Electronics', 6: 'Jack-o-T'},
            'Merchants': {1: 'Vehicle', 2: 'Vacc Suit', 3: 'Jack-o-T', 4: 'Steward', 5: 'Electronics', 6: 'Gun Combat'},
            'Others': {1: 'Vehicle', 2: 'Gambling', 3: 'Brawling', 4: 'Bribery', 5: 'Blade Combat', 6: 'Gun Combat'}
        }
        
        # Advanced Education (requires EDU 8+)
        advanced_education = {
            'Navy': {1: 'Vacc Suit', 2: 'Mechanical', 3: 'Electronics', 4: 'Engineering', 5: 'Gunnery', 6: 'Computer'},
            'Marines': {1: 'Vehicle', 2: 'Mechanical', 3: 'Electronics', 4: 'Tactics', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Army': {1: 'Vehicle', 2: 'Mechanical', 3: 'Electronics', 4: 'Tactics', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Scouts': {1: 'Vehicle', 2: 'Mechanical', 3: 'Electronics', 4: 'Jack-o-T', 5: 'Gunnery', 6: 'Medical'},
            'Merchants': {1: 'Streetwise', 2: 'Mechanical', 3: 'Electronics', 4: 'Navigation', 5: 'Engineering', 6: 'Computer'},
            'Others': {1: 'Streetwise', 2: 'Mechanical', 3: 'Electronics', 4: 'Gambling', 5: 'Brawling', 6: 'Forgery'}
        }
        
        # Advanced Education 2 (officer/specialized - requires EDU 10+ or rank)
        advanced_education_2 = {
            'Navy': {1: 'Medical', 2: 'Navigation', 3: 'Engineering', 4: 'Computer', 5: 'Pilot', 6: 'Admin'},
            'Marines': {1: 'Medical', 2: 'Tactics', 3: 'Tactics', 4: 'Computer', 5: 'Leader', 6: 'Admin'},
            'Army': {1: 'Medical', 2: 'Tactics', 3: 'Tactics', 4: 'Computer', 5: 'Leader', 6: 'Admin'},
            'Scouts': {1: 'Medical', 2: 'Navigation', 3: 'Engineering', 4: 'Computer', 5: 'Pilot', 6: 'Jack-o-T'},
            'Merchants': {1: 'Medical', 2: 'Navigation', 3: 'Engineering', 4: 'Computer', 5: 'Pilot', 6: 'Admin'},
            'Others': {1: 'Medical', 2: 'Forgery', 3: 'Electronics', 4: 'Computer', 5: 'Streetwise', 6: 'Jack-o-T'}
        }
        
        return {
            'personal': personal_development.get(career, {}),
            'service': service_skills.get(career, {}),
            'advanced': advanced_education.get(career, {}),
            'advanced2': advanced_education_2.get(career, {})
        }
    
    def roll_for_skills(self, career, num_skills=2):
        """Roll for skills during a term"""
        print(f"\nSkill rolls for term {self.terms_served}:")
        
        tables = self.get_skill_tables(career)
        
        for i in range(num_skills):
            # Determine available tables
            available_tables = ['personal', 'service']
            
            # Add advanced tables if education is high enough
            if self.characteristics.get('edu', 0) >= 8:
                available_tables.append('advanced')
            if self.characteristics.get('edu', 0) >= 10:
                available_tables.append('advanced2')
            
            # Choose a random table
            chosen_table = random.choice(available_tables)
            table = tables[chosen_table]
            
            # Roll on the table
            roll = random.randint(1, 6)
            result = table.get(roll, 'No skill')
            
            print(f"  Rolling on {chosen_table} table: {roll} = {result}")
            
            # Apply the result
            if result.startswith('+1'):
                # Characteristic increase
                stat = result.split()[1].lower()
                if stat in self.characteristics:
                    self.characteristics[stat] += 1
                    print(f"  → Increased {stat.upper()} to {self.characteristics[stat]}")
            else:
                # Skill gain
                self.add_skill(result)
    
    def get_commission_bonus_skills(self, career):
        """Get automatic skills for being commissioned"""
        commission_skills = {
            'Navy': 'Social Standing +1',
            'Marines': 'Revolver',
            'Army': 'SMG',
            'Scouts': None,  # No commission in Scouts
            'Merchants': None,  # No commission in Merchants
            'Others': None
        }
        return commission_skills.get(career)
    
    @staticmethod
    def check_commission(career, characteristics):
        """Check if character receives commission (simplified)"""
        if career in ['Scouts', 'Merchants', 'Others']:
            return False
            
        commission_target = {
            'Navy': 10,
            'Marines': 9,
            'Army': 5
        }
        
        roll = Character.roll_2d6()
        target = commission_target.get(career, 12)
        
        # Add modifiers based on characteristics
        modifier = 0
        if career == 'Navy' and characteristics.get('soc', 0) >= 9:
            modifier += 1
        elif career == 'Marines' and characteristics.get('edu', 0) >= 7:
            modifier += 1
        elif career == 'Army' and characteristics.get('end', 0) >= 7:
            modifier += 1
            
        success = (roll + modifier) >= target
        if success:
            print(f"[Commission Check] Roll: {roll} + {modifier} = {roll + modifier} (Need {target}) → COMMISSIONED!")
        
        return success

    def display_character_sheet(self):
        """Display character information"""
        print(f"\n{'='*50}")
        print(f"CHARACTER SHEET")
        print(f"{'='*50}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Terms Served: {self.terms_served}")
        print(f"\nCharacteristics:")
        for attr, value in self.characteristics.items():
            hex_val = hex(value)[2:].upper() if 10 <= value <= 15 else str(value)
            print(f"  {attr.upper()}: {value} ({hex_val})")
        
        hex_chars = self.convert_characteristics_to_hex(self.characteristics)
        upp = self.create_hex_string(hex_chars)
        print(f"\nUPP: {upp}")
        
        if self.skills:
            print(f"\nSkills:")
            for skill, level in sorted(self.skills.items()):
                print(f"  {skill}-{level}")
        else:
            print(f"\nNo skills acquired")
        
        if self.career_history:
            print(f"\nCareer History:")
            for term in self.career_history:
                print(f"  Term {term['term']}: {term['career']} (Age {term['age_start']}-{term['age_end']})")
        print(f"{'='*50}\n")


# --- TEST FUNCTIONS ---
def test_character_stats():
    """Test characteristic generation"""
    characteristics = Character.generate_characteristics()
    print("Generated Stats:", characteristics)
    hex_chars = Character.convert_characteristics_to_hex(characteristics)
    print("Hex Values:", hex_chars)
    print("UPP String:", Character.create_hex_string(hex_chars))

def test_get_career_choice_modifiers():
    """Test career modifier calculation"""
    characteristics = {'str': 8, 'dex': 6, 'end': 5, 'int': 9, 'edu': 9, 'soc': 7}
    for career in Character.get_available_careers():
        modifiers = Character.get_career_choice_modifiers(characteristics, career)
        print(f"Modifiers for {career}: +{modifiers}")

def test_attempt_enlistment():
    """Test enlistment process"""
    characteristics = {'str': 8, 'dex': 6, 'end': 5, 'int': 9, 'edu': 9, 'soc': 7}
    chosen_career = 'Navy'
    result = Character.attempt_enlistment(characteristics, chosen_career)
    final_career, status, required_roll, roll, modifier = result
    print(f"Attempting {chosen_career}: Roll {roll} + {modifier} = {roll + modifier} (Need {required_roll})")
    print(f"Result: {status.upper()} as {final_career}")

def test_check_survival():
    """Test survival check"""
    characteristics = {'str': 8, 'dex': 6, 'end': 5, 'int': 9, 'edu': 9, 'soc': 7}
    career = 'Marines'
    survival_outcome = Character.check_survival(career, characteristics)
    print(f"Survival Outcome for {career}: {survival_outcome}")

def run_full_character_generation():
    """Run a complete character generation"""
    print("\n" + "="*60)
    print("TRAVELLER CHARACTER GENERATION")
    print("="*60 + "\n")
    
    # Create character
    c = Character()
    c.characteristics = c.generate_characteristics()
    
    print(f"Character Name: {c.name}")
    print("Generated Stats:", c.characteristics)
    
    # Pick a career to attempt
    chosen_career = Character.get_random_career()
    print(f"\nAttempting to enlist in: {chosen_career}")
    
    # Attempt enlistment
    final_career, status, required_roll, roll, modifier = Character.attempt_enlistment(c.characteristics, chosen_career)
    print(f"Roll: {roll} + Modifier: {modifier} = {roll + modifier}")
    print(f"Needed: {required_roll} → Result: {status.upper()} as {final_career}")
    
    if status == "drafted":
        print(f"Failed enlistment, drafted into: {final_career}")
    
    c.career = final_career
    
    # Check for commission in first term (military careers only)
    commissioned = False
    if c.terms_served == 0 and final_career in ['Navy', 'Marines', 'Army']:
        commissioned = Character.check_commission(final_career, c.characteristics)
        if commissioned:
            commission_skill = c.get_commission_bonus_skills(final_career)
            if commission_skill:
                if commission_skill == 'Social Standing +1':
                    c.characteristics['soc'] += 1
                    print(f"  → Commission bonus: SOC increased to {c.characteristics['soc']}")
                else:
                    c.add_skill(commission_skill)
    
    MAX_TERMS = 7
    
    while c.terms_served < MAX_TERMS:
        print(f"\n--- Term {c.terms_served + 1} in {final_career} ---")
        
        # Check survival
        survived = Character.check_survival(final_career, c.characteristics)
        if not survived:
            print(f"☠️  Died during term {c.terms_served + 1} in {final_career}. Final Age: {c.age}")
            break
        
        # Complete the term
        c.complete_term()
        c.add_career_term(final_career, c.terms_served)
        
        # Roll for skills (2 per term, +1 if first term)
        num_skills = 3 if c.terms_served == 1 else 2
        c.roll_for_skills(final_career, num_skills)
        
        print(f"\n✅ Survived term {c.terms_served}. Age: {c.age}")
        
        # Check if reached max terms
        if c.terms_served >= MAX_TERMS:
            print(f"\n🎖️  Reached maximum service limit ({MAX_TERMS} terms).")
            break
        
        # Attempt reenlistment
        if not Character.attempt_reenlistment(final_career):
            print(f"🔚 Reenlistment denied. Career ends after {c.terms_served} terms at age {c.age}.")
            break
    
    # Display final character sheet
    c.display_character_sheet()


if __name__ == "__main__":
    # Run the full character generation
    run_full_character_generation()
    
    # Uncomment below to run individual tests
    # print("\n--- Testing Individual Components ---\n")
    # test_character_stats()
    # print()
    # test_get_career_choice_modifiers()
    # print()
    # test_attempt_enlistment()
    # print()
    # test_check_survival()