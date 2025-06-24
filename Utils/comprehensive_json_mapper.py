import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.CallAiService import CallAiService

class ComprehensiveJsonMapper:
    """
    Comprehensive JSON mapper that handles all field mappings between source and target JSON structures
    Supports various naming conventions, semantic matching, and custom mappings
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.db_service = JsonMappingDatabaseService(config)
        self.ai_service = CallAiService(config)
        self.logger = logging.getLogger(__name__)
        
        # Define comprehensive field mappings for your specific use case
        self.field_mappings = {
            # Name mappings
            "legal_name": ["CD_Legal_Name", "CD_LLC_Name", "CD_Entity_Name"],
            "alternate_legal_name": ["CD_Alternate_Legal_Name", "CD_DBA_Name"],
            
            # Address mappings
            "city": ["PA_City", "RA_City", "Org_City", "Billing_City", "Mailing_City"],
            "state": ["PA_State", "RA_State", "Org_State", "Billing_State", "Mailing_State"],
            "zip_code": ["PA_Postal_Code", "RA_Postal_Code", "Org_Postal_Code", "Billing_Postal_Code"],
            "street_address": ["PA_Address_Line1", "RA_Address_Line1", "Org_Address_Line1"],
            "address_line 2": ["PA_Address_Line2", "RA_Address_Line2", "Org_Address_Line2"],
            "addressLine1": ["PA_Address_Line1", "RA_Address_Line1", "Org_Address_Line1"],
            "addressLine2": ["PA_Address_Line2", "RA_Address_Line2", "Org_Address_Line2"],
            
            # Contact mappings
            "emailId": ["Email", "Og_Email", "Billing_Email", "Mailing_Email"],
            "email address": ["Email", "Og_Email", "Billing_Email", "Mailing_Email"],
            "email_address": ["Email", "Og_Email", "Billing_Email", "Mailing_Email"],
            "contactNo": ["Contact_No", "Og_Contact_No", "Billing_Contact_No"],
            "contact_no": ["Contact_No", "Og_Contact_No", "Billing_Contact_No"],
            "postalCode": ["PA_Postal_Code", "RA_Postal_Code", "Org_Postal_Code"],
            
            # Personnel mappings
            "keyPersonnelName": ["RA_Name", "Org_Name", "Contact_Name"],
            "name": ["RA_Name", "Org_Name", "Contact_Name", "Mailing_Name"],
            
            # Entity and State mappings
            "orderType": ["OrderType"],
            "orderShortName": ["ShortName"],
            "orderFullDesc": ["FullDescription"],
            "stateShortName": ["ShortName"],
            "stateFullDesc": ["FullDescription"],
            "stateUrl": ["Url"],
            "filingWebsiteUsername": ["FilingUsername"],
            "filingWebsitePassword": ["FilingPassword"],
            "countryShortName": ["ShortName"],
            "countryFullDesc": ["FullDescription"],
            
            # Metadata mappings
            "createdBy": ["CreatedBy"],
            "creationDate": ["CreationDate"],
            "lastModifiedBy": ["LastModifiedBy"],
            "lastModifiedDate": ["LastModifiedDate"],
            "id": ["Id"],
            "formProgress": ["FormProgress"]
        }
        
        # Define context-based mapping rules
        self.context_mappings = {
            "payload.name": {
                "legal_name": "data.Payload.Name.CD_Legal_Name",
                "alternate_legal_name": "data.Payload.Name.CD_Alternate_Legal_Name"
            },
            "payload.principal_address": {
                "city": "data.Payload.Principal_Address.PA_City",
                "state": "data.Payload.Principal_Address.PA_State",
                "zip_code": "data.Payload.Principal_Address.PA_Postal_Code",
                "street_address": "data.Payload.Principal_Address.PA_Address_Line1",
                "address_line 2": "data.Payload.Principal_Address.PA_Address_Line2"
            },
            "payload.registered_agent.Address": {
                "city": "data.Payload.Registered_Agent.Address.RA_City",
                "state ": "data.Payload.Registered_Agent.Address.RA_State",
                "zip_code": "data.Payload.Registered_Agent.Address.RA_Postal_Code",
                "street_address": "data.Payload.Registered_Agent.Address.RA_Address_Line1",
                "address_line 2": "data.Payload.Registered_Agent.Address.RA_Address_Line2"
            },
            "payload.registered_agent": {
                "emailId": "data.Payload.Registered_Agent.Name.Email",
                "contactNo": "data.Payload.Registered_Agent.Name.Contact_No",
                "keyPersonnelName": "data.Payload.Registered_Agent.Name.RA_Name"
            },
            "payload.registered_agent.Billing Information": {
                "city ": "data.Payload.Registered_Agent.Billing.City",
                "emailId": "data.Payload.Registered_Agent.Billing.Email",
                "stateId": "data.Payload.Registered_Agent.Billing.State",
                "contactNo": "data.Payload.Registered_Agent.Billing.Contact_No",
                "postalCode": "data.Payload.Registered_Agent.Billing.Postal_Code",
                "addressLine1": "data.Payload.Registered_Agent.Billing.Address_Line1",
                "addressLine2": "data.Payload.Registered_Agent.Billing.Address_Line2",
                "keyPersonnelName": "data.Payload.Registered_Agent.Billing.Personnel_Name"
            },
            "payload.registered_agent.Mailing Information": {
                "city": "data.Payload.Registered_Agent.Mailing.City",
                "name": "data.Payload.Registered_Agent.Mailing.Name",
                "state": "data.Payload.Registered_Agent.Mailing.State",
                "zip_code": "data.Payload.Registered_Agent.Mailing.Postal_Code",
                "contact_no": "data.Payload.Registered_Agent.Mailing.Contact_No",
                "email_address": "data.Payload.Registered_Agent.Mailing.Email",
                "address_line 2": "data.Payload.Registered_Agent.Mailing.Address_Line2",
                "street_address": "data.Payload.Registered_Agent.Mailing.Address_Line1"
            },
            "payload.contact_information": {
                "name": "data.Payload.Organizer_Information.Organizer_Details.Org_Name",
                "contact_no": "data.Payload.Organizer_Information.Organizer_Details.Og_Contact_No",
                "email address": "data.Payload.Organizer_Information.Organizer_Details.Og_Email"
            },
            "payload.contact_information.Address": {
                "city": "data.Payload.Organizer_Information.Org_Address.Org_City",
                "state ": "data.Payload.Organizer_Information.Org_Address.Org_State",
                "zip_code": "data.Payload.Organizer_Information.Org_Address.Org_Postal_Code",
                "address_line 2": "data.Payload.Organizer_Information.Org_Address.Org_Address_Line2",
                "street_address": "data.Payload.Organizer_Information.Org_Address.Org_Address_Line1"
            },
            "payload.organizer_information": {
                "emailId": "data.Payload.Organizer_Information.Organizer_Details.Og_Email",
                "contactNo": "data.Payload.Organizer_Information.Organizer_Details.Og_Contact_No",
                "keyPersonnelName": "data.Payload.Organizer_Information.Organizer_Details.Org_Name"
            },
            "EntityType": {
                "createdBy": "data.EntityType.CreatedBy",
                "creationDate": "data.EntityType.CreationDate",
                "lastModifiedBy": "data.EntityType.LastModifiedBy",
                "lastModifiedDate": "data.EntityType.LastModifiedDate",
                "id": "data.EntityType.Id",
                "orderShortName": "data.EntityType.ShortName",
                "orderFullDesc": "data.EntityType.FullDescription"
            },
            "State": {
                "createdBy": "data.State.CreatedBy",
                "creationDate": "data.State.CreationDate",
                "lastModifiedBy": "data.State.LastModifiedBy",
                "lastModifiedDate": "data.State.LastModifiedDate",
                "id": "data.State.Id",
                "stateShortName": "data.State.ShortName",
                "stateFullDesc": "data.State.FullDescription",
                "stateUrl": "data.State.Url",
                "filingWebsiteUsername": "data.State.FilingUsername",
                "filingWebsitePassword": "data.State.FilingPassword"
            },
            "State.countryMaster": {
                "createdBy": "data.State.Country.CreatedBy",
                "creationDate": "data.State.Country.CreationDate",
                "lastModifiedBy": "data.State.Country.LastModifiedBy",
                "lastModifiedDate": "data.State.Country.LastModifiedDate",
                "id": "data.State.Country.Id",
                "countryShortName": "data.State.Country.ShortName",
                "countryFullDesc": "data.State.Country.FullDescription"
            }
        }
    
    def extract_payload_from_source(self, source_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extract payload from the nested source JSON structure"""
        # Handle the nested structure where payload is inside a numbered key
        for key, value in source_json.items():
            if isinstance(value, dict) and 'payload' in value:
                return value['payload']
        return source_json.get('payload', {})
    
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
        """Find the best mapping for a source field"""
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
                    # Find the full target path
                    for path, _ in target_paths:
                        if path.split('.')[-1] == target_field:
                            return path
        
        return None
    
    def transform_json(self, source_json: Dict[str, Any], target_template: Dict[str, Any]) -> Dict[str, Any]:
        """Transform source JSON to target structure"""
        try:
            # Extract payload from source
            source_payload = self.extract_payload_from_source(source_json)
            
            # Create a complete source object including EntityType and State
            complete_source = {
                "payload": source_payload,
                "EntityType": source_json.get("1", {}).get("EntityType", {}),
                "State": source_json.get("1", {}).get("State", {}),
                "orderType": source_json.get("1", {}).get("orderType"),
                "formProgress": source_json.get("1", {}).get("formProgress")
            }
            
            # Extract all source fields
            source_fields = self.extract_all_field_paths(complete_source)
            
            # Create result by copying target template
            result = json.loads(json.dumps(target_template))
            
            # Apply mappings
            mappings_applied = []
            
            for source_path, source_value in source_fields:
                if source_value is not None:
                    target_path = self.find_best_mapping(source_path, source_value, target_template)
                    
                    if target_path:
                        self._set_value_by_path(result, target_path, source_value)
                        mappings_applied.append({
                            'source_path': source_path,
                            'target_path': target_path,
                            'value': source_value
                        })
                        self.logger.debug(f"Mapped {source_path} -> {target_path}: {source_value}")
            
            self.logger.info(f"Applied {len(mappings_applied)} mappings")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to transform JSON: {e}")
            raise
    
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
        source_payload = self.extract_payload_from_source(source_json)
        complete_source = {
            "payload": source_payload,
            "EntityType": source_json.get("1", {}).get("EntityType", {}),
            "State": source_json.get("1", {}).get("State", {}),
            "orderType": source_json.get("1", {}).get("orderType"),
            "formProgress": source_json.get("1", {}).get("formProgress")
        }
        
        source_fields = self.extract_all_field_paths(complete_source)
        target_fields = self.extract_all_field_paths(target_json)
        
        mappings = []
        unmapped_source = []
        
        for source_path, source_value in source_fields:
            if source_value is not None:
                target_path = self.find_best_mapping(source_path, source_value, target_json)
                if target_path:
                    mappings.append({
                        'source_path': source_path,
                        'target_path': target_path,
                        'source_value': source_value
                    })
                else:
                    unmapped_source.append((source_path, source_value))
        
        return {
            'total_source_fields': len(source_fields),
            'total_target_fields': len(target_fields),
            'mapped_fields': len(mappings),
            'mapping_accuracy': len(mappings) / len(source_fields) if source_fields else 0,
            'mappings': mappings,
            'unmapped_source_fields': unmapped_source
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
    
    def initialize_comprehensive_mappings(self):
        """Initialize database with comprehensive mappings for your use case"""
        try:
            # Create tables
            self.db_service.create_json_mapping_tables()
            
            # Define comprehensive mappings
            comprehensive_mappings = [
                # Name mappings
                {
                    "source_path": "payload.name.legal_name",
                    "target_path": "data.Payload.Name.CD_Legal_Name",
                    "semantic_meaning": "legal_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Direct mapping of legal name to CD_Legal_Name",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.name.alternate_legal_name",
                    "target_path": "data.Payload.Name.CD_Alternate_Legal_Name",
                    "semantic_meaning": "alternate_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Direct mapping of alternate legal name",
                    "is_required": False,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                
                # Principal Address mappings
                {
                    "source_path": "payload.principal_address.city",
                    "target_path": "data.Payload.Principal_Address.PA_City",
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
                    "source_path": "payload.principal_address.state",
                    "target_path": "data.Payload.Principal_Address.PA_State",
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
                    "source_path": "payload.principal_address.zip_code",
                    "target_path": "data.Payload.Principal_Address.PA_Postal_Code",
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
                    "target_path": "data.Payload.Principal_Address.PA_Address_Line1",
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
                    "source_path": "payload.principal_address.address_line 2",
                    "target_path": "data.Payload.Principal_Address.PA_Address_Line2",
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
                
                # Registered Agent mappings
                {
                    "source_path": "payload.registered_agent.Address.city",
                    "target_path": "data.Payload.Registered_Agent.Address.RA_City",
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
                    "source_path": "payload.registered_agent.Address.state ",
                    "target_path": "data.Payload.Registered_Agent.Address.RA_State",
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
                    "source_path": "payload.registered_agent.Address.zip_code",
                    "target_path": "data.Payload.Registered_Agent.Address.RA_Postal_Code",
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
                    "source_path": "payload.registered_agent.Address.street_address",
                    "target_path": "data.Payload.Registered_Agent.Address.RA_Address_Line1",
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
                    "source_path": "payload.registered_agent.Address.address_line 2",
                    "target_path": "data.Payload.Registered_Agent.Address.RA_Address_Line2",
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
                    "target_path": "data.Payload.Registered_Agent.Name.RA_Name",
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
                    "source_path": "payload.registered_agent.emailId",
                    "target_path": "data.Payload.Registered_Agent.Name.Email",
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
                    "source_path": "payload.registered_agent.contactNo",
                    "target_path": "data.Payload.Registered_Agent.Name.Contact_No",
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
                
                # Organizer Information mappings
                {
                    "source_path": "payload.organizer_information.keyPersonnelName",
                    "target_path": "data.Payload.Organizer_Information.Organizer_Details.Org_Name",
                    "semantic_meaning": "personnel_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Organizer personnel name mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.organizer_information.emailId",
                    "target_path": "data.Payload.Organizer_Information.Organizer_Details.Og_Email",
                    "semantic_meaning": "email",
                    "field_type": "email",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Organizer email mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                {
                    "source_path": "payload.organizer_information.contactNo",
                    "target_path": "data.Payload.Organizer_Information.Organizer_Details.Og_Contact_No",
                    "semantic_meaning": "contact_number",
                    "field_type": "phone",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Organizer contact number mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 1
                },
                
                # Contact Information mappings
                {
                    "source_path": "payload.contact_information.name",
                    "target_path": "data.Payload.Organizer_Information.Organizer_Details.Org_Name",
                    "semantic_meaning": "personnel_name",
                    "field_type": "name",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Contact information name mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 2
                },
                {
                    "source_path": "payload.contact_information.email address",
                    "target_path": "data.Payload.Organizer_Information.Organizer_Details.Og_Email",
                    "semantic_meaning": "email",
                    "field_type": "email",
                    "data_type": "str",
                    "confidence": 1.0,
                    "reasoning": "Contact information email mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 2
                },
                {
                    "source_path": "payload.contact_information.contact_no",
                    "target_path": "data.Payload.Organizer_Information.Organizer_Details.Og_Contact_No",
                    "semantic_meaning": "contact_number",
                    "field_type": "phone",
                    "data_type": "int",
                    "confidence": 1.0,
                    "reasoning": "Contact information contact number mapping",
                    "is_required": True,
                    "validation_rules": [],
                    "mapping_strategy": "database",
                    "priority": 2
                }
            ]
            
            # Insert mappings into database
            self.db_service.insert_json_field_mappings(comprehensive_mappings)
            
            self.logger.info(f"Initialized {len(comprehensive_mappings)} comprehensive mappings")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize comprehensive mappings: {e}")
            raise 