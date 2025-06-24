from Services.MappingRulesDatabaseService import MappingRulesDatabaseService
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Utils.capitalized_json_mapper import CapitalizedJsonMapper
import logging
import json
from typing import Dict, Any, List

def generate_mapping_rules(config: dict) -> dict:
    """
    Generate mapping rules from database
    """
    try:
        # Initialize database service
        db_service = MappingRulesDatabaseService(config)
        
        # Create tables if they don't exist
        db_service.create_tables()
        
        # Force re-initialization to ensure correct mappings are in database
        initialize_database_with_default_data(config)
        
        mapping_rules = db_service.get_all_mapping_rules()
        
        return mapping_rules
        
    except Exception as e:
        logging.error(f"Failed to generate mapping rules from database: {e}")
        # Fallback to empty dict if database fails
        return {}

def generate_json_mapping_rules(config: dict) -> List[Dict]:
    """
    Generate JSON mapping rules from database with AI enhancement
    """
    try:
        # Initialize JSON mapping database service
        json_db_service = JsonMappingDatabaseService(config)
        
        # Create tables if they don't exist
        json_db_service.create_json_mapping_tables()
        
        # Initialize with default JSON mappings
        initialize_json_mapping_database(config)
        
        # Get all mappings (database + AI enhanced)
        mappings = json_db_service.get_all_json_mappings()
        
        return mappings
        
    except Exception as e:
        logging.error(f"Failed to generate JSON mapping rules: {e}")
        return []

def transform_json_with_mappings(source_json: Dict[str, Any], config: dict) -> Dict[str, Any]:
    """
    Transform source JSON to target structure using database-driven mappings with capitalized keys
    """
    try:
        # Initialize capitalized JSON mapper
        capitalized_mapper = CapitalizedJsonMapper(config)
        
        # Initialize capitalized mappings in database
        capitalized_mapper.initialize_capitalized_mappings()
        
        # Create target template
        target_template = _create_target_template()
        
        # Transform JSON using capitalized mapper (this uses the semantic mappings from database)
        result = capitalized_mapper.transform_json(source_json, target_template)
        
        logging.info(f"Capitalized JSON transformation completed successfully using database semantic mappings")
        
        return result
        
    except Exception as e:
        logging.error(f"Failed to transform JSON with capitalized mapper: {e}")
        # Fallback to original method
        try:
            return transform_json_with_mappings_fallback(source_json, config)
        except Exception as fallback_error:
            logging.error(f"Fallback JSON transformation also failed: {fallback_error}")
            raise

def transform_json_with_mappings_fallback(source_json: Dict[str, Any], config: dict) -> Dict[str, Any]:
    """
    Fallback method for JSON transformation using original approach
    """
    try:
        # Get JSON mappings
        json_mappings = generate_json_mapping_rules(config)
        
        # Extract payload from source
        source_payload = _extract_payload(source_json)
        
        # Create target template
        target_template = _create_target_template()
        
        # Apply mappings
        result = _apply_json_mappings(target_template, json_mappings, source_payload)
        
        logging.info(f"Fallback JSON transformation completed with {len(json_mappings)} mappings")
        
        return result
        
    except Exception as e:
        logging.error(f"Failed to transform JSON with fallback method: {e}")
        raise

def transform_json_with_capitalized_mapping(source_json: Dict[str, Any], config: dict) -> Dict[str, Any]:
    """
    Transform source JSON to target structure using capitalized key mappings
    This is the main function to use for capitalized JSON mapping
    """
    try:
        # Initialize capitalized JSON mapper
        capitalized_mapper = CapitalizedJsonMapper(config)
        
        # Initialize capitalized mappings in database
        capitalized_mapper.initialize_capitalized_mappings()
        
        # Create target template
        target_template = _create_target_template()
        
        # Transform JSON using capitalized mapper
        result = capitalized_mapper.transform_json(source_json, target_template)
        
        # Generate mapping report
        report = capitalized_mapper.get_mapping_report(source_json, result)
        
        logging.info(f"Capitalized JSON transformation completed with {report['mapped_fields']} mappings "
                    f"({report['database_mappings']} database, {report['fallback_mappings']} fallback)")
        
        return result
        
    except Exception as e:
        logging.error(f"Failed to transform JSON with capitalized mapping: {e}")
        raise

