#!/usr/bin/env python3
"""
Test script to verify semantic mapping is working correctly
"""

import json
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Services.FillOfflinePdf import FillOfflinePdf

def test_semantic_mapping():
    """Test semantic mapping with real data"""
    
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
    
    # Sample PDF form fields with various naming conventions
    form_keys = [
        {"key": "CD_Legal_Name", "text_near_key": ["Legal Name"], "placeholder": ""},
        {"key": "CD_LLC_Name", "text_near_key": ["LLC Name"], "placeholder": ""},
        {"key": "CD_Alternate_Legal_Name", "text_near_key": ["Alternate Name"], "placeholder": ""},
        {"key": "PA_City", "text_near_key": ["City"], "placeholder": ""},
        {"key": "PA_State", "text_near_key": ["State"], "placeholder": ""},
        {"key": "PA_Address_Line2", "text_near_key": ["Address Line 2"], "placeholder": ""},
        {"key": "PA_Street_Address", "text_near_key": ["Street Address"], "placeholder": ""},
        {"key": "PA_Zip_Code", "text_near_key": ["Zip Code"], "placeholder": ""},
        {"key": "RA_City", "text_near_key": ["Registered Agent City"], "placeholder": ""},
        {"key": "RA_Email", "text_near_key": ["Registered Agent Email"], "placeholder": ""},
        {"key": "RA_Contact_No", "text_near_key": ["Registered Agent Phone"], "placeholder": ""},
        {"key": "RA_Key_Personnel_Name", "text_near_key": ["Registered Agent Name"], "placeholder": ""},
        {"key": "Email", "text_near_key": ["Email"], "placeholder": ""},
        {"key": "Contact_No", "text_near_key": ["Phone"], "placeholder": ""},
        {"key": "Key_Personnel_Name", "text_near_key": ["Key Personnel"], "placeholder": ""},
        # Add more fields with different naming conventions
        {"key": "Business_Name", "text_near_key": ["Business Name"], "placeholder": ""},
        {"key": "Entity_Name", "text_near_key": ["Entity Name"], "placeholder": ""},
        {"key": "Company_City", "text_near_key": ["Company City"], "placeholder": ""},
        {"key": "Company_State", "text_near_key": ["Company State"], "placeholder": ""},
        {"key": "Contact_Email", "text_near_key": ["Contact Email"], "placeholder": ""},
        {"key": "Phone_Number", "text_near_key": ["Phone Number"], "placeholder": ""},
        {"key": "Address_Line_2", "text_near_key": ["Address Line 2"], "placeholder": ""},
        {"key": "Street_Address", "text_near_key": ["Street Address"], "placeholder": ""},
        {"key": "Postal_Code", "text_near_key": ["Postal Code"], "placeholder": ""},
        {"key": "Agent_City", "text_near_key": ["Agent City"], "placeholder": ""},
        {"key": "Agent_Email", "text_near_key": ["Agent Email"], "placeholder": ""},
        {"key": "Agent_Phone", "text_near_key": ["Agent Phone"], "placeholder": ""},
        {"key": "Agent_Name", "text_near_key": ["Agent Name"], "placeholder": ""},
        {"key": "Representative_Name", "text_near_key": ["Representative Name"], "placeholder": ""},
        {"key": "Contact_Person", "text_near_key": ["Contact Person"], "placeholder": ""},
        {"key": "DBA_Name", "text_near_key": ["DBA Name"], "placeholder": ""},
        {"key": "Doing_Business_As", "text_near_key": ["Doing Business As"], "placeholder": ""},
        {"key": "Municipality", "text_near_key": ["Municipality"], "placeholder": ""},
        {"key": "Province", "text_near_key": ["Province"], "placeholder": ""},
        {"key": "Zip", "text_near_key": ["Zip"], "placeholder": ""},
        {"key": "E_Mail", "text_near_key": ["E-Mail"], "placeholder": ""},
        {"key": "Telephone", "text_near_key": ["Telephone"], "placeholder": ""}
    ]
    
    print("🧪 Testing Semantic Database Mapping")
    print("=" * 60)
    
    print(f"\n📄 PDF Form Fields ({len(form_keys)} fields):")
    for i, field in enumerate(form_keys):
        print(f"  {i+1:2d}. {field['key']}")
    
    print(f"\n📋 Real User JSON (payload section):")
    print(json.dumps(real_user_json["payload"], indent=2))
    
    print(f"\n🔄 Testing Semantic Database Mapping...")
    
    # Test semantic mapping
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
        
        # Show semantic mapping details
        print(f"\n🎯 Semantic Mapping Analysis:")
        semantic_categories = {
            'legal_name': [],
            'alternate_name': [],
            'city': [],
            'state': [],
            'zip_code': [],
            'address_line2': [],
            'street_address': [],
            'email': [],
            'contact_no': [],
            'key_personnel': []
        }
        
        for field_name, value in result.items():
            if value:
                field_lower = field_name.lower()
                if any(keyword in field_lower for keyword in ['legal', 'llc', 'entity', 'company', 'business', 'name']):
                    semantic_categories['legal_name'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['alternate', 'dba', 'doing business as']):
                    semantic_categories['alternate_name'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['city', 'town', 'municipality']):
                    semantic_categories['city'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['state', 'province']):
                    semantic_categories['state'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['zip', 'postal', 'code']):
                    semantic_categories['zip_code'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['address line 2', 'address_line2', 'line2']):
                    semantic_categories['address_line2'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['street', 'address', 'line1']):
                    semantic_categories['street_address'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['email', 'e-mail', 'mail']):
                    semantic_categories['email'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['contact', 'phone', 'telephone', 'number']):
                    semantic_categories['contact_no'].append(f"{field_name}: {value}")
                elif any(keyword in field_lower for keyword in ['key personnel', 'personnel', 'contact person', 'representative']):
                    semantic_categories['key_personnel'].append(f"{field_name}: {value}")
        
        for category, mappings in semantic_categories.items():
            if mappings:
                print(f"  {category.upper()}: {mappings}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_semantic_mapping() 