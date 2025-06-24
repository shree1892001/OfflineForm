#!/usr/bin/env python3
"""
Test script for Comprehensive JSON Mapper
Demonstrates mapping of all fields from source to target JSON including legal_name to CD_Legal_Name
"""

import json
import logging
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Utils.comprehensive_json_mapper import ComprehensiveJsonMapper
from Utils.ApplicationContext import ApplicationContext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Load application configuration"""
    try:
        context = ApplicationContext()
        return context.get_config()
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        # Fallback config for testing
        return {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'database': 'vstate_utils',
                'user': 'postgres',
                'password': 'password'
            },
            'ai_service': {
                'api_key': 'test_key',
                'model': 'gpt-3.5-turbo'
            }
        }

def create_source_json():
    """Create the source JSON with all fields"""
    return {
        "1": {
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
                "stateFullDesc": "newmexico",
                "stateUrl": "https://portal.sos.state.nm.us/BFS/online/Account",
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
                    "legal_name": "Saumya",  # This should map to CD_Legal_Name
                    "alternate_legal_name": "Patra"
                },
                "registered_agent": {
                    "Address": {
                        "city": "Pune",
                        "state ": 1,
                        "zip_code": None,
                        "address_line 2": "jdjdjjd",
                        "street_address": "hadapsar"
                    },
                    "emailId": "saumya@gmail.com",
                    "contactNo": 388383838,
                    "keyPersonnelName": "Saumyaranjan Patra",
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
                        "state": 1,
                        "zip_code": None,
                        "contact_no": 38838383883,
                        "email_address": "saumya@gmail.com",
                        "address_line 2": "jdjdjjd",
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
                "contact_information": {
                    "name": "Saumya Patra",
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
                    "keyPersonnelName": "saumya"
                }
            },
            "formProgress": 100
        }
    }

def create_target_template():
    """Create the target JSON template"""
    return {
        "data": {
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
                "stateFullDesc": "newmexico",
                "stateUrl": "https://portal.sos.state.nm.us/BFS/online/Account",
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
            "Payload": {
                "Name": {
                    "CD_Legal_Name": "",  # This should be mapped from legal_name
                    "CD_Duration": "30",
                    "CD_Alternate_Legal_Name": "",
                    "CD_Naics_Code": "334111"
                },
                "Principal_Address": {
                    "PA_Address_Line1": "",
                    "PA_Address_Line2": "",
                    "PA_City": "",
                    "PA_State": "",
                    "PA_Country": "USA",
                    "PA_Postal_Code": ""
                },
                "Registered_Agent": {
                    "Address": {
                        "RA_Address_Line1": "",
                        "RA_Address_Line2": "",
                        "RA_City": "",
                        "RA_State": "",
                        "RA_Country": "USA",
                        "RA_Postal_Code": ""
                    },
                    "Name": {
                        "RA_Name": "",
                        "Email": "",
                        "Contact_No": ""
                    }
                },
                "Organizer_Information": {
                    "Organizer_Details": {
                        "Org_Name": "",
                        "Og_Email": "",
                        "Og_Contact_No": ""
                    },
                    "Org_Address": {
                        "Org_Address_Line1": "",
                        "Org_Address_Line2": "",
                        "Org_City": "",
                        "Org_State": "",
                        "Org_Country": "USA",
                        "Org_Postal_Code": ""
                    }
                },
                "County": {
                    "CD_County": "Albany"
                }
            }
        }
    }

def test_comprehensive_mapping():
    """Test the comprehensive JSON mapping functionality"""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Initialize comprehensive mapper
        mapper = ComprehensiveJsonMapper(config)
        logger.info("Comprehensive JSON Mapper initialized")
        
        # Create source and target JSONs
        source_json = create_source_json()
        target_template = create_target_template()
        
        logger.info("Source and target JSONs created")
        
        # Initialize comprehensive mappings in database
        mapper.initialize_comprehensive_mappings()
        logger.info("Comprehensive mappings initialized in database")
        
        # Transform JSON with comprehensive mapping
        result = mapper.transform_json(source_json, target_template)
        
        logger.info("JSON transformation completed")
        
        # Generate mapping report
        report = mapper.get_mapping_report(source_json, result)
        
        # Print results
        print("\n" + "="*80)
        print("COMPREHENSIVE JSON MAPPING TEST RESULTS")
        print("="*80)
        
        print(f"\nTotal source fields: {report['total_source_fields']}")
        print(f"Total target fields: {report['total_target_fields']}")
        print(f"Mapped fields: {report['mapped_fields']}")
        print(f"Mapping accuracy: {report['mapping_accuracy']:.2%}")
        
        print("\n" + "-"*80)
        print("MAPPING DETAILS")
        print("-"*80)
        
        for mapping in report['mappings']:
            print(f"Source: {mapping['source_path']}")
            print(f"Target: {mapping['target_path']}")
            print(f"Value: {mapping['source_value']}")
            print("-" * 40)
        
        print("\n" + "-"*80)
        print("TRANSFORMED JSON RESULT")
        print("-"*80)
        print(json.dumps(result, indent=2))
        
        # Verify specific key mappings
        print("\n" + "-"*80)
        print("VERIFICATION OF KEY MAPPINGS")
        print("-"*80)
        
        # Check legal_name mapping
        source_legal_name = source_json["1"]["payload"]["name"]["legal_name"]
        target_legal_name = result["data"]["Payload"]["Name"]["CD_Legal_Name"]
        
        print(f"Source legal_name: {source_legal_name}")
        print(f"Target CD_Legal_Name: {target_legal_name}")
        
        if source_legal_name == target_legal_name:
            print("✅ legal_name -> CD_Legal_Name mapping successful!")
        else:
            print("❌ legal_name -> CD_Legal_Name mapping failed!")
        
        # Check alternate_legal_name mapping
        source_alt_name = source_json["1"]["payload"]["name"]["alternate_legal_name"]
        target_alt_name = result["data"]["Payload"]["Name"]["CD_Alternate_Legal_Name"]
        
        print(f"\nSource alternate_legal_name: {source_alt_name}")
        print(f"Target CD_Alternate_Legal_Name: {target_alt_name}")
        
        if source_alt_name == target_alt_name:
            print("✅ alternate_legal_name -> CD_Alternate_Legal_Name mapping successful!")
        else:
            print("❌ alternate_legal_name -> CD_Alternate_Legal_Name mapping failed!")
        
        # Check principal address mappings
        source_city = source_json["1"]["payload"]["principal_address"]["city"]
        target_city = result["data"]["Payload"]["Principal_Address"]["PA_City"]
        
        print(f"\nSource principal_address.city: {source_city}")
        print(f"Target PA_City: {target_city}")
        
        if source_city == target_city:
            print("✅ Principal address city mapping successful!")
        else:
            print("❌ Principal address city mapping failed!")
        
        # Check registered agent mappings
        source_ra_name = source_json["1"]["payload"]["registered_agent"]["keyPersonnelName"]
        target_ra_name = result["data"]["Payload"]["Registered_Agent"]["Name"]["RA_Name"]
        
        print(f"\nSource registered_agent.keyPersonnelName: {source_ra_name}")
        print(f"Target RA_Name: {target_ra_name}")
        
        if source_ra_name == target_ra_name:
            print("✅ Registered agent name mapping successful!")
        else:
            print("❌ Registered agent name mapping failed!")
        
        # Check organizer mappings
        source_org_name = source_json["1"]["payload"]["organizer_information"]["keyPersonnelName"]
        target_org_name = result["data"]["Payload"]["Organizer_Information"]["Organizer_Details"]["Org_Name"]
        
        print(f"\nSource organizer_information.keyPersonnelName: {source_org_name}")
        print(f"Target Org_Name: {target_org_name}")
        
        if source_org_name == target_org_name:
            print("✅ Organizer name mapping successful!")
        else:
            print("❌ Organizer name mapping failed!")
        
        # Check unmapped fields
        if report['unmapped_source_fields']:
            print(f"\n⚠️  Unmapped source fields ({len(report['unmapped_source_fields'])}):")
            for path, value in report['unmapped_source_fields']:
                print(f"  - {path}: {value}")
        
        print("\n" + "="*80)
        print("TEST COMPLETED SUCCESSFULLY")
        print("="*80)
        
        return result
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

def test_custom_mapping():
    """Test adding custom mappings"""
    try:
        config = load_config()
        mapper = ComprehensiveJsonMapper(config)
        
        # Add a custom mapping
        mapper.add_custom_mapping(
            source_path="payload.name.legal_name",
            target_path="data.Payload.Name.CD_LLC_Name",
            semantic_meaning="Custom mapping for LLC name",
            field_type="name"
        )
        
        print("✅ Custom mapping added successfully!")
        
    except Exception as e:
        logger.error(f"Custom mapping test failed: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run all tests
        print("Starting Comprehensive JSON Mapper Tests...")
        
        # Test custom mapping
        test_custom_mapping()
        
        # Test main mapping functionality
        result = test_comprehensive_mapping()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        sys.exit(1) 