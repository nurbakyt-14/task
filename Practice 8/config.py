from psycopg2 import OperationalError
import psycopg2

def load_config():
    """Database connection configuration"""
    return {
        'host': 'localhost',
        'database': 'phonebook_db',
        'user': 'postgres',
        'password': '12345678',
        'port': 5432
    }
