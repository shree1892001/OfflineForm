#!/usr/bin/env python3
"""
Debug script to test "RA Name" special case mapping
"""

import json
import yaml
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Utils.capitalized_json_mapper import CapitalizedJsonMapper
from Utils.mapping_utils import generate_mapping_rules, initialize_database_with_default_data

def debug_ra_name_mapping():
    """Debug the RA Name special case mapping"""
    
    print("🔍 Debugging RA Name Special Case Mapping")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize mapper
    mapper = CapitalizedJsonMapper(config)
    
    # Real user JSON
    real_user_json = {
        "payload": {
            "Registered_Agent": {
                "keyPersonnelName": "Sam sharan",
                "emailId": "saumya@gmail.com",
                "contactNo": 388383838,
                "Address": {
                    "city": "Pune",
                    "state ": 1,
                    "zip_code": "07004"
                }
            }
        }
    }
    
    print("📋 Test User JSON:")
    print(json.dumps(real_user_json, indent=2))
    
    # Extract payload
    extracted_payload = mapper.extract_payload_from_source(real_user_json)
    print(f"\n📋 Extracted payload:")
    print(json.dumps(extracted_payload, indent=2))
    
    # Get mapping rules
    initialize_database_with_default_data(config)
    mapping_rules = generate_mapping_rules(config)
    
    print(f"\n🔍 Special Cases in mapping rules:")
    if 'special_cases' in mapping_rules:
        for key, value in mapping_rules['special_cases'].items():
            print(f"  '{key}' -> '{value}'")
    
    # Test RA Name specifically
    pdf_field_name = "RA Name"
    print(f"\n🎯 Testing specific case: '{pdf_field_name}'")
    
    if 'special_cases' in mapping_rules and pdf_field_name in mapping_rules['special_cases']:
        special_case_target = mapping_rules['special_cases'][pdf_field_name]
        print(f"✅ Found special case: '{pdf_field_name}' -> '{special_case_target}'")
        
        # Test the current logic
        user_value = None
        if 'Legal Name' in special_case_target:
            user_value = mapper._get_value_by_path(extracted_payload, "name.legal_name")
            print(f"  Tried 'Legal Name' path: name.legal_name -> {user_value}")
        elif 'Registered Agent' in special_case_target:
            if 'City' in special_case_target:
                user_value = mapper._get_value_by_path(extracted_payload, "Registered_Agent.Address.city")
                print(f"  Tried 'City' path: Registered_Agent.Address.city -> {user_value}")
            elif 'State' in special_case_target:
                user_value = mapper._get_value_by_path(extracted_payload, "Registered_Agent.Address.state")
                print(f"  Tried 'State' path: Registered_Agent.Address.state -> {user_value}")
            elif 'Zip Code' in special_case_target:
                user_value = mapper._get_value_by_path(extracted_payload, "Registered_Agent.Address.zip_code")
                print(f"  Tried 'Zip Code' path: Registered_Agent.Address.zip_code -> {user_value}")
            elif 'Name' in special_case_target:
                user_value = mapper._get_value_by_path(extracted_payload, "Registered_Agent.keyPersonnelName")
                print(f"  Tried 'Name' path: Registered_Agent.keyPersonnelName -> {user_value}")
        
        print(f"\n📊 Result: {user_value}")
        
        # Test all possible paths for Registered Agent
        print(f"\n🔍 Testing all possible Registered Agent paths:")
        possible_paths = [
            "Registered_Agent.keyPersonnelName",
            "Registered_Agent.name",
            "Registered_Agent.Name",
            "Registered_Agent.personnelName",
            "Registered_Agent.contactName"
        ]
        
        for path in possible_paths:
            value = mapper._get_value_by_path(extracted_payload, path)
            print(f"  {path} -> {value}")
    
    else:
        print(f"❌ Special case '{pdf_field_name}' not found in mapping rules")

if __name__ == "__main__":
    debug_ra_name_mapping() 