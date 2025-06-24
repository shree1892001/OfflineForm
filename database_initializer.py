import yaml
import logging
from Utils.mapping_utils import initialize_database_with_default_data

def run_initializer():
    """
    Runs the database initialization process.
    """
    print("Starting database initialization...")
    try:
        # Load config
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize database with default data
        initialize_database_with_default_data(config)
        
        print("\nDatabase has been successfully populated with default mapping rules.")
        
    except FileNotFoundError:
        print("\nERROR: config.yaml not found. Make sure you are running this script from the project root.")
    except Exception as e:
        print(f"\nAn error occurred during database initialization: {e}")
        logging.error(f"Database initialization failed: {e}")

if __name__ == "__main__":
    run_initializer() 