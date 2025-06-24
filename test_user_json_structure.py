#!/usr/bin/env python3
"""
Test to see the actual user JSON structure and fix mappings
"""

import json
import yaml
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

def test_user_json_structure():
    """Test to see the actual user JSON structure"""
    
    # Sample user JSON (replace with your actual JSON)
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
    
    # Create target template
    target_template = {
        "CD_LLC_Name": "",
        "CD_Legal_Name": "",
        "PA_City": "",
        "RA_Name": "",
        "Email": ""
    }
    
    # Transform JSON
    result = mapper.transform_json(sample_user_json, target_template)
    
    print("Original User JSON:")
    print(json.dumps(sample_user_json, indent=2))
    print("\n" + "="*50)
    print("Transformed Result:")
    print(json.dumps(result, indent=2))
    
    # Get mapping report
    report = mapper.get_mapping_report(sample_user_json, result)
    print("\n" + "="*50)
    print("Mapping Report:")
    print(f"Database mappings: {report['database_mappings']}")
    print(f"Fallback mappings: {report['fallback_mappings']}")
    print(f"Total mapped: {report['mapped_fields']}")
    
    for mapping in report['mappings']:
        print(f"  {mapping['source_path']} -> {mapping['target_path']}: {mapping['source_value']}")

if __name__ == "__main__":
    test_user_json_structure() 