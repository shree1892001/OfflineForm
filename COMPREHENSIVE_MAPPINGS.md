# Comprehensive JSON Mapping Support

## Overview
The database-driven mapping system now supports **ALL keys** from your provided JSON structure, making it fully extensible for adding more keys in the future.

## Supported JSON Keys

### 1. Order and Entity Information
```json
{
  "orderType": "Entity Formation",
  "EntityType": {
    "orderShortName": "LLC",
    "orderFullDesc": "LLC"
  }
}
```

### 2. State and Country Information
```json
{
  "State": {
    "stateShortName": "CL",
    "stateFullDesc": "newmexico",
    "stateUrl": "https://portal.sos.state.nm.us/BFS/online/Account",
    "filingWebsiteUsername": "redberyl",
    "filingWebsitePassword": "yD7?ddG0!$09",
    "countryMaster": {
      "countryShortName": "USA",
      "countryFullDesc": "United States Of America"
    }
  }
}
```

### 3. Entity Name Information
```json
{
  "name": {
    "legal_name": "Saumya",
    "alternate_legal_name": "Patra"
  }
}
```

### 4. Registered Agent Information
```json
{
  "registered_agent": {
    "Address": {
      "city": "Pune",
      "state ": 1,
      "zip_code": null,
      "address_line 2": "jdjdjjd",
      "street_address": "hadapsar"
    },
    "emailId": "saumya@gmail.com",
    "contactNo": 388383838,
    "keyPersonnelName": "Saumyaranjan Patra",
    "Billing Information": {
      "city ": "Pune",
      "emailId": "saumya@gmail.com",
      "stateId": 1,
      "contactNo": 838383883,
      "postalCode": null,
      "addressLine1": "hadapsar",
      "addressLine2": "djjdjjd",
      "keyPersonnelName": "Saumyaranjan Patra"
    },
    "Mailing Information": {
      "city": "Pune",
      "name": "Saumya",
      "state": 1,
      "zip_code": null,
      "contact_no": 38838383883,
      "email_address": "saumya@gmail.com",
      "address_line 2": "jdjjjd",
      "street_address": "hadapsar"
    }
  }
}
```

### 5. Principal Address Information
```json
{
  "principal_address": {
    "city": "Pune",
    "state": null,
    "zip_code": 412207,
    "address_line 2": "",
    "street_address": "hadapsar"
  }
}
```

### 6. Contact Information
```json
{
  "contact_information": {
    "name": "Saumyaranjan Patra",
    "Address": {
      "city": "Pune",
      "state ": 1,
      "zip_code": 41220,
      "address_line 2": "jdjdjjdj",
      "street_address": "hadapsar"
    },
    "contact_no": 83838383,
    "email address": "saumya@gmail.com"
  }
}
```

### 7. Organizer Information
```json
{
  "organizer_information": {
    "emailId": "saumya@gmail.com",
    "contactNo": 838383838,
    "keyPersonnelName": "saumya"
  }
}
```

### 8. Form Progress
```json
{
  "formProgress": 100
}
```

## Database Mappings Created

### Field Types Supported:
- **name**: Name-related fields with text validation
- **address**: Address fields with alphanumeric validation
- **contact**: Contact information fields
- **email**: Email fields with email validation
- **phone**: Phone number fields with phone validation
- **id**: ID and reference fields with numeric validation
- **url**: URL fields with URL validation
- **date**: Date fields with date validation
- **boolean**: Boolean and flag fields
- **numeric**: Numeric fields with number validation

### Semantic Meanings Supported:
- **legal_name**: Legal entity names
- **alternate_name**: Alternative business names
- **city**: City names
- **state**: State names or IDs
- **zip_code**: Postal/ZIP codes
- **street_address**: Street addresses
- **address_line2**: Secondary address lines
- **email**: Email addresses
- **contact_number**: Phone numbers
- **personnel_name**: Personnel names
- **billing_information**: Billing details
- **mailing_information**: Mailing details
- **order_type**: Order types
- **entity_type**: Entity types
- **state_info**: State information
- **country_info**: Country information
- **form_progress**: Form completion progress
- **creation_info**: Creation metadata

## Mapping Examples

### 1. Direct Field Mapping
```python
# Source: "name.legal_name" 
# Target: "data.Payload.Name.CD_Legal_Name"
# Semantic: "legal_name"
# Validation: Text only
```

### 2. Nested Object Mapping
```python
# Source: "registered_agent.Address.city"
# Target: "data.Payload.Registered_Agent.Address.RA_City"
# Semantic: "city"
# Validation: Text only
```

### 3. Numeric Field Mapping
```python
# Source: "registered_agent.contactNo"
# Target: "data.Payload.Registered_Agent.Name.Contact_No"
# Semantic: "contact_number"
# Validation: Numeric only
```

### 4. Complex Nested Mapping
```python
# Source: "registered_agent.Billing Information.addressLine1"
# Target: "data.Payload.Registered_Agent.Billing.Address_Line1"
# Semantic: "street_address"
# Validation: Alphanumeric
```

## Adding New Keys

### To add new keys, simply:

1. **Add to semantic meanings** (if new semantic type):
```python
"new_field_type": {
    "description": "Description of the field type",
    "category": "category_name",
    "synonyms": ["synonym1", "synonym2"],
    "business_domain": "domain_name"
}
```

2. **Add to field types** (if new validation needed):
```python
"new_type": {
    "description": "Description",
    "validation_patterns": [r'regex_pattern'],
    "business_context": "context"
}
```

3. **Add mapping rule**:
```python
{
    "source_path": "new.path.to.field",
    "target_path": "data.Target.Path",
    "semantic_meaning": "semantic_type",
    "field_type": "field_type",
    "data_type": "str/int/bool",
    "confidence": 1.0,
    "reasoning": "Mapping explanation",
    "is_required": True/False,
    "validation_rules": [r'regex_pattern'],
    "mapping_strategy": "database",
    "priority": 1
}
```

## Benefits

✅ **Complete Coverage**: All keys from your JSON are supported
✅ **Extensible**: Easy to add new keys without code changes
✅ **Validated**: Each field has appropriate validation rules
✅ **Semantic**: Fields are categorized by meaning and business context
✅ **Flexible**: Supports different data types (string, integer, boolean, null)
✅ **Nested**: Handles complex nested JSON structures
✅ **Business-Aware**: Understands entity formation domain context

## Usage

The system automatically:
1. **Extracts** all fields from your JSON
2. **Maps** them using database rules
3. **Validates** data according to field types
4. **Transforms** to target structure
5. **Provides** confidence scores and reasoning

This makes your system **100% database-driven** and **fully extensible** for any new JSON structures you need to support. 