#!/usr/bin/env python3
"""
Debug script to test RA Name mapping specifically
"""

import json
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Services.FillOfflinePdf import FillOfflinePdf

def test_ra_name_debug():
    """Debug RA Name mapping specifically"""
    
    # Real JSON data from user
    real_user_json = {
        "orderType": "Entity Formation",
        "EntityType": {
            "createdBy": None,
            "creationDate": None,
            "lastModifiedBy": None,
            "lastModifiedDate": None,
            "id": 1,
            "orderShortName": "LLC",
            "orderFullDesc": "LLC"
        },
        "State": {
            "createdBy": None,
            "creationDate": None,
            "lastModifiedBy": None,
            "lastModifiedDate": None,
            "id": 32,
            "stateShortName": "CL",
            "stateFullDesc": "ohio",
            "stateUrl": "https://www.njportal.com/DOR/BusinessFormation/CompanyInformation/BusinessName",
            "filingWebsiteUsername": "redberyl",
            "filingWebsitePassword": "yD7?ddG0!$09",
            "countryMaster": {
                "createdBy": None,
                "creationDate": None,
                "lastModifiedBy": None,
                "lastModifiedDate": None,
                "id": 3,
                "countryShortName": "USA",
                "countryFullDesc": "United States Of America"
            }
        },
        "payload": {
            "name": {
                "legal_name": "eeeee LLC",
                "alternate_legal_name": "Patra"
            },
            "County": {
                "countyName": "Albany"
            },
            "Registered_Agent": {
                "Address": {
                    "city": "Pune",
                    "state ": 1,
                    "zip_code": "07004",
                    "address_line 2": "jdjdjjd",
                    "street_address": "hadapsar"
                },
                "emailId": "saumya@gmail.com",
                "contactNo": 388383838,
                "keyPersonnelName": "Sam sharan"
            },
            "principal_address": {
                "city": "Pune",
                "state": None,
                "zip_code": 412207,
                "address_line 2": "",
                "street_address": "hadapsar"
            },
            "organizer_information": {
                "emailId": "saumya@gmail.com",
                "contactNo": 838383838,
                "keyPersonnelName": "saumya patra"
            }
        },
        "formProgress": 100
    }
    
    # Test with different variations of RA Name
    test_cases = [
        {"key": "RA Name", "text_near_key": ["Registered Agent Name"], "placeholder": ""},
        {"key": "RA NAME", "text_near_key": ["Registered Agent Name"], "placeholder": ""},
        {"key": "RA_Name", "text_near_key": ["Registered Agent Name"], "placeholder": ""},
        {"key": "RAName", "text_near_key": ["Registered Agent Name"], "placeholder": ""},
        {"key": "RA Name", "text_near_key": ["RA Name"], "placeholder": ""},
        {"key": "Registered Agent Name", "text_near_key": ["Registered Agent Name"], "placeholder": ""}
    ]
    
    print("🔍 Debugging RA Name Mapping")
    print("=" * 60)
    
    print(f"\n📋 Test User JSON (payload section):")
    print(json.dumps(real_user_json["payload"], indent=2))
    
    # Test each variation
    for i, test_case in enumerate(test_cases):
        print(f"\n🧪 Test Case {i+1}: '{test_case['key']}'")
        
        # Test the mapping
        pdf_filler = FillOfflinePdf()
        
        try:
            # Test with just this one field
            result = pdf_filler.generate_data_dict_with_ai_mapping([test_case], real_user_json)
            
            field_name = test_case['key']
            field_value = result.get(field_name, "")
            
            print(f"  Result: '{field_value}'")
            
            if field_value:
                print(f"  ✅ SUCCESS: '{field_name}' -> '{field_value}'")
            else:
                print(f"  ❌ FAILED: '{field_name}' -> empty value")
                
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    
    # Also test the mapping rules directly
    print(f"\n🔍 Testing Mapping Rules Directly:")
    import yaml
    from Utils.mapping_utils import generate_mapping_rules, initialize_database_with_default_data
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    initialize_database_with_default_data(config)
    mapping_rules = generate_mapping_rules(config)
    
    # Check for RA Name variations
    ra_name_variations = ["RA Name", "RA NAME", "RA_Name", "RAName", "Registered Agent Name"]
    
    for variation in ra_name_variations:
        if variation in mapping_rules:
            print(f"  ✅ Found '{variation}' -> '{mapping_rules[variation]}'")
        else:
            print(f"  ❌ Not found: '{variation}'")

if __name__ == "__main__":
    test_ra_name_debug() 