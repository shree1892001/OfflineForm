#!/usr/bin/env python3
"""
Test the new payload structure transformation
"""

import json
import yaml
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

def test_payload_transformation():
    """Test the new payload structure transformation"""
    
    # Sample user JSON
    sample_user_json = {
        "1": {
            "EntityType": {"entityType": "LLC"},
            "State": {"state": "Delaware"},
            "OrderType": "Entity Formation",
            "FormProgress": "Complete"
        },
        "payload": {
            "name": {
                "legal_name": "Test Company LLC",
                "alternate_legal_name": "Test Company"
            },
            "principal_address": {
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "street_address": "123 Main St"
            },
            "registered_agent": {
                "keyPersonnelName": "John Doe",
                "emailId": "john@example.com",
                "contactNo": "555-1234"
            }
        }
    }
    
    # Load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Initialize mapper
    mapper = CapitalizedJsonMapper(config)
    
    # Initialize mappings
    mapper.initialize_capitalized_mappings()
    
    # Transform payload structure
    result = mapper.transform_payload_structure(sample_user_json)
    
    print("Original User JSON:")
    print(json.dumps(sample_user_json, indent=2))
    print("\n" + "="*60)
    print("Transformed Payload Structure:")
    print(json.dumps(result, indent=2))
    
    # Show specific transformations
    print("\n" + "="*60)
    print("Key Transformations Applied:")
    
    transformations = {
        "CD_Legal_Name": "Legal_Name",
        "CD_LLC_Name": "Legal_Name",
        "CD_Alternate_Legal_Name": "Alternate_Legal_Name", 
        "PA_City": "City",
        "PA_State": "State",
        "PA_Postal_Code": "Zip_Code",
        "PA_Address_Line1": "Street_Address",
        "RA_Name": "Name",
        "Email": "EmailId",
        "Contact_No": "ContactNo"
    }
    
    for old_name, new_name in transformations.items():
        if old_name in result:
            print(f"✅ {old_name} -> {new_name}: {result[old_name]}")
        if new_name in result:
            print(f"✅ {new_name}: {result[new_name]}")

if __name__ == "__main__":
    test_payload_transformation() 