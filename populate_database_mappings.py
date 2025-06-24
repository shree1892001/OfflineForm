#!/usr/bin/env python3
"""
Script to populate the database with JSON field mappings
"""

import yaml
import logging
from Utils.capitalized_json_mapper import CapitalizedJsonMapper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def populate_database_mappings():
    """Populate the database with JSON field mappings"""
    try:
        # Load configuration
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        logger.info("Configuration loaded successfully")
        
        # Initialize capitalized mapper
        mapper = CapitalizedJsonMapper(config)
        logger.info("Capitalized JSON Mapper initialized")
        
        # Initialize capitalized mappings in database
        mapper.initialize_capitalized_mappings()
        logger.info("✅ Database populated with capitalized mappings successfully!")
        
        # Verify the mappings were inserted
        mappings = mapper.db_service.get_all_json_mappings()
        logger.info(f"✅ Verified {len(mappings)} mappings are now in the database")
        
        # Show some sample mappings
        print("\n" + "="*60)
        print("SAMPLE MAPPINGS INSERTED INTO DATABASE")
        print("="*60)
        
        for i, mapping in enumerate(mappings[:10]):  # Show first 10
            print(f"{i+1}. {mapping.source_path} -> {mapping.target_path}")
            print(f"   Semantic: {mapping.semantic_meaning}")
            print(f"   Type: {mapping.field_type}")
            print()
        
        if len(mappings) > 10:
            print(f"... and {len(mappings) - 10} more mappings")
        
        print("="*60)
        print("✅ Database population completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to populate database mappings: {e}")
        raise

if __name__ == "__main__":
    populate_database_mappings() 