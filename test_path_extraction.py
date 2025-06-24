#!/usr/bin/env python3
"""
Test script to verify path extraction issue
"""

import json
import yaml
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

def test_path_extraction():
    """Test the path extraction issue"""
    
    print("🔍 Testing Path Extraction")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize mapper
    mapper = CapitalizedJsonMapper(config)
    
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
    
    print("📋 Test User JSON:")
    print(json.dumps(test_user_json, indent=2))
    
    # Test different paths
    test_paths = [
        "payload.name.legal_name",
        "1.Payload.name.legal_name", 
        "Payload.name.legal_name",
        "name.legal_name"
    ]
    
    print(f"\n🔍 Testing Path Extraction:")
    for path in test_paths:
        value = mapper._get_value_by_path(test_user_json, path)
        print(f"  Path: '{path}' -> Value: {value}")
    
    # Test the correct approach - extract payload first
    print(f"\n🔧 Testing Correct Approach:")
    
    # Extract payload from the nested structure
    payload = mapper.extract_payload_from_source(test_user_json)
    print(f"Extracted payload: {json.dumps(payload, indent=2)}")
    
    # Now test paths on the extracted payload
    test_paths_on_payload = [
        "name.legal_name",
        "principal_address.city",
        "contact.emailId"
    ]
    
    for path in test_paths_on_payload:
        value = mapper._get_value_by_path(payload, path)
        print(f"  Path: '{path}' -> Value: {value}")
    
    print(f"\n🎯 Conclusion:")
    print(f"- Database mappings expect paths like 'payload.name.legal_name'")
    print(f"- But actual JSON has structure '1.Payload.name.legal_name'")
    print(f"- Need to extract payload first, then use relative paths")

if __name__ == "__main__":
    test_path_extraction() 