def get_capitalized_mapping_report(source_json: Dict[str, Any], config: dict) -> Dict[str, Any]:
    """
    Get a comprehensive mapping report for capitalized JSON mapping
    """
    try:
        # Initialize capitalized JSON mapper
        capitalized_mapper = CapitalizedJsonMapper(config)
        
        # Create target template
        target_template = _create_target_template()
        
        # Generate mapping report
        report = capitalized_mapper.get_mapping_report(source_json, target_template)
        
        return report
        
    except Exception as e:
        logging.error(f"Failed to get capitalized mapping report: {e}")
        raise

def add_custom_capitalized_mapping(source_path: str, target_path: str, config: dict, 
                                 semantic_meaning: str = "", field_type: str = "string"):
    """
    Add a custom mapping to the database for capitalized keys
    """
    try:
        # Initialize capitalized JSON mapper
        capitalized_mapper = CapitalizedJsonMapper(config)
        
        # Add custom mapping
        capitalized_mapper.add_custom_mapping(
            source_path=source_path,
            target_path=target_path,
            semantic_meaning=semantic_meaning,
            field_type=field_type
        )
        
        logging.info(f"Added custom capitalized mapping: {source_path} -> {target_path}")
        
    except Exception as e:
        logging.error(f"Failed to add custom capitalized mapping: {e}")
        raise

def initialize_database_with_default_data(config: dict):
    """
    Initialize database with default base entities, attributes, and special cases
    """
    try:
        db_service = MappingRulesDatabaseService(config)
        
        # Create tables
        db_service.create_tables()
        
        # Clear all existing data first
        db_service.clear_all_data()
        
        # Default base entities
        base_entities = {
            "RA": "Registered Agent",
            "Dr": "Director",
            "P": "Principal Address",
            "Inc": "Incorporator",
            "Mom": "Member or Manager",
            "MOM": "Member or Manager",
            "PA": "Principal Address",
        }
        
        # Default attributes
        attributes = {
            "zip": "Zip Code",
            "Zip": "Zip Code",
            "st": "State",
            "S": "State",
            "city": "City",
            "state": "State",
            "Address line 1": "street address",
            "Address line 2": "Address Line 2",
            "Address Zip Code": "Address Zip Code",
            "Mailing address": "Mailing Address",
        }
        
        # Default special cases
        special_cases = {
            "RAMAZ": "Registered Agent Mailing  Information Zip Code",
            "DS": "Director State",
            "RS": "Registered Agent State", 
            "PS": "Principal Address State",
            "IS": "Incorporator State",
            "PZIP": "Principal Address Zip Code",
            "RA MailingAdd zip": "Registered Agent Mailing Information Zip Code",
            "Entity Name": "Legal Name",
            "RA Zip": "Registered Agent Zip Code",
            "RA Address city": "Registered Agent City",
            "Register Agent MI_state": "Registered Agent Mailing Information State",
            "RA Name":"Registered Agent Name"
        }
        
        # Insert data into database
        db_service.insert_base_entities(base_entities)
        db_service.insert_attributes(attributes)
        db_service.insert_special_cases(special_cases)
        
        logging.info("Database initialized with default data successfully")
        
    except Exception as e:
        logging.error(f"Failed to initialize database with default data: {e}")
        raise

