import json
import logging
import re
from typing import Dict, Any, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import hashlib
from difflib import SequenceMatcher
from Services.CallAiService import CallAiService

class FieldType(Enum):
    """Field type enumeration for better categorization"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"
    NAME = "name"
    DATE = "date"
    ID = "id"

@dataclass
class FieldMapping:
    """Data class for field mapping information"""
    source_path: str
    target_path: str
    confidence: float
    reasoning: str
    field_type: FieldType
    data_type: str
    is_required: bool = False
    validation_rules: List[str] = None
    
    def __post_init__(self):
        if self.validation_rules is None:
            self.validation_rules = []

@dataclass
class MappingResult:
    """Data class for mapping results"""
    success: bool
    mapped_fields: List[FieldMapping]
    unmapped_source_fields: List[str]
    unmapped_target_fields: List[str]
    confidence_score: float
    errors: List[str]
    warnings: List[str]
    execution_time: float

class AdvancedAIJsonMapper:
    def __init__(self, config: Dict):
        """
        Initialize advanced AI-driven JSON mapper
        """
        self.config = config
        self.ai_service = CallAiService()
        self.logger = logging.getLogger(__name__)
        
        # Advanced field type detection patterns
        self.type_patterns = {
            FieldType.EMAIL: [
                r'email', r'emailId', r'email_address', r'e_mail', r'mail'
            ],
            FieldType.PHONE: [
                r'phone', r'contact', r'contactNo', r'contact_no', r'telephone', r'mobile', r'cell'
            ],
            FieldType.ADDRESS: [
                r'address', r'street', r'city', r'state', r'zip', r'postal', r'location'
            ],
            FieldType.NAME: [
                r'name', r'legal_name', r'entity_name', r'company_name', r'business_name', r'personnel'
            ],
            FieldType.DATE: [
                r'date', r'created', r'modified', r'updated', r'timestamp'
            ],
            FieldType.ID: [
                r'id', r'_id', r'identifier', r'key'
            ]
        }
        
        # Business domain specific patterns
        self.business_patterns = {
            'entity_formation': [
                r'entity', r'formation', r'incorporation', r'registration', r'filing'
            ],
            'legal': [
                r'legal', r'registered', r'agent', r'principal', r'organizer'
            ],
            'address': [
                r'address', r'location', r'street', r'city', r'state', r'zip'
            ],
            'contact': [
                r'contact', r'email', r'phone', r'communication'
            ]
        }
        
        # Field validation rules
        self.validation_rules = {
            FieldType.EMAIL: [
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            ],
            FieldType.PHONE: [
                r'^\+?[\d\s\-\(\)]+$'
            ],
            FieldType.ADDRESS: [
                r'^[a-zA-Z0-9\s\.,\-]+$'
            ]
        }
    
    def detect_field_type(self, field_name: str, field_value: Any) -> FieldType:
        """
        Advanced field type detection based on name and value
        """
        field_lower = field_name.lower()
        
        # Check value type first
        if field_value is None:
            return FieldType.NULL
        elif isinstance(field_value, bool):
            return FieldType.BOOLEAN
        elif isinstance(field_value, (int, float)):
            return FieldType.NUMBER
        elif isinstance(field_value, list):
            return FieldType.ARRAY
        elif isinstance(field_value, dict):
            return FieldType.OBJECT
        
        # Check patterns for string types
        for field_type, patterns in self.type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, field_lower, re.IGNORECASE):
                    return field_type
        
        return FieldType.STRING
    
    def extract_field_metadata(self, obj: Dict[str, Any], prefix: str = "") -> List[Dict[str, Any]]:
        """
        Extract comprehensive field metadata including type, validation, and business context
        """
        metadata = []
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                # Recursively extract from nested objects
                nested_metadata = self.extract_field_metadata(value, current_path)
                metadata.extend(nested_metadata)
            else:
                # Extract metadata for leaf field
                field_type = self.detect_field_type(key, value)
                
                field_meta = {
                    'path': current_path,
                    'name': key,
                    'value': value,
                    'type': field_type,
                    'data_type': type(value).__name__,
                    'business_context': self._detect_business_context(key),
                    'validation_rules': self._get_validation_rules(field_type),
                    'is_required': self._is_required_field(key, value),
                    'sample_values': [value] if value is not None else []
                }
                
                metadata.append(field_meta)
        
        return metadata
    
    def _detect_business_context(self, field_name: str) -> List[str]:
        """
        Detect business context from field name
        """
        contexts = []
        field_lower = field_name.lower()
        
        for context, patterns in self.business_patterns.items():
            for pattern in patterns:
                if re.search(pattern, field_lower, re.IGNORECASE):
                    contexts.append(context)
        
        return contexts
    
    def _get_validation_rules(self, field_type: FieldType) -> List[str]:
        """
        Get validation rules for field type
        """
        return self.validation_rules.get(field_type, [])
    
    def _is_required_field(self, field_name: str, field_value: Any) -> bool:
        """
        Determine if field is required based on business logic
        """
        required_patterns = [
            r'legal_name', r'entity_name', r'name', r'email', r'contact',
            r'address', r'city', r'state', r'zip'
        ]
        
        field_lower = field_name.lower()
        for pattern in required_patterns:
            if re.search(pattern, field_lower, re.IGNORECASE):
                return True
        
        return False
    
    def create_advanced_mapping_prompt(self, source_metadata: List[Dict], target_metadata: List[Dict], 
                                     business_context: str = "") -> str:
        """
        Create sophisticated AI prompt for field mapping
        """
        prompt = f"""
