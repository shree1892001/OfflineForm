#!/usr/bin/env python3
"""
Integration script for Database-Driven Capitalized JSON Mapper
Shows how to integrate the capitalized mapper into existing code
"""

import json
import logging
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Utils.capitalized_json_mapper import CapitalizedJsonMapper
from Utils.ApplicationContext import ApplicationContext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CapitalizedJsonMappingService:
    """
    Service class that integrates the capitalized JSON mapper into your existing codebase
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.mapper = CapitalizedJsonMapper(config)
        self.logger = logging.getLogger(__name__)
        
        # Initialize mappings if not already done
        try:
            self.mapper.initialize_capitalized_mappings()
            self.logger.info("Capitalized mappings initialized")
        except Exception as e:
            self.logger.warning(f"Mappings may already be initialized: {e}")
    
    def map_source_to_target(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map source JSON to target JSON using capitalized keys
        
        Args:
            source_json: Source JSON with lowercase keys (e.g., legal_name)
            target_template: Target JSON template with target structure
            
        Returns:
            Mapped JSON with values from source mapped to target
        """
        try:
            self.logger.info("Starting JSON mapping with capitalized keys")
            
            # Transform the JSON
            result = self.mapper.transform_json(source_json, target_template)
            
            self.logger.info("JSON mapping completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to map JSON: {e}")
            raise
    
    def get_mapping_report(self, source_json: Dict[str, Any], target_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a detailed mapping report
        
        Args:
            source_json: Source JSON
            target_json: Target JSON
            
        Returns:
            Mapping report with statistics and details
        """
        return self.mapper.get_mapping_report(source_json, target_json)
    
    def add_custom_mapping(self, source_path: str, target_path: str, 
                          semantic_meaning: str = "", field_type: str = "string"):
        """
        Add a custom mapping to the database
        
        Args:
            source_path: Source field path (e.g., "Payload.Name.Legal_Name")
            target_path: Target field path (e.g., "data.Payload.Name.CD_Legal_Name")
            semantic_meaning: Semantic meaning of the field
            field_type: Type of the field
        """
        self.mapper.add_custom_mapping(source_path, target_path, semantic_meaning, field_type)
    
    def get_all_mappings(self) -> List:
        """
        Get all mappings from the database
        
        Returns:
            List of all mappings
        """
        return self.mapper.db_service.get_all_json_mappings()

def create_sample_source_json():
    """Create a sample source JSON with lowercase keys"""
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
                    "legal_name": "Saumya",  # Will become Legal_Name
                    "alternate_legal_name": "Patra"  # Will become Alternate_Legal_Name
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
                    "keyPersonnelName": "Saumyaranjan Patra"
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
                    "keyPersonnelName": "saumya"
                }
            },
            "formProgress": 100
        }
    }

def create_sample_target_template():
    """Create a sample target JSON template"""
    return {
        "data": {
            "EntityType": {},
            "State": {},
            "Payload": {
                "Name": {
                    "CD_Legal_Name": "",
                    "CD_Alternate_Legal_Name": ""
                },
                "Principal_Address": {
                    "PA_City": "",
                    "PA_State": "",
                    "PA_Postal_Code": "",
                    "PA_Address_Line1": "",
                    "PA_Address_Line2": ""
                },
                "Registered_Agent": {
                    "Address": {
                        "RA_City": "",
                        "RA_State": "",
                        "RA_Postal_Code": "",
                        "RA_Address_Line1": "",
                        "RA_Address_Line2": ""
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
                    }
                }
            }
        }
    }

def demonstrate_integration():
    """Demonstrate how to integrate the capitalized mapper into your code"""
    try:
        # Load configuration
        context = ApplicationContext()
        config = context.get_config()
        
        # Initialize the service
        service = CapitalizedJsonMappingService(config)
        
        # Create sample data
        source_json = create_sample_source_json()
        target_template = create_sample_target_template()
        
        print("="*80)
        print("CAPITALIZED JSON MAPPER INTEGRATION DEMONSTRATION")
        print("="*80)
        
        # Show source JSON
        print("\nSource JSON (with lowercase keys):")
        print(json.dumps(source_json, indent=2))
        
        # Map the JSON
        result = service.map_source_to_target(source_json, target_template)
        
        print("\nMapped JSON (with capitalized keys):")
        print(json.dumps(result, indent=2))
        
        # Get mapping report
        report = service.get_mapping_report(source_json, result)
        
        print(f"\nMapping Statistics:")
        print(f"- Total source fields: {report['total_source_fields']}")
        print(f"- Mapped fields: {report['mapped_fields']}")
        print(f"- Database mappings: {report['database_mappings']}")
        print(f"- Fallback mappings: {report['fallback_mappings']}")
        print(f"- Mapping accuracy: {report['mapping_accuracy']:.2%}")
        
        # Show specific mappings
        print(f"\nKey Mappings:")
        for mapping in report['mappings'][:5]:  # Show first 5 mappings
            print(f"- {mapping['source_path']} -> {mapping['target_path']} ({mapping['mapping_type']})")
        
        # Demonstrate adding custom mapping
        print(f"\nAdding custom mapping...")
        service.add_custom_mapping(
            source_path="Payload.Name.Legal_Name",
            target_path="data.Payload.Name.CD_LLC_Name",
            semantic_meaning="Custom LLC name mapping",
            field_type="name"
        )
        
        # Get all mappings
        all_mappings = service.get_all_mappings()
        print(f"Total mappings in database: {len(all_mappings)}")
        
        print("\n" + "="*80)
        print("INTEGRATION DEMONSTRATION COMPLETED")
        print("="*80)
        
        return result
        
    except Exception as e:
        logger.error(f"Integration demonstration failed: {e}")
        raise

def show_usage_examples():
    """Show usage examples for the capitalized mapper"""
    print("\n" + "="*80)
    print("USAGE EXAMPLES")
    print("="*80)
    
    print("""
# Example 1: Basic Usage
from Utils.capitalized_json_mapper import CapitalizedJsonMapper
from Utils.ApplicationContext import ApplicationContext

# Initialize
context = ApplicationContext()
config = context.get_config()
mapper = CapitalizedJsonMapper(config)

# Initialize mappings (run once)
mapper.initialize_capitalized_mappings()

# Map JSON
source_json = {...}  # Your source JSON with lowercase keys
target_template = {...}  # Your target template
result = mapper.transform_json(source_json, target_template)

# Example 2: Using the Service Class
from integrate_capitalized_mapper import CapitalizedJsonMappingService

service = CapitalizedJsonMappingService(config)
result = service.map_source_to_target(source_json, target_template)

# Example 3: Adding Custom Mappings
mapper.add_custom_mapping(
    source_path="Payload.Name.Legal_Name",
    target_path="data.Payload.Name.CD_LLC_Name",
    semantic_meaning="Custom LLC name mapping",
    field_type="name"
)

# Example 4: Getting Mapping Report
report = mapper.get_mapping_report(source_json, result)
print(f"Mapped {report['mapped_fields']} fields with {report['mapping_accuracy']:.2%} accuracy")
""")

if __name__ == "__main__":
    try:
        # Show usage examples
        show_usage_examples()
        
        # Demonstrate integration
        result = demonstrate_integration()
        
        print("\n🎉 Integration demonstration completed successfully!")
        
    except Exception as e:
        logger.error(f"Integration demonstration failed: {e}")
        sys.exit(1) 