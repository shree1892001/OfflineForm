import json
import logging
from typing import Dict, Any, List
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

class JsonMapper:
    def __init__(self, config: Dict):
        """
        Initialize JSON mapper with database service and capitalized mapper
        """
        self.config = config
        self.db_service = JsonMappingDatabaseService(config)
        self.capitalized_mapper = CapitalizedJsonMapper(config)
        self.logger = logging.getLogger(__name__)
        
    def transform_json(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform source JSON to target structure using database mappings with capitalized keys
        """
        try:
            # Initialize capitalized mappings in database
            self.capitalized_mapper.initialize_capitalized_mappings()
            
            # Initialize target structure
            target_json = {
                "data": {
                    "EntityType": {},
                    "State": {},
                    "Payload": {
                        "Name": {},
                        "Principal_Address": {},
                        "Registered_Agent": {
                            "Address": {},
                            "Name": {}
                        },
                        "Organizer_Information": {
                            "Organizer_Details": {},
                            "Org_Address": {}
                        },
                        "County": {}
                    }
                }
            }
            
            # Use capitalized mapper for transformation
            result = self.capitalized_mapper.transform_json(source_json, target_json)
            
            self.logger.info("JSON transformation completed with capitalized keys")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON: {e}")
            # Fallback to original method
            try:
                return self._transform_json_fallback(source_json)
            except Exception as fallback_error:
                self.logger.error(f"Fallback JSON transformation also failed: {fallback_error}")
                raise
    
    def _transform_json_fallback(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback method using original transformation logic
        """
        try:
            # Get mappings from database
            mappings = self.db_service.get_all_json_mappings()
            
            # Initialize target structure
            target_json = {
                "data": {
                    "EntityType": {},
                    "State": {},
                    "Payload": {
                        "Name": {},
                        "Principal_Address": {},
                        "Registered_Agent": {
                            "Address": {},
                            "Name": {}
                        },
                        "Organizer_Information": {
                            "Organizer_Details": {},
                            "Org_Address": {}
                        },
                        "County": {}
                    }
                }
            }
            
            # Extract payload from source (handle nested structure)
            source_payload = self._extract_payload(source_json)
            
            # Apply mappings
            for mapping in mappings:
                source_path = mapping.source_path
                target_path = mapping.target_path
                
                # Get value from source using path
                source_value = self._get_value_by_path(source_payload, source_path)
                
                if source_value is not None:
                    # Set value in target using path
                    self._set_value_by_path(target_json, target_path, source_value)
            
            return target_json
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON with fallback method: {e}")
            raise
    
    def get_mapping_report(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a comprehensive mapping report using capitalized mapper
        """
        try:
            # Initialize capitalized mappings
            self.capitalized_mapper.initialize_capitalized_mappings()
            
            # Create target template
            target_template = {
                "data": {
                    "EntityType": {},
                    "State": {},
                    "Payload": {
                        "Name": {},
                        "Principal_Address": {},
                        "Registered_Agent": {
                            "Address": {},
                            "Name": {}
                        },
                        "Organizer_Information": {
                            "Organizer_Details": {},
                            "Org_Address": {}
                        },
                        "County": {}
                    }
                }
            }
            
            # Generate mapping report
            report = self.capitalized_mapper.get_mapping_report(source_json, target_template)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to get mapping report: {e}")
            raise
    
    def add_custom_mapping(self, source_path: str, target_path: str, 
                          semantic_meaning: str = "", field_type: str = "string"):
        """
        Add a custom mapping using capitalized mapper
        """
        try:
            self.capitalized_mapper.add_custom_mapping(
                source_path=source_path,
                target_path=target_path,
                semantic_meaning=semantic_meaning,
                field_type=field_type
            )
            
        except Exception as e:
            self.logger.error(f"Failed to add custom mapping: {e}")
            raise

    def _extract_payload(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract payload from source JSON structure
        """
        # Handle the nested structure where payload is inside a numbered key
        for key, value in source_json.items():
            if isinstance(value, dict) and 'payload' in value:
                return value['payload']
        return source_json.get('payload', {})
    
    def _get_value_by_path(self, obj: Dict[str, Any], path: str) -> Any:
        """
        Get value from object using dot notation path
        """
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
    
    def _set_value_by_path(self, obj: Dict[str, Any], path: str, value: Any):
        """
        Set value in object using dot notation path
        """
        try:
            keys = path.split('.')
            current = obj
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
        except Exception as e:
            self.logger.error(f"Failed to set value at path {path}: {e}")
    
    def initialize_default_mappings(self):
        """
        Initialize database with default JSON field mappings using capitalized mapper
        """
        try:
            # Use capitalized mapper to initialize mappings
            self.capitalized_mapper.initialize_capitalized_mappings()
            
            self.logger.info("JSON mapping database initialized with capitalized mappings successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize JSON mapping database: {e}")
            raise 