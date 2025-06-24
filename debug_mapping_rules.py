#!/usr/bin/env python3
"""
Debug script to check what mapping rules are being loaded
"""

import yaml
from Utils.mapping_utils import generate_mapping_rules, initialize_database_with_default_data

def debug_mapping_rules():
    """Debug what mapping rules are being loaded"""
    
    print("🔍 Debugging Mapping Rules Loading")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize database with default data
    print("1. Initializing database with default data...")
    initialize_database_with_default_data(config)
    
    # Get mapping rules
    print("2. Getting mapping rules...")
    mapping_rules = generate_mapping_rules(config)
    
    print(f"\n📊 Mapping Rules Structure:")
    print(f"Keys in mapping_rules: {list(mapping_rules.keys())}")
    
    # Check each section
    for key, value in mapping_rules.items():
        print(f"\n🔍 {key.upper()}:")
        if isinstance(value, dict):
            print(f"  Type: dict with {len(value)} items")
            for k, v in list(value.items())[:5]:  # Show first 5
                print(f"    '{k}' -> '{v}'")
            if len(value) > 5:
                print(f"    ... and {len(value) - 5} more items")
        else:
            print(f"  Type: {type(value)}")
            print(f"  Value: {value}")
    
    # Specifically check for RA Name
    print(f"\n🎯 Looking for 'RA Name' specifically:")
    if 'special_cases' in mapping_rules:
        if 'RA Name' in mapping_rules['special_cases']:
            print(f"✅ Found 'RA Name' -> '{mapping_rules['special_cases']['RA Name']}'")
        else:
            print(f"❌ 'RA Name' not found in special_cases")
            print(f"Available special cases: {list(mapping_rules['special_cases'].keys())}")
    else:
        print(f"❌ No 'special_cases' section found in mapping rules")

if __name__ == "__main__":
    debug_mapping_rules() 