#!/usr/bin/env python3
"""
Test script using real JSON data to verify database mapping
"""

import json
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Services.FillOfflinePdf import FillOfflinePdf

def test_real_json_mapping():
    """Test database mapping with real JSON data"""
    
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
                "keyPersonnelName": "Sam sharan",
                "Billing Information": {
                    "city ": "Pune",
                    "emailId": "saumya@gmail.com",
                    "stateId": 1,
                    "contactNo": 838383883,
                    "postalCode": None,
                    "addressLine1": "hadapsar",
                    "addressLine2": "djjdjjd",
                    "keyPersonnelName": "Saumyaranjan Patra"
                },
                "Mailing Information": {
                    "city": "Pune",
                    "name": "Saumya",
                    "State": 1,
                    "Zip_Code": 9700,
                    "contact_no": 38838383883,
                    "email_address": "saumya@gmail.com",
                    "address_line 2": "jdjjjd",
                    "street_address": "hadapsar"
                }
            },
            "principal_address": {
                "city": "Pune",
                "state": None,
                "zip_code": 412207,
                "address_line 2": "",
                "street_address": "hadapsar"
            },
            "Stock_Details": {
                "Number_Of_Shares": 10,
                "Shares_Par_Value": 1000
            },
            "Purpose": {
                "purpose": "Any legal purpose"
            },
            "Incorporator_Information": {
                "keyPersonnelName": "Pawan Singh",
                "}State": "Delhi"
            },
            "contact_information": {
                "name": "Saumyaranjan Patra",
                "Address": {
                    "city": "Pune",
                    "state ": 1,
                    "zip_code": 41220,
                    "address_line 2": "jdjdjjdj",
                    "street_address": "hadapsar"
                },
                "contact_no": 83838383,
                "email address": "saumya@gmail.com"
            },
            "organizer_information": {
                "emailId": "saumya@gmail.com",
                "contactNo": 838383838,
                "keyPersonnelName": "saumya patra"
            }
        },
        "formProgress": 100
    }
    
    # Sample PDF form fields (extracted from a PDF template)
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
        {"key": "Key_Personnel_Name", "text_near_key": ["Key Personnel"], "placeholder": ""}
    ]
    
    print("🧪 Testing Real JSON Database Mapping")
    print("=" * 60)
    
    print("\n📄 PDF Form Fields:")
    for field in form_keys:
        print(f"  - {field['key']}")
    
    print("\n📋 Real User JSON (payload section):")
    print(json.dumps(real_user_json["payload"], indent=2))
    
    print("\n🔄 Testing Database Mapping...")
    
    # Test database mapping
    pdf_filler = FillOfflinePdf()
    
    try:
        # Test the mapping
        result = pdf_filler.generate_data_dict_with_ai_mapping(form_keys, real_user_json)
        
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
            "CD_Alternate_Legal_Name": "payload.name.alternate_legal_name",
            "PA_City": "payload.principal_address.city",
            "PA_State": "payload.principal_address.state",
            "PA_Address_Line2": "payload.principal_address.address_line 2",
            "PA_Street_Address": "payload.principal_address.street_address",
            "PA_Zip_Code": "payload.principal_address.zip_code",
            "RA_City": "payload.Registered_Agent.Address.city",
            "RA_Email": "payload.Registered_Agent.emailId",
            "RA_Contact_No": "payload.Registered_Agent.contactNo",
            "RA_Key_Personnel_Name": "payload.Registered_Agent.keyPersonnelName",
            "Email": "payload.organizer_information.emailId",
            "Contact_No": "payload.organizer_information.contactNo",
            "Key_Personnel_Name": "payload.organizer_information.keyPersonnelName"
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
    test_real_json_mapping() 