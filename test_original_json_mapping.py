#!/usr/bin/env python3
"""
Test script to demonstrate original JSON mapping approach
Shows how PDF fields are mapped to original user JSON without transforming the JSON
"""

import json
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Services.FillOfflinePdf import FillOfflinePdf

def test_original_json_mapping():
    """Test the original JSON mapping approach"""
    
    # Sample PDF form fields (extracted from a PDF template)
    form_keys = [
        {"key": "CD_Legal_Name", "text_near_key": ["Legal Name"], "placeholder": ""},
        {"key": "CD_LLC_Name", "text_near_key": ["LLC Name"], "placeholder": ""},
        {"key": "PA_City", "text_near_key": ["City"], "placeholder": ""},
        {"key": "PA_State", "text_near_key": ["State"], "placeholder": ""},
        {"key": "PA_Postal_Code", "text_near_key": ["Zip Code"], "placeholder": ""},
        {"key": "Email", "text_near_key": ["Email"], "placeholder": ""},
        {"key": "Contact_No", "text_near_key": ["Phone"], "placeholder": ""},
        {"key": "RA_Name", "text_near_key": ["Registered Agent"], "placeholder": ""},
        {"key": "RA_City", "text_near_key": ["Agent City"], "placeholder": ""}
    ]
    
    # Original user JSON (untouched/not transformed)
    original_user_json = {
        "1": {
            "Payload": {
                "name": {
                    "legal_name": "Test Company LLC",
                    "alternate_legal_name": "Test Corp"
                },
                "address": {
                    "street_address": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10001"
                },
                "contact": {
                    "emailId": "test@example.com",
                    "contactNo": "555-123-4567"
                },
                "registered_agent": {
                    "keyPersonnelName": "John Doe",
                    "address": {
                        "city": "Los Angeles",
                        "state": "CA"
                    }
                }
            },
            "EntityType": {"type": "LLC"},
            "State": {"name": "Delaware"},
            "OrderType": "formation",
            "FormProgress": 75
        }
    }
    
    print("🧪 Testing Original JSON Mapping Approach")
    print("=" * 60)
    
    print("\n📄 PDF Form Fields:")
    for field in form_keys:
        print(f"  - {field['key']}")
    
    print("\n📋 Original User JSON (untouched):")
    print(json.dumps(original_user_json, indent=2))
    
    print("\n🔄 Testing AI Mapping (Primary Method)...")
    
    # Test AI mapping
    pdf_filler = FillOfflinePdf()
    
    try:
        # Test AI mapping (primary method)
        ai_result = pdf_filler.generate_data_dict_with_ai_mapping(form_keys, original_user_json)
        
        print("\n✅ AI Mapping Result:")
        print(json.dumps(ai_result, indent=2))
        
        # Test database fallback mapping
        print("\n🔄 Testing Database Fallback Mapping...")
        db_result = pdf_filler.generate_data_dict_with_database_fallback(form_keys, original_user_json)
        
        print("\n✅ Database Fallback Result:")
        print(json.dumps(db_result, indent=2))
        
        # Compare results
        print("\n📊 Comparison:")
        print("AI Mapped Fields:", len([v for v in ai_result.values() if v]))
        print("DB Mapped Fields:", len([v for v in db_result.values() if v]))
        
        # Show specific mappings
        print("\n🎯 Key Mappings:")
        key_mappings = [
            ("CD_Legal_Name", "payload.name.legal_name"),
            ("PA_City", "payload.address.city"),
            ("Email", "payload.contact.emailId"),
            ("RA_Name", "payload.registered_agent.keyPersonnelName")
        ]
        
        for pdf_field, user_path in key_mappings:
            ai_value = ai_result.get(pdf_field, "")
            db_value = db_result.get(pdf_field, "")
            print(f"  {pdf_field}:")
            print(f"    AI: '{ai_value}'")
            print(f"    DB: '{db_value}'")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def test_database_mappings():
    """Test database mappings directly"""
    print("\n🔍 Testing Database Mappings Directly...")
    
    try:
        from Utils.capitalized_json_mapper import CapitalizedJsonMapper
        import yaml
        
        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize mapper
        mapper = CapitalizedJsonMapper(config)
        mapper.initialize_capitalized_mappings()
        
        # Get all database mappings
        db_mappings = mapper.db_service.get_all_json_mappings()
        
        print(f"\n📊 Database contains {len(db_mappings)} mappings:")
        for mapping in db_mappings[:10]:  # Show first 10
            print(f"  {mapping.source_path} -> {mapping.target_path}")
        
        if len(db_mappings) > 10:
            print(f"  ... and {len(db_mappings) - 10} more mappings")
        
    except Exception as e:
        print(f"❌ Error testing database mappings: {e}")

if __name__ == "__main__":
    print("🚀 Starting Original JSON Mapping Tests")
    print("=" * 60)
    
    # Test database mappings first
    test_database_mappings()
    
    # Test the main mapping functionality
    test_original_json_mapping()
    
    print("\n✅ Testing completed!")
    print("\n📝 Summary:")
    print("- System now keeps original user JSON as-is")
    print("- PDF fields are mapped to original JSON keys")
    print("- No JSON transformation occurs")
    print("- AI maps PDF fields to user JSON paths")
    print("- Database provides fallback mappings") 