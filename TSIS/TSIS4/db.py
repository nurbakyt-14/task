import psycopg2
from datetime import datetime

class Database:
    def __init__(self, dbname="snake_game", user="postgres", password="12345678", host="localhost", port="5432"):
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.create_tables()
            print("Database connected successfully!")
        except Exception as e:
            print(f"Cannot connect to PostgreSQL: {e}")
            print("Running without database...")
    
    def create_tables(self):
        if not self.conn:
            return
        cur = self.conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
    
    def get_or_create_player(self, username):
        if not self.conn:
            return None
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            result = cur.fetchone()
            
            if result:
                player_id = result[0]
            else:
                cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                player_id = cur.fetchone()[0]
            
            self.conn.commit()
            return player_id
        except Exception as e:
            print(f"Error in get_or_create_player: {e}")
            return None
        finally:
            cur.close()
    
    def save_game_result(self, username, score, level_reached):
        if not self.conn:
            print("No database connection - result not saved")
            return
        player_id = self.get_or_create_player(username)
        if player_id:
            cur = self.conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                    (player_id, score, level_reached)
                )
                self.conn.commit()
                print(f"Game saved: {username} - Score: {score}, Level: {level_reached}")
            except Exception as e:
                print(f"Error saving game result: {e}")
            finally:
                cur.close()
    
    def get_leaderboard(self, limit=10):
        if not self.conn:
            print("No database connection - returning empty leaderboard")
            return []
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT %s
            """, (limit,))
            results = cur.fetchall()
            return results
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
        finally:
            cur.close()
    
    def get_personal_best(self, username):
        if not self.conn:
            return 0
        player_id = self.get_or_create_player(username)
        if player_id:
            cur = self.conn.cursor()
            try:
                cur.execute("""
                    SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id = %s
                """, (player_id,))
                result = cur.fetchone()[0]
                return result
            except Exception as e:
                print(f"Error getting personal best: {e}")
                return 0
            finally:
                cur.close()
        return 0
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")