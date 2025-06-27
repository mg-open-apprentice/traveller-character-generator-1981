import random

def set_random_seed(seed=None):
    """Set a random seed for reproducible results during testing"""
    if seed is not None:
        random.seed(seed)
        print(f"Random seed set to: {seed}")
    else:
        # Use current time for truly random results
        import time
        random.seed(time.time())
        print("Using random seed based on current time")

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
        self.aging_log = []  # List of dicts: {'term': int, 'age': int, 'effects': [str]}
        self.term_log = []  # List of dicts: {'term': int, 'age': int, 'skills': [(table, result)], 'aging': [str]}
        self.skill_acquisition_log = []  # List of dicts: {'term': int, 'event': str, 'skill': str, 'level': int}
        self.automatic_skills_granted = set()  # Track which automatic skills have been granted
        self.commissioned = False  # Officer status
        self.rank = 0  # 0 = enlisted, 1+ = officer ranks
        self.drafted = False  # Track if drafted in first term
        self.promotions = 0  # Number of promotions (after commission)

    def complete_term(self):
        """Complete a 4-year term of service"""
        self.age += 4
        self.terms_served += 1

        # Check for aging effects
        aging_effects = self.check_aging()
        if aging_effects:
            print(f"\U0001F4C9 Aging effects this term: {', '.join(aging_effects)}")
            self.aging_log.append({
                'term': self.terms_served,  # The term just completed
                'age': self.age,
                'effects': aging_effects
            })
        # Add aging effects to the latest term_log entry (if any)
        if self.term_log and self.term_log[-1]['term'] == self.terms_served:
            self.term_log[-1]['aging'] = aging_effects

    def get_age(self):
        return self.age

    def check_aging(self):
        """Check for aging effects when crossing age thresholds"""
        aging_thresholds = [34, 38, 42, 46, 50, 54, 58, 62]
        advanced_aging_start = 66
    
        # Check which thresholds we've crossed this term
        previous_age = self.age - 4
        current_age = self.age
    
        aging_effects = []

        # Check standard thresholds (34 - 62)
        for threshold in aging_thresholds:
            if previous_age < threshold < current_age:
                print(f"\n⏰ Aging check at age {threshold}:")
                effects = self.apply_aging_effects(threshold)
                aging_effects.extend(effects)

        # Check advanced aging (66+)
        if current_age >= advanced_aging_start:
            for age in range(max(66, ((previous_age // 4) + 1) * 4), current_age + 1, 4):
                if age >= advanced_aging_start:
                    print(f"\n⚰️  Advanced aging check at age {age}:")
                    effects = self.apply_advanced_aging_effects(age)
                    aging_effects.extend(effects)

        return aging_effects

    def apply_aging_effects(self, age):
        """Apply aging effects at a specific age"""
        effects = []

        if age in [34, 38, 42, 46]:
            # Phase 1: Early aging
            checks = [
                ('str', 8, 1), ('dex', 7, 1), ('end', 8, 1)
            ]
        elif age in [50, 54, 58, 62]:
            # Phase 2: Advanced aging  
            checks = [
                ('str', 9, 1), ('dex', 8, 1), ('end', 9, 1)  # Using 'end' to match your existing code
            ]
        
        for stat, target, loss in checks:
            roll = self.roll_2d6()
            if roll < target:
                old_value = self.characteristics[stat]
                self.characteristics[stat] = max(0, self.characteristics[stat] - loss)  # Prevent negative
                actual_loss = old_value - self.characteristics[stat]
                print(f"  {stat.upper()}: Roll {roll} < {target} → Lost {actual_loss} point(s) ({old_value} → {self.characteristics[stat]})")
                effects.append(f"-{actual_loss} {stat.upper()}")
            else:
                print(f"  {stat.upper()}: Roll {roll} ≥ {target} → No loss")
        
        return effects

    def apply_advanced_aging_effects(self, age):
        """Apply advanced aging effects for ages 66+"""
        effects = []
        
        # Advanced aging affects STR, DEX, END, and INT
        checks = [
            ('str', 9, 2), ('dex', 9, 2), ('end', 9, 2), ('int', 9, 1)
        ]
        
        for stat, target, loss in checks:
            roll = self.roll_2d6()
            if roll < target:
                old_value = self.characteristics[stat]
                self.characteristics[stat] = max(0, self.characteristics[stat] - loss)  # Prevent negative
                actual_loss = old_value - self.characteristics[stat]
                print(f"  {stat.upper()}: Roll {roll} < {target} → Lost {actual_loss} point(s) ({old_value} → {self.characteristics[stat]})")
                effects.append(f"-{actual_loss} {stat.upper()}")
            else:
                print(f"  {stat.upper()}: Roll {roll} ≥ {target} → No loss")
        
        return effects

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

        if career not in survival_dict:
            print(f"WARNING: Unknown career '{career}' in survival_roll")

        return survival_dict.get(career, 5)

    @staticmethod
    def survival_bonuses(career):
        """Get characteristic requirements and bonuses for survival"""
        survival_bonuses = {
            'Navy': {'int': (7, 2)},
            'Marines': {'end': (8, 2)},
            'Army': {'edu': (6, 2)},
            'Scouts': {'end': (9, 2)},
            'Merchants': {'int': (7, 2)},
            'Others': {'int': (9, 2)}
        }
        return survival_bonuses.get(career, {})

    @staticmethod
    def check_survival(career, characteristics, death_rule_enabled=False):
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

        if survived:
            print(f"[Survival Check] Career: {career} | Roll: {roll} + Bonus: {bonus} = {total} (Need {required_roll}) → SURVIVED")
            return 'survived'
        else:
            if death_rule_enabled:
                print(f"[Survival Check] Career: {career} | Roll: {roll} + Bonus: {bonus} = {total} (Need {required_roll}) → DIED")
                return 'died'
            else:
                print(f"[Survival Check] Career: {career} | Roll: {roll} + Bonus: {bonus} = {total} (Need {required_roll}) → INJURED")
                return 'injured'

    @staticmethod
    def reenlistment_roll(career):
        """Get the target number for reenlistment"""
        reenlistment_targets = {
            'Navy': 6,
            'Marines': 6,
            'Army': 7,
            'Scouts': 3,
            'Merchants': 4,
            'Others': 5
        }
        return reenlistment_targets.get(career, 5)

    @staticmethod
    def attempt_reenlistment(career, age):
        """Attempt to reenlist for another term"""
        target = Character.reenlistment_roll(career)
        roll = Character.roll_2d6()
        
        if roll == 12:
            # Mandatory re-enlistment - always allowed regardless of age
            print(f"[Reenlistment Check] Career: {career} | Roll: {roll} → MANDATORY RE-ENLISTMENT!")
            return 'mandatory'
        elif age >= 46:
            # Characters 46+ can only continue on roll of 12
            print(f"[Reenlistment Check] Career: {career} | Age: {age} | Roll: {roll} → AGE LIMIT: MUST MUSTER OUT")
            return 'denied'
        elif roll < target:
            # Re-enlistment denied
            print(f"[Reenlistment Check] Career: {career} | Roll: {roll} < {target} → RE-ENLISTMENT DENIED")
            return 'denied'
        else:
            # Re-enlistment approved - character chooses to stay (for characters under 46)
            print(f"[Reenlistment Check] Career: {career} | Roll: {roll} ≥ {target} → RE-ENLISTMENT APPROVED (character chooses to stay)")
            return 'approved'

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

    def add_career_term(self, career, term_number, partial_term=False):
        """Add a career term to history"""
        years_served = 2 if partial_term else 4
        self.career_history.append({
            'career': career,
            'term': term_number,
            'age_start': self.age - years_served,
            'age_end': self.age,
            'partial_term': partial_term
        })

    def add_skill(self, skill_name, levels=1):
        """Add or increase a skill"""
        if skill_name in self.skills:
            self.skills[skill_name] += levels
        else:
            self.skills[skill_name] = levels
        print(f"  → Gained {skill_name} +{levels} (now level {self.skills[skill_name]})")
        # Log skill acquisition
        self.skill_acquisition_log.append({
            'term': self.terms_served,
            'event': 'skill_roll',  # Will be overridden for automatic skills
            'skill': skill_name,
            'level': levels
        })

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
        
        # Advanced (Specialist) Skills
        advanced = {
            'Navy': {1: 'Vacc Suit', 2: 'Mechanical', 3: 'Electronics', 4: 'Engineering', 5: 'Gunnery', 6: 'Computer'},
            'Marines': {1: 'Vehicle', 2: 'Mechanical', 3: 'Electronics', 4: 'Tactics', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Army': {1: 'Vehicle', 2: 'Mechanical', 3: 'Electronics', 4: 'Tactics', 5: 'Blade Combat', 6: 'Gun Combat'},
            'Scouts': {1: 'Vehicle', 2: 'Mechanical', 3: 'Electronics', 4: 'Jack-o-T', 5: 'Gunnery', 6: 'Medical'},
            'Merchants': {1: 'Streetwise', 2: 'Mechanical', 3: 'Electronics', 4: 'Navigation', 5: 'Engineering', 6: 'Computer'},
            'Others': {1: 'Streetwise', 2: 'Mechanical', 3: 'Electronics', 4: 'Gambling', 5: 'Brawling', 6: 'Forgery'}
        }
        
        # Advanced Education (EDU 8+)
        advanced_education = {
            'Navy': {1: 'Medical', 2: 'Navigation', 3: 'Engineering', 4: 'Computer', 5: 'Pilot', 6: 'Admin'},
            'Marines': {1: 'Medical', 2: 'Tactics', 3: 'Tactics', 4: 'Computer', 5: 'Leader', 6: 'Admin'},
            'Army': {1: 'Medical', 2: 'Tactics', 3: 'Tactics', 4: 'Computer', 5: 'Leader', 6: 'Admin'},
            'Scouts': {1: 'Medical', 2: 'Navigation', 3: 'Engineering', 4: 'Computer', 5: 'Pilot', 6: 'Jack-o-T'},
            'Merchants': {1: 'Medical', 2: 'Navigation', 3: 'Engineering', 4: 'Computer', 5: 'Pilot', 6: 'Admin'},
            'Others': {1: 'Medical', 2: 'Forgery', 3: 'Electronics', 4: 'Computer', 5: 'Streetwise', 6: 'Jack-o-T'}
        }
        
        return {
            'personal': personal_development,
            'service': service_skills,
            'advanced': advanced,
            'advanced_education': advanced_education
        }
    
    def roll_for_skills(self, career, num_skills=2):
        """Roll for skills during a term"""
        print(f"\nSkill rolls for term {self.terms_served}:")
        
        tables = self.get_skill_tables(career)
        skill_rolls_this_term = []
        for i in range(num_skills):
            # All characters may roll on personal, service, and advanced
            available_tables = ['personal', 'service', 'advanced']
            # Only add advanced_education if EDU >= 8
            if self.characteristics.get('edu', 0) >= 8:
                available_tables.append('advanced_education')
            # Choose a random table
            chosen_table = random.choice(available_tables)
            table = tables[chosen_table][career]
            # Roll on the table
            roll = random.randint(1, 6)
            result = table.get(roll, 'No skill')
            print(f"  Rolling on {chosen_table} table: {roll} = {result}")
            skill_rolls_this_term.append((chosen_table, result))
            # Apply the result
            if result.startswith('+1'):
                # Characteristic increase
                stat = result.split()[1].lower()
                if stat in self.characteristics:
                    self.characteristics[stat] += 1
                    print(f"  → Increased {stat.upper()} to {self.characteristics[stat]}")
                    # Log characteristic increase
                    self.skill_acquisition_log.append({
                        'term': self.terms_served,
                        'event': 'term_skill_roll',
                        'skill': stat.upper(),
                        'level': 1
                    })
            else:
                # Skill gain
                self.add_skill(result)
                # Update the last skill acquisition log entry
                if self.skill_acquisition_log:
                    self.skill_acquisition_log[-1]['event'] = 'term_skill_roll'
        # Store skill rolls for this term in term_log (aging effects will be added after complete_term)
        self.term_log.append({'term': self.terms_served, 'age': self.age, 'skills': skill_rolls_this_term, 'aging': []})
    
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
        if career in ['Scouts', 'Others']:
            return False
            
        commission_target = {
            'Navy': 10,
            'Marines': 9,
            'Army': 5,
            'Merchants': 4
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
        elif career == 'Merchants' and characteristics.get('int', 0) >= 9:
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
                if term.get('partial_term', False):
                    # Calculate which term they were injured in
                    injury_term = int(term['term'] + 0.5)  # Convert 0.5 to 1, 1.5 to 2, etc.
                    print(f"  Injured Term {injury_term}: {term['career']} (Age {term['age_start']}-{term['age_end']})")
                else:
                    print(f"  Term {term['term']}: {term['career']} (Age {term['age_start']}-{term['age_end']})")
        if self.skill_acquisition_log:
            print(f"\nSkill Acquisition History:")
            for entry in self.skill_acquisition_log:
                event_desc = {
                    'enlistment': 'Enlistment/Draft',
                    'commission': 'Commission',
                    'commission_skill_roll': 'Commission Skill Roll',
                    'promotion_skill_roll': 'Promotion Skill Roll',
                    'term_skill_roll': 'Term Skill Roll',
                    'rank_4': 'Rank 4 (Merchant First Officer)',
                    'rank_5': 'Rank 5 (Navy Captain)',
                    'rank_6': 'Rank 6 (Navy Admiral)'
                }.get(entry['event'], entry['event'])
                print(f"  Term {entry['term']}: {entry['skill']} +{entry['level']} ({event_desc})")
        if self.term_log:
            print(f"\nPer-Term Summary:")
            for entry in self.term_log:
                print(f"  Term {entry['term']} (Age {entry['age']}):")
                for idx, (table, result) in enumerate(entry['skills'], 1):
                    print(f"    Skill Roll {idx}: {table.replace('_', ' ').title()} → {result}")
                if entry['aging']:
                    print(f"    Aging Effects: {', '.join(entry['aging'])}")
                else:
                    print(f"    Aging Effects: None")
        if self.aging_log:
            print(f"\nAging Effects History:")
            for entry in self.aging_log:
                print(f"  Term {entry['term']} (Age {entry['term']}): {', '.join(entry['effects'])}")
        print(f"{'='*50}\n")

    def grant_automatic_enlistment_skill(self, career):
        """Grant automatic skill on enlistment or draft, only once per character"""
        if career == 'Army' and 'army_enlist' not in self.automatic_skills_granted:
            self.add_skill('Rifle')
            self.automatic_skills_granted.add('army_enlist')
            print("  → Automatic skill: Rifle +1 (Army enlistment/draft)")
            # Update the last skill acquisition log entry
            if self.skill_acquisition_log:
                self.skill_acquisition_log[-1]['event'] = 'enlistment'
        elif career == 'Marines' and 'marines_enlist' not in self.automatic_skills_granted:
            self.add_skill('Cutlass')
            self.automatic_skills_granted.add('marines_enlist')
            print("  → Automatic skill: Cutlass +1 (Marines enlistment/draft)")
            if self.skill_acquisition_log:
                self.skill_acquisition_log[-1]['event'] = 'enlistment'
        elif career == 'Scouts' and 'scouts_enlist' not in self.automatic_skills_granted:
            self.add_skill('Pilot')
            self.automatic_skills_granted.add('scouts_enlist')
            print("  → Automatic skill: Pilot +1 (Scouts enlistment/draft)")
            if self.skill_acquisition_log:
                self.skill_acquisition_log[-1]['event'] = 'enlistment'

    def grant_automatic_commission_skill(self, career):
        """Grant automatic skill on commission, only once per character"""
        if career == 'Army' and 'army_commission' not in self.automatic_skills_granted:
            self.add_skill('SMG')
            self.automatic_skills_granted.add('army_commission')
            print("  → Automatic skill: SMG +1 (Army commission)")
            if self.skill_acquisition_log:
                self.skill_acquisition_log[-1]['event'] = 'commission'
        elif career == 'Marines' and 'marines_commission' not in self.automatic_skills_granted:
            self.add_skill('Revolver')
            self.automatic_skills_granted.add('marines_commission')
            print("  → Automatic skill: Revolver +1 (Marines commission)")
            if self.skill_acquisition_log:
                self.skill_acquisition_log[-1]['event'] = 'commission'
        # Navy and Merchants do NOT get automatic skills on commission - only skill rolls

    def grant_automatic_rank_skill(self, career, rank):
        """Grant automatic skill for specific ranks, only once per character/rank"""
        if career == 'Merchants' and rank == 4 and 'merchants_rank4' not in self.automatic_skills_granted:
            self.add_skill('Pilot')
            self.automatic_skills_granted.add('merchants_rank4')
            print("  → Automatic skill: Pilot +1 (Merchant rank 4)")
            if self.skill_acquisition_log:
                self.skill_acquisition_log[-1]['event'] = f'rank_{rank}'
        elif career == 'Navy' and rank == 5 and 'navy_rank5' not in self.automatic_skills_granted:
            self.characteristics['soc'] += 1
            self.automatic_skills_granted.add('navy_rank5')
            print("  → Automatic skill: SOC +1 (Navy rank 5)")
            # Log SOC increase as a skill acquisition
            self.skill_acquisition_log.append({
                'term': self.terms_served,
                'event': f'rank_{rank}',
                'skill': 'SOC',
                'level': 1
            })
        elif career == 'Navy' and rank == 6 and 'navy_rank6' not in self.automatic_skills_granted:
            self.characteristics['soc'] += 1
            self.automatic_skills_granted.add('navy_rank6')
            print("  → Automatic skill: SOC +1 (Navy rank 6)")
            # Log SOC increase as a skill acquisition
            self.skill_acquisition_log.append({
                'term': self.terms_served,
                'event': f'rank_{rank}',
                'skill': 'SOC',
                'level': 1
            })

    def calculate_mustering_out_rolls(self):
        """Calculate number of mustering out rolls based on terms and rank"""
        # Count full terms only (half terms don't count)
        full_terms = int(self.terms_served)
        term_rolls = full_terms
        
        # Rank-based rolls
        rank_rolls = 0
        if self.rank >= 1 and self.rank <= 2:
            rank_rolls = 1
        elif self.rank >= 3 and self.rank <= 4:
            rank_rolls = 2
        elif self.rank >= 5 and self.rank <= 6:
            rank_rolls = 3
        
        total_rolls = term_rolls + rank_rolls
        print(f"\n💰 Mustering Out Rolls: {term_rolls} term rolls + {rank_rolls} rank rolls = {total_rolls} total")
        return total_rolls


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

def run_full_character_generation(death_rule_enabled=False):
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
        c.drafted = True
    
    c.career = final_career
    # Grant automatic skill for enlistment/draft
    c.grant_automatic_enlistment_skill(final_career)
    
    # Commission and promotion logic
    MAX_PROMOTIONS = {'Navy': 5, 'Marines': 5, 'Army': 5, 'Merchants': 4}
    eligible_for_commission = final_career in ['Navy', 'Marines', 'Army', 'Merchants']
    eligible_for_promotion = final_career in ['Navy', 'Marines', 'Army', 'Merchants']
    # Track commission attempt eligibility (not in first term if drafted)
    commission_attempted = False
    # Remove MAX_TERMS limit - characters can continue if they roll 12
    while True:  # Continue until career ends naturally
        print(f"\n--- Term {c.terms_served + 1} in {final_career} ---")
        # Check survival
        survived = Character.check_survival(final_career, c.characteristics)
        
        # Handle different survival outcomes
        if survived == 'died':
            print(f"\u2620\ufe0f  Died during term {c.terms_served + 1} in {final_career}. Final Age: {c.age}")
            break
        elif survived == 'injured':
            print(f"\u26d4\ufe0f  Injured during term {c.terms_served + 1} in {final_career}. Must muster out immediately.")
            # Update age and terms first
            c.age += 2  # Only 2 years served
            c.terms_served += 0.5
            # Then add career term with correct ages
            c.add_career_term(final_career, c.terms_served, partial_term=True)
            print(f"Final Age: {c.age}, Terms Served: {c.terms_served}")
            break
        else:  # survived == 'survived'
            # Complete the term normally
            c.complete_term()
            c.add_career_term(final_career, c.terms_served)
            
            # Commission attempt (if not already commissioned, not first term if drafted, and eligible career)
            commission_this_term = False
            if eligible_for_commission and not c.commissioned and not c.drafted:
                # Explicitly prevent commission for Scouts and Others
                if final_career in ['Navy', 'Marines', 'Army', 'Merchants']:
                    commission_this_term = Character.check_commission(final_career, c.characteristics)
                    if commission_this_term:
                        c.commissioned = True
                        c.rank = 1
                        print(f"[Commission] {final_career}: Commissioned as officer (Rank 1)")
                        # Skill roll for commission
                        c.roll_for_skills(final_career, 1)
                    else:
                        print(f"[Commission] {final_career}: Commission attempt FAILED.")
                    commission_attempted = True
            # Promotion attempt (if commissioned, not at max promotions)
            promotion_this_term = False
            max_promos = MAX_PROMOTIONS.get(final_career, 0)
            if eligible_for_promotion and c.commissioned and c.promotions < max_promos:
                # Explicitly prevent promotion for Scouts and Others
                if final_career in ['Navy', 'Marines', 'Army', 'Merchants']:
                    promotion_target = {'Navy': 8, 'Marines': 9, 'Army': 6, 'Merchants': 10}
                    roll = Character.roll_2d6()
                    target = promotion_target.get(final_career, 12)
                    modifier = 0
                    if final_career == 'Navy' and c.characteristics.get('edu', 0) >= 8:
                        modifier += 1
                    elif final_career == 'Marines' and c.characteristics.get('int', 0) >= 8:
                        modifier += 1
                    elif final_career == 'Army' and c.characteristics.get('edu', 0) >= 7:
                        modifier += 1
                    elif final_career == 'Merchants' and c.characteristics.get('int', 0) >= 9:
                        modifier += 1
                    success = (roll + modifier) >= target
                    print(f"[Promotion Check] {final_career}: Roll {roll} + {modifier} = {roll + modifier} (Need {target}) → {'PROMOTED' if success else 'FAILED'}")
                    if success:
                        c.promotions += 1
                        c.rank += 1
                        print(f"[Promotion] {final_career}: Promoted to rank {c.rank}")
                        # Grant automatic skill for specific ranks
                        c.grant_automatic_rank_skill(final_career, c.rank)
                        # Skill roll for promotion
                        c.roll_for_skills(final_career, 1)
            # Roll for term skills
            if final_career == 'Scouts':
                num_skills = 2
            else:
                num_skills = 2 if c.terms_served == 1 else 1
            c.roll_for_skills(final_career, num_skills)
            # Report aging effects for this term, if any
            if c.aging_log and c.aging_log[-1]['term'] == c.terms_served:
                effects = c.aging_log[-1]['effects']
                print(f"\n\U0001F9B4 Aging effects this term: {', '.join(effects)}")
            print(f"\n✅ Survived term {c.terms_served}. Age: {c.age}")
            
            # Attempt reenlistment
            reenlistment_result = Character.attempt_reenlistment(final_career, c.age)
            if reenlistment_result == 'denied':
                print(f"\U0001F51A Reenlistment denied. Career ends after {c.terms_served} terms at age {c.age}.")
                break
            elif reenlistment_result == 'mandatory':
                print(f"\U0001F4E5 Mandatory re-enlistment! Character must continue service.")
                # Continue to next term regardless of term count
            elif reenlistment_result == 'approved':
                print(f"\U0001F4E5 Reenlistment approved. Continuing service.")
                # Continue to next term
            
            # If drafted and successfully re-enlisted, change status to enlisted
            if c.drafted and reenlistment_result in ['approved', 'mandatory']:
                print(f"[Status Change] {final_career}: Drafted → Enlisted (successful re-enlistment)")
                c.drafted = False
    
    # Display final character sheet
    c.display_character_sheet()
    
    # Calculate mustering out rolls at the very end
    c.calculate_mustering_out_rolls()

if __name__ == "__main__":
    # Set the random seed for reproducible results
    # Change this number to get different but reproducible results
    # Set to None for truly random results
    set_random_seed(None)  # Use seed=42 for testing, or seed=None for random
    
    # By default, injury rule is enabled (survival failures = injury)
    # Set death_rule_enabled=True to enable death on survival failures
    run_full_character_generation(death_rule_enabled=False)
    
    # Uncomment below to run individual tests
    # print("\n--- Testing Individual Components ---\n")
    # test_character_stats()
    # print()
    # test_get_career_choice_modifiers()
    # print()
    # test_attempt_enlistment()
    # print()
    # test_check_survival()