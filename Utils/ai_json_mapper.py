import json
import logging
from typing import Dict, Any, List, Tuple
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.CallAiService import CallAiService
import re

class AIJsonMapper:
    """
    AI-driven JSON mapper that uses database mappings and AI enhancement
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.json_db_service = JsonMappingDatabaseService(config)
        self.ai_service = CallAiService(config)
        
    def map_json_with_ai_enhancement(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map source JSON to target structure using database mappings with AI enhancement
        """
        try:
            # Get existing database mappings
            db_mappings = self.json_db_service.get_all_json_mappings()
            
            # Extract source fields
            source_fields = self._extract_all_fields(source_json)
            
            # Extract target fields
            target_fields = self._extract_all_fields(target_template)
            
            # Generate AI-enhanced mappings
            ai_mappings = self._generate_ai_mappings(source_fields, target_fields, db_mappings)
            
            # Combine database and AI mappings
            all_mappings = self._combine_mappings(db_mappings, ai_mappings)
            
            # Apply mappings to create result
            result = self._apply_mappings_to_template(target_template, all_mappings, source_json)
            
            logging.info(f"AI-enhanced JSON mapping completed with {len(all_mappings)} total mappings")
            
            return result
            
        except Exception as e:
            logging.error(f"Failed to map JSON with AI enhancement: {e}")
            raise
    
    def _extract_all_fields(self, json_obj: Dict[str, Any], prefix: str = "") -> List[Dict[str, Any]]:
        """
        Extract all fields from JSON object with their paths and metadata
        """
        fields = []
        
        def extract_recursive(obj, current_path):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    
                    if isinstance(value, (dict, list)):
                        extract_recursive(value, new_path)
                    else:
                        # Extract field metadata
                        field_info = {
                            "path": new_path,
                            "value": value,
                            "data_type": type(value).__name__,
                            "field_name": key,
                            "parent_path": current_path,
                            "is_leaf": True
                        }
                        
                        # Add semantic analysis
                        field_info.update(self._analyze_field_semantics(key, value))
                        fields.append(field_info)
                        
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{current_path}[{i}]"
                    extract_recursive(item, new_path)
        
        extract_recursive(json_obj, prefix)
        return fields
    
    def _analyze_field_semantics(self, field_name: str, value: Any) -> Dict[str, Any]:
        """
        Analyze field semantics based on name and value patterns
        """
        analysis = {
            "semantic_category": "unknown",
            "confidence": 0.0,
            "patterns": [],
            "suggested_meanings": []
        }
        
        # Convert to string for pattern matching
        field_str = str(field_name).lower()
        value_str = str(value).lower() if value is not None else ""
        
        # Name patterns
        name_patterns = {
            "name": [r"name", r"title", r"legal", r"business"],
            "address": [r"address", r"street", r"city", r"state", r"zip", r"postal"],
            "contact": [r"email", r"phone", r"contact", r"tel"],
            "date": [r"date", r"time", r"created", r"updated"],
            "id": [r"id", r"number", r"code", r"reference"]
        }
        
        # Value patterns
        value_patterns = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^\+?[\d\s\-\(\)]+$",
            "zip_code": r"^\d{5}(-\d{4})?$",
            "date": r"^\d{4}-\d{2}-\d{2}$"
        }
        
        # Analyze field name
        for category, patterns in name_patterns.items():
            for pattern in patterns:
                if re.search(pattern, field_str):
                    analysis["semantic_category"] = category
                    analysis["confidence"] = 0.7
                    analysis["patterns"].append(f"name_pattern:{pattern}")
                    break
        
        # Analyze value patterns
        for pattern_name, pattern in value_patterns.items():
            if re.match(pattern, value_str):
                analysis["patterns"].append(f"value_pattern:{pattern_name}")
                if analysis["confidence"] < 0.8:
                    analysis["confidence"] = 0.8
        
        # Generate suggested meanings
        analysis["suggested_meanings"] = self._generate_suggested_meanings(field_name, value)
        
        return analysis
    
    def _generate_suggested_meanings(self, field_name: str, value: Any) -> List[str]:
        """
        Generate suggested semantic meanings for a field
        """
        suggestions = []
        field_lower = field_name.lower()
        
        # Common field mappings
        field_mappings = {
            "legal_name": ["legal_name", "entity_name", "company_name"],
            "alternate_name": ["alternate_name", "dba", "trade_name"],
            "city": ["city", "town", "municipality"],
            "state": ["state", "province", "region"],
            "zip_code": ["zip_code", "postal_code", "zip"],
            "email": ["email", "email_address", "emailId"],
            "contact_number": ["contact_number", "phone", "contactNo"],
            "street_address": ["street_address", "address_line1", "street"],
            "personnel_name": ["personnel_name", "keyPersonnelName", "contact_name"]
        }
        
        for meaning, synonyms in field_mappings.items():
            if any(synonym in field_lower for synonym in synonyms):
                suggestions.append(meaning)
        
        return suggestions
    
    def _generate_ai_mappings(self, source_fields: List[Dict], target_fields: List[Dict], 
                            existing_mappings: List[Dict]) -> List[Dict]:
        """
        Generate AI-enhanced mappings for unmapped fields
        """
        ai_mappings = []
        
        # Find unmapped source fields
        mapped_source_paths = {mapping.get("source_path", "") for mapping in existing_mappings}
        unmapped_source_fields = [f for f in source_fields if f["path"] not in mapped_source_paths]
        
        # Find unmapped target fields
        mapped_target_paths = {mapping.get("target_path", "") for mapping in existing_mappings}
        unmapped_target_fields = [f for f in target_fields if f["path"] not in mapped_target_paths]
        
        if not unmapped_source_fields or not unmapped_target_fields:
            return ai_mappings
        
        # Generate AI prompts for mapping suggestions
        for source_field in unmapped_source_fields:
            for target_field in unmapped_target_fields:
                mapping_suggestion = self._get_ai_mapping_suggestion(source_field, target_field)
                
                if mapping_suggestion and mapping_suggestion["confidence"] > 0.5:
                    ai_mappings.append(mapping_suggestion)
        
        return ai_mappings
    
    def _get_ai_mapping_suggestion(self, source_field: Dict, target_field: Dict) -> Dict:
        """
        Get AI suggestion for mapping between source and target fields
        """
        try:
            # Create AI prompt
            prompt = self._create_mapping_prompt(source_field, target_field)
            
            # Get AI response
            ai_response = self.ai_service.call_ai(prompt)
            
            # Parse AI response
            mapping = self._parse_ai_mapping_response(ai_response, source_field, target_field)
            
            return mapping
            
        except Exception as e:
            logging.warning(f"Failed to get AI mapping suggestion: {e}")
            return None
    
    def _create_mapping_prompt(self, source_field: Dict, target_field: Dict) -> str:
        """
        Create AI prompt for mapping suggestion
        """
        prompt = f"""
        Analyze the semantic similarity between these two JSON fields and suggest if they should be mapped:

        Source Field:
        - Path: {source_field['path']}
        - Name: {source_field['field_name']}
        - Value: {source_field['value']}
        - Data Type: {source_field['data_type']}
        - Semantic Category: {source_field.get('semantic_category', 'unknown')}
        - Suggested Meanings: {source_field.get('suggested_meanings', [])}

        Target Field:
        - Path: {target_field['path']}
        - Name: {target_field['field_name']}
        - Value: {target_field['value']}
        - Data Type: {target_field['data_type']}
        - Semantic Category: {target_field.get('semantic_category', 'unknown')}
        - Suggested Meanings: {target_field.get('suggested_meanings', [])}

        Consider:
        1. Semantic similarity of field names
        2. Data type compatibility
        3. Business context (entity formation)
        4. Value patterns and validation

        Respond with a JSON object containing:
        {{
            "should_map": true/false,
            "confidence": 0.0-1.0,
            "reasoning": "explanation",
            "semantic_meaning": "suggested_meaning",
            "field_type": "suggested_type",
            "validation_rules": ["regex_patterns"],
            "is_required": true/false
        }}
        """
        
        return prompt
    
    def _parse_ai_mapping_response(self, ai_response: str, source_field: Dict, target_field: Dict) -> Dict:
        """
        Parse AI response into mapping object
        """
        try:
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if not json_match:
                return None
            
            ai_suggestion = json.loads(json_match.group())
            
            if not ai_suggestion.get("should_map", False):
                return None
            
            # Create mapping object
            mapping = {
                "source_path": source_field["path"],
                "target_path": target_field["path"],
                "semantic_meaning": ai_suggestion.get("semantic_meaning", "unknown"),
                "field_type": ai_suggestion.get("field_type", "unknown"),
                "data_type": source_field["data_type"],
                "confidence": ai_suggestion.get("confidence", 0.0),
                "reasoning": ai_suggestion.get("reasoning", "AI suggested mapping"),
                "is_required": ai_suggestion.get("is_required", False),
                "validation_rules": ai_suggestion.get("validation_rules", []),
                "mapping_strategy": "ai_enhanced",
                "priority": 2  # Lower priority than database mappings
            }
            
            return mapping
            
        except Exception as e:
            logging.warning(f"Failed to parse AI mapping response: {e}")
            return None
    
    def _combine_mappings(self, db_mappings: List[Dict], ai_mappings: List[Dict]) -> List[Dict]:
        """
        Combine database and AI mappings, prioritizing database mappings
        """
        combined = []
        
        # Add database mappings first (higher priority)
        for mapping in db_mappings:
            combined.append(mapping)
        
        # Add AI mappings, avoiding conflicts
        db_source_paths = {m.get("source_path", "") for m in db_mappings}
        db_target_paths = {m.get("target_path", "") for m in db_mappings}
        
        for ai_mapping in ai_mappings:
            source_path = ai_mapping.get("source_path", "")
            target_path = ai_mapping.get("target_path", "")
            
            # Only add if not conflicting with database mappings
            if source_path not in db_source_paths and target_path not in db_target_paths:
                combined.append(ai_mapping)
        
        return combined
    
    def _apply_mappings_to_template(self, template: Dict[str, Any], mappings: List[Dict], 
                                  source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply mappings to template to create result
        """
        result = json.loads(json.dumps(template))  # Deep copy
        
        for mapping in mappings:
            try:
                source_path = mapping.get("source_path", "")
                target_path = mapping.get("target_path", "")
                
                # Get value from source
                source_value = self._get_value_by_path(source_json, source_path)
                
                if source_value is not None:
                    # Validate value if rules exist
                    if self._validate_value(source_value, mapping.get("validation_rules", [])):
                        # Set value in target
                        self._set_value_by_path(result, target_path, source_value)
                        
                        logging.debug(f"Mapped {source_path} -> {target_path}: {source_value}")
                    else:
                        logging.warning(f"Validation failed for {source_path}: {source_value}")
                        
            except Exception as e:
                logging.warning(f"Failed to apply mapping {mapping.get('source_path', '')} -> {mapping.get('target_path', '')}: {e}")
        
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
            parts = path.split('.')
            current = obj
            
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            current[parts[-1]] = value
            
        except Exception as e:
            logging.error(f"Failed to set value at path {path}: {e}")
    
    def _validate_value(self, value: Any, validation_rules: List[str]) -> bool:
        """Validate value against regex patterns"""
        if not validation_rules:
            return True
        
        value_str = str(value)
        
        for pattern in validation_rules:
            try:
                if not re.match(pattern, value_str):
                    return False
            except Exception:
                continue
        
        return True 