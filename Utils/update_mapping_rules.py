import yaml
from Services.MappingRulesDatabaseService import MappingRulesDatabaseService

def update_mapping_rules():
    """Update existing mapping rules with corrected field names"""
    try:
        # Load config
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize database service
        db_service = MappingRulesDatabaseService(config)
        
        # Updated special cases with correct JSON field names
        updated_special_cases = {
            "RAMAZ": "Registered Agent Mailing Information Zip Code",
            "DS": "Director State",
            "RS": "Registered Agent State", 
            "PS": "Principal Address State",
            "IS": "Incorporator State",
            "PZIP": "Principal Address Zip Code",
            "RA MailingAdd zip": "Registered Agent Mailing Information Zip Code",
            "Entity Name": "Legal Name",
            "RA Zip": "Registered Agent Zip Code",
            "RA Address city": "Registered Agent City",
            "Register Agent MI_state": "Registered Agent Mailing Information State"
        }
        
        # Clear existing special cases and insert updated ones
        print("Updating special cases in database...")
        
        # Delete all existing special cases
        cursor = db_service.db_connection.get_cursor()
        cursor.execute("DELETE FROM special_cases")
        db_service.db_connection.get_connection().commit()
        cursor.close()
        
        # Insert updated special cases
        db_service.insert_special_cases(updated_special_cases)
        
        print("Mapping rules updated successfully!")
        
        # Verify the update
        mapping_rules = db_service.get_all_mapping_rules()
        print(f"Total mapping rules: {len(mapping_rules)}")
        
        # Show the specific rule that was causing the issue
        if "Register Agent MI_state" in mapping_rules:
            print(f"Updated rule: 'Register Agent MI_state' -> '{mapping_rules['Register Agent MI_state']}'")
        
    except Exception as e:
        print(f"Error updating mapping rules: {e}")
        raise

if __name__ == "__main__":
    update_mapping_rules() 