def initialize_json_mapping_database(config: dict):
    """
    Initialize JSON mapping database with default mappings including capitalized keys
    """
    try:
        json_db_service = JsonMappingDatabaseService(config)
        
        # Create tables
        json_db_service.create_json_mapping_tables()
        
        # Default field types
        field_types = {
            "name": {
                "description": "Name related fields",
                "validation_patterns": [r'^[a-zA-Z\s]+$'],
                "business_context": "entity_formation"
            },
            "address": {
                "description": "Address related fields",
                "validation_patterns": [r'^[a-zA-Z0-9\s\.,\-]+$'],
                "business_context": "location"
            },
            "contact": {
                "description": "Contact information fields",
                "validation_patterns": [],
                "business_context": "communication"
            },
            "email": {
                "description": "Email address fields",
                "validation_patterns": [r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'],
                "business_context": "communication"
            },
            "phone": {
                "description": "Phone number fields",
                "validation_patterns": [r'^\+?[\d\s\-\(\)]+$'],
                "business_context": "communication"
            },
            "id": {
                "description": "ID and reference fields",
                "validation_patterns": [r'^\d+$'],
                "business_context": "reference"
            },
            "url": {
                "description": "URL and website fields",
                "validation_patterns": [r'^https?://.+'],
                "business_context": "web"
            },
            "date": {
                "description": "Date and timestamp fields",
                "validation_patterns": [r'^\d{4}-\d{2}-\d{2}$'],
                "business_context": "temporal"
            },
            "boolean": {
                "description": "Boolean and flag fields",
                "validation_patterns": [],
                "business_context": "logic"
            },
            "numeric": {
                "description": "Numeric fields",
                "validation_patterns": [r'^\d+(\.\d+)?$'],
                "business_context": "calculation"
            }
        }
        
        # Default semantic meanings
        semantic_meanings = {
            "legal_name": {
                "description": "Legal name of the entity",
                "category": "entity",
                "synonyms": ["Legal_Name", "entity_name", "Entity_Name", "company_name", "Company_Name"],
                "business_domain": "entity_formation"
            },
            "alternate_name": {
                "description": "Alternative name for the entity",
                "category": "entity",
                "synonyms": ["Alternate_Legal_Name", "dba_name", "DBA_Name", "trade_name", "Trade_Name"],
                "business_domain": "entity_formation"
            },
            "city": {
                "description": "City name",
                "category": "location",
                "synonyms": ["City", "town", "municipality"],
                "business_domain": "address"
            },
            "state": {
                "description": "State name or ID",
                "category": "location",
                "synonyms": ["State", "province", "region"],
                "business_domain": "address"
            },
            "zip_code": {
                "description": "Postal/ZIP code",
                "category": "location",
                "synonyms": ["Zip_Code", "postal_code", "Postal_Code", "zipcode"],
                "business_domain": "address"
            },
            "street_address": {
                "description": "Street address line",
                "category": "location",
                "synonyms": ["Street_Address", "address_line1", "AddressLine1"],
                "business_domain": "address"
            },
            "address_line2": {
                "description": "Secondary address line",
                "category": "location",
                "synonyms": ["Address_Line_2", "addressline2", "AddressLine2"],
                "business_domain": "address"
            },
            "email": {
                "description": "Email address",
                "category": "contact",
                "synonyms": ["EmailId", "email_address", "Email_Address"],
                "business_domain": "communication"
            },
            "contact_number": {
                "description": "Contact phone number",
                "category": "contact",
                "synonyms": ["ContactNo", "contact_no", "Contact_No", "phone"],
                "business_domain": "communication"
            },
            "personnel_name": {
                "description": "Name of key personnel",
                "category": "person",
                "synonyms": ["KeyPersonnelName", "personnel_name", "contact_name"],
                "business_domain": "personnel"
            }
        }
        
        # Insert field types and semantic meanings
        json_db_service.insert_field_types(field_types)
        json_db_service.insert_semantic_meanings(semantic_meanings)
        
        # Initialize capitalized mappings
        capitalized_mapper = CapitalizedJsonMapper(config)
        capitalized_mapper.initialize_capitalized_mappings()
        
        logging.info("JSON mapping database initialized with capitalized mappings successfully")
        
    except Exception as e:
        logging.error(f"Failed to initialize JSON mapping database: {e}")
        raise

def _extract_payload(source_json: Dict[str, Any]) -> Dict[str, Any]:
    """Extract payload from source JSON structure"""
    for key, value in source_json.items():
        if isinstance(value, dict) and 'payload' in value:
            return value['payload']
    return source_json.get('payload', {})

def _create_target_template() -> Dict[str, Any]:
    """Create target JSON structure template"""
    return {
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
                }
            }
        }
    }

def _apply_json_mappings(template: Dict[str, Any], mappings: List, source_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Apply JSON mappings to template"""
    result = json.loads(json.dumps(template))  # Deep copy
    
    for mapping in mappings:
        try:
            source_path = mapping.source_path
            target_path = mapping.target_path
            
            # Get value from source using path
            source_value = _get_value_by_path(source_payload, source_path)
            
            if source_value is not None:
                # Set value in target using path
                _set_value_by_path(result, target_path, source_value)
                
        except Exception as e:
            logging.warning(f"Failed to apply mapping {mapping.source_path} -> {mapping.target_path}: {e}")
    
    return result

def _get_value_by_path(obj: Dict[str, Any], path: str) -> Any:
    """Get value from object using dot notation path"""
    try:
        keys = path.split('.')
        current = obj
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    except Exception:
        return None

def _set_value_by_path(obj: Dict[str, Any], path: str, value: Any):
    """Set value in object using dot notation path"""
    try:
        parts = path.split('.')
        current = obj
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
        
    except Exception as e:
        logging.error(f"Failed to set value at path {path}: {e}") 