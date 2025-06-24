#!/usr/bin/env python3
"""
Simple database check to verify mappings are properly database-driven
"""

import yaml
import json
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService

def check_database_mappings():
    """Check if mappings are properly database-driven"""
    print("🔍 Checking Database-Driven Mappings")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    try:
        # Initialize the JSON mapping database service
        json_db_service = JsonMappingDatabaseService(config)
        
        # Create tables if they don't exist
        print("1. Creating/checking database tables...")
        json_db_service.create_json_mapping_tables()
        print("✅ Database tables ready")
        
        # Get all mappings from database
        print("\n2. Getting all mappings from database...")
        mappings = json_db_service.get_all_json_mappings()
        print(f"✅ Found {len(mappings)} mappings in database")
        
        if mappings:
            print("\nSample mappings from database:")
            for i, mapping in enumerate(mappings[:10]):
                print(f"  {i+1}. {mapping.source_path} -> {mapping.target_path}")
                print(f"     Semantic: {mapping.semantic_meaning}, Type: {mapping.field_type.value}")
                print(f"     Strategy: {mapping.mapping_strategy}, Confidence: {mapping.confidence}")
                print()
            
            if len(mappings) > 10:
                print(f"  ... and {len(mappings) - 10} more mappings")
        else:
            print("❌ No mappings found in database!")
            print("Initializing default mappings...")
            
            # Initialize default mappings
            from Utils.capitalized_json_mapper import CapitalizedJsonMapper
            mapper = CapitalizedJsonMapper(config)
            mapper.initialize_capitalized_mappings()
            
            # Check again
            mappings = json_db_service.get_all_json_mappings()
            print(f"✅ Now found {len(mappings)} mappings in database")
        
        # Test specific mappings
        print("\n3. Testing specific field mappings:")
        test_fields = [
            ("payload.name.legal_name", "CD_Legal_Name"),
            ("payload.address.city", "PA_City"),
            ("payload.contact.emailId", "Email"),
            ("payload.registered_agent.keyPersonnelName", "RA_Name")
        ]
        
        for source_path, target_path in test_fields:
            # Find mapping in database
            found_mapping = None
            for mapping in mappings:
                if mapping.source_path == source_path and mapping.target_path == target_path:
                    found_mapping = mapping
                    break
            
            if found_mapping:
                print(f"✅ Found mapping: {source_path} -> {target_path}")
                print(f"   Semantic: {found_mapping.semantic_meaning}")
                print(f"   Strategy: {found_mapping.mapping_strategy}")
            else:
                print(f"❌ Missing mapping: {source_path} -> {target_path}")
        
        # Test the mapping service with sample data
        print("\n4. Testing mapping service with sample data:")
        sample_user_json = {
            "1": {
                "Payload": {
                    "name": {
                        "legal_name": "Test Company LLC"
                    },
                    "address": {
                        "city": "New York"
                    },
                    "contact": {
                        "emailId": "test@example.com"
                    }
                }
            }
        }
        
        # Test database-driven mapping
        from Services.FillOfflinePdf import FillOfflinePdf
        pdf_filler = FillOfflinePdf()
        
        form_keys = [
            {"key": "CD_Legal_Name"},
            {"key": "PA_City"},
            {"key": "Email"}
        ]
        
        print("Testing database-driven mapping...")
        result = pdf_filler.generate_data_dict_with_ai_mapping(form_keys, sample_user_json)
        
        print("Mapping result:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        
        # Check if mappings are actually being used
        mapped_count = len([v for v in result.values() if v])
        print(f"\n📊 Database mapping effectiveness: {mapped_count}/{len(result)} fields mapped")
        
        if mapped_count > 0:
            print("✅ Database-driven mapping is working!")
        else:
            print("❌ Database-driven mapping is not working properly")
        
    except Exception as e:
        print(f"❌ Error checking database mappings: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            json_db_service.close_connection()
        except:
            pass
    
    print("\n" + "=" * 60)
    print("Database check completed!")

if __name__ == "__main__":
    check_database_mappings() 