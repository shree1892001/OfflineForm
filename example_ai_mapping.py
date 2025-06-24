import json
import yaml
from Utils.ai_json_mapper import AIJsonMapper

def main():
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create AI JSON mapper
    mapper = AIJsonMapper(config)
    
    # Your source JSON (the input structure)
    source_json = {
        "1": {
            "orderType": "Entity Formation",
            "EntityType": {
                "id": 1,
                "orderShortName": "LLC",
                "orderFullDesc": "LLC"
            },
            "State": {
                "id": 32,
                "stateShortName": "CL",
                "stateFullDesc": "newmexico"
            },
            "payload": {
                "name": {
                    "legal_name": "Saumya",
                    "alternate_legal_name": "Patra"
                },
                "registered_agent": {
                    "Address": {
                        "city": "Pune",
                        "state": 1,
                        "zip_code": None,
                        "address_line 2": "jdjdjjd",
                        "street_address": "hadapsar"
                    },
                    "emailId": "saumya@gmail.com",
                    "contactNo": 388383838,
                    "keyPersonnelName": "Saumyaranjan Patra"
                },
                "principal_address": {
                    "city": "Pune",
                    "state": None,
                    "zip_code": 412207,
                    "address_line 2": "",
                    "street_address": "hadapsar"
                },
                "contact_information": {
                    "name": "Saumyaranjan Patra",
                    "contact_no": 83838383,
                    "email address": "saumya@gmail.com"
                },
                "organizer_information": {
                    "emailId": "saumya@gmail.com",
                    "contactNo": 838383838,
                    "keyPersonnelName": "saumya"
                }
            },
            "formProgress": 100
        }
    }
    
    # Target template (the desired output structure)
    target_template = {
        "data": {
            "EntityType": {
                "id": None,
                "orderShortName": None,
                "orderFullDesc": None
            },
            "State": {
                "id": None,
                "stateShortName": None,
                "stateFullDesc": None
            },
            "Payload": {
                "Name": {
                    "CD_Legal_Name": None,
                    "CD_Alternate_Legal_Name": None
                },
                "Principal_Address": {
                    "PA_City": None,
                    "PA_State": None,
                    "PA_Postal_Code": None,
                    "PA_Address_Line1": None,
                    "PA_Address_Line2": None
                },
                "Registered_Agent": {
                    "Address": {
                        "RA_City": None,
                        "RA_State": None,
                        "RA_Postal_Code": None,
                        "RA_Address_Line1": None,
                        "RA_Address_Line2": None
                    },
                    "Name": {
                        "RA_Name": None,
                        "Email": None,
                        "Contact_No": None
                    }
                },
                "Organizer_Information": {
                    "Organizer_Details": {
                        "Org_Name": None,
                        "Og_Email": None,
                        "Og_Contact_No": None
                    },
                    "Org_Address": {
                        "Org_City": None,
                        "Org_State": None,
                        "Org_Postal_Code": None
                    }
                },
                "County": {
                    "CD_County": None
                }
            }
        }
    }
    
    print("Source JSON:")
    print(json.dumps(source_json, indent=2))
    print("\n" + "="*50 + "\n")
    
    # Transform using AI
    print("Transforming with AI...")
    result = mapper.transform_json_with_ai(source_json, target_template)
    
    print("Transformed JSON:")
    print(json.dumps(result, indent=2))
    print("\n" + "="*50 + "\n")
    
    # Get mapping analysis
    analysis = mapper.get_mapping_analysis(source_json, result)
    print("Mapping Analysis:")
    print(f"Source fields: {analysis['source_field_count']}")
    print(f"Target fields: {analysis['target_field_count']}")
    print(f"Mapping coverage: {analysis['mapping_coverage']:.2%}")
    
    # Example of enhancing with context
    print("\n" + "="*50 + "\n")
    print("Enhancing mapping with business context...")
    
    context = """
    This is for a business entity formation system. The data represents:
    - Legal entity information (LLC, Corporation, etc.)
    - Registered agent details (required for legal service)
    - Principal business address
    - Organizer/incorporator information
    - Contact details for business operations
    """
    
    enhanced_suggestions = mapper.enhance_mapping_with_context(source_json, context)
    print("AI Suggestions with Context:")
    print(json.dumps(enhanced_suggestions, indent=2))

if __name__ == "__main__":
    main() 