You are an expert data architect specializing in JSON schema mapping for business entity formation systems.

BUSINESS CONTEXT:
{business_context}

SOURCE FIELDS METADATA:
{json.dumps(source_metadata, indent=2, default=str)}

TARGET FIELDS METADATA:
{json.dumps(target_metadata, indent=2, default=str)}

MAPPING REQUIREMENTS:
1. Analyze field names, types, business context, and validation rules
2. Consider data type compatibility and business logic
3. Prioritize exact matches, then semantic similarity
4. Ensure data integrity and business rule compliance
5. Handle nested object structures appropriately

Return ONLY a valid JSON object with this structure:
{{
  "mappings": [
    {{
      "source_field": "source.field.path",
      "target_field": "target.field.path",
      "confidence": 0.95,
      "reasoning": "Detailed explanation of mapping logic",
      "field_type": "string|number|boolean|object|array|email|phone|address|name|date|id",
      "data_type": "str|int|float|bool|dict|list",
      "is_required": true|false,
      "validation_rules": ["rule1", "rule2"],
      "business_context": ["context1", "context2"]
    }}
  ],
  "unmapped_source_fields": ["field1", "field2"],
  "unmapped_target_fields": ["field1", "field2"],
  "overall_confidence": 0.85,
  "mapping_strategy": "exact_match|semantic_similarity|business_logic|fallback"
}}

