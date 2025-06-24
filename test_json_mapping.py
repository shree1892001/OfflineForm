#!/usr/bin/env python3
"""
Test script for the updated JSON mapping system
Demonstrates database-driven mappings with AI enhancement
"""

import json
import logging
from Utils.mapping_utils import transform_json_with_mappings, generate_json_mapping_rules
from Utils.ai_json_mapper import AIJsonMapper
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """Load configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return {}

def test_database_driven_mapping():
    """Test the database-driven JSON mapping system"""
    print("\n" + "="*60)
    print("TESTING DATABASE-DRIVEN JSON MAPPING")
    print("="*60)
    
    config = load_config()
    
    # Sample source JSON (similar to your examples)
    source_json = {
        "payload": {
            "name": {
                "legal_name": "Test Company LLC",
                "alternate_legal_name": "Test Co"
            },
            "registered_agent": {
                "keyPersonnelName": "John Doe",
                "emailId": "john.doe@example.com",
                "contactNo": "+1-555-123-4567",
                "Address": {
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10001",
                    "street_address": "123 Main Street"
                }
            },
            "principal_address": {
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "90210",
                "street_address": "456 Business Ave"
            },
            "organizer_information": {
                "keyPersonnelName": "Jane Smith",
                "emailId": "jane.smith@example.com",
                "contactNo": "+1-555-987-6543"
            }
        }
    }
    
    print("\nSource JSON:")
    print(json.dumps(source_json, indent=2))
    
    try:
        # Test database-driven mapping
        result = transform_json_with_mappings(source_json, config)
        
        print("\nTransformed JSON (Database-driven):")
        print(json.dumps(result, indent=2))
        
        # Show mapping rules used
        mapping_rules = generate_json_mapping_rules(config)
        print(f"\nUsed {len(mapping_rules)} database mapping rules")
        
        return True
        
    except Exception as e:
        print(f"Error in database-driven mapping: {e}")
        return False

def test_ai_enhanced_mapping():
    """Test the AI-enhanced JSON mapping system"""
    print("\n" + "="*60)
    print("TESTING AI-ENHANCED JSON MAPPING")
    print("="*60)
    
    config = load_config()
    
    # Sample source JSON with some unmapped fields
    source_json = {
        "payload": {
            "name": {
                "legal_name": "AI Test Company",
                "alternate_legal_name": "AI Test Co"
            },
            "registered_agent": {
                "keyPersonnelName": "AI Agent",
                "emailId": "ai.agent@example.com",
                "contactNo": "+1-555-111-2222",
                "Address": {
                    "city": "San Francisco",
                    "state": "CA",
                    "zip_code": "94102",
                    "street_address": "789 Tech Street"
                }
            },
            "principal_address": {
                "city": "Seattle",
                "state": "WA",
                "zip_code": "98101",
                "street_address": "321 Innovation Blvd"
            },
            "organizer_information": {
                "keyPersonnelName": "AI Organizer",
                "emailId": "ai.organizer@example.com",
                "contactNo": "+1-555-333-4444"
            },
            # Add some unmapped fields for AI to discover
            "additional_info": {
                "website": "www.aitestcompany.com",
                "founded_date": "2024-01-15",
                "business_type": "Technology"
            }
        }
    }
    
    print("\nSource JSON (with unmapped fields):")
    print(json.dumps(source_json, indent=2))
    
    try:
        # Create AI mapper
        ai_mapper = AIJsonMapper(config)
        
        # Create target template
        target_template = {
            "data": {
                "EntityType": {},
                "State": {},
                "Payload": {
                    "Name": {
                        "CD_Legal_Name": None,
                        "CD_Alternate_Legal_Name": None
                    },
                    "Principal_Address": {
                        "PA_City": None,
                        "PA_State": None,
                        "PA_Postal_Code": None,
                        "PA_Address_Line1": None,
                        "PA_Address_Line2": None
                    },
                    "Registered_Agent": {
                        "Address": {
                            "RA_City": None,
                            "RA_State": None,
                            "RA_Postal_Code": None,
                            "RA_Address_Line1": None,
                            "RA_Address_Line2": None
                        },
                        "Name": {
                            "RA_Name": None,
                            "Email": None,
                            "Contact_No": None
                        }
                    },
                    "Organizer_Information": {
                        "Organizer_Details": {
                            "Org_Name": None,
                            "Og_Email": None,
                            "Og_Contact_No": None
                        },
                        "Org_Address": {
                            "Org_City": None,
                            "Org_State": None,
                            "Org_Postal_Code": None
                        }
                    },
                    "County": {
                        "CD_County": None
                    },
                    # Add some unmapped target fields for AI to discover
                    "Additional_Info": {
                        "Website": None,
                        "Founded_Date": None,
                        "Business_Type": None
                    }
                }
            }
        }
        
        # Test AI-enhanced mapping
        result = ai_mapper.map_json_with_ai_enhancement(source_json, target_template)
        
        print("\nTransformed JSON (AI-enhanced):")
        print(json.dumps(result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"Error in AI-enhanced mapping: {e}")
        return False

def main():
    """Run all tests"""
    print("JSON MAPPING SYSTEM TEST")
    print("="*60)
    
    # Test 1: Database-driven mapping
    success1 = test_database_driven_mapping()
    
    # Test 2: AI-enhanced mapping
    success2 = test_ai_enhanced_mapping()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Database-driven mapping: {'✓ PASS' if success1 else '✗ FAIL'}")
    print(f"AI-enhanced mapping: {'✓ PASS' if success2 else '✗ FAIL'}")
    
    if all([success1, success2]):
        print("\n🎉 All tests passed! The JSON mapping system is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 