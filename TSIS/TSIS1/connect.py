import psycopg2
from config import DB_CONFIG

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def test_connection():
    conn = get_connection()
    if conn:
        print("Successfully connected to database!")
        conn.close()
        return True
    else:
        print("Failed to connect to database")
        return False

def execute_query(query, params=None):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Query execution error: {e}")
        conn.rollback()
        conn.close()
        return None

def execute_procedure(proc_name, params=None):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        if params:
            cur.callproc(proc_name, params)
        else:
            cur.callproc(proc_name)
        conn.commit()
        result = cur.fetchall() if cur.description else None
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Procedure execution error: {e}")
        conn.rollback()
        conn.close()
        return None

if __name__ == "__main__":
    test_connection()
