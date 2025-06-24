import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import Optional, Dict
import threading

class DatabaseConnection:
    """
    Singleton class for managing PostgreSQL database connections
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, config: Dict = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Dict = None):
        if self._initialized:
            return
            
        self.config = config or {}
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self._initialized = True
    
    def get_connection(self):
        """Get database connection, creating it if necessary"""
        if self.connection is None or self.connection.closed:
            try:
                db_config = self.config.get('database', {}).get('postgres', {})
                self.connection = psycopg2.connect(
                    host=db_config.get('host', 'localhost'),
                    port=db_config.get('port', 5432),
                    database=db_config.get('database', 'mapping_rules'),
                    user=db_config.get('username', 'postgres'),
                    password=db_config.get('password', '')
                )
                self.logger.info("Database connection established successfully")
            except Exception as e:
                self.logger.error(f"Failed to connect to database: {e}")
                raise
        return self.connection
    
    def get_cursor(self, dict_cursor: bool = False):
        """Get a database cursor"""
        conn = self.get_connection()
        if dict_cursor:
            return conn.cursor(cursor_factory=RealDictCursor)
        return conn.cursor()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Execute a query and optionally fetch results"""
        try:
            cursor = self.get_cursor()
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to execute query: {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def execute_many(self, query: str, params_list: list):
        """Execute a query with multiple parameter sets"""
        try:
            cursor = self.get_cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute many: {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def close_connection(self):
        """Close the database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.logger.info("Database connection closed")
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close_connection() 