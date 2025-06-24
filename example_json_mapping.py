import json
import logging
from typing import Dict, Any, List
from difflib import SequenceMatcher

class DynamicJsonMapper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Semantic patterns - can be easily extended
        self.semantic_patterns = {
            "name": ["name", "legal_name", "entity_name", "company_name"],
            "city": ["city", "town", "municipality"],
            "state": ["state", "province", "region"],
            "zip": ["zip", "zip_code", "postal_code"],
            "address": ["address", "street", "street_address"],
            "email": ["email", "emailId", "email_address"],
            "phone": ["phone", "contact", "contactNo", "contact_no"],
            "personnel": ["personnel", "keyPersonnel", "representative"]
        }
    
    def extract_fields(self, obj: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Extract all nested fields with paths"""
        fields = {}
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                nested_fields = self.extract_fields(value, current_path)
                fields.update(nested_fields)
            else:
                fields[current_path] = value
        
        return fields
    
    def find_semantic_match(self, field_name: str, target_fields: List[str]) -> tuple:
        """Find best semantic match"""
        field_lower = field_name.lower()
        best_match = None
        best_score = 0
        
        for target_field in target_fields:
            target_lower = target_field.lower()
            
            # Check semantic patterns
            for category, patterns in self.semantic_patterns.items():
                if any(pattern in field_lower for pattern in patterns) and any(pattern in target_lower for pattern in patterns):
                    return target_field, 0.9
            
            # Fuzzy matching
            similarity = SequenceMatcher(None, field_lower, target_lower).ratio()
            if similarity > best_score and similarity > 0.7:
                best_score = similarity
                best_match = target_field
        
        return best_match, best_score
    
    def transform_json(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """Transform source JSON to target structure"""
        try:
            # Extract payload from source
            source_payload = self._extract_payload(source_json)
            source_fields = self.extract_fields(source_payload)
            
            # Create target structure
            target_structure = self._create_target_structure()
            target_fields = list(self.extract_fields(target_structure).keys())
            
            # Map fields
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
            
            # Apply mappings
            result = self._apply_mappings(target_structure, mappings)
            
            print(f"Mapped {len(mappings)} fields out of {len(source_fields)} source fields")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON: {e}")
            raise
    
    def _extract_payload(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extract payload from source JSON"""
        for key, value in source_json.items():
            if isinstance(value, dict) and 'payload' in value:
                return value['payload']
        return source_json.get('payload', {})
    
    def _create_target_structure(self) -> Dict[str, Any]:
        """Create target JSON structure"""
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
                        }
                    }
                }
            }
        }
    
    def _apply_mappings(self, template: Dict[str, Any], mappings: Dict[str, Dict]) -> Dict[str, Any]:
        """Apply mappings to template"""
        result = json.loads(json.dumps(template))
        
        for source_path, mapping_info in mappings.items():
            target_path = mapping_info['target_path']
            value = mapping_info['value']
            self._set_nested_value(result, target_path, value)
        
        return result
    
    def _set_nested_value(self, obj: Dict[str, Any], path: str, value: Any):
        """Set value in nested object"""
        parts = path.split('.')
        current = obj
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value

# Example usage
if __name__ == "__main__":
    # Source JSON (your input)
    source_json = {
        "1": {
            "payload": {
                "name": {
                    "legal_name": "Saumya",
                    "alternate_legal_name": "Patra"
                },
                "registered_agent": {
                    "Address": {
                        "city": "Pune",
                        "state": 1,
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
                }
            }
        }
    }
    
    # Create mapper and transform
    mapper = DynamicJsonMapper()
    result = mapper.transform_json(source_json)
    
    print("Transformed JSON:")
    print(json.dumps(result, indent=2)) 