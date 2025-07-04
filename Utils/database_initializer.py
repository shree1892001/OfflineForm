import logging
from Services.MappingRulesDatabaseService import MappingRulesDatabaseService

def initialize_mapping_rules_database(config: dict):
    """
    Initialize the mapping rules database with all the base entities, attributes, and special cases
    """
    try:
        # Initialize database service
        db_service = MappingRulesDatabaseService(config)
        
        # Create tables
        db_service.create_tables()
        
        # Base entities data - these are the main entity types
        base_entities = {
            "RA": "Registered Agent",
            "Dr": "Director", 
            "P": "Principal Address",
            "Inc": "Incorporator",
            "Mom": "Member or Manager",
            "MOM": "Member or Manager",
            "PA": "Principal Address",
        }
        
        # Attributes data - these are the different types of information
        attributes = {
            "zip": "Zip Code",
            "Zip": "Zip Code", 
            "st": "State",
            "S": "State",
            "city": "City",
            "state": "State",
            "Address line 1": "street address",
            "Address line 2": "Address Line 2",
            "Address Zip Code": "Address Zip Code",
            "Mailing address": "Mailing Address",
        }
        
        # Special cases data - these are specific field mappings that don't follow the pattern
        special_cases = {
            "RAMAZ": "RA mailing Address zip code",
            "DS": "Director State",
            "RS": "Registered Agent state", 
            "PS": "Principal Address state",
            "IS": "Incorporator State",
            "PZIP": "Principal Address Zip Code",
            "RA MailingAdd zip": "RA mailing Address zip code",
            "Entity Name": "Legal Name",
            "RA Zip": "Register Agent Zip Code",
            "RA Address city": "Registered Agent City"
        }
        
        # Insert data into database tables
        print("Inserting base entities...")
        db_service.insert_base_entities(base_entities)
        
        print("Inserting attributes...")
        db_service.insert_attributes(attributes)
        
        print("Inserting special cases...")
        db_service.insert_special_cases(special_cases)
        
        print("Database initialization completed successfully!")
        
        # Verify the data was inserted correctly
        print("\nVerifying data insertion...")
        mapping_rules = db_service.get_all_mapping_rules()
        print(f"Total mapping rules generated: {len(mapping_rules)}")
        
        # Show some examples of generated rules
        print("\nSample generated mapping rules:")
        sample_rules = list(mapping_rules.items())[:10]
        for placeholder, mapped_value in sample_rules:
            print(f"  '{placeholder}' -> '{mapped_value}'")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        logging.error(f"Failed to initialize database: {e}")
        raise

if __name__ == "__main__":
    # Load config
    import yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize database
    initialize_mapping_rules_database(config)
 