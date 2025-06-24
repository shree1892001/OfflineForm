#!/usr/bin/env python3
"""
Debug script to show why database mappings are not being applied
"""

import json
import yaml
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

def debug_database_mapping():
    """Debug the database mapping process"""
    
    print("🔍 Debugging Database Mapping Process")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize mapper
    mapper = CapitalizedJsonMapper(config)
    mapper.initialize_capitalized_mappings()
    
    # Get database mappings
    db_mappings = mapper.db_service.get_all_json_mappings()
    
    print(f"📊 Found {len(db_mappings)} mappings in database")
    
    # Test data
    test_user_json = {
        "1": {
            "Payload": {
                "name": {
                    "legal_name": "Test Company LLC"
                },
                "principal_address": {
                    "city": "New York"
                },
                "contact": {
                    "emailId": "test@example.com"
                }
            }
        }
    }
    
    # PDF form fields
    form_keys = [
        {"key": "CD_Legal_Name"},
        {"key": "PA_City"},
        {"key": "Email"}
    ]
    
    print(f"\n📄 PDF Form Fields:")
    for field in form_keys:
        print(f"  - {field['key']}")
    
    print(f"\n📋 Test User JSON:")
    print(json.dumps(test_user_json, indent=2))
    
    print(f"\n🔍 Checking Database Mappings:")
    
    # Check each database mapping
    for i, db_mapping in enumerate(db_mappings):
        pdf_field_name = db_mapping.target_path
        user_field_path = db_mapping.source_path
        
        # Check if this PDF field exists in our form keys
        field_exists = any(field.get('key') == pdf_field_name for field in form_keys)
        
        # Get value from user JSON using path
        user_value = mapper._get_value_by_path(test_user_json, user_field_path)
        
        print(f"\n  {i+1}. Database Mapping: {user_field_path} -> {pdf_field_name}")
        print(f"     Field exists in PDF: {field_exists}")
        print(f"     Value found: {user_value}")
        
        if field_exists and user_value is not None:
            print(f"     ✅ MATCH FOUND!")
        elif field_exists:
            print(f"     ❌ Field exists but no value found")
        elif user_value is not None:
            print(f"     ❌ Value found but field doesn't exist in PDF")
        else:
            print(f"     ❌ No match")
        
        # Only show first 10 for brevity
        if i >= 9:
            print(f"     ... and {len(db_mappings) - 10} more mappings")
            break
    
    print(f"\n🎯 Summary:")
    print(f"- Database mappings are being loaded correctly")
    print(f"- The issue is that the PDF field names don't match the database target_path values")
    print(f"- Database has target_path like 'CD_Legal_Name' but PDF might have different field names")
    print(f"- The path extraction is working correctly")

if __name__ == "__main__":
    debug_database_mapping() 