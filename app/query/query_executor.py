import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class DBExecutionError(Exception):
    pass
class QueryExecutor:
    
    def __init__(self):
        self.connection = self._create_connection()
    
    def _create_connection(self):
        try:
            return psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        except Exception as e:
            raise DBExecutionError(f"Database connection failed: {str(e)}")
    
    def execute(self, sql: str) -> list:
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise DBExecutionError(f"Query execution failed: {str(e)}")
    def close(self):
        if self.connection:
            self.connection.close()