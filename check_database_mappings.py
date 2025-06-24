#!/usr/bin/env python3
"""
Direct database check to verify mappings are stored and accessible
"""

import yaml
import json
from Services.JsonMappingDatabaseService import JsonMappingDatabaseService
from Services.DatabaseConnectionService import DatabaseConnectionService

def check_database_mappings():
    """Check if mappings are actually stored in the database"""
    print("🔍 Checking Database Mappings Directly")
    print("=" * 60)
    
    # Load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Create direct database connection
    db_connection = DatabaseConnectionService(config)
    
    try:
        # Check if json_field_mappings table exists and has data
        print("\n1. Checking json_field_mappings table:")
        query = "SELECT COUNT(*) FROM json_field_mappings"
        result = db_connection.execute_query(query)
        
        if result:
            count = result[0][0]
            print(f"✅ Found {count} mappings in json_field_mappings table")
            
            if count > 0:
                # Show some sample mappings
                sample_query = "SELECT source_path, target_path, semantic_meaning FROM json_field_mappings LIMIT 5"
                samples = db_connection.execute_query(sample_query)
                print("Sample mappings:")
                for sample in samples:
                    print(f"  - {sample[0]} -> {sample[1]} (semantic: {sample[2]})")
        else:
            print("❌ No mappings found in json_field_mappings table")
        
        # Check for legal_name specifically
        print("\n2. Checking for legal_name mappings specifically:")
        query = "SELECT source_path, target_path, semantic_meaning FROM json_field_mappings WHERE semantic_meaning = 'legal_name' OR source_path LIKE '%legal_name%'"
        rows = db_connection.execute_query(query)
        
        if rows:
            print(f"Found {len(rows)} legal_name related mappings:")
            for row in rows:
                source_path, target_path, semantic_meaning = row
                print(f"  - {source_path} -> {target_path} (semantic: {semantic_meaning})")
        else:
            print("❌ No legal_name mappings found in database!")
        
        # Check if tables exist
        print("\n3. Checking if tables exist:")
        tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('semantic_meanings', 'json_field_mappings', 'field_types')
        """
        tables = db_connection.execute_query(tables_query)
        
        if tables:
            print("Tables found:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("❌ No mapping tables found!")
        
        # Check table structure
        print("\n4. Checking table structure:")
        for table_name in ['semantic_meanings', 'json_field_mappings']:
            try:
                structure_query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
                columns = db_connection.execute_query(structure_query)
                print(f"\n{table_name} table structure:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            except Exception as e:
                print(f"❌ Error checking {table_name} structure: {e}")
        
        # Test JSON mapping service
        print("\n5. Testing JSON mapping service:")
        try:
            json_db_service = JsonMappingDatabaseService(config)
            mappings = json_db_service.get_all_json_mappings()
            print(f"✅ JSON mapping service returned {len(mappings)} mappings")
            
            if mappings:
                print("Sample mappings from service:")
                for mapping in mappings[:3]:
                    print(f"  - {mapping.source_path} -> {mapping.target_path}")
        except Exception as e:
            print(f"❌ Error with JSON mapping service: {e}")
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
    finally:
        db_connection.close_connection()
    
    print("\n" + "=" * 60)
    print("Database check completed!")

if __name__ == "__main__":
    check_database_mappings() 