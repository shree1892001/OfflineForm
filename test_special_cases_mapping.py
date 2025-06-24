#!/usr/bin/env python3
"""
Test script to verify special cases mapping from mapping_utils.py
"""

import json
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Services.FillOfflinePdf import FillOfflinePdf

def test_special_cases_mapping():
    """Test special cases mapping with real data"""
    
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
    
    # PDF form fields including special cases from mapping_utils.py
    form_keys = [
        # Special cases from mapping_utils.py
        {"key": "RAMAZ", "text_near_key": ["Registered Agent Mailing Zip"], "placeholder": ""},
        {"key": "DS", "text_near_key": ["Director State"], "placeholder": ""},
        {"key": "RS", "text_near_key": ["Registered Agent State"], "placeholder": ""},
        {"key": "PS", "text_near_key": ["Principal Address State"], "placeholder": ""},
        {"key": "IS", "text_near_key": ["Incorporator State"], "placeholder": ""},
        {"key": "PZIP", "text_near_key": ["Principal Address Zip"], "placeholder": ""},
        {"key": "RA MailingAdd zip", "text_near_key": ["RA Mailing Address Zip"], "placeholder": ""},
        {"key": "Entity Name", "text_near_key": ["Entity Name"], "placeholder": ""},
        {"key": "RA Zip", "text_near_key": ["Registered Agent Zip"], "placeholder": ""},
        {"key": "RA Address city", "text_near_key": ["Registered Agent City"], "placeholder": ""},
        {"key": "Register Agent MI_state", "text_near_key": ["Registered Agent Mailing State"], "placeholder": ""},
        {"key": "RA Name", "text_near_key": ["Registered Agent Name"], "placeholder": ""},
        
        # Base entities from mapping_utils.py
        {"key": "RA_City", "text_near_key": ["Registered Agent City"], "placeholder": ""},
        {"key": "RA_State", "text_near_key": ["Registered Agent State"], "placeholder": ""},
        {"key": "RA_Zip", "text_near_key": ["Registered Agent Zip"], "placeholder": ""},
        {"key": "RA_Email", "text_near_key": ["Registered Agent Email"], "placeholder": ""},
        {"key": "RA_Contact", "text_near_key": ["Registered Agent Contact"], "placeholder": ""},
        {"key": "PA_City", "text_near_key": ["Principal Address City"], "placeholder": ""},
        {"key": "PA_State", "text_near_key": ["Principal Address State"], "placeholder": ""},
        {"key": "PA_Zip", "text_near_key": ["Principal Address Zip"], "placeholder": ""},
        {"key": "PA_Address", "text_near_key": ["Principal Address"], "placeholder": ""},
        
        # Regular database mappings
        {"key": "CD_Legal_Name", "text_near_key": ["Legal Name"], "placeholder": ""},
        {"key": "CD_LLC_Name", "text_near_key": ["LLC Name"], "placeholder": ""},
        {"key": "CD_Alternate_Legal_Name", "text_near_key": ["Alternate Name"], "placeholder": ""},
        {"key": "Email", "text_near_key": ["Email"], "placeholder": ""},
        {"key": "Contact_No", "text_near_key": ["Phone"], "placeholder": ""},
        {"key": "Key_Personnel_Name", "text_near_key": ["Key Personnel"], "placeholder": ""}
    ]
    
    print("🧪 Testing Special Cases Mapping from mapping_utils.py")
    print("=" * 70)
    
    print(f"\n📄 PDF Form Fields ({len(form_keys)} fields):")
    for i, field in enumerate(form_keys):
        print(f"  {i+1:2d}. {field['key']}")
    
    print(f"\n📋 Real User JSON (payload section):")
    print(json.dumps(real_user_json["payload"], indent=2))
    
    print(f"\n🔄 Testing Special Cases Database Mapping...")
    
    # Test special cases mapping
    pdf_filler = FillOfflinePdf()
    
    try:
        # Test the mapping
        result = pdf_filler.generate_data_dict_with_ai_mapping(form_keys, real_user_json)
        
        print(f"\n✅ Mapping Result:")
        print(json.dumps(result, indent=2))
        
        # Check which fields were mapped
        mapped_fields = [k for k, v in result.items() if v]
        unmapped_fields = [k for k, v in result.items() if not v]
        
        print(f"\n📊 Results:")
        print(f"✅ Mapped fields ({len(mapped_fields)}): {mapped_fields}")
        print(f"❌ Unmapped fields ({len(unmapped_fields)}): {unmapped_fields}")
        
        # Show special cases mapping details
        print(f"\n🎯 Special Cases Mapping Analysis:")
        special_cases = {
            'RAMAZ': 'Registered Agent Mailing Information Zip Code',
            'DS': 'Director State',
            'RS': 'Registered Agent State',
            'PS': 'Principal Address State',
            'IS': 'Incorporator State',
            'PZIP': 'Principal Address Zip Code',
            'RA MailingAdd zip': 'Registered Agent Mailing Information Zip Code',
            'Entity Name': 'Legal Name',
            'RA Zip': 'Registered Agent Zip Code',
            'RA Address city': 'Registered Agent City',
            'Register Agent MI_state': 'Registered Agent Mailing Information State',
            'RA Name': 'Registered Agent Name'
        }
        
        for field_name, expected_mapping in special_cases.items():
            actual_value = result.get(field_name, "")
            if actual_value:
                print(f"  ✅ {field_name}: '{actual_value}' (Special case: {expected_mapping})")
            else:
                print(f"  ❌ {field_name}: Not mapped (Expected: {expected_mapping})")
        
        # Show base entities mapping details
        print(f"\n🏢 Base Entities Mapping Analysis:")
        base_entities = {
            'RA_City': 'Registered Agent City',
            'RA_State': 'Registered Agent State', 
            'RA_Zip': 'Registered Agent Zip',
            'RA_Email': 'Registered Agent Email',
            'RA_Contact': 'Registered Agent Contact',
            'PA_City': 'Principal Address City',
            'PA_State': 'Principal Address State',
            'PA_Zip': 'Principal Address Zip',
            'PA_Address': 'Principal Address'
        }
        
        for field_name, expected_mapping in base_entities.items():
            actual_value = result.get(field_name, "")
            if actual_value:
                print(f"  ✅ {field_name}: '{actual_value}' (Base entity: {expected_mapping})")
            else:
                print(f"  ❌ {field_name}: Not mapped (Expected: {expected_mapping})")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_special_cases_mapping() 