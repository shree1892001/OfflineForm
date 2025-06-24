import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.CallAiService import CallAiService

class EnhancedJsonMapper:
    """
    Enhanced JSON mapper with support for various naming conventions and patterns
    including capitalized keys, prefix mappings, and semantic matching
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_service = JsonMappingDatabaseService(config)
        self.ai_service = CallAiService(config)
        self.logger = logging.getLogger(__name__)
        
        # Define naming convention patterns
        self.naming_patterns = {
            'snake_case': r'^[a-z][a-z0-9_]*$',
            'camel_case': r'^[a-z][a-zA-Z0-9]*$',
            'pascal_case': r'^[A-Z][a-zA-Z0-9]*$',
            'kebab_case': r'^[a-z][a-z0-9-]*$',
            'upper_snake': r'^[A-Z][A-Z0-9_]*$',
            'mixed_case': r'^[A-Z][a-z]+[A-Z][a-zA-Z0-9]*$'
        }
        
        # Define common field prefixes and their mappings
        self.field_prefixes = {
            'CD_': ['legal_name', 'Legal_Name', 'entity_name', 'Entity_Name', 'company_name', 'Company_Name'],
            'PA_': ['principal_address', 'Principal_Address', 'address', 'Address'],
            'RA_': ['registered_agent', 'Registered_Agent', 'agent', 'Agent'],
            'Org_': ['organizer', 'Organizer', 'organizer_information', 'Organizer_Information'],
            'Contact_': ['contact', 'Contact', 'contact_information', 'Contact_Information'],
            'Billing_': ['billing', 'Billing', 'billing_information', 'Billing_Information'],
            'Mailing_': ['mailing', 'Mailing', 'mailing_information', 'Mailing_Information']
        }
        
        # Define semantic field mappings
        self.semantic_mappings = {
            'legal_name': ['CD_Legal_Name', 'CD_LLC_Name', 'CD_Corp_Name', 'CD_Entity_Name'],
            'alternate_legal_name': ['CD_Alternate_Legal_Name', 'CD_DBA_Name', 'CD_Trade_Name'],
            'entity_name': ['CD_Entity_Name', 'CD_LLC_Name', 'CD_Corp_Name'],
            'company_name': ['CD_Company_Name', 'CD_Legal_Name', 'CD_Entity_Name'],
            'business_name': ['CD_Business_Name', 'CD_Legal_Name', 'CD_Entity_Name'],
            'city': ['PA_City', 'RA_City', 'Org_City', 'Billing_City', 'Mailing_City'],
            'state': ['PA_State', 'RA_State', 'Org_State', 'Billing_State', 'Mailing_State'],
            'zip_code': ['PA_Postal_Code', 'RA_Postal_Code', 'Org_Postal_Code', 'Billing_Postal_Code'],
            'street_address': ['PA_Address_Line1', 'RA_Address_Line1', 'Org_Address_Line1'],
            'address_line2': ['PA_Address_Line2', 'RA_Address_Line2', 'Org_Address_Line2'],
            'email': ['Contact_Email', 'RA_Email', 'Org_Email', 'Billing_Email'],
            'contact_no': ['Contact_Phone', 'RA_Phone', 'Org_Phone', 'Billing_Phone'],
            'personnel_name': ['RA_Name', 'Org_Name', 'Contact_Name', 'Billing_Name']
        }
    
    def detect_naming_convention(self, field_name: str) -> str:
        """Detect the naming convention of a field"""
        for convention, pattern in self.naming_patterns.items():
            if re.match(pattern, field_name):
                return convention
        return 'unknown'
    
    def normalize_field_name(self, field_name: str, target_convention: str = 'pascal_case') -> str:
        """Normalize field name to target convention"""
        # Remove common prefixes first
        clean_name = field_name
        for prefix in self.field_prefixes.keys():
            if field_name.startswith(prefix):
                clean_name = field_name[len(prefix):]
                break
        
        # Convert to target convention
        if target_convention == 'pascal_case':
            # Convert snake_case to PascalCase
            if '_' in clean_name:
                return ''.join(word.title() for word in clean_name.split('_'))
            # Convert camelCase to PascalCase
            elif clean_name and clean_name[0].islower():
                return clean_name[0].upper() + clean_name[1:]
            else:
                return clean_name
        elif target_convention == 'snake_case':
            # Convert PascalCase to snake_case
            return re.sub(r'([A-Z])', r'_\1', clean_name).lower().lstrip('_')
        
        return clean_name
    
    def find_semantic_match(self, source_field: str, target_fields: List[str]) -> Optional[str]:
        """Find semantic match for a source field among target fields"""
        source_normalized = self.normalize_field_name(source_field, 'snake_case')
        
        # Check direct semantic mappings
        if source_normalized in self.semantic_mappings:
            for target_candidate in self.semantic_mappings[source_normalized]:
                if target_candidate in target_fields:
                    return target_candidate
        
        # Check prefix-based mappings
        for prefix, field_types in self.field_prefixes.items():
            if any(field_type in source_normalized for field_type in field_types):
                for field_type in field_types:
                    if field_type in source_normalized:
                        # Try to find matching target field with prefix
                        for target_field in target_fields:
                            if target_field.startswith(prefix) and field_type.replace('_', '').lower() in target_field.lower():
                                return target_field
        
        # Fuzzy matching based on similarity
        best_match = None
        best_score = 0.0
        
        for target_field in target_fields:
            target_normalized = self.normalize_field_name(target_field, 'snake_case')
            similarity = self.calculate_similarity(source_normalized, target_normalized)
            if similarity > best_score and similarity > 0.7:
                best_score = similarity
                best_match = target_field
        
        return best_match
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        # Simple Jaccard similarity
        set1 = set(str1.lower())
        set2 = set(str2.lower())
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def extract_all_field_paths(self, obj: Dict[str, Any], prefix: str = "") -> List[Tuple[str, Any]]:
        """Extract all field paths from JSON object"""
        paths = []
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                nested_paths = self.extract_all_field_paths(value, current_path)
                paths.extend(nested_paths)
            else:
                paths.append((current_path, value))
        
        return paths
    
    def create_mapping_rules(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> List[Dict]:
        """Create mapping rules between source and target JSONs"""
        source_fields = self.extract_all_field_paths(source_json)
        target_fields = self.extract_all_field_paths(target_template)
        
        target_field_names = [path.split('.')[-1] for path, _ in target_fields]
        
        mappings = []
        
        for source_path, source_value in source_fields:
            source_field_name = source_path.split('.')[-1]
            
            # Find semantic match
            target_field = self.find_semantic_match(source_field_name, target_field_names)
            
            if target_field:
                # Find the full target path
                target_path = None
                for path, _ in target_fields:
                    if path.split('.')[-1] == target_field:
                        target_path = path
                        break
                
                if target_path:
                    mappings.append({
                        'source_path': source_path,
                        'target_path': target_path,
                        'source_field': source_field_name,
                        'target_field': target_field,
                        'confidence': 0.9,
                        'mapping_type': 'semantic'
                    })
        
        return mappings
    
    def transform_json_with_enhanced_mapping(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> Dict[str, Any]:
        """Transform source JSON to target structure using enhanced mapping"""
        try:
            # Get database mappings first
            db_mappings = self.db_service.get_all_json_mappings()
            
            # Create dynamic mappings for unmapped fields
            dynamic_mappings = self.create_mapping_rules(source_json, target_template)
            
            # Combine mappings
            all_mappings = []
            
            # Add database mappings
            for db_mapping in db_mappings:
                all_mappings.append({
                    'source_path': db_mapping.source_path,
                    'target_path': db_mapping.target_path,
                    'confidence': db_mapping.confidence,
                    'mapping_type': 'database'
                })
            
            # Add dynamic mappings for unmapped fields
            mapped_source_paths = {m['source_path'] for m in all_mappings}
            for dynamic_mapping in dynamic_mappings:
                if dynamic_mapping['source_path'] not in mapped_source_paths:
                    all_mappings.append(dynamic_mapping)
            
            # Apply mappings
            result = self._apply_mappings_to_template(target_template, all_mappings, source_json)
            
            self.logger.info(f"Enhanced JSON mapping completed with {len(all_mappings)} mappings")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON with enhanced mapping: {e}")
            raise
    
    def _apply_mappings_to_template(self, template: Dict[str, Any], mappings: List[Dict], 
                                  source_json: Dict[str, Any]) -> Dict[str, Any]:
        """Apply mappings to template"""
        result = json.loads(json.dumps(template))  # Deep copy
        
        for mapping in mappings:
            try:
                source_path = mapping['source_path']
                target_path = mapping['target_path']
                
                # Get value from source
                source_value = self._get_value_by_path(source_json, source_path)
                
                if source_value is not None:
                    # Set value in target
                    self._set_value_by_path(result, target_path, source_value)
                    
                    self.logger.debug(f"Mapped {source_path} -> {target_path}: {source_value}")
                    
            except Exception as e:
                self.logger.warning(f"Failed to apply mapping {mapping.get('source_path', '')} -> {mapping.get('target_path', '')}: {e}")
        
        return result
    
    def _get_value_by_path(self, obj: Dict[str, Any], path: str) -> Any:
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
    
    def _set_value_by_path(self, obj: Dict[str, Any], path: str, value: Any):
        """Set value in object using dot notation path"""
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
    
    def add_custom_mapping(self, source_field: str, target_field: str, 
                          semantic_meaning: str = "", field_type: str = "string"):
        """Add a custom mapping to the database"""
        try:
            self.db_service.add_json_mapping(
                source_path=source_field,
                target_path=target_field,
                semantic_meaning=semantic_meaning or f"Custom mapping: {source_field} -> {target_field}",
                field_type=field_type,
                data_type="str",
                confidence=1.0,
                reasoning=f"Custom mapping for {source_field} to {target_field}",
                is_required=False,
                validation_rules=[],
                mapping_strategy="custom"
            )
            self.logger.info(f"Added custom mapping: {source_field} -> {target_field}")
            
        except Exception as e:
            self.logger.error(f"Failed to add custom mapping: {e}")
            raise
    
    def get_mapping_report(self, source_json: Dict[str, Any], target_json: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive mapping report"""
        source_fields = self.extract_all_field_paths(source_json)
        target_fields = self.extract_all_field_paths(target_json)
        
        mappings = self.create_mapping_rules(source_json, target_json)
        
        return {
            'total_source_fields': len(source_fields),
            'total_target_fields': len(target_fields),
            'mapped_fields': len(mappings),
            'mapping_accuracy': len(mappings) / len(source_fields) if source_fields else 0,
            'mappings': mappings,
            'unmapped_source_fields': [
                path for path, _ in source_fields 
                if not any(m['source_path'] == path for m in mappings)
            ],
            'unmapped_target_fields': [
                path for path, _ in target_fields 
                if not any(m['target_path'] == path for m in mappings)
            ]
        } 