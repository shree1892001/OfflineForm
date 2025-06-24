#!/usr/bin/env python3
"""
Test script to demonstrate database mappings with exact paths
"""

import json
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Services.FillOfflinePdf import FillOfflinePdf

def test_exact_database_mapping():
    """Test database mapping with exact paths that match the database"""
    
    # Sample PDF form fields (extracted from a PDF template)
    form_keys = [
        {"key": "CD_Legal_Name", "text_near_key": ["Legal Name"], "placeholder": ""},
        {"key": "CD_LLC_Name", "text_near_key": ["LLC Name"], "placeholder": ""},
        {"key": "PA_City", "text_near_key": ["City"], "placeholder": ""},
        {"key": "PA_State", "text_near_key": ["State"], "placeholder": ""},
        {"key": "Email", "text_near_key": ["Email"], "placeholder": ""},
        {"key": "Contact_No", "text_near_key": ["Phone"], "placeholder": ""}
    ]
    
    # User JSON with EXACT paths that match the database mappings
    exact_user_json = {
        "1": {
            "Payload": {
                "name": {
                    "legal_name": "Test Company LLC",
                    "alternate_legal_name": "Test Corp"
                },
                "principal_address": {
                    "city": "New York",
                    "state": "NY",
                    "address_line_2": "Suite 100"
                },
                "contact": {
                    "emailId": "test@example.com",
                    "contactNo": "555-123-4567"
                }
            }
        }
    }
    
    print("🧪 Testing Database Mapping with Exact Paths")
    print("=" * 60)
    
    print("\n📄 PDF Form Fields:")
    for field in form_keys:
        print(f"  - {field['key']}")
    
    print("\n📋 User JSON with Exact Database Paths:")
    print(json.dumps(exact_user_json, indent=2))
    
    print("\n🔄 Testing Database Mapping...")
    
    # Test database mapping
    pdf_filler = FillOfflinePdf()
    
    try:
        # Test the mapping
        result = pdf_filler.generate_data_dict_with_ai_mapping(form_keys, exact_user_json)
        
        print("\n✅ Mapping Result:")
        print(json.dumps(result, indent=2))
        
        # Check which fields were mapped
        mapped_fields = [k for k, v in result.items() if v]
        unmapped_fields = [k for k, v in result.items() if not v]
        
        print(f"\n📊 Results:")
        print(f"✅ Mapped fields ({len(mapped_fields)}): {mapped_fields}")
        print(f"❌ Unmapped fields ({len(unmapped_fields)}): {unmapped_fields}")
        
        # Show specific mappings
        print(f"\n🎯 Specific Mappings:")
        expected_mappings = {
            "CD_Legal_Name": "payload.name.legal_name",
            "CD_LLC_Name": "payload.name.legal_name", 
            "PA_City": "payload.principal_address.city",
            "PA_State": "payload.principal_address.state",
            "Email": "payload.contact.emailId",
            "Contact_No": "payload.contact.contactNo"
        }
        
        for pdf_field, expected_path in expected_mappings.items():
            actual_value = result.get(pdf_field, "")
            if actual_value:
                print(f"  ✅ {pdf_field}: '{actual_value}' (from {expected_path})")
            else:
                print(f"  ❌ {pdf_field}: Not mapped (expected from {expected_path})")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_exact_database_mapping() 