#!/usr/bin/env python3
"""
Scalable Mapping System
A configuration-driven approach to JSON mapping that scales automatically
"""

import json
import logging
import re
import yaml
from typing import Dict, Any, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.CallAiService import CallAiService

@dataclass
class MappingTemplate:
    """Template for generating mappings"""
    name: str
    description: str
    source_patterns: List[str]
    target_template: str
    field_type: str
    semantic_meaning: str
    validation_rules: List[str]
    synonyms: List[str]
    priority: int
    is_required: bool
    data_type: str

@dataclass
class MappingRule:
    """Rule for mapping generation"""
    condition: str
    action: str
    parameters: Dict[str, Any]
    priority: int

class ScalableMappingSystem:
    """
    A scalable, configuration-driven mapping system
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.json_db_service = JsonMappingDatabaseService(config)
        self.ai_service = CallAiService(config)
        self.logger = logging.getLogger(__name__)
        
        # Load configuration files
        self.mapping_templates = self._load_mapping_templates()
        self.mapping_rules = self._load_mapping_rules()
        self.field_definitions = self._load_field_definitions()
        
    def _load_mapping_templates(self) -> List[MappingTemplate]:
        """Load mapping templates from configuration"""
        templates = []
        
        # Define templates in code (can be moved to YAML files later)
        template_definitions = [
            {
                "name": "entity_type_mapping",
                "description": "Map entity type fields",
                "source_patterns": [
                    r"EntityType\.(\w+)",
                    r"entity_type\.(\w+)",
                    r"type\.(\w+)"
                ],
                "target_template": "data.EntityType.{field}",
                "field_type": "name",
                "semantic_meaning": "entity_type",
                "validation_rules": [],
                "synonyms": ["entity_type", "type", "EntityType"],
                "priority": 1,
                "is_required": True,
                "data_type": "str"
            },
            {
                "name": "state_mapping",
                "description": "Map state information fields",
                "source_patterns": [
                    r"State\.(\w+)",
                    r"state\.(\w+)",
                    r"state_info\.(\w+)"
                ],
                "target_template": "data.State.{field}",
                "field_type": "name",
                "semantic_meaning": "state_info",
                "validation_rules": [],
                "synonyms": ["state", "State", "state_info"],
                "priority": 1,
                "is_required": True,
                "data_type": "str"
            },
            {
                "name": "name_mapping",
                "description": "Map name fields",
                "source_patterns": [
                    r"name\.(\w+)",
                    r"Name\.(\w+)",
                    r"legal_name\.(\w+)",
                    r"legalName\.(\w+)"
                ],
                "target_template": "data.Payload.Name.{field}",
                "field_type": "name",
                "semantic_meaning": "legal_name",
                "validation_rules": [r'^[a-zA-Z\s]+$'],
                "synonyms": ["name", "Name", "legal_name", "legalName"],
                "priority": 1,
                "is_required": True,
                "data_type": "str"
            },
            {
                "name": "contact_mapping",
                "description": "Map contact information fields",
                "source_patterns": [
                    r"contact\.(\w+)",
                    r"Contact\.(\w+)",
                    r"email\.(\w+)",
                    r"phone\.(\w+)"
                ],
                "target_template": "data.Payload.Contact_Information.{field}",
                "field_type": "contact",
                "semantic_meaning": "contact",
                "validation_rules": [],
                "synonyms": ["contact", "Contact", "email", "phone"],
                "priority": 1,
                "is_required": False,
                "data_type": "str"
            },
            {
                "name": "address_mapping",
                "description": "Map address fields",
                "source_patterns": [
                    r"address\.(\w+)",
                    r"Address\.(\w+)",
                    r"street\.(\w+)",
                    r"city\.(\w+)",
                    r"zip\.(\w+)"
                ],
                "target_template": "data.Payload.Address.{field}",
                "field_type": "address",
                "semantic_meaning": "address",
                "validation_rules": [],
                "synonyms": ["address", "Address", "street", "city", "zip"],
                "priority": 1,
                "is_required": False,
                "data_type": "str"
            }
        ]
        
        for template_def in template_definitions:
            templates.append(MappingTemplate(**template_def))
        
        return templates
    
    def _load_mapping_rules(self) -> List[MappingRule]:
        """Load mapping rules from configuration"""
        rules = []
        
        # Define rules in code (can be moved to YAML files later)
        rule_definitions = [
            {
                "condition": "field_contains_name",
                "action": "apply_name_template",
                "parameters": {"template": "name_mapping"},
                "priority": 1
            },
            {
                "condition": "field_contains_contact",
                "action": "apply_contact_template",
                "parameters": {"template": "contact_mapping"},
                "priority": 1
            },
            {
                "condition": "field_contains_address",
                "action": "apply_address_template",
                "parameters": {"template": "address_mapping"},
                "priority": 1
            },
            {
                "condition": "field_contains_entity_type",
                "action": "apply_entity_type_template",
                "parameters": {"template": "entity_type_mapping"},
                "priority": 1
            }
        ]
        
        for rule_def in rule_definitions:
            rules.append(MappingRule(**rule_def))
        
        return rules
    
    def _load_field_definitions(self) -> Dict[str, Dict]:
        """Load field definitions for automatic type detection"""
        return {
            "name_fields": {
                "patterns": [r"name", r"Name", r"legal_name", r"legalName"],
                "data_type": "str",
                "field_type": "name",
                "validation": [r'^[a-zA-Z\s]+$']
            },
            "email_fields": {
                "patterns": [r"email", r"Email", r"emailId"],
                "data_type": "str",
                "field_type": "email",
                "validation": [r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$']
            },
            "phone_fields": {
                "patterns": [r"phone", r"Phone", r"contact", r"Contact"],
                "data_type": "str",
                "field_type": "phone",
                "validation": [r'^\d+$']
            },
            "numeric_fields": {
                "patterns": [r"id", r"Id", r"code", r"Code", r"number", r"Number"],
                "data_type": "int",
                "field_type": "numeric",
                "validation": [r'^\d+$']
            },
            "address_fields": {
                "patterns": [r"address", r"Address", r"street", r"city", r"zip"],
                "data_type": "str",
                "field_type": "address",
                "validation": [r'^[a-zA-Z0-9\s\.,\-]+$']
            }
        }
    
    def generate_mappings(self, source_json: Dict[str, Any], target_schema: Optional[Dict] = None) -> List[Dict]:
        """
        Generate mappings using the scalable system
        """
        try:
            # Extract all fields from source JSON
            source_fields = self._extract_all_fields(source_json)
            
            # Generate mappings using templates and rules
            mappings = []
            
            for field_path in source_fields:
                # Apply mapping rules
                mapping = self._apply_mapping_rules(field_path, source_json)
                if mapping:
                    mappings.append(mapping)
                else:
                    # Fallback to template matching
                    mapping = self._apply_template_matching(field_path, source_json)
                    if mapping:
                        mappings.append(mapping)
            
            # If target schema provided, enhance mappings
            if target_schema:
                mappings = self._enhance_with_target_schema(mappings, target_schema)
            
            self.logger.info(f"Generated {len(mappings)} mappings using scalable system")
            return mappings
            
        except Exception as e:
            self.logger.error(f"Failed to generate mappings: {e}")
            return []
    
    def _extract_all_fields(self, json_obj: Dict[str, Any], prefix: str = "") -> Set[str]:
        """Extract all field paths from JSON object"""
        fields = set()
        
        def extract_recursive(obj, current_path):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    
                    if isinstance(value, (dict, list)):
                        extract_recursive(value, new_path)
                    else:
                        fields.add(new_path)
                        
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{current_path}[{i}]"
                    extract_recursive(item, new_path)
        
        extract_recursive(json_obj, prefix)
        return fields
    
    def _apply_mapping_rules(self, field_path: str, source_json: Dict) -> Optional[Dict]:
        """Apply mapping rules to field"""
        try:
            for rule in sorted(self.mapping_rules, key=lambda x: x.priority):
                if self._evaluate_condition(rule.condition, field_path, source_json):
                    return self._execute_action(rule.action, field_path, source_json, rule.parameters)
            return None
        except Exception as e:
            self.logger.warning(f"Failed to apply mapping rule for {field_path}: {e}")
            return None
    
    def _evaluate_condition(self, condition: str, field_path: str, source_json: Dict) -> bool:
        """Evaluate mapping rule condition"""
        try:
            if condition == "field_contains_name":
                return any(pattern in field_path.lower() for pattern in ["name", "legal"])
            elif condition == "field_contains_contact":
                return any(pattern in field_path.lower() for pattern in ["contact", "email", "phone"])
            elif condition == "field_contains_address":
                return any(pattern in field_path.lower() for pattern in ["address", "street", "city", "zip"])
            elif condition == "field_contains_entity_type":
                return any(pattern in field_path.lower() for pattern in ["entity", "type"])
            return False
        except Exception:
            return False
    
    def _execute_action(self, action: str, field_path: str, source_json: Dict, parameters: Dict) -> Optional[Dict]:
        """Execute mapping rule action"""
        try:
            if action == "apply_name_template":
                return self._apply_template(field_path, "name_mapping", source_json)
            elif action == "apply_contact_template":
                return self._apply_template(field_path, "contact_mapping", source_json)
            elif action == "apply_address_template":
                return self._apply_template(field_path, "address_mapping", source_json)
            elif action == "apply_entity_type_template":
                return self._apply_template(field_path, "entity_type_mapping", source_json)
            return None
        except Exception as e:
            self.logger.warning(f"Failed to execute action {action}: {e}")
            return None
    
    def _apply_template_matching(self, field_path: str, source_json: Dict) -> Optional[Dict]:
        """Apply template matching to field"""
        try:
            for template in self.mapping_templates:
                for pattern in template.source_patterns:
                    if re.match(pattern, field_path):
                        return self._create_mapping_from_template(field_path, template, source_json)
            return None
        except Exception as e:
            self.logger.warning(f"Failed to apply template matching for {field_path}: {e}")
            return None
    
    def _apply_template(self, field_path: str, template_name: str, source_json: Dict) -> Optional[Dict]:
        """Apply specific template to field"""
        try:
            template = next((t for t in self.mapping_templates if t.name == template_name), None)
            if template:
                return self._create_mapping_from_template(field_path, template, source_json)
            return None
        except Exception as e:
            self.logger.warning(f"Failed to apply template {template_name}: {e}")
            return None
    
    def _create_mapping_from_template(self, field_path: str, template: MappingTemplate, source_json: Dict) -> Dict:
        """Create mapping from template"""
        try:
            # Extract field name from path
            field_name = self._extract_field_name(field_path)
            
            # Generate target path
            target_path = template.target_template.format(field=field_name)
            
            # Determine field type and data type
            field_type, data_type = self._determine_field_type(field_name)
            
            # Create mapping
            mapping = {
                "source_path": field_path,
                "target_path": target_path,
                "semantic_meaning": template.semantic_meaning,
                "field_type": field_type,
                "data_type": data_type,
                "confidence": 0.9,
                "reasoning": f"Generated using template: {template.description}",
                "is_required": template.is_required,
                "validation_rules": template.validation_rules,
                "mapping_strategy": "template_based",
                "priority": template.priority
            }
            
            return mapping
            
        except Exception as e:
            self.logger.warning(f"Failed to create mapping from template: {e}")
            return None
    
    def _extract_field_name(self, field_path: str) -> str:
        """Extract field name from path"""
        return field_path.split('.')[-1]
    
    def _determine_field_type(self, field_name: str) -> Tuple[str, str]:
        """Determine field type and data type"""
        for field_type, definition in self.field_definitions.items():
            for pattern in definition["patterns"]:
                if re.search(pattern, field_name, re.IGNORECASE):
                    return definition["field_type"], definition["data_type"]
        
        # Default
        return "unknown", "str"
    
    def _enhance_with_target_schema(self, mappings: List[Dict], target_schema: Dict) -> List[Dict]:
        """Enhance mappings with target schema information"""
        try:
            enhanced_mappings = []
            
            for mapping in mappings:
                # Check if target path exists in schema
                if self._path_exists_in_schema(mapping["target_path"], target_schema):
                    mapping["confidence"] = min(1.0, mapping["confidence"] + 0.1)
                    mapping["reasoning"] += " (target path confirmed in schema)"
                else:
                    mapping["confidence"] = max(0.0, mapping["confidence"] - 0.2)
                    mapping["reasoning"] += " (target path not found in schema)"
                
                enhanced_mappings.append(mapping)
            
            return enhanced_mappings
            
        except Exception as e:
            self.logger.warning(f"Failed to enhance mappings with schema: {e}")
            return mappings
    
    def _path_exists_in_schema(self, path: str, schema: Dict) -> bool:
        """Check if path exists in schema"""
        try:
            keys = path.split('.')
            current = schema
            
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return False
            
            return True
        except Exception:
            return False
    
    def generate_ai_enhanced_mappings(self, source_json: Dict, target_schema: Optional[Dict] = None) -> List[Dict]:
        """Generate AI-enhanced mappings for complex cases"""
        try:
            # Get base mappings
            base_mappings = self.generate_mappings(source_json, target_schema)
            
            # Find unmapped fields
            mapped_source_paths = {m["source_path"] for m in base_mappings}
            source_fields = self._extract_all_fields(source_json)
            unmapped_fields = source_fields - mapped_source_paths
            
            # Generate AI suggestions for unmapped fields
            ai_mappings = []
            for field_path in unmapped_fields:
                ai_mapping = self._generate_ai_suggestion(field_path, source_json, target_schema)
                if ai_mapping:
                    ai_mappings.append(ai_mapping)
            
            # Combine mappings
            all_mappings = base_mappings + ai_mappings
            
            self.logger.info(f"Generated {len(base_mappings)} base + {len(ai_mappings)} AI mappings")
            return all_mappings
            
        except Exception as e:
            self.logger.error(f"Failed to generate AI-enhanced mappings: {e}")
            return []
    
    def _generate_ai_suggestion(self, field_path: str, source_json: Dict, target_schema: Optional[Dict]) -> Optional[Dict]:
        """Generate AI suggestion for unmapped field"""
        try:
            # Create AI prompt
            prompt = self._create_ai_prompt(field_path, source_json, target_schema)
            
            # Get AI response
            ai_response = self.ai_service.call_ai(prompt)
            
            # Parse response
            return self._parse_ai_response(ai_response, field_path)
            
        except Exception as e:
            self.logger.warning(f"Failed to generate AI suggestion for {field_path}: {e}")
            return None
    
    def _create_ai_prompt(self, field_path: str, source_json: Dict, target_schema: Optional[Dict]) -> str:
        """Create AI prompt for mapping suggestion"""
        prompt = f"""
        Suggest a mapping for this JSON field:

        Source Field: {field_path}
        Source Value: {self._get_value_by_path(source_json, field_path)}
        
        Target Schema: {json.dumps(target_schema, indent=2) if target_schema else "Not provided"}
        
        Consider:
        1. Semantic similarity
        2. Business context (entity formation)
        3. Data type compatibility
        4. Field naming conventions
        
        Respond with JSON:
        {{
            "target_path": "suggested.target.path",
            "semantic_meaning": "field_meaning",
            "field_type": "field_type",
            "data_type": "str/int/bool",
            "confidence": 0.0-1.0,
            "reasoning": "explanation",
            "is_required": true/false,
            "validation_rules": ["regex_patterns"]
        }}
        """
        return prompt
    
    def _parse_ai_response(self, ai_response: str, field_path: str) -> Optional[Dict]:
        """Parse AI response into mapping object"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if not json_match:
                return None
            
            ai_suggestion = json.loads(json_match.group())
            
            # Create mapping
            mapping = {
                "source_path": field_path,
                "target_path": ai_suggestion.get("target_path", ""),
                "semantic_meaning": ai_suggestion.get("semantic_meaning", "unknown"),
                "field_type": ai_suggestion.get("field_type", "unknown"),
                "data_type": ai_suggestion.get("data_type", "str"),
                "confidence": ai_suggestion.get("confidence", 0.5),
                "reasoning": ai_suggestion.get("reasoning", "AI suggested mapping"),
                "is_required": ai_suggestion.get("is_required", False),
                "validation_rules": ai_suggestion.get("validation_rules", []),
                "mapping_strategy": "ai_enhanced",
                "priority": 2
            }
            
            return mapping
            
        except Exception as e:
            self.logger.warning(f"Failed to parse AI response: {e}")
            return None
    
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
    
    def save_mappings_to_database(self, mappings: List[Dict]):
        """Save generated mappings to database"""
        try:
            # Clear existing mappings
            self.json_db_service.clear_json_mappings()
            
            # Insert new mappings
            self.json_db_service.insert_json_field_mappings(mappings)
            
            self.logger.info(f"Saved {len(mappings)} mappings to database")
            
        except Exception as e:
            self.logger.error(f"Failed to save mappings to database: {e}")
            raise
    
    def export_mappings_to_config(self, mappings: List[Dict], output_file: str):
        """Export mappings to configuration file"""
        try:
            config_data = {
                "mappings": mappings,
                "generated_at": str(datetime.now()),
                "version": "1.0"
            }
            
            with open(output_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            
            self.logger.info(f"Exported {len(mappings)} mappings to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to export mappings: {e}")
            raise 