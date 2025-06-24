#!/usr/bin/env python3
"""
Test script for Enhanced JSON Mapper
Demonstrates mapping from Legal_Name to CD_LLC_Name and other robust mapping scenarios
"""

import json
import logging
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Utils.enhanced_json_mapper import EnhancedJsonMapper
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
    """Create the source JSON with Legal_Name and other fields"""
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
                    "Legal_Name": "Saumya",  # This should map to CD_LLC_Name
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
                    "CD_Legal_Name": "",  # This should be mapped from Legal_Name
                    "CD_LLC_Name": "",    # This should also be mapped from Legal_Name
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

def test_enhanced_mapping():
    """Test the enhanced JSON mapping functionality"""
    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Initialize enhanced mapper
        mapper = EnhancedJsonMapper(config)
        logger.info("Enhanced JSON Mapper initialized")
        
        # Create source and target JSONs
        source_json = create_source_json()
        target_template = create_target_template()
        
        logger.info("Source and target JSONs created")
        
        # Add custom mapping for Legal_Name to CD_LLC_Name
        mapper.add_custom_mapping(
            source_field="payload.name.Legal_Name",
            target_field="data.Payload.Name.CD_LLC_Name",
            semantic_meaning="Legal name mapping to LLC name field",
            field_type="name"
        )
        
        # Add custom mapping for Legal_Name to CD_Legal_Name as well
        mapper.add_custom_mapping(
            source_field="payload.name.Legal_Name",
            target_field="data.Payload.Name.CD_Legal_Name",
            semantic_meaning="Legal name mapping to legal name field",
            field_type="name"
        )
        
        logger.info("Custom mappings added")
        
        # Transform JSON with enhanced mapping
        result = mapper.transform_json_with_enhanced_mapping(source_json, target_template)
        
        logger.info("JSON transformation completed")
        
        # Generate mapping report
        report = mapper.get_mapping_report(source_json, result)
        
        # Print results
        print("\n" + "="*80)
        print("ENHANCED JSON MAPPING TEST RESULTS")
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
            print(f"Type: {mapping.get('mapping_type', 'unknown')}")
            print(f"Confidence: {mapping.get('confidence', 'N/A')}")
            print("-" * 40)
        
        print("\n" + "-"*80)
        print("TRANSFORMED JSON RESULT")
        print("-"*80)
        print(json.dumps(result, indent=2))
        
        # Verify specific mappings
        print("\n" + "-"*80)
        print("VERIFICATION OF KEY MAPPINGS")
        print("-"*80)
        
        # Check Legal_Name mapping
        source_legal_name = source_json["1"]["payload"]["name"]["Legal_Name"]
        target_llc_name = result["data"]["Payload"]["Name"]["CD_LLC_Name"]
        target_legal_name = result["data"]["Payload"]["Name"]["CD_Legal_Name"]
        
        print(f"Source Legal_Name: {source_legal_name}")
        print(f"Target CD_LLC_Name: {target_llc_name}")
        print(f"Target CD_Legal_Name: {target_legal_name}")
        
        if source_legal_name == target_llc_name:
            print("✅ Legal_Name -> CD_LLC_Name mapping successful!")
        else:
            print("❌ Legal_Name -> CD_LLC_Name mapping failed!")
        
        if source_legal_name == target_legal_name:
            print("✅ Legal_Name -> CD_Legal_Name mapping successful!")
        else:
            print("❌ Legal_Name -> CD_Legal_Name mapping failed!")
        
        # Check other key mappings
        source_city = source_json["1"]["payload"]["principal_address"]["city"]
        target_city = result["data"]["Payload"]["Principal_Address"]["PA_City"]
        
        print(f"\nSource city: {source_city}")
        print(f"Target PA_City: {target_city}")
        
        if source_city == target_city:
            print("✅ City mapping successful!")
        else:
            print("❌ City mapping failed!")
        
        print("\n" + "="*80)
        print("TEST COMPLETED SUCCESSFULLY")
        print("="*80)
        
        return result
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

def test_naming_convention_detection():
    """Test naming convention detection"""
    try:
        config = load_config()
        mapper = EnhancedJsonMapper(config)
        
        test_fields = [
            "legal_name",
            "Legal_Name", 
            "legalName",
            "LEGAL_NAME",
            "legal-name",
            "LegalName"
        ]
        
        print("\n" + "="*80)
        print("NAMING CONVENTION DETECTION TEST")
        print("="*80)
        
        for field in test_fields:
            convention = mapper.detect_naming_convention(field)
            normalized = mapper.normalize_field_name(field, 'pascal_case')
            print(f"Field: {field:15} | Convention: {convention:12} | Normalized: {normalized}")
        
        print("="*80)
        
    except Exception as e:
        logger.error(f"Naming convention test failed: {e}")
        raise

def test_semantic_matching():
    """Test semantic matching functionality"""
    try:
        config = load_config()
        mapper = EnhancedJsonMapper(config)
        
        source_fields = ["Legal_Name", "legal_name", "entity_name", "company_name"]
        target_fields = ["CD_Legal_Name", "CD_LLC_Name", "CD_Entity_Name", "CD_Company_Name"]
        
        print("\n" + "="*80)
        print("SEMANTIC MATCHING TEST")
        print("="*80)
        
        for source_field in source_fields:
            match = mapper.find_semantic_match(source_field, target_fields)
            print(f"Source: {source_field:15} | Match: {match or 'No match'}")
        
        print("="*80)
        
    except Exception as e:
        logger.error(f"Semantic matching test failed: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run all tests
        print("Starting Enhanced JSON Mapper Tests...")
        
        # Test naming convention detection
        test_naming_convention_detection()
        
        # Test semantic matching
        test_semantic_matching()
        
        # Test main mapping functionality
        result = test_enhanced_mapping()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        sys.exit(1) 