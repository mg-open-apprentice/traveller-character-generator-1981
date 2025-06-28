#!/usr/bin/env python3

from character_generator import Character

def test_characteristics_order():
    """Test that characteristics are displayed in the correct order: STR, DEX, END, INT, EDU, SOC"""
    
    # Create a character with known characteristics
    c = Character()
    c.characteristics = {
        'str': 10,  # A
        'dex': 8,   # 8
        'end': 12,  # C
        'int': 9,   # 9
        'edu': 11,  # B
        'soc': 7    # 7
    }
    
    print("Testing characteristic order...")
    print("Expected order: STR, DEX, END, INT, EDU, SOC")
    print("Expected UPP: A8C9B7")
    print()
    
    # Test UPP generation
    hex_chars = Character.convert_characteristics_to_hex(c.characteristics)
    upp = Character.create_hex_string(hex_chars)
    print(f"Generated UPP: {upp}")
    print(f"Expected UPP:  A8C9B7")
    print(f"Match: {'✓' if upp == 'A8C9B7' else '✗'}")
    print()
    
    # Test character sheet display
    print("Character sheet display:")
    c.display_character_sheet()
    
    print("Test completed!")

if __name__ == "__main__":
    test_characteristics_order() 