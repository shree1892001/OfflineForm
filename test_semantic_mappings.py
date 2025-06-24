#!/usr/bin/env python3
"""
Test script to verify semantic mappings usage in FillPDFService
"""

import yaml
import json
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.MappingRulesDatabaseService import MappingRulesDatabaseService
from Utils.mapping_utils import transform_json_with_mappings, initialize_json_mapping_database

def test_semantic_mappings():
    """Test if semantic mappings are being used"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print("🔍 Testing Semantic Mappings Usage in FillPDFService")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database with semantic mappings...")
    initialize_json_mapping_database(config)
    
    # Test JSON mapping database service
    json_db_service = JsonMappingDatabaseService(config)
    
    print("\n2. Checking semantic meanings in database...")
    try:
        # Get semantic meanings
        query = "SELECT meaning, synonyms, business_domain FROM semantic_meanings"
        semantic_rows = json_db_service.db_connection.execute_query(query)
        
        print(f"Found {len(semantic_rows)} semantic meanings:")
        for row in semantic_rows:
            meaning, synonyms, domain = row
            synonyms_list = json.loads(synonyms) if synonyms else []
            print(f"  - {meaning}: {synonyms_list} (domain: {domain})")
            
    except Exception as e:
        print(f"❌ Error getting semantic meanings: {e}")
    
    print("\n3. Checking JSON field mappings in database...")
    try:
        # Get JSON field mappings
        json_mappings = json_db_service.get_all_json_mappings()
        print(f"Found {len(json_mappings)} JSON field mappings:")
        
        for mapping in json_mappings[:10]:  # Show first 10
            print(f"  - {mapping.source_path} -> {mapping.target_path} (semantic: {mapping.semantic_meaning})")
            
        if len(json_mappings) > 10:
            print(f"  ... and {len(json_mappings) - 10} more mappings")
            
    except Exception as e:
        print(f"❌ Error getting JSON mappings: {e}")
    
    print("\n4. Testing JSON transformation with sample data...")
    
    # Sample input JSON
    sample_json = {
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
    
    try:
        # Transform using the same method as FillPDFService
        transformed = transform_json_with_mappings(sample_json, config)
        
        print("✅ JSON transformation completed")
        print("Transformed data structure:")
        print(json.dumps(transformed, indent=2))
        
        # Check if semantic mappings were applied
        if 'data' in transformed and 'Payload' in transformed['data']:
            payload = transformed['data']['Payload']
            
            print("\n5. Checking if semantic mappings were applied:")
            
            # Check for legal_name mapping
            if 'Name' in payload and 'CD_Legal_Name' in payload['Name']:
                print(f"✅ legal_name -> CD_Legal_Name: {payload['Name']['CD_Legal_Name']}")
            else:
                print("❌ legal_name -> CD_Legal_Name mapping not found")
            
            # Check for city mapping
            if 'Principal_Address' in payload and 'PA_City' in payload['Principal_Address']:
                print(f"✅ city -> PA_City: {payload['Principal_Address']['PA_City']}")
            else:
                print("❌ city -> PA_City mapping not found")
                
        else:
            print("❌ Expected data structure not found in transformed JSON")
            
    except Exception as e:
        print(f"❌ Error during JSON transformation: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    test_semantic_mappings() 