import json
import logging
from typing import Dict, Any, List, Tuple
from difflib import SequenceMatcher
import re

class DynamicJsonMapper:
    def __init__(self, config: Dict):
        """
        Initialize dynamic JSON mapper
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def create_semantic_mapping_rules(self) -> Dict[str, List[str]]:
        """
        Create semantic mapping rules based on common patterns
        """
        return {
            "legal_name": ["legal_name", "legalname", "entity_name", "company_name", "business_name", "name"],
            "alternate_name": ["alternate_legal_name", "alternate_name", "dba", "doing_business_as", "trade_name"],
            "city": ["city", "town", "municipality"],
            "state": ["state", "province", "region"],
            "zip_code": ["zip_code", "zipcode", "postal_code", "postalcode", "zip"],
            "street_address": ["street_address", "address_line1", "addressline1", "street", "address"],
            "address_line2": ["address_line2", "addressline2", "address_line_2", "suite", "unit"],
            "email": ["email", "emailId", "email_address", "emailaddress", "e_mail"],
            "contact_number": ["contactNo", "contact_no", "contact_number", "phone", "telephone", "mobile"],
            "personnel_name": ["keyPersonnelName", "personnel_name", "contact_name", "representative_name"],
            "country": ["country", "nation"],
            "county": ["county", "district", "parish"]
        }
    
    def extract_field_paths(self, obj: Dict[str, Any], prefix: str = "") -> List[Tuple[str, Any]]:
        """
        Recursively extract all field paths from a JSON object
        """
        paths = []
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                # Recursively extract paths from nested objects
                nested_paths = self.extract_field_paths(value, current_path)
                paths.extend(nested_paths)
            else:
                # Add leaf node
                paths.append((current_path, value))
        
        return paths
    
    def calculate_semantic_similarity(self, field_name: str, semantic_patterns: List[str]) -> float:
        """
        Calculate semantic similarity between field name and patterns
        """
        field_lower = field_name.lower()
        max_similarity = 0.0
        
        for pattern in semantic_patterns:
            # Direct match
            if field_lower == pattern.lower():
                return 1.0
            
            # Partial match
            if pattern.lower() in field_lower or field_lower in pattern.lower():
                similarity = 0.8
            else:
                # Use sequence matcher for fuzzy matching
                similarity = SequenceMatcher(None, field_lower, pattern.lower()).ratio()
            
            max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def find_best_matches(self, source_fields: List[Tuple[str, Any]], target_fields: List[Tuple[str, Any]], 
                         semantic_rules: Dict[str, List[str]], threshold: float = 0.6) -> List[Dict]:
        """
        Find best semantic matches between source and target fields
        """
        matches = []
        
        for source_path, source_value in source_fields:
            best_match = None
            best_similarity = 0.0
            
            for target_path, target_value in target_fields:
                # Extract field name from path
                source_field = source_path.split('.')[-1]
                target_field = target_path.split('.')[-1]
                
                # Check semantic similarity for each category
                for semantic_category, patterns in semantic_rules.items():
                    source_similarity = self.calculate_semantic_similarity(source_field, patterns)
                    target_similarity = self.calculate_semantic_similarity(target_field, patterns)
                    
                    # Combined similarity
                    combined_similarity = (source_similarity + target_similarity) / 2
                    
                    if combined_similarity > best_similarity and combined_similarity >= threshold:
                        best_similarity = combined_similarity
                        best_match = {
                            'source_path': source_path,
                            'target_path': target_path,
                            'semantic_category': semantic_category,
                            'similarity_score': combined_similarity,
                            'source_value': source_value
                        }
            
            if best_match:
                matches.append(best_match)
        
        return matches
    
    def transform_json_dynamically(self, source_json: Dict[str, Any], target_template: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Transform source JSON to target structure using dynamic semantic matching
        """
        try:
            # Extract all field paths from source
            source_fields = self.extract_field_paths(source_json)
            
            # If no target template provided, create a flat structure
            if target_template is None:
                target_template = self._create_flat_target_structure(source_fields)
            
            # Extract all field paths from target template
            target_fields = self.extract_field_paths(target_template)
            
            # Get semantic mapping rules
            semantic_rules = self.create_semantic_mapping_rules()
            
            # Find best matches
            matches = self.find_best_matches(source_fields, target_fields, semantic_rules)
            
            # Create target JSON
            target_json = self._create_target_json(target_template, matches)
            
            self.logger.info(f"Found {len(matches)} semantic matches")
            
            return target_json
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON dynamically: {e}")
            raise
    
    def _create_flat_target_structure(self, source_fields: List[Tuple[str, Any]]) -> Dict[str, Any]:
        """
        Create a flat target structure based on source fields
        """
        target = {}
        
        for path, value in source_fields:
            # Convert path to target format
            target_path = self._convert_path_format(path)
            self._set_nested_value(target, target_path, None)  # Set placeholder value
        
        return target
    
    def _convert_path_format(self, path: str) -> str:
        """
        Convert source path format to target format
        """
        # Example: "payload.name.legal_name" -> "data.Payload.Name.CD_Legal_Name"
        parts = path.split('.')
        
        # Apply conversion rules
        converted_parts = []
        for part in parts:
            # Convert to title case and add prefixes based on context
            if part == "payload":
                converted_parts.append("data.Payload")
            elif part == "name":
                converted_parts.append("Name")
            elif part == "legal_name":
                converted_parts.append("CD_Legal_Name")
            elif part == "registered_agent":
                converted_parts.append("Registered_Agent")
            elif part == "principal_address":
                converted_parts.append("Principal_Address")
            elif part == "organizer_information":
                converted_parts.append("Organizer_Information")
            else:
                # Generic conversion
                converted_part = part.replace('_', ' ').title().replace(' ', '_')
                converted_parts.append(converted_part)
        
        return '.'.join(converted_parts)
    
    def _set_nested_value(self, obj: Dict[str, Any], path: str, value: Any):
        """
        Set value in nested object using dot notation
        """
        parts = path.split('.')
        current = obj
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    def _create_target_json(self, template: Dict[str, Any], matches: List[Dict]) -> Dict[str, Any]:
        """
        Create target JSON using template and matches
        """
        target_json = json.loads(json.dumps(template))  # Deep copy
        
        for match in matches:
            target_path = match['target_path']
            source_value = match['source_value']
            
            # Set value in target JSON
            self._set_nested_value(target_json, target_path, source_value)
        
        return target_json
    
    def get_mapping_report(self, source_json: Dict[str, Any], target_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a mapping report showing what was mapped
        """
        source_fields = self.extract_field_paths(source_json)
        target_fields = self.extract_field_paths(target_json)
        semantic_rules = self.create_semantic_mapping_rules()
        matches = self.find_best_matches(source_fields, target_fields, semantic_rules)
        
        return {
            'total_source_fields': len(source_fields),
            'total_target_fields': len(target_fields),
            'mapped_fields': len(matches),
            'mapping_accuracy': len(matches) / len(source_fields) if source_fields else 0,
            'matches': matches,
            'unmapped_source_fields': [path for path, _ in source_fields if not any(m['source_path'] == path for m in matches)]
        } 