import logging
from typing import Dict, List, Optional, Any
from Utils.DatabaseConnection import DatabaseConnection
from Services.CallAiService import CallAiService
import json
import re
from dataclasses import dataclass
from enum import Enum

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
    semantic_meaning: str
    confidence: float
    reasoning: str
    field_type: FieldType
    data_type: str
    is_required: bool = False
    validation_rules: List[str] = None
    mapping_strategy: str = "database"  # database, ai, hybrid
    
    def __post_init__(self):
        if self.validation_rules is None:
            self.validation_rules = []

class JsonMappingDatabaseService:
    def __init__(self, config: Dict):
        """
        Initialize the JSON mapping database service with AI integration
        """
        self.config = config
        self.db_connection = DatabaseConnection(config)
        self.ai_service = CallAiService()
        self.logger = logging.getLogger(__name__)
        
        # Advanced field type detection patterns
        self.type_patterns = {
            FieldType.EMAIL: [r'email', r'emailId', r'email_address', r'e_mail', r'mail'],
            FieldType.PHONE: [r'phone', r'contact', r'contactNo', r'contact_no', r'telephone', r'mobile', r'cell'],
            FieldType.ADDRESS: [r'address', r'street', r'city', r'state', r'zip', r'postal', r'location'],
            FieldType.NAME: [r'name', r'legal_name', r'entity_name', r'company_name', r'business_name', r'personnel'],
            FieldType.DATE: [r'date', r'created', r'modified', r'updated', r'timestamp'],
            FieldType.ID: [r'id', r'_id', r'identifier', r'key']
        }
        
    def create_json_mapping_tables(self):
        """Create comprehensive tables for JSON field mappings"""
        try:
            # Create json_field_mappings table with advanced fields
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS json_field_mappings (
                    id SERIAL PRIMARY KEY,
                    source_path VARCHAR(255) NOT NULL,
                    target_path VARCHAR(255) NOT NULL,
                    semantic_meaning VARCHAR(100) NOT NULL,
                    field_type VARCHAR(50) NOT NULL,
                    data_type VARCHAR(50) NOT NULL,
                    confidence FLOAT DEFAULT 1.0,
                    reasoning TEXT,
                    is_required BOOLEAN DEFAULT FALSE,
                    validation_rules JSONB,
                    mapping_strategy VARCHAR(20) DEFAULT 'database',
                    priority INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(source_path, target_path)
                )
            """, fetch=False)
            
            # Create field_types table for categorization
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS field_types (
                    id SERIAL PRIMARY KEY,
                    type_name VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT,
                    validation_patterns JSONB,
                    business_context VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """, fetch=False)
            
            # Create semantic_meanings table
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS semantic_meanings (
                    id SERIAL PRIMARY KEY,
                    meaning VARCHAR(100) UNIQUE NOT NULL,
                    description TEXT,
                    category VARCHAR(50),
                    synonyms JSONB,
                    business_domain VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """, fetch=False)
            
            # Create mapping_strategies table
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS mapping_strategies (
                    id SERIAL PRIMARY KEY,
                    strategy_name VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT,
                    ai_prompt_template TEXT,
                    confidence_threshold FLOAT DEFAULT 0.7,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """, fetch=False)
            
            self.logger.info("Advanced JSON mapping tables created successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to create JSON mapping tables: {e}")
            raise
    
    def detect_field_type(self, field_name: str, field_value: Any) -> FieldType:
        """Advanced field type detection based on name and value"""
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
        """Extract comprehensive field metadata"""
        metadata = []
        
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                nested_metadata = self.extract_field_metadata(value, current_path)
                metadata.extend(nested_metadata)
            else:
                field_type = self.detect_field_type(key, value)
                
                field_meta = {
                    'path': current_path,
                    'name': key,
                    'value': value,
                    'type': field_type.value,
                    'data_type': type(value).__name__,
                    'is_required': self._is_required_field(key, value),
                    'validation_rules': self._get_validation_rules(field_type)
                }
                
                metadata.append(field_meta)
        
        return metadata
    
    def _is_required_field(self, field_name: str, field_value: Any) -> bool:
        """Determine if field is required based on business logic"""
        required_patterns = [
            r'legal_name', r'entity_name', r'name', r'email', r'contact',
            r'address', r'city', r'state', r'zip'
        ]
        
        field_lower = field_name.lower()
        for pattern in required_patterns:
            if re.search(pattern, field_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _get_validation_rules(self, field_type: FieldType) -> List[str]:
        """Get validation rules for field type"""
        validation_rules = {
            FieldType.EMAIL: [r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'],
            FieldType.PHONE: [r'^\+?[\d\s\-\(\)]+$'],
            FieldType.ADDRESS: [r'^[a-zA-Z0-9\s\.,\-]+$']
        }
        return validation_rules.get(field_type, [])
    
    def insert_field_types(self, field_types: Dict[str, Dict]):
        """Insert field types with validation patterns"""
        try:
            query = """
                INSERT INTO field_types (type_name, description, validation_patterns, business_context)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (type_name) DO UPDATE SET
                description = EXCLUDED.description,
                validation_patterns = EXCLUDED.validation_patterns,
                business_context = EXCLUDED.business_context
            """
            
            params_list = [
                (type_name, data.get('description', ''), 
                 json.dumps(data.get('validation_patterns', [])),
                 data.get('business_context', ''))
                for type_name, data in field_types.items()
            ]
            
            self.db_connection.execute_many(query, params_list)
            self.logger.info(f"Inserted {len(field_types)} field types")
            
        except Exception as e:
            self.logger.error(f"Failed to insert field types: {e}")
            raise
    
    def insert_semantic_meanings(self, semantic_meanings: Dict[str, Dict]):
        """Insert semantic meanings with synonyms and business domain"""
        try:
            query = """
                INSERT INTO semantic_meanings (meaning, description, category, synonyms, business_domain)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (meaning) DO UPDATE SET
                description = EXCLUDED.description,
                category = EXCLUDED.category,
                synonyms = EXCLUDED.synonyms,
                business_domain = EXCLUDED.business_domain
            """
            
            params_list = [
                (meaning, data.get('description', ''),
                 data.get('category', ''),
                 json.dumps(data.get('synonyms', [])),
                 data.get('business_domain', ''))
                for meaning, data in semantic_meanings.items()
            ]
            
            self.db_connection.execute_many(query, params_list)
            self.logger.info(f"Inserted {len(semantic_meanings)} semantic meanings")
            
        except Exception as e:
            self.logger.error(f"Failed to insert semantic meanings: {e}")
            raise
    
    def insert_json_field_mappings(self, mappings: List[Dict]):
        """Insert advanced JSON field mappings"""
        try:
            # Clear existing mappings first
            self.db_connection.execute_query("DELETE FROM json_field_mappings", fetch=False)
            
            query = """
                INSERT INTO json_field_mappings 
                (source_path, target_path, semantic_meaning, field_type, data_type, 
                 confidence, reasoning, is_required, validation_rules, mapping_strategy, priority)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_path, target_path) DO UPDATE SET
                semantic_meaning = EXCLUDED.semantic_meaning,
                field_type = EXCLUDED.field_type,
                data_type = EXCLUDED.data_type,
                confidence = EXCLUDED.confidence,
                reasoning = EXCLUDED.reasoning,
                is_required = EXCLUDED.is_required,
                validation_rules = EXCLUDED.validation_rules,
                mapping_strategy = EXCLUDED.mapping_strategy,
                priority = EXCLUDED.priority
            """
            
            params_list = [
                (mapping['source_path'], mapping['target_path'], 
                 mapping['semantic_meaning'], mapping['field_type'], mapping['data_type'],
                 mapping.get('confidence', 1.0), mapping.get('reasoning', ''),
                 mapping.get('is_required', False), json.dumps(mapping.get('validation_rules', [])),
                 mapping.get('mapping_strategy', 'database'), mapping.get('priority', 1))
                for mapping in mappings
            ]
            
            self.db_connection.execute_many(query, params_list)
            self.logger.info(f"Inserted {len(mappings)} advanced JSON field mappings")
            
        except Exception as e:
            self.logger.error(f"Failed to insert JSON field mappings: {e}")
            raise
    
    def get_all_json_mappings(self) -> List[FieldMapping]:
        """Get all JSON field mappings as FieldMapping objects"""
        try:
            query = """
                SELECT source_path, target_path, semantic_meaning, field_type, data_type,
                       confidence, reasoning, is_required, validation_rules, mapping_strategy, priority
                FROM json_field_mappings
                WHERE is_active = TRUE
                ORDER BY priority DESC, source_path
            """
            
            rows = self.db_connection.execute_query(query)
            
            mappings = []
            for row in rows:
                validation_rules = json.loads(row[8]) if row[8] else []
                
                field_mapping = FieldMapping(
                    source_path=row[0],
                    target_path=row[1],
                    semantic_meaning=row[2],
                    confidence=row[5],
                    reasoning=row[6] or '',
                    field_type=FieldType(row[3]),
                    data_type=row[4],
                    is_required=row[7],
                    validation_rules=validation_rules,
                    mapping_strategy=row[9]
                )
                mappings.append(field_mapping)
            
            return mappings
            
        except Exception as e:
            self.logger.error(f"Failed to get JSON mappings: {e}")
            raise
    
    def get_ai_enhanced_mappings(self, source_metadata: List[Dict], target_metadata: List[Dict]) -> List[FieldMapping]:
        """Get AI-enhanced mappings for fields not in database"""
        try:
            # Get existing database mappings
            db_mappings = self.get_all_json_mappings()
            db_source_paths = {mapping.source_path for mapping in db_mappings}
            
            # Find unmapped source fields
            unmapped_source = [meta for meta in source_metadata if meta['path'] not in db_source_paths]
            
            if not unmapped_source:
                return db_mappings
            
            # Create AI prompt for unmapped fields
            prompt = self._create_ai_mapping_prompt(unmapped_source, target_metadata)
            
            # Get AI suggestions
            response = self.ai_service.call_ai(prompt)
            
            try:
                ai_suggestions = json.loads(response)
                ai_mappings = ai_suggestions.get('mappings', [])
                
                # Convert AI suggestions to FieldMapping objects
                for suggestion in ai_mappings:
                    field_mapping = FieldMapping(
                        source_path=suggestion['source_field'],
                        target_path=suggestion['target_field'],
                        semantic_meaning=suggestion.get('semantic_meaning', ''),
                        confidence=suggestion.get('confidence', 0.8),
                        reasoning=suggestion.get('reasoning', 'AI-generated mapping'),
                        field_type=FieldType(suggestion.get('field_type', 'string')),
                        data_type=suggestion.get('data_type', 'str'),
                        is_required=suggestion.get('is_required', False),
                        validation_rules=suggestion.get('validation_rules', []),
                        mapping_strategy='ai'
                    )
                    db_mappings.append(field_mapping)
                
                self.logger.info(f"AI enhanced mappings with {len(ai_mappings)} additional mappings")
                
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse AI response, using database mappings only")
            
            return db_mappings
            
        except Exception as e:
            self.logger.error(f"Failed to get AI enhanced mappings: {e}")
            return self.get_all_json_mappings()
    
    def _create_ai_mapping_prompt(self, source_metadata: List[Dict], target_metadata: List[Dict]) -> str:
        """Create AI prompt for field mapping"""
        prompt = f"""
You are an expert at mapping JSON fields between different data structures for business entity formation.

SOURCE FIELDS:
{json.dumps(source_metadata, indent=2, default=str)}

TARGET FIELDS:
{json.dumps(target_metadata, indent=2, default=str)}

Find the best semantic matches between source and target fields. Consider:
- Field purpose and meaning
- Data type compatibility
- Business logic and domain knowledge
- Common naming conventions

Return ONLY a valid JSON object:
{{
  "mappings": [
    {{
      "source_field": "source.field.path",
      "target_field": "target.field.path",
      "confidence": 0.95,
      "reasoning": "Brief explanation",
      "field_type": "string|number|boolean|email|phone|address|name|date|id",
      "data_type": "str|int|float|bool|dict|list",
      "is_required": true|false,
      "validation_rules": ["rule1", "rule2"]
    }}
  ]
}}

Only include mappings where confidence > 0.7.
"""
        return prompt
    
    def add_json_mapping(self, source_path: str, target_path: str, semantic_meaning: str, 
                        field_type: str, data_type: str, confidence: float = 1.0, 
                        reasoning: str = "", is_required: bool = False, 
                        validation_rules: List[str] = None, mapping_strategy: str = "database"):
        """Add a new JSON field mapping"""
        try:
            if validation_rules is None:
                validation_rules = []
                
            query = """
                INSERT INTO json_field_mappings 
                (source_path, target_path, semantic_meaning, field_type, data_type,
                 confidence, reasoning, is_required, validation_rules, mapping_strategy)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (source_path, target_path) DO UPDATE SET
                semantic_meaning = EXCLUDED.semantic_meaning,
                field_type = EXCLUDED.field_type,
                data_type = EXCLUDED.data_type,
                confidence = EXCLUDED.confidence,
                reasoning = EXCLUDED.reasoning,
                is_required = EXCLUDED.is_required,
                validation_rules = EXCLUDED.validation_rules,
                mapping_strategy = EXCLUDED.mapping_strategy
            """
            
            self.db_connection.execute_query(
                query, 
                (source_path, target_path, semantic_meaning, field_type, data_type,
                 confidence, reasoning, is_required, json.dumps(validation_rules), mapping_strategy),
                fetch=False
            )
            
            self.logger.info(f"Added JSON mapping: {source_path} -> {target_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to add JSON mapping: {e}")
            raise
    
    def close_connection(self):
        """Close database connection"""
        self.db_connection.close_connection() 