import logging
from typing import Dict, List, Optional
from Utils.DatabaseConnection import DatabaseConnection

class MappingRulesDatabaseService:
    def __init__(self, config: Dict):
        """
        Initialize the database service with PostgreSQL configuration
        """
        self.config = config
        self.db_connection = DatabaseConnection(config)
        self.logger = logging.getLogger(__name__)
        
    def create_tables(self):
        """Create necessary tables for mapping rules"""
        try:
            # Create base_entities table
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS base_entities (
                    id SERIAL PRIMARY KEY,
                    abbreviation VARCHAR(50) UNIQUE NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """, fetch=False)
            
            # Create attributes table
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS attributes (
                    id SERIAL PRIMARY KEY,
                    abbreviation VARCHAR(50) UNIQUE NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """, fetch=False)
            
            # Create special_cases table
            self.db_connection.execute_query("""
                CREATE TABLE IF NOT EXISTS special_cases (
                    id SERIAL PRIMARY KEY,
                    placeholder VARCHAR(100) UNIQUE NOT NULL,
                    mapped_value VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """, fetch=False)
            
            self.logger.info("Tables created successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to create tables: {e}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            raise
    
    def clear_all_data(self):
        """Clear all data from all tables"""
        try:
            # Clear special cases
            self.db_connection.execute_query("DELETE FROM special_cases", fetch=False)
            
            # Clear attributes
            self.db_connection.execute_query("DELETE FROM attributes", fetch=False)
            
            # Clear base entities
            self.db_connection.execute_query("DELETE FROM base_entities", fetch=False)
            
            self.logger.info("All data cleared from database tables")
            
        except Exception as e:
            self.logger.error(f"Failed to clear data: {e}")
            raise
    
    def insert_base_entities(self, entities: Dict[str, str]):
        """Insert base entities into the database"""
        try:
            # Clear existing data first
            self.db_connection.execute_query("DELETE FROM base_entities", fetch=False)
            
            query = """
                INSERT INTO base_entities (abbreviation, full_name)
                VALUES (%s, %s)
                ON CONFLICT (abbreviation) DO UPDATE SET
                full_name = EXCLUDED.full_name
            """
            
            params_list = [(abbr, full_name) for abbr, full_name in entities.items()]
            self.db_connection.execute_many(query, params_list)
            
            self.logger.info(f"Inserted {len(entities)} base entities")
            
        except Exception as e:
            self.logger.error(f"Failed to insert base entities: {e}")
            raise
    
    def insert_attributes(self, attributes: Dict[str, str]):
        """Insert attributes into the database"""
        try:
            # Clear existing data first
            self.db_connection.execute_query("DELETE FROM attributes", fetch=False)
            
            query = """
                INSERT INTO attributes (abbreviation, full_name)
                VALUES (%s, %s)
                ON CONFLICT (abbreviation) DO UPDATE SET
                full_name = EXCLUDED.full_name
            """
            
            params_list = [(abbr, full_name) for abbr, full_name in attributes.items()]
            self.db_connection.execute_many(query, params_list)
            
            self.logger.info(f"Inserted {len(attributes)} attributes")
            
        except Exception as e:
            self.logger.error(f"Failed to insert attributes: {e}")
            raise
    
    def insert_special_cases(self, special_cases: Dict[str, str]):
        """Insert special cases into the database"""
        try:
            # Clear existing data first
            self.db_connection.execute_query("DELETE FROM special_cases", fetch=False)
            
            query = """
                INSERT INTO special_cases (placeholder, mapped_value)
                VALUES (%s, %s)
                ON CONFLICT (placeholder) DO UPDATE SET
                mapped_value = EXCLUDED.mapped_value
            """
            
            params_list = [(placeholder, mapped_value) for placeholder, mapped_value in special_cases.items()]
            self.db_connection.execute_many(query, params_list)
            
            self.logger.info(f"Inserted {len(special_cases)} special cases")
            
        except Exception as e:
            self.logger.error(f"Failed to insert special cases: {e}")
            raise
    
    def get_all_mapping_rules(self) -> Dict[str, str]:
        """Get all mapping rules from database"""
        try:
            # Get base entities and attributes
            query = """
                SELECT be.abbreviation as entity_abbr, be.full_name as entity_name,
                       a.abbreviation as attr_abbr, a.full_name as attr_name
                FROM base_entities be
                CROSS JOIN attributes a
            """
            
            rows = self.db_connection.execute_query(query)
            
            generated_rules = {}
            for row in rows:
                entity_abbr = row[0]  # abbreviation
                entity_name = row[1]  # full_name
                attr_abbr = row[2]    # abbreviation
                attr_name = row[3]    # full_name
                
                # Generate different combinations
                generated_rules[f"{entity_abbr} {attr_abbr}"] = f"{entity_name} {attr_name}"
                generated_rules[f"{entity_abbr} {attr_abbr.lower()}"] = f"{entity_name} {attr_name}"
                
                if not attr_abbr.islower():
                    generated_rules[f"{entity_abbr}{attr_abbr}"] = f"{entity_name} {attr_name}"
                generated_rules[f"{entity_abbr}{attr_abbr.lower()}"] = f"{entity_name} {attr_name}"
            
            # Get special cases
            special_cases_query = "SELECT placeholder, mapped_value FROM special_cases"
            special_cases_rows = self.db_connection.execute_query(special_cases_query)
            special_cases = {row[0]: row[1] for row in special_cases_rows}
            
            # Combine generated rules with special cases
            generated_rules.update(special_cases)
            
            return generated_rules
            
        except Exception as e:
            self.logger.error(f"Failed to get mapping rules: {e}")
            raise
    
    def add_mapping_rule(self, placeholder: str, mapped_value: str):
        """Add a new mapping rule"""
        try:
            query = """
                INSERT INTO special_cases (placeholder, mapped_value)
                VALUES (%s, %s)
                ON CONFLICT (placeholder) DO UPDATE SET
                mapped_value = EXCLUDED.mapped_value
            """
            
            self.db_connection.execute_query(query, (placeholder, mapped_value), fetch=False)
            self.logger.info(f"Added mapping rule: {placeholder} -> {mapped_value}")
            
        except Exception as e:
            self.logger.error(f"Failed to add mapping rule: {e}")
            raise
    
    def delete_mapping_rule(self, placeholder: str):
        """Delete a mapping rule"""
        try:
            query = "DELETE FROM special_cases WHERE placeholder = %s"
            self.db_connection.execute_query(query, (placeholder,), fetch=False)
            self.logger.info(f"Deleted mapping rule: {placeholder}")
            
        except Exception as e:
            self.logger.error(f"Failed to delete mapping rule: {e}")
            raise
    
    def close_connection(self):
        """Close database connection"""
        self.db_connection.close_connection() 