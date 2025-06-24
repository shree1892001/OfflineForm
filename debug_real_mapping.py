#!/usr/bin/env python3
"""
Debug script to show why database mappings are not being applied to 32 PDF fields
"""

import json
import yaml
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

def debug_real_mapping():
    """Debug the real mapping process"""
    
    print("🔍 Debugging Real Database Mapping Process")
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
    
    # Real user JSON
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
    
    # Extract payload
    extracted_payload = mapper.extract_payload_from_source(real_user_json)
    print(f"\n📋 Extracted payload: {json.dumps(extracted_payload, indent=2)}")
    
    # Simulate 32 PDF form fields (you need to replace this with your actual PDF fields)
    # This is just an example - you need to show me your actual PDF field names
    sample_pdf_fields = [
        {"key": "CD_Legal_Name"},
        {"key": "CD_LLC_Name"},
        {"key": "CD_Alternate_Legal_Name"},
        {"key": "PA_City"},
        {"key": "PA_State"},
        {"key": "PA_Address_Line2"},
        {"key": "PA_Street_Address"},
        {"key": "PA_Zip_Code"},
        {"key": "RA_City"},
        {"key": "RA_Email"},
        {"key": "RA_Contact_No"},
        {"key": "RA_Key_Personnel_Name"},
        {"key": "Email"},
        {"key": "Contact_No"},
        {"key": "Key_Personnel_Name"},
        # Add more fields to reach 32...
    ]
    
    print(f"\n📄 Sample PDF Fields (first 15):")
    for i, field in enumerate(sample_pdf_fields):
        print(f"  {i+1}. {field['key']}")
    
    print(f"\n🔍 Checking Database Mappings vs PDF Fields:")
    
    # Check each database mapping
    matches_found = 0
    for i, db_mapping in enumerate(db_mappings):
        pdf_field_name = db_mapping.target_path
        user_field_path = db_mapping.source_path
        
        # Remove "payload." prefix from the path
        relative_path = user_field_path.replace("payload.", "")
        
        # Check if this PDF field exists in our form keys
        field_exists = any(field.get('key') == pdf_field_name for field in sample_pdf_fields)
        
        # Get value from user JSON using path
        user_value = mapper._get_value_by_path(extracted_payload, relative_path)
        
        if i < 10:  # Show first 10 for brevity
            print(f"\n  {i+1}. Database Mapping: {user_field_path} -> {pdf_field_name}")
            print(f"     Relative path: {relative_path}")
            print(f"     Field exists in PDF: {field_exists}")
            print(f"     Value found: {user_value}")
            
            if field_exists and user_value is not None:
                print(f"     ✅ MATCH FOUND!")
                matches_found += 1
            elif field_exists:
                print(f"     ❌ Field exists but no value found")
            elif user_value is not None:
                print(f"     ❌ Value found but field doesn't exist in PDF")
            else:
                print(f"     ❌ No match")
    
    print(f"\n📊 Summary:")
    print(f"- Database mappings found: {len(db_mappings)}")
    print(f"- Sample PDF fields shown: {len(sample_pdf_fields)}")
    print(f"- Matches found in sample: {matches_found}")
    print(f"\n🎯 The issue is likely:")
    print(f"1. Your actual PDF has 32 fields with different names than the database mappings")
    print(f"2. The database target_path values don't match your actual PDF field names")
    print(f"3. You need to show me your actual 32 PDF field names to debug this properly")

if __name__ == "__main__":
    debug_real_mapping() 