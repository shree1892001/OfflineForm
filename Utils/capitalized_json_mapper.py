import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.CallAiService import CallAiService

class CapitalizedJsonMapper:
    """
    Database-driven JSON mapper that handles capitalized key names and comprehensive field mappings
    Maps fields like Legal_Name to CD_Legal_Name and handles all other field mappings
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_service = JsonMappingDatabaseService(config)
        self.ai_service = CallAiService()
        self.logger = logging.getLogger(__name__)
        
        # Define comprehensive field mappings for capitalized keys
        self.field_mappings = {
            # Name mappings
            "Legal_Name": ["CD_Legal_Name", "CD_LLC_Name", "CD_Entity_Name"],
            "Alternate_Legal_Name": ["CD_Alternate_Legal_Name", "CD_DBA_Name"],
            
            # Address mappings
            "City": ["PA_City", "RA_City", "Org_City", "Billing_City", "Mailing_City"],
            "State": ["PA_State", "RA_State", "Org_State", "Billing_State", "Mailing_State"],
            "Zip_Code": ["PA_Postal_Code", "RA_Postal_Code", "Org_Postal_Code", "Billing_Postal_Code"],
            "Street_Address": ["PA_Address_Line1", "RA_Address_Line1", "Org_Address_Line1"],
            "Address_Line_2": ["PA_Address_Line2", "RA_Address_Line2", "Org_Address_Line2"],
            "AddressLine1": ["PA_Address_Line1", "RA_Address_Line1", "Org_Address_Line1"],
            "AddressLine2": ["PA_Address_Line2", "RA_Address_Line2", "Org_Address_Line2"],
            
            # Contact mappings
            "EmailId": ["Email", "Og_Email", "Billing_Email", "Mailing_Email"],
            "Email_Address": ["Email", "Og_Email", "Billing_Email", "Mailing_Email"],
            "ContactNo": ["Contact_No", "Og_Contact_No", "Billing_Contact_No"],
            "Contact_No": ["Contact_No", "Og_Contact_No", "Billing_Contact_No"],
            "PostalCode": ["PA_Postal_Code", "RA_Postal_Code", "Org_Postal_Code"],
            
            # Personnel mappings
            "KeyPersonnelName": ["RA_Name", "Org_Name", "Contact_Name"],
            "Name": ["RA_Name", "Org_Name", "Contact_Name", "Mailing_Name"],
            
            # Entity and State mappings
            "OrderType": ["OrderType"],
            "OrderShortName": ["ShortName"],
            "OrderFullDesc": ["FullDescription"],
            "StateShortName": ["ShortName"],
            "StateFullDesc": ["FullDescription"],
            "StateUrl": ["Url"],
            "FilingWebsiteUsername": ["FilingUsername"],
            "FilingWebsitePassword": ["FilingPassword"],
            "CountryShortName": ["ShortName"],
            "CountryFullDesc": ["FullDescription"],
            
            # Metadata mappings
            "CreatedBy": ["CreatedBy"],
            "CreationDate": ["CreationDate"],
            "LastModifiedBy": ["LastModifiedBy"],
            "LastModifiedDate": ["LastModifiedDate"],
            "Id": ["Id"],
            "FormProgress": ["FormProgress"]
        }
        
        # Define context-based mapping rules for capitalized keys
        self.context_mappings = {
            "Payload.Name": {
                "Legal_Name": "data.Payload.Name.CD_Legal_Name",
                "Alternate_Legal_Name": "data.Payload.Name.CD_Alternate_Legal_Name"
            },
            "Payload.Principal_Address": {
                "City": "data.Payload.Principal_Address.PA_City",
                "State": "data.Payload.Principal_Address.PA_State",
                "Zip_Code": "data.Payload.Principal_Address.PA_Postal_Code",
                "Street_Address": "data.Payload.Principal_Address.PA_Address_Line1",
                "Address_Line_2": "data.Payload.Principal_Address.PA_Address_Line2"
            },
            "Payload.Registered_Agent.Address": {
                "City": "data.Payload.Registered_Agent.Address.RA_City",
                "State": "data.Payload.Registered_Agent.Address.RA_State",
                "Zip_Code": "data.Payload.Registered_Agent.Address.RA_Postal_Code",
                "Street_Address": "data.Payload.Registered_Agent.Address.RA_Address_Line1",
                "Address_Line_2": "data.Payload.Registered_Agent.Address.RA_Address_Line2"
            },
            "Payload.Registered_Agent": {
                "EmailId": "data.Payload.Registered_Agent.Name.Email",
                "ContactNo": "data.Payload.Registered_Agent.Name.Contact_No",
                "KeyPersonnelName": "data.Payload.Registered_Agent.Name.RA_Name"
            },
            "Payload.Registered_Agent.Billing_Information": {
                "City": "data.Payload.Registered_Agent.Billing.City",
                "EmailId": "data.Payload.Registered_Agent.Billing.Email",
                "StateId": "data.Payload.Registered_Agent.Billing.State",
                "ContactNo": "data.Payload.Registered_Agent.Billing.Contact_No",
                "PostalCode": "data.Payload.Registered_Agent.Billing.Postal_Code",
                "AddressLine1": "data.Payload.Registered_Agent.Billing.Address_Line1",
                "AddressLine2": "data.Payload.Registered_Agent.Billing.Address_Line2",
                "KeyPersonnelName": "data.Payload.Registered_Agent.Billing.Personnel_Name"
            },
            "Payload.Registered_Agent.Mailing_Information": {
                "City": "data.Payload.Registered_Agent.Mailing.City",
                "Name": "data.Payload.Registered_Agent.Mailing.Name",
                "State": "data.Payload.Registered_Agent.Mailing.State",
                "Zip_Code": "data.Payload.Registered_Agent.Mailing.Postal_Code",
                "Contact_No": "data.Payload.Registered_Agent.Mailing.Contact_No",
                "Email_Address": "data.Payload.Registered_Agent.Mailing.Email",
                "Address_Line_2": "data.Payload.Registered_Agent.Mailing.Address_Line2",
                "Street_Address": "data.Payload.Registered_Agent.Mailing.Address_Line1"
            },
            "Payload.Contact_Information": {
                "Name": "data.Payload.Organizer_Information.Organizer_Details.Org_Name",
                "Contact_No": "data.Payload.Organizer_Information.Organizer_Details.Og_Contact_No",
                "Email_Address": "data.Payload.Organizer_Information.Organizer_Details.Og_Email"
            },
            "Payload.Contact_Information.Address": {
                "City": "data.Payload.Organizer_Information.Org_Address.Org_City",
                "State": "data.Payload.Organizer_Information.Org_Address.Org_State",
                "Zip_Code": "data.Payload.Organizer_Information.Org_Address.Org_Postal_Code",
                "Address_Line_2": "data.Payload.Organizer_Information.Org_Address.Org_Address_Line2",
                "Street_Address": "data.Payload.Organizer_Information.Org_Address.Org_Address_Line1"
            },
            "Payload.Organizer_Information": {
                "EmailId": "data.Payload.Organizer_Information.Organizer_Details.Og_Email",
                "ContactNo": "data.Payload.Organizer_Information.Organizer_Details.Og_Contact_No",
                "KeyPersonnelName": "data.Payload.Organizer_Information.Organizer_Details.Org_Name"
            },
            "EntityType": {
                "CreatedBy": "data.EntityType.CreatedBy",
                "CreationDate": "data.EntityType.CreationDate",
                "LastModifiedBy": "data.EntityType.LastModifiedBy",
                "LastModifiedDate": "data.EntityType.LastModifiedDate",
                "Id": "data.EntityType.Id",
                "OrderShortName": "data.EntityType.ShortName",
                "OrderFullDesc": "data.EntityType.FullDescription"
            },
            "State": {
                "CreatedBy": "data.State.CreatedBy",
                "CreationDate": "data.State.CreationDate",
                "LastModifiedBy": "data.State.LastModifiedBy",
                "LastModifiedDate": "data.State.LastModifiedDate",
                "Id": "data.State.Id",
                "StateShortName": "data.State.ShortName",
                "StateFullDesc": "data.State.FullDescription",
                "StateUrl": "data.State.Url",
                "FilingWebsiteUsername": "data.State.FilingUsername",
                "FilingWebsitePassword": "data.State.FilingPassword"
            },
            "State.CountryMaster": {
                "CreatedBy": "data.State.Country.CreatedBy",
                "CreationDate": "data.State.Country.CreationDate",
                "LastModifiedBy": "data.State.Country.LastModifiedBy",
                "LastModifiedDate": "data.State.Country.LastModifiedDate",
                "Id": "data.State.Country.Id",
                "CountryShortName": "data.State.Country.ShortName",
                "CountryFullDesc": "data.State.Country.FullDescription"
            }
        }
    
    def capitalize_keys(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively capitalize all keys in a dictionary"""
        if isinstance(obj, dict):
            return {self.capitalize_key(k): self.capitalize_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.capitalize_keys(item) for item in obj]
        else:
            return obj
    
    def capitalize_key(self, key: str) -> str:
        """Capitalize a single key"""
        # Handle special cases
        if key == "orderType":
            return "OrderType"
        elif key == "formProgress":
            return "FormProgress"
        elif key == "state ":
            return "State"
        elif key == "city ":
            return "City"
        elif key == "email address":
            return "Email_Address"
        elif key == "address_line 2":
            return "Address_Line_2"
        elif key == "Billing Information":
            return "Billing_Information"
        elif key == "Mailing Information":
            return "Mailing_Information"
        elif key == "contact_information":
            return "Contact_Information"
        elif key == "organizer_information":
            return "Organizer_Information"
        elif key == "principal_address":
            return "Principal_Address"
        elif key == "registered_agent":
            return "Registered_Agent"
        elif key == "countryMaster":
            return "CountryMaster"
        
        # General capitalization
        return key.replace('_', ' ').title().replace(' ', '_')
    
    def extract_payload_from_source(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extract payload from the nested source JSON structure"""
        # First, check if payload is directly at root level
        if 'payload' in source_json:
            return source_json['payload']
        if 'Payload' in source_json:
            return source_json['Payload']
        
        # Handle the nested structure where payload is inside a numbered key
        for key, value in source_json.items():
            if isinstance(value, dict):
                if 'payload' in value:
                    return value['payload']
                if 'Payload' in value:
                    return value['Payload']
        
        # If no payload found, return empty dict
        return {}
    
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
    
    def find_best_mapping(self, source_path: str, source_value: Any, target_template: Dict[str, Any]) -> Optional[str]:
        """Find the best mapping for a source field using database and fallback logic"""
        source_field = source_path.split('.')[-1]
        
        # First, try context-based mapping
        context_path = '.'.join(source_path.split('.')[:-1])
        if context_path in self.context_mappings:
            if source_field in self.context_mappings[context_path]:
                return self.context_mappings[context_path][source_field]
        
        # Try semantic mapping
        if source_field in self.field_mappings:
            target_fields = self.field_mappings[source_field]
            target_paths = self.extract_all_field_paths(target_template)
            target_field_names = [path.split('.')[-1] for path, _ in target_paths]
            
            for target_field in target_fields:
                if target_field in target_field_names:
                    # Return just the field name, not the full path
                    return target_field
        
        return None
    
    def transform_json(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> Dict[str, Any]:
        """Transform source JSON to target structure with capitalized keys and database mappings"""
        try:
            # First, capitalize all keys in the source JSON
            capitalized_source = self.capitalize_keys(source_json)
            
            # Extract payload from capitalized source
            source_payload = self.extract_payload_from_source(capitalized_source)
            
            # Create a complete source object including EntityType and State
            complete_source = {
                "Payload": source_payload,
                "EntityType": capitalized_source.get("1", {}).get("EntityType", {}),
                "State": capitalized_source.get("1", {}).get("State", {}),
                "OrderType": capitalized_source.get("1", {}).get("OrderType"),
                "FormProgress": capitalized_source.get("1", {}).get("FormProgress")
            }
            
            # Get database mappings
            db_mappings = self.db_service.get_all_json_mappings()
            
            # Create result by copying target template
            result = json.loads(json.dumps(target_template))
            
            # Apply database mappings first
            mappings_applied = []
            
            for db_mapping in db_mappings:
                user_field_path = db_mapping.source_path  # User input path like "payload.name.legal_name"
                pdf_field_name = db_mapping.target_path   # PDF field name like "CD_LLC_Name"
                
                # Get value from user input using path
                user_value = self._get_value_by_path(complete_source, user_field_path)
                
                if user_value is not None:
                    # Set the value in result using the PDF field name
                    result[pdf_field_name] = user_value
                    mappings_applied.append({
                        'pdf_field': pdf_field_name,
                        'user_field_path': user_field_path,
                        'value': user_value,
                        'mapping_type': 'database'
                    })
                    self.logger.debug(f"Database mapped {user_field_path} -> {pdf_field_name}: {user_value}")
            
            # Apply fallback mappings for unmapped fields
            source_fields = self.extract_all_field_paths(complete_source)
            mapped_user_paths = {m['user_field_path'] for m in mappings_applied}
            
            for source_path, source_value in source_fields:
                if source_path not in mapped_user_paths and source_value is not None:
                    pdf_field_name = self.find_best_mapping(source_path, source_value, target_template)
                    
                    if pdf_field_name:
                        result[pdf_field_name] = source_value
                        mappings_applied.append({
                            'pdf_field': pdf_field_name,
                            'user_field_path': source_path,
                            'value': source_value,
                            'mapping_type': 'fallback'
                        })
                        self.logger.debug(f"Fallback mapped {source_path} -> {pdf_field_name}: {source_value}")
            
            self.logger.info(f"Applied {len(mappings_applied)} mappings ({len([m for m in mappings_applied if m['mapping_type'] == 'database'])} database, {len([m for m in mappings_applied if m['mapping_type'] == 'fallback'])} fallback)")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON: {e}")
            raise
    
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
    
    def get_mapping_report(self, source_json: Dict[str, Any], target_json: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive mapping report"""
        # Capitalize source JSON first
        capitalized_source = self.capitalize_keys(source_json)
        source_payload = self.extract_payload_from_source(capitalized_source)
        complete_source = {
            "Payload": source_payload,
            "EntityType": capitalized_source.get("1", {}).get("EntityType", {}),
            "State": capitalized_source.get("1", {}).get("State", {}),
            "OrderType": capitalized_source.get("1", {}).get("OrderType"),
            "FormProgress": capitalized_source.get("1", {}).get("FormProgress")
        }
        
        source_fields = self.extract_all_field_paths(complete_source)
        target_fields = self.extract_all_field_paths(target_json)
        
        # Get database mappings
        db_mappings = self.db_service.get_all_json_mappings()
        
        mappings = []
        unmapped_source = []
        
        # Check database mappings first
        for db_mapping in db_mappings:
            source_path = db_mapping.source_path
            target_path = db_mapping.target_path
            source_value = self._get_value_by_path(complete_source, source_path)
            
            if source_value is not None:
                mappings.append({
                    'source_path': source_path,
                    'target_path': target_path,
                    'source_value': source_value,
                    'mapping_type': 'database'
                })
        
        # Check fallback mappings for unmapped fields
        mapped_source_paths = {m['source_path'] for m in mappings}
        for source_path, source_value in source_fields:
            if source_path not in mapped_source_paths and source_value is not None:
                target_path = self.find_best_mapping(source_path, source_value, target_json)
                if target_path:
                    mappings.append({
                        'source_path': source_path,
                        'target_path': target_path,
                        'source_value': source_value,
                        'mapping_type': 'fallback'
                    })
                else:
                    unmapped_source.append((source_path, source_value))
        
        return {
            'total_source_fields': len(source_fields),
            'total_target_fields': len(target_fields),
            'mapped_fields': len(mappings),
            'mapping_accuracy': len(mappings) / len(source_fields) if source_fields else 0,
            'mappings': mappings,
            'unmapped_source_fields': unmapped_source,
            'database_mappings': len([m for m in mappings if m['mapping_type'] == 'database']),
            'fallback_mappings': len([m for m in mappings if m['mapping_type'] == 'fallback'])
        }
    
    def add_custom_mapping(self, source_path: str, target_path: str, 
                          semantic_meaning: str = "", field_type: str = "string"):
        """Add a custom mapping to the database"""
        try:
            self.db_service.add_json_mapping(
                source_path=source_path,
                target_path=target_path,
                semantic_meaning=semantic_meaning or f"Custom mapping: {source_path} -> {target_path}",
                field_type=field_type,
                data_type="str",
                confidence=1.0,
                reasoning=f"Custom mapping for {source_path} to {target_path}",
                is_required=False,
                validation_rules=[],
                mapping_strategy="custom"
            )
            self.logger.info(f"Added custom mapping: {source_path} -> {target_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to add custom mapping: {e}")
            raise
    
    def initialize_capitalized_mappings(self):
        """Initialize database with capitalized key mappings"""
        try:
            # Create tables
            self.db_service.create_json_mapping_tables()
            
            # Define comprehensive mappings for capitalized keys
            capitalized_mappings = [
                # Name mappings - Entity_Name maps to Legal_Name, Legal_Name stays as is
                {
                    "source_path": "payload.name.entity_name",
                    "target_path": "Legal_Name",
                    "semantic_meaning": "legal_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map Entity_Name to Legal_Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.name.legal_name",
                    "target_path": "Legal_Name",
                    "semantic_meaning": "legal_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Legal_Name stays as Legal_Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                # PDF field mappings - CD_LLC_Name, CD_Legal_Name, Entity Name all map to Legal_Name
                {
                    "source_path": "payload.name.legal_name",
                    "target_path": "CD_LLC_Name",
                    "semantic_meaning": "legal_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map legal_name to CD_LLC_Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.name.legal_name",
                    "target_path": "CD_Legal_Name",
                    "semantic_meaning": "legal_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map legal_name to CD_Legal_Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.name.legal_name",
                    "target_path": "Entity Name",
                    "semantic_meaning": "legal_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map legal_name to Entity Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.name.alternate_legal_name",
                    "target_path": "CD_Alternate_Legal_Name",
                    "semantic_meaning": "alternate_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Direct mapping of alternate_legal_name to CD_Alternate_Legal_Name",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                
                # Principal Address mappings - handle key replacements and multiple targets
                {
                    "source_path": "payload.principal_address.city",
                    "target_path": "PA_City",
                    "semantic_meaning": "city",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Principal address city mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.principal_address.city",
                    "target_path": "Principle city",
                    "semantic_meaning": "city",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map city to Principle city",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.principal_address.state",
                    "target_path": "PA_State",
                    "semantic_meaning": "state",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Principal address state mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.principal_address.state",
                    "target_path": "AK",
                    "semantic_meaning": "state",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map state to AK",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.principal_address.zip_code",
                    "target_path": "PA_Postal_Code",
                    "semantic_meaning": "zip_code",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Principal address postal code mapping",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.principal_address.street_address",
                    "target_path": "PA_Address_Line1",
                    "semantic_meaning": "street_address",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Principal address line 1 mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.principal_address.address_line_2",
                    "target_path": "PA_Address_Line2",
                    "semantic_meaning": "address_line2",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Principal address line 2 mapping",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                
                # Registered Agent mappings - handle key replacements and multiple targets
                {
                    "source_path": "payload.registered_agent.address.city",
                    "target_path": "RA_City",
                    "semantic_meaning": "city",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Registered agent city mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.city",
                    "target_path": "Register_Agent MI_city",
                    "semantic_meaning": "city",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map city to Register_Agent MI_city",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.city",
                    "target_path": "RA city",
                    "semantic_meaning": "city",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map city to RA city",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.state",
                    "target_path": "RA_State",
                    "semantic_meaning": "state",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Registered agent state mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.state",
                    "target_path": "Register_Agent MI_state",
                    "semantic_meaning": "state",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Map state to Register_Agent MI_state",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.state",
                    "target_path": "OH",
                    "semantic_meaning": "state",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Map state to OH",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.zip_code",
                    "target_path": "RA_Postal_Code",
                    "semantic_meaning": "zip_code",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Registered agent postal code mapping",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.zip_code",
                    "target_path": "Register_Agent MI_zip code",
                    "semantic_meaning": "zip_code",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Map zip_code to Register_Agent MI_zip code",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.zip_code",
                    "target_path": "RA zip",
                    "semantic_meaning": "zip_code",
                    "field_type": "address",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Map zip_code to RA zip",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.street_address",
                    "target_path": "RA_Address_Line1",
                    "semantic_meaning": "street_address",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Registered agent address line 1 mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.street_address",
                    "target_path": "Register_Agent MI_Address_line_1",
                    "semantic_meaning": "street_address",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map street_address to Register_Agent MI_Address_line_1",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.street_address",
                    "target_path": "RA address",
                    "semantic_meaning": "street_address",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map street_address to RA address",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.address.address_line_2",
                    "target_path": "RA_Address_Line2",
                    "semantic_meaning": "address_line2",
                    "field_type": "address",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Registered agent address line 2 mapping",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.keyPersonnelName",
                    "target_path": "RA_Name",
                    "semantic_meaning": "personnel_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Registered agent personnel name mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.keyPersonnelName",
                    "target_path": "Register Agent Name",
                    "semantic_meaning": "personnel_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map keyPersonnelName to Register Agent Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.keyPersonnelName",
                    "target_path": "RA Name",
                    "semantic_meaning": "personnel_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map keyPersonnelName to RA Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.keyPersonnelName",
                    "target_path": "statutoryAgent",
                    "semantic_meaning": "personnel_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map keyPersonnelName to statutoryAgent",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.emailId",
                    "target_path": "Email",
                    "semantic_meaning": "email",
                    "field_type": "email",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Registered agent email mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.emailId",
                    "target_path": "Register Agent email",
                    "semantic_meaning": "email",
                    "field_type": "email",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Map emailId to Register Agent email",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.contactNo",
                    "target_path": "Contact_No",
                    "semantic_meaning": "contact_number",
                    "field_type": "phone",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Registered agent contact number mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.registered_agent.contactNo",
                    "target_path": "Register_Agent MI_phone number",
                    "semantic_meaning": "contact_number",
                    "field_type": "phone",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Map contactNo to Register_Agent MI_phone number",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                }
            ]
            
            # Insert mappings into database
            self.db_service.insert_json_field_mappings(capitalized_mappings)
            
            self.logger.info(f"Initialized {len(capitalized_mappings)} capitalized mappings in database")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize capitalized mappings: {e}")
            raise
    
    def transform_payload_structure(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """Transform payload structure by replacing field names and flattening"""
        try:
            # First, capitalize all keys in the source JSON
            capitalized_source = self.capitalize_keys(source_json)
            
            # Extract payload from capitalized source
            source_payload = self.extract_payload_from_source(capitalized_source)
            
            # Create a complete source object including EntityType and State
            complete_source = {
                "Payload": source_payload,
                "EntityType": capitalized_source.get("1", {}).get("EntityType", {}),
                "State": capitalized_source.get("1", {}).get("State", {}),
                "OrderType": capitalized_source.get("1", {}).get("OrderType"),
                "FormProgress": capitalized_source.get("1", {}).get("FormProgress")
            }
            
            # Get database mappings
            db_mappings = self.db_service.get_all_json_mappings()
            
            # Create a flattened result with replaced field names
            result = {}
            
            # Apply database mappings to transform field names
            for db_mapping in db_mappings:
                user_field_path = db_mapping.source_path  # User input path like "payload.name.legal_name"
                pdf_field_name = db_mapping.target_path   # PDF field name like "CD_LLC_Name"
                
                # Get value from user input using path
                user_value = self._get_value_by_path(complete_source, user_field_path)
                
                if user_value is not None:
                    # Add to result with the PDF field name
                    result[pdf_field_name] = user_value
                    self.logger.debug(f"Transformed {user_field_path} -> {pdf_field_name}: {user_value}")
            
            # Also add direct mappings for common field replacements
            field_replacements = {
                "CD_Legal_Name": "Legal_Name",
                "CD_LLC_Name": "Legal_Name", 
                "CD_Alternate_Legal_Name": "Alternate_Legal_Name",
                "PA_City": "City",
                "PA_State": "State",
                "PA_Postal_Code": "Zip_Code",
                "PA_Address_Line1": "Street_Address",
                "PA_Address_Line2": "Address_Line_2",
                "RA_City": "City",
                "RA_State": "State", 
                "RA_Postal_Code": "Zip_Code",
                "RA_Address_Line1": "Street_Address",
                "RA_Address_Line2": "Address_Line_2",
                "RA_Name": "Name",
                "Email": "EmailId",
                "Contact_No": "ContactNo"
            }
            
            # Apply field name replacements
            for old_name, new_name in field_replacements.items():
                if old_name in result:
                    result[new_name] = result[old_name]
                    self.logger.debug(f"Field replacement: {old_name} -> {new_name}")
            
            self.logger.info(f"Transformed payload structure with {len(result)} fields")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to transform payload structure: {e}")
            raise 