CRITERIA:
- Only include mappings with confidence > 0.7
- Provide detailed reasoning for each mapping
- Consider field types and validation rules
- Respect business domain knowledge
- Handle edge cases and data transformations
"""
        return prompt
    
    def get_advanced_ai_mappings(self, source_metadata: List[Dict], target_metadata: List[Dict], 
                                business_context: str = "") -> Dict[str, Any]:
        """
        Get advanced AI mappings with comprehensive metadata
        """
        try:
            prompt = self.create_advanced_mapping_prompt(source_metadata, target_metadata, business_context)
            
            # Call AI service with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.ai_service.call_ai(prompt)
                    
                    # Parse and validate AI response
                    mapping_data = json.loads(response)
                    
                    # Validate response structure
                    if not self._validate_ai_response(mapping_data):
                        raise ValueError("Invalid AI response structure")
                    
                    return mapping_data
                    
                except (json.JSONDecodeError, ValueError) as e:
                    self.logger.warning(f"AI response parsing failed (attempt {attempt + 1}): {e}")
                    if attempt == max_retries - 1:
                        raise
                    continue
                    
        except Exception as e:
            self.logger.error(f"Failed to get advanced AI mappings: {e}")
            return {
                "mappings": [],
                "unmapped_source_fields": [],
                "unmapped_target_fields": [],
                "overall_confidence": 0.0,
                "mapping_strategy": "fallback"
            }
    
    def _validate_ai_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate AI response structure and content
        """
        required_keys = ["mappings", "unmapped_source_fields", "unmapped_target_fields", 
                        "overall_confidence", "mapping_strategy"]
        
        if not all(key in response for key in required_keys):
            return False
        
        if not isinstance(response["mappings"], list):
            return False
        
        # Validate each mapping
        for mapping in response["mappings"]:
            required_mapping_keys = ["source_field", "target_field", "confidence", "reasoning"]
            if not all(key in mapping for key in required_mapping_keys):
                return False
            
            if not (0.0 <= mapping["confidence"] <= 1.0):
                return False
        
        return True
    
    def transform_json_advanced(self, source_json: Dict[str, Any], target_template: Dict[str, Any] = None,
                               business_context: str = "", validation_mode: bool = True) -> MappingResult:
        """
        Advanced JSON transformation with comprehensive validation and error handling
        """
        import time
        start_time = time.time()
        
        try:
            # Extract payload from source
            source_payload = self._extract_payload(source_json)
            
            # Extract comprehensive metadata
            source_metadata = self.extract_field_metadata(source_payload)
            source_values = self._extract_field_values(source_payload)
            
            # Create or use target template
            if target_template is None:
                target_template = self._create_advanced_target_template(source_metadata)
            
            target_metadata = self.extract_field_metadata(target_template)
            
            # Get advanced AI mappings
            ai_result = self.get_advanced_ai_mappings(source_metadata, target_metadata, business_context)
            
            # Convert to FieldMapping objects
            field_mappings = []
            for mapping_data in ai_result.get("mappings", []):
                field_mapping = FieldMapping(
                    source_path=mapping_data["source_field"],
                    target_path=mapping_data["target_field"],
                    confidence=mapping_data["confidence"],
                    reasoning=mapping_data["reasoning"],
                    field_type=FieldType(mapping_data.get("field_type", "string")),
                    data_type=mapping_data.get("data_type", "str"),
                    is_required=mapping_data.get("is_required", False),
                    validation_rules=mapping_data.get("validation_rules", [])
                )
                field_mappings.append(field_mapping)
            
            # Apply mappings with validation
            target_json, errors, warnings = self._apply_advanced_mappings(
                target_template, field_mappings, source_values, validation_mode
            )
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(field_mappings)
            
            # Create mapping result
            result = MappingResult(
                success=len(errors) == 0,
                mapped_fields=field_mappings,
                unmapped_source_fields=ai_result.get("unmapped_source_fields", []),
                unmapped_target_fields=ai_result.get("unmapped_target_fields", []),
                confidence_score=overall_confidence,
                errors=errors,
                warnings=warnings,
                execution_time=time.time() - start_time
            )
            
            self.logger.info(f"Advanced transformation completed: {len(field_mappings)} fields mapped, "
                           f"confidence: {overall_confidence:.2f}, time: {result.execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Advanced transformation failed: {e}")
            return MappingResult(
                success=False,
                mapped_fields=[],
                unmapped_source_fields=[],
                unmapped_target_fields=[],
                confidence_score=0.0,
                errors=[str(e)],
                warnings=[],
                execution_time=time.time() - start_time
            )
    
    def _apply_advanced_mappings(self, template: Dict[str, Any], field_mappings: List[FieldMapping], 
                                source_values: Dict[str, Any], validation_mode: bool) -> Tuple[Dict[str, Any], List[str], List[str]]:
        """
        Apply advanced mappings with validation and error handling
        """
        result = json.loads(json.dumps(template))
        errors = []
        warnings = []
        
        for mapping in field_mappings:
            try:
                if mapping.confidence > 0.7 and mapping.source_path in source_values:
                    value = source_values[mapping.source_path]
                    
                    # Validate value if validation mode is enabled
                    if validation_mode:
                        validation_result = self._validate_field_value(value, mapping)
                        if not validation_result["valid"]:
                            errors.append(f"Validation failed for {mapping.source_path}: {validation_result['errors']}")
                            continue
                        if validation_result["warnings"]:
                            warnings.extend(validation_result["warnings"])
                    
                    # Transform value if needed
                    transformed_value = self._transform_field_value(value, mapping)
                    
                    # Set value in result
                    self._set_nested_value(result, mapping.target_path, transformed_value)
                    
                    self.logger.info(f"Mapped '{mapping.source_path}' -> '{mapping.target_path}' "
                                   f"(confidence: {mapping.confidence:.2f})")
                else:
                    warnings.append(f"Low confidence mapping skipped: {mapping.source_path} -> {mapping.target_path}")
                    
            except Exception as e:
                errors.append(f"Failed to apply mapping {mapping.source_path} -> {mapping.target_path}: {e}")
        
        return result, errors, warnings
    
    def _validate_field_value(self, value: Any, mapping: FieldMapping) -> Dict[str, Any]:
        """
        Validate field value against mapping rules
        """
        result = {"valid": True, "errors": [], "warnings": []}
        
        # Check required fields
        if mapping.is_required and (value is None or value == ""):
            result["valid"] = False
            result["errors"].append("Required field is empty")
        
        # Apply validation rules
        for rule in mapping.validation_rules:
            if isinstance(value, str) and not re.match(rule, value):
                result["valid"] = False
                result["errors"].append(f"Value does not match pattern: {rule}")
        
        # Type-specific validation
        if mapping.field_type == FieldType.EMAIL and isinstance(value, str):
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                result["warnings"].append("Email format may be invalid")
        
        return result
    
    def _transform_field_value(self, value: Any, mapping: FieldMapping) -> Any:
        """
        Transform field value based on mapping requirements
        """
        if value is None:
            return None
        
        # Type-specific transformations
        if mapping.field_type == FieldType.PHONE and isinstance(value, str):
            # Clean phone number
            return re.sub(r'[^\d\+\(\)\-\s]', '', value)
        
        elif mapping.field_type == FieldType.EMAIL and isinstance(value, str):
            # Normalize email
            return value.lower().strip()
        
        elif mapping.field_type == FieldType.ADDRESS and isinstance(value, str):
            # Clean address
            return re.sub(r'\s+', ' ', value.strip())
        
        return value
    
    def _calculate_overall_confidence(self, field_mappings: List[FieldMapping]) -> float:
        """
        Calculate overall confidence score
        """
        if not field_mappings:
            return 0.0
        
        total_confidence = sum(mapping.confidence for mapping in field_mappings)
        return total_confidence / len(field_mappings)
    
    def _extract_payload(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract payload from source JSON structure
        """
        for key, value in source_json.items():
            if isinstance(value, dict) and 'payload' in value:
                return value['payload']
        return source_json.get('payload', {})
    
    def _extract_field_values(self, obj: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """
        Extract all field paths and their values
        """
        fields = {}
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                nested_fields = self._extract_field_values(value, current_path)
                fields.update(nested_fields)
            else:
                fields[current_path] = value
        
        return fields
    
    def _create_advanced_target_template(self, source_metadata: List[Dict]) -> Dict[str, Any]:
        """
        Create advanced target template based on source metadata analysis
        """
        # Analyze source metadata to create intelligent template
        field_categories = {}
        
        for meta in source_metadata:
            context = meta.get('business_context', [])
            for ctx in context:
                if ctx not in field_categories:
                    field_categories[ctx] = []
                field_categories[ctx].append(meta)
        
        # Create template based on categories
        template = {
            "data": {
                "EntityType": {},
                "State": {},
                "Payload": {}
            }
        }
        
        # Add categorized sections
        for category, fields in field_categories.items():
            if category == 'entity_formation':
                template["data"]["Payload"]["Name"] = {}
            elif category == 'legal':
                template["data"]["Payload"]["Registered_Agent"] = {
                    "Address": {},
                    "Name": {}
                }
            elif category == 'address':
                template["data"]["Payload"]["Principal_Address"] = {}
            elif category == 'contact':
                template["data"]["Payload"]["Organizer_Information"] = {
                    "Organizer_Details": {}
                }
        
        return template
    
    def _set_nested_value(self, obj: Dict[str, Any], path: str, value: Any):
        """
        Set value in nested object using dot notation path
        """
        try:
            parts = path.split('.')
            current = obj
            
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            current[parts[-1]] = value
            
        except Exception as e:
            self.logger.error(f"Failed to set value at path {path}: {e}")
            raise 