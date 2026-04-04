# connect.py
import psycopg2
from psycopg2 import OperationalError
from config import load_config

def get_connection():
    """Establish database connection"""
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except OperationalError as e:
        print(f"Connection error: {e}")
        return None

