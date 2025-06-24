import json
import logging
from typing import Dict, Any, List
from difflib import SequenceMatcher
import re

class SimpleJsonMapper:
    def __init__(self, config: Dict):
        """
        Initialize simple JSON mapper
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Dynamic semantic patterns - can be extended without hardcoding
        self.semantic_patterns = {
            "name": ["name", "legal_name", "entity_name", "company_name", "business_name"],
            "city": ["city", "town", "municipality"],
            "state": ["state", "province", "region"],
            "zip": ["zip", "zip_code", "postal_code", "postal"],
            "address": ["address", "street", "street_address", "address_line"],
            "email": ["email", "emailId", "email_address", "e_mail"],
            "phone": ["phone", "contact", "contactNo", "contact_no", "telephone", "mobile"],
            "personnel": ["personnel", "keyPersonnel", "representative", "contact_name"]
        }
    
    def extract_nested_fields(self, obj: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """
        Extract all nested fields with their full paths
        """
        fields = {}
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                # Recursively extract nested fields
                nested_fields = self.extract_nested_fields(value, current_path)
                fields.update(nested_fields)
            else:
                # Store leaf field
                fields[current_path] = value
        
        return fields
    
    def find_semantic_match(self, field_name: str, target_fields: List[str]) -> tuple:
        """
        Find the best semantic match for a field
        """
        field_lower = field_name.lower()
        best_match = None
        best_score = 0
        
        for target_field in target_fields:
            target_lower = target_field.lower()
            
            # Check semantic patterns
            for pattern_category, patterns in self.semantic_patterns.items():
                if any(pattern in field_lower for pattern in patterns) and any(pattern in target_lower for pattern in patterns):
                    score = 0.9  # High score for semantic match
                    if score > best_score:
                        best_score = score
                        best_match = target_field
                        break
            
            # If no semantic match, try fuzzy matching
            if not best_match:
                similarity = SequenceMatcher(None, field_lower, target_lower).ratio()
                if similarity > best_score and similarity > 0.7:
                    best_score = similarity
                    best_match = target_field
        
        return best_match, best_score
    
    def transform_json(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform source JSON to target structure using semantic matching
        """
        try:
            # Extract all fields from source
            source_fields = self.extract_nested_fields(source_json)
            
            # Create target structure template
            target_structure = self._create_target_structure()
            
            # Extract target field paths
            target_fields = list(self.extract_nested_fields(target_structure).keys())
            
            # Map source fields to target fields
            mappings = {}
            for source_path, source_value in source_fields.items():
                source_field = source_path.split('.')[-1]
                best_match, score = self.find_semantic_match(source_field, target_fields)
                
                if best_match and score > 0.7:
                    mappings[source_path] = {
                        'target_path': best_match,
                        'value': source_value,
                        'confidence': score
                    }
            
            # Apply mappings to create target JSON
            target_json = self._apply_mappings(target_structure, mappings)
            
            self.logger.info(f"Mapped {len(mappings)} fields out of {len(source_fields)} source fields")
            
            return target_json
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON: {e}")
            raise
    
    def _create_target_structure(self) -> Dict[str, Any]:
        """
        Create the target JSON structure template
        """
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
    
    def _apply_mappings(self, template: Dict[str, Any], mappings: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Apply mappings to template to create final JSON
        """
        result = json.loads(json.dumps(template))  # Deep copy
        
        for source_path, mapping_info in mappings.items():
            target_path = mapping_info['target_path']
            value = mapping_info['value']
            
            # Set value in result using target path
            self._set_nested_value(result, target_path, value)
        
        return result
    
    def _set_nested_value(self, obj: Dict[str, Any], path: str, value: Any):
        """
        Set value in nested object using dot notation path
        """
        parts = path.split('.')
        current = obj
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    def add_semantic_pattern(self, category: str, patterns: List[str]):
        """
        Add new semantic patterns dynamically
        """
        if category not in self.semantic_patterns:
            self.semantic_patterns[category] = []
        
        self.semantic_patterns[category].extend(patterns)
        self.logger.info(f"Added {len(patterns)} patterns to category '{category}'")
    
    def get_mapping_summary(self, source_json: Dict[str, Any], target_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a summary of the mapping process
        """
        source_fields = self.extract_nested_fields(source_json)
        target_fields = self.extract_nested_fields(target_json)
        
        return {
            'source_field_count': len(source_fields),
            'target_field_count': len(target_fields),
            'source_fields': list(source_fields.keys()),
            'target_fields': list(target_fields.keys())
        } 