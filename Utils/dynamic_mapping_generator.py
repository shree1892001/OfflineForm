#!/usr/bin/env python3
"""
Dynamic Mapping Generator
Creates scalable, rule-based mappings instead of hardcoded individual mappings
"""

import json
import logging
import re
from typing import Dict, Any, List, Tuple, Set
from dataclasses import dataclass
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.CallAiService import CallAiService

@dataclass
class MappingRule:
    """Represents a mapping rule pattern"""
    pattern: str
    target_template: str
    field_type: str
    semantic_meaning: str
    validation_rules: List[str]
    priority: int
    description: str

@dataclass
class FieldPattern:
    """Represents a field pattern for automatic mapping"""
    source_pattern: str
    target_pattern: str
    field_type: str
    semantic_meaning: str
    synonyms: List[str]
    validation_patterns: List[str]

class DynamicMappingGenerator:
    """
    Generates mappings dynamically based on patterns and rules
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.json_db_service = JsonMappingDatabaseService(config)
        self.ai_service = CallAiService(config)
        self.logger = logging.getLogger(__name__)
        
        # Define mapping patterns for automatic generation
        self.mapping_patterns = self._initialize_mapping_patterns()
        self.field_patterns = self._initialize_field_patterns()
        
    def _initialize_mapping_patterns(self) -> List[MappingRule]:
        """Initialize mapping rules based on patterns"""
        return [
            # Entity Type Patterns
            MappingRule(
                pattern=r"EntityType\.(\w+)",
                target_template="data.EntityType.{field}",
                field_type="name",
                semantic_meaning="entity_type",
                validation_rules=[],
                priority=1,
                description="Entity type field mapping"
            ),
            
            # State Patterns
            MappingRule(
                pattern=r"State\.(\w+)",
                target_template="data.State.{field}",
                field_type="name",
                semantic_meaning="state_info",
                validation_rules=[],
                priority=1,
                description="State information mapping"
            ),
            
            # Country Patterns
            MappingRule(
                pattern=r"State\.countryMaster\.(\w+)",
                target_template="data.State.Country.{field}",
                field_type="name",
                semantic_meaning="country_info",
                validation_rules=[],
                priority=1,
                description="Country information mapping"
            ),
            
            # Name Patterns
            MappingRule(
                pattern=r"name\.(\w+)",
                target_template="data.Payload.Name.{field}",
                field_type="name",
                semantic_meaning="legal_name",
                validation_rules=[r'^[a-zA-Z\s]+$'],
                priority=1,
                description="Entity name mapping"
            ),
            
            # Registered Agent Patterns
            MappingRule(
                pattern=r"registered_agent\.(\w+)",
                target_template="data.Payload.Registered_Agent.{field}",
                field_type="contact",
                semantic_meaning="personnel_name",
                validation_rules=[],
                priority=1,
                description="Registered agent basic field mapping"
            ),
            
            # Registered Agent Address Patterns
            MappingRule(
                pattern=r"registered_agent\.Address\.(\w+)",
                target_template="data.Payload.Registered_Agent.Address.{field}",
                field_type="address",
                semantic_meaning="address",
                validation_rules=[],
                priority=1,
                description="Registered agent address mapping"
            ),
            
            # Registered Agent Billing Patterns
            MappingRule(
                pattern=r"registered_agent\.Billing Information\.(\w+)",
                target_template="data.Payload.Registered_Agent.Billing.{field}",
                field_type="billing",
                semantic_meaning="billing_information",
                validation_rules=[],
                priority=1,
                description="Registered agent billing mapping"
            ),
            
            # Registered Agent Mailing Patterns
            MappingRule(
                pattern=r"registered_agent\.Mailing Information\.(\w+)",
                target_template="data.Payload.Registered_Agent.Mailing.{field}",
                field_type="mailing",
                semantic_meaning="mailing_information",
                validation_rules=[],
                priority=1,
                description="Registered agent mailing mapping"
            ),
            
            # Principal Address Patterns
            MappingRule(
                pattern=r"principal_address\.(\w+)",
                target_template="data.Payload.Principal_Address.{field}",
                field_type="address",
                semantic_meaning="address",
                validation_rules=[],
                priority=1,
                description="Principal address mapping"
            ),
            
            # Contact Information Patterns
            MappingRule(
                pattern=r"contact_information\.(\w+)",
                target_template="data.Payload.Contact_Information.{field}",
                field_type="contact",
                semantic_meaning="contact",
                validation_rules=[],
                priority=1,
                description="Contact information mapping"
            ),
            
            # Contact Information Address Patterns
            MappingRule(
                pattern=r"contact_information\.Address\.(\w+)",
                target_template="data.Payload.Contact_Information.Address.{field}",
                field_type="address",
                semantic_meaning="address",
                validation_rules=[],
                priority=1,
                description="Contact information address mapping"
            ),
            
            # Organizer Information Patterns
            MappingRule(
                pattern=r"organizer_information\.(\w+)",
                target_template="data.Payload.Organizer_Information.Organizer_Details.{field}",
                field_type="contact",
                semantic_meaning="personnel_name",
                validation_rules=[],
                priority=1,
                description="Organizer information mapping"
            ),
            
            # Form Progress Patterns
            MappingRule(
                pattern=r"formProgress",
                target_template="data.FormProgress",
                field_type="numeric",
                semantic_meaning="form_progress",
                validation_rules=[r'^\d+$'],
                priority=1,
                description="Form progress mapping"
            ),
            
            # Order Type Patterns
            MappingRule(
                pattern=r"orderType",
                target_template="data.OrderType",
                field_type="name",
                semantic_meaning="order_type",
                validation_rules=[],
                priority=1,
                description="Order type mapping"
            )
        ]
    
    def _initialize_field_patterns(self) -> List[FieldPattern]:
        """Initialize field patterns for automatic field type detection"""
        return [
            # Name patterns
            FieldPattern(
                source_pattern=r"name|Name|keyPersonnelName",
                target_pattern=r"Name|Name",
                field_type="name",
                semantic_meaning="personnel_name",
                synonyms=["name", "Name", "keyPersonnelName", "personnelName"],
                validation_patterns=[r'^[a-zA-Z\s]+$']
            ),
            
            # Email patterns
            FieldPattern(
                source_pattern=r"email|Email|emailId|email_address|email address",
                target_pattern=r"Email|Email",
                field_type="email",
                semantic_meaning="email",
                synonyms=["email", "Email", "emailId", "email_address", "email address"],
                validation_patterns=[r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$']
            ),
            
            # Contact patterns
            FieldPattern(
                source_pattern=r"contact|Contact|contactNo|contact_no|contactNo",
                target_pattern=r"Contact_No|Contact_No",
                field_type="phone",
                semantic_meaning="contact_number",
                synonyms=["contact", "Contact", "contactNo", "contact_no", "phone"],
                validation_patterns=[r'^\d+$']
            ),
            
            # City patterns
            FieldPattern(
                source_pattern=r"city|City",
                target_pattern=r"City|City",
                field_type="address",
                semantic_meaning="city",
                synonyms=["city", "City", "town", "municipality"],
                validation_patterns=[r'^[a-zA-Z\s]+$']
            ),
            
            # State patterns
            FieldPattern(
                source_pattern=r"state|State|stateId",
                target_pattern=r"State|State",
                field_type="id",
                semantic_meaning="state",
                synonyms=["state", "State", "stateId", "province"],
                validation_patterns=[r'^\d+$']
            ),
            
            # Zip code patterns
            FieldPattern(
                source_pattern=r"zip_code|zipCode|postalCode|postal_code",
                target_pattern=r"Postal_Code|Postal_Code",
                field_type="numeric",
                semantic_meaning="zip_code",
                synonyms=["zip_code", "zipCode", "postalCode", "postal_code", "zip"],
                validation_patterns=[r'^\d+$']
            ),
            
            # Address line patterns
            FieldPattern(
                source_pattern=r"street_address|addressLine1|address_line1",
                target_pattern=r"Address_Line1|Address_Line1",
                field_type="address",
                semantic_meaning="street_address",
                synonyms=["street_address", "addressLine1", "address_line1", "street"],
                validation_patterns=[r'^[a-zA-Z0-9\s\.,\-]+$']
            ),
            
            FieldPattern(
                source_pattern=r"address_line2|addressLine2|address_line 2",
                target_pattern=r"Address_Line2|Address_Line2",
                field_type="address",
                semantic_meaning="address_line2",
                synonyms=["address_line2", "addressLine2", "address_line 2"],
                validation_patterns=[r'^[a-zA-Z0-9\s\.,\-]+$']
            ),
            
            # Legal name patterns
            FieldPattern(
                source_pattern=r"legal_name|legalName",
                target_pattern=r"CD_Legal_Name",
                field_type="name",
                semantic_meaning="legal_name",
                synonyms=["legal_name", "legalName", "entity_name"],
                validation_patterns=[r'^[a-zA-Z\s]+$']
            ),
            
            # Alternate name patterns
            FieldPattern(
                source_pattern=r"alternate_legal_name|alternateName",
                target_pattern=r"CD_Alternate_Legal_Name",
                field_type="name",
                semantic_meaning="alternate_name",
                synonyms=["alternate_legal_name", "alternateName", "dba"],
                validation_patterns=[r'^[a-zA-Z\s]+$']
            )
        ]
    
    def generate_mappings_from_json(self, source_json: Dict[str, Any]) -> List[Dict]:
        """
        Dynamically generate mappings from source JSON structure
        """
        try:
            mappings = []
            source_fields = self._extract_all_fields(source_json)
            
            for field_path in source_fields:
                mapping = self._create_mapping_for_field(field_path)
                if mapping:
                    mappings.append(mapping)
            
            self.logger.info(f"Generated {len(mappings)} dynamic mappings")
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
    
    def _create_mapping_for_field(self, field_path: str) -> Dict:
        """Create mapping for a specific field path"""
        try:
            # Find matching pattern rule
            pattern_rule = self._find_matching_pattern(field_path)
            if not pattern_rule:
                return None
            
            # Extract field name from path
            field_name = self._extract_field_name(field_path, pattern_rule.pattern)
            if not field_name:
                return None
            
            # Find field pattern for type detection
            field_pattern = self._find_field_pattern(field_name)
            
            # Generate target path
            target_path = self._generate_target_path(field_path, pattern_rule, field_pattern)
            
            # Determine data type
            data_type = self._determine_data_type(field_name, field_pattern)
            
            # Create mapping
            mapping = {
                "source_path": field_path,
                "target_path": target_path,
                "semantic_meaning": field_pattern.semantic_meaning if field_pattern else pattern_rule.semantic_meaning,
                "field_type": field_pattern.field_type if field_pattern else pattern_rule.field_type,
                "data_type": data_type,
                "confidence": 0.9,  # High confidence for pattern-based mappings
                "reasoning": f"Auto-generated mapping using pattern: {pattern_rule.description}",
                "is_required": self._is_required_field(field_name),
                "validation_rules": field_pattern.validation_patterns if field_pattern else pattern_rule.validation_rules,
                "mapping_strategy": "dynamic_pattern",
                "priority": pattern_rule.priority
            }
            
            return mapping
            
        except Exception as e:
            self.logger.warning(f"Failed to create mapping for {field_path}: {e}")
            return None
    
    def _find_matching_pattern(self, field_path: str) -> MappingRule:
        """Find matching pattern rule for field path"""
        for rule in self.mapping_patterns:
            if re.match(rule.pattern, field_path):
                return rule
        return None
    
    def _extract_field_name(self, field_path: str, pattern: str) -> str:
        """Extract field name from path using pattern"""
        match = re.match(pattern, field_path)
        if match:
            return match.group(1)
        return None
    
    def _find_field_pattern(self, field_name: str) -> FieldPattern:
        """Find matching field pattern for field name"""
        for pattern in self.field_patterns:
            if re.search(pattern.source_pattern, field_name, re.IGNORECASE):
                return pattern
        return None
    
    def _generate_target_path(self, field_path: str, pattern_rule: MappingRule, field_pattern: FieldPattern) -> str:
        """Generate target path using pattern rule and field pattern"""
        field_name = self._extract_field_name(field_path, pattern_rule.pattern)
        
        if field_pattern:
            # Use field pattern target template
            target_field = field_pattern.target_pattern
        else:
            # Use field name as is
            target_field = field_name
        
        # Replace placeholder in pattern rule template
        target_path = pattern_rule.target_template.format(field=target_field)
        
        return target_path
    
    def _determine_data_type(self, field_name: str, field_pattern: FieldPattern) -> str:
        """Determine data type based on field name and pattern"""
        if field_pattern:
            if field_pattern.field_type in ["phone", "id", "numeric"]:
                return "int"
            elif field_pattern.field_type == "boolean":
                return "bool"
            else:
                return "str"
        
        # Default based on field name patterns
        if re.search(r"Id|id|No|no|Code|code", field_name):
            return "int"
        elif re.search(r"email|Email", field_name):
            return "str"
        else:
            return "str"
    
    def _is_required_field(self, field_name: str) -> bool:
        """Determine if field is required based on name patterns"""
        required_patterns = [
            r"legal_name", r"name", r"city", r"state", r"email", 
            r"contact", r"keyPersonnelName", r"orderType"
        ]
        
        for pattern in required_patterns:
            if re.search(pattern, field_name, re.IGNORECASE):
                return True
        return False
    
    def generate_ai_enhanced_mappings(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> List[Dict]:
        """
        Generate AI-enhanced mappings for complex cases
        """
        try:
            # Get existing dynamic mappings
            dynamic_mappings = self.generate_mappings_from_json(source_json)
            
            # Extract unmapped fields
            mapped_source_paths = {m["source_path"] for m in dynamic_mappings}
            source_fields = self._extract_all_fields(source_json)
            unmapped_fields = source_fields - mapped_source_paths
            
            # Generate AI suggestions for unmapped fields
            ai_mappings = []
            for field_path in unmapped_fields:
                ai_mapping = self._generate_ai_mapping_suggestion(field_path, source_json, target_template)
                if ai_mapping:
                    ai_mappings.append(ai_mapping)
            
            # Combine dynamic and AI mappings
            all_mappings = dynamic_mappings + ai_mappings
            
            self.logger.info(f"Generated {len(dynamic_mappings)} dynamic + {len(ai_mappings)} AI mappings")
            return all_mappings
            
        except Exception as e:
            self.logger.error(f"Failed to generate AI-enhanced mappings: {e}")
            return []
    
    def _generate_ai_mapping_suggestion(self, field_path: str, source_json: Dict, target_template: Dict) -> Dict:
        """Generate AI suggestion for unmapped field"""
        try:
            # Create AI prompt for mapping suggestion
            prompt = self._create_ai_mapping_prompt(field_path, source_json, target_template)
            
            # Get AI response
            ai_response = self.ai_service.call_ai(prompt)
            
            # Parse AI response
            mapping = self._parse_ai_mapping_response(ai_response, field_path)
            
            return mapping
            
        except Exception as e:
            self.logger.warning(f"Failed to generate AI mapping for {field_path}: {e}")
            return None
    
    def _create_ai_mapping_prompt(self, field_path: str, source_json: Dict, target_template: Dict) -> str:
        """Create AI prompt for mapping suggestion"""
        prompt = f"""
        Analyze this JSON field and suggest a mapping to the target structure:

        Source Field: {field_path}
        Source Value: {self._get_value_by_path(source_json, field_path)}
        
        Target Template Structure:
        {json.dumps(target_template, indent=2)}
        
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
    
    def _parse_ai_mapping_response(self, ai_response: str, field_path: str) -> Dict:
        """Parse AI response into mapping object"""
        try:
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if not json_match:
                return None
            
            ai_suggestion = json.loads(json_match.group())
            
            # Create mapping object
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
                "priority": 2  # Lower priority than pattern-based mappings
            }
            
            return mapping
            
        except Exception as e:
            self.logger.warning(f"Failed to parse AI mapping response: {e